# -*- coding: utf-8 -*-
import os
import markdown
from flask import (Flask, jsonify, request, send_from_directory, render_template_string,
                   abort, flash, redirect, url_for, render_template)
from werkzeug.utils import safe_join
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import time
import logging
from flask import g
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import joinedload, selectinload
import datetime
from models import UserBadge # Keep specific imports if needed elsewhere
from threading import Lock # Import Lock for thread safety

load_dotenv()

app = Flask(__name__, static_folder="static")


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("DATABASE_URL environment variable not set.")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Import all models needed for caching/operations
from models import db, User, Graph, Node, Exercise, Ctf, Badge
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


from core import nodes as core_nodes
from core import data as core_data
from core import ctfs as core_ctfs
from core import badges as core_badges
from core import streak as core_streak


try:
    app_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(app_dir, "index.html")
    with open(index_path) as f:
        INDEX_HTML = f.read()
except FileNotFoundError:
    INDEX_HTML = "<!DOCTYPE html><html><head><title>Error</title></head><body><h1>Error</h1><p>index.html not found.</p></body></html>"
    print(f"Error: index.html not found at {index_path}. Serving basic error page.")


# --- Caching Setup ---
_ALL_CTFS_CACHE = None
_ALL_BADGES_CACHE = None
_cache_lock = Lock()

def _get_cached_static_definitions():
    """Fetches and caches all CTFs and Badges if not already cached."""
    global _ALL_CTFS_CACHE, _ALL_BADGES_CACHE
    def _len(obj):
        return len(obj) if obj is not None else 0
    
    with _cache_lock: # Ensure thread safety when checking/updating cache
        if _ALL_CTFS_CACHE is None or _ALL_BADGES_CACHE is None:
            print("CACHE MISS: Populating static CTF and Badge definitions...")
            try:
                with app.app_context(): # Need app context for DB queries
                    # Fetch CTFs
                    all_ctfs_db = Ctf.query.order_by(Ctf.id).all()
                    _ALL_CTFS_CACHE = [
                        {'id': c.id, 'title': c.title, 'description': c.description, 'link': c.link}
                        for c in all_ctfs_db
                    ]

                    # Fetch Badges
                    all_badges_db = Badge.query.order_by(Badge.id).all()
                    _ALL_BADGES_CACHE = {b.id: {
                         'id': b.id, 'title': b.title, 'description': b.description, 'image_path': b.image_path
                        } for b in all_badges_db
                    }
                    print(f"CACHE POPULATED: {_len(_ALL_CTFS_CACHE)} CTFs, {_len(_ALL_BADGES_CACHE)} Badges.")
            except Exception as e:
                 # Log error but potentially allow app to continue without cache
                 print(f"CRITICAL: Failed to populate static definition cache: {e}")
                 # Set to empty lists/dicts to avoid repeated attempts on error?
                 _ALL_CTFS_CACHE = []
                 _ALL_BADGES_CACHE = {}

    return _ALL_CTFS_CACHE, _ALL_BADGES_CACHE
# --- End Caching Setup ---


REGISTER_HTML = """...""" # Keep HTML templates as they were
LOGIN_HTML = """...""" # Keep HTML templates as they were

@app.route('/register', methods=['GET', 'POST'])
def register():
    # --- Keep register logic ---
    if current_user.is_authenticated: return redirect(url_for('index'))
    if request.method == 'POST':
        # ... (form processing) ...
        existing_user = User.query.filter((User.username == request.form.get('username')) | (User.email == request.form.get('email'))).first()
        if existing_user: flash('Username or email already exists.', 'danger'); return redirect(url_for('register'))
        new_user = User(username=request.form.get('username'), email=request.form.get('email'))
        new_user.set_password(request.form.get('password'))
        try:
            db.session.add(new_user)
            db.session.commit()
            core_streak.update_user_streak(new_user.id)
            flash('Registration successful! Please login.', 'success'); return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback(); flash(f'Error during registration: {e}', 'danger'); print(f"Registration error: {e}"); return redirect(url_for('register'))
    return render_template_string(REGISTER_HTML)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # --- Keep login logic ---
    if current_user.is_authenticated: return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user); core_streak.update_user_streak(user.id)
            next_page = request.args.get('next'); return redirect(next_page or url_for('index'))
        else: flash('Invalid username or password.', 'danger')
    return render_template_string(LOGIN_HTML)


@app.route('/logout')
@login_required
def logout():
    # --- Keep logout logic ---
    logout_user(); flash('You have been logged out.', 'info'); return redirect(url_for('login'))


@app.route("/")
@login_required
def index():
    # --- Keep index logic ---
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(app_dir, "index.html")
        with open(index_path) as f: return render_template_string(f.read())
    except FileNotFoundError: abort(404)


# --- MODIFIED State Calculation ---
def _get_full_user_state(user_id, graph_id):
    """Fetches all data and computes the full user state for the API."""
    try:
        # --- Use Cached Static Definitions ---
        all_ctfs_list_cached, all_badge_defs_map_cached = _get_cached_static_definitions()
        if all_ctfs_list_cached is None or all_badge_defs_map_cached is None:
            # Handle case where cache failed to populate
            print("Warning: Static definitions cache not ready.")
            # Fallback to direct query (or return error if cache is critical)
            all_ctfs_list_cached = core_ctfs.get_all_ctfs() # Direct fetch as fallback
            badges_db = Badge.query.all()
            all_badge_defs_map_cached = {b.id: {'id': b.id, 'title': b.title, 'description': b.description, 'image_path': b.image_path} for b in badges_db}
        # --- End Cache Usage ---

        # --- Fetch user-specific and graph-specific data ---
        streak_data = core_streak.update_user_streak(user_id) # Updates and returns streak
        user_node_status_map, completed_exercise_ids = core_data.get_user_progress(user_id, graph_id)
        user_ctf_completions = core_ctfs.get_user_ctf_completions(user_id)
        user_badge_ids = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).with_entities(UserBadge.badge_id).all()}
        static_nodes_list, static_links_list = core_data.get_cached_static_graph_data(graph_id) # Graph-specific cache

        # Fetch exercises (already graph-specific)
        exercises_with_cats = db.session.query(Exercise).options(selectinload(Exercise.categories)).join(Node).filter(Node.graph_id == graph_id).all()
        required_exercises = [ex for ex in exercises_with_cats if not ex.optional]

        # --- Compute dynamic state ---
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(
            user_id, graph_id, static_nodes_list, static_links_list,
            user_node_status_map, completed_exercise_ids
        )
        abilities = core_nodes.compute_abilities(user_id, completed_exercise_ids, user_ctf_completions, exercises_with_cats)

        # Pass cached badge definitions to badge check function
        newly_awarded_badge_defs_list = core_badges.check_and_award_badges(
            user_id, graph_id, streak_data, user_ctf_completions, user_node_status_map,
            completed_exercise_ids, required_exercises, user_badge_ids,
            all_badge_defs_map_cached # Pass cached map
        )

        # Commit any changes made during state computation (streak updates, badge awards, node status updates)
        db.session.commit()

        # Fetch the final list of user badges after potential awards
        # TODO: Optimization - Can we avoid this second query if we use the cached badge defs?
        # Maybe check_and_award_badges returns the full UserBadge object (incl badge details from cache)?
        # For now, keeping the separate query.
        final_user_badges_list = core_badges.get_user_badges(user_id)

        # Combine CTF definitions (from cache) with user progress
        combined_ctfs = [
            {**ctf_def, 'completed': user_ctf_completions.get(ctf_def['id'], 0)}
            for ctf_def in all_ctfs_list_cached # Use cached list
        ]
        graph = db.session.get(Graph, graph_id); graph_name = graph.name if graph else 'x'

        # Assemble the final state dictionary
        state = {
            "nodes": nodes, "links": links, "unlocked": {nid: status for nid, status in unlocked.items()},
            "discovered": list(discovered), "streak": streak_data, "ctfs": combined_ctfs,
            "abilities": abilities, "badges": final_user_badges_list, "current_graph": graph_name
            # Add newly awarded badges for popup?
            # "newly_awarded_badges": newly_awarded_badge_defs_list # Pass badge *objects* or just IDs? Frontend needs details.
        }
        return state

    except Exception as e:
        print(f"Error in _get_full_user_state for user {user_id}, graph {graph_id}: {e}")
        db.session.rollback() # Rollback on error
        return {"error": "Failed to compute state"}
# --- End MODIFIED State Calculation ---



@app.route("/data", methods=["GET"])
@login_required
def get_data():
    # --- Keep get_data logic (calls the optimized _get_full_user_state) ---
    graph_name = request.args.get('graph', 'x')
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1
    state = _get_full_user_state(current_user.id, graph_id)
    if "error" in state: return jsonify(state), 500
    return jsonify(state)


@app.route("/data", methods=["POST"])
@login_required
def post_data():
    # --- Use the refactored version from Step 1 ---
    user_id = current_user.id
    payload = request.json
    update_successful = True
    try:
        if 'exercise_update' in payload:
             ex_data = payload['exercise_update']
             exercise_id = ex_data.get('exercise_id'); is_completed = ex_data.get('completed')
             if exercise_id is not None and is_completed is not None: update_successful &= core_data.update_user_exercise_completion(user_id, exercise_id, is_completed)
             else: update_successful = False; print(f"Invalid exercise update payload")
        elif 'notes_update' in payload:
             notes_data = payload['notes_update']
             node_id = notes_data.get('node_id'); notes = notes_data.get('notes')
             if node_id is not None and notes is not None: update_successful &= core_data.update_user_node_notes(user_id, node_id, notes)
             else: update_successful = False; print(f"Invalid notes update payload")
        else: return jsonify({"error": "Unknown or missing update type in payload"}), 400

        if not update_successful: db.session.rollback(); return jsonify({"error": "Failed to apply update"}), 400
        db.session.commit() # Commit successful update
        return jsonify({"status": "ok"}) # Return minimal confirmation

    except Exception as e:
        db.session.rollback(); print(f"Error processing POST /data for user {user_id}: {e}")
        return jsonify({"error": "Failed to process data update", "details": str(e)}), 500


@app.route("/ctfs", methods=["POST"])
@login_required
def post_ctfs():
    # --- Use the refactored version from Step 1 ---
    user_id = current_user.id
    ctf_updates = request.json
    if not isinstance(ctf_updates, list): return jsonify({"error": "Invalid payload format, expected a list of CTFs"}), 400
    try:
        current_completions = core_ctfs.get_user_ctf_completions(user_id)
        update_failed = False; any_updates_made = False
        for ctf_data in ctf_updates:
             ctf_id = ctf_data.get('id'); new_count = ctf_data.get('completed')
             if ctf_id is None or new_count is None: continue
             current_count = current_completions.get(ctf_id, 0)
             delta = new_count - current_count
             if delta != 0:
                 success = core_ctfs.update_user_ctf_completion(user_id, ctf_id, delta)
                 if success: any_updates_made = True
                 else: update_failed = True; print(f"Failed to update CTF {ctf_id}...")
        if update_failed: print(f"Warning: One or more CTF updates failed...") # Decide on rollback/partial commit
        if any_updates_made: db.session.commit() # Commit if changes were made
        return jsonify({"status": "ok"}) # Return minimal confirmation

    except Exception as e:
        db.session.rollback(); print(f"Error processing POST /ctfs for user {user_id}: {e}")
        return jsonify({"error": "Failed to process CTF data update", "details": str(e)}), 500


@app.route("/update_badges", methods=["POST"])
@login_required
def update_badges_shown_status():
    # --- Keep update_badges logic ---
    user_id = current_user.id; payload = request.json
    badge_ids_to_mark = payload.get("badgeIds", [])
    if not isinstance(badge_ids_to_mark, list): return jsonify({"error": "Invalid payload format..."}), 400
    updated_count = 0
    try:
        for badge_id in badge_ids_to_mark:
             if isinstance(badge_id, (str, int)): # Allow int or string IDs
                 # Pass cached map if core_badges.mark_user_badge_shown is adapted, otherwise it queries anyway
                 success = core_badges.mark_user_badge_shown(user_id, str(badge_id))
                 if success: updated_count += 1
        if updated_count > 0: db.session.commit() # Commit only if changes were made
        return jsonify({"status": "ok", "updated": updated_count > 0})
    except Exception as e:
         db.session.rollback(); print(f"Error processing POST /update_badges...")
         return jsonify({"error": "Failed to update badge status", "details": str(e)}), 500


@app.route("/static/<path:path>")
def static_files(path):
    # --- Keep static_files logic ---
    try:
        safe_path = safe_join(app.static_folder, path)
        if safe_path is None: abort(404)
        return send_from_directory(os.path.dirname(safe_path), os.path.basename(safe_path))
    except Exception as e: print(f"Error serving static file {path}: {e}"); abort(500)


@app.route("/md/<path:filename>")
@login_required
def serve_markdown_md(filename):
     # --- Keep markdown logic ---
    return serve_markdown(filename, "md")

@app.route("/mdml/<path:filename>")
@login_required
def serve_markdown_mdml(filename):
     # --- Keep markdown logic ---
    return serve_markdown(filename, "mdml")

def serve_markdown(filename, folder):
    """Serves markdown files rendered as HTML with the correct theme."""
    markdown_dir = os.path.join(app.root_path, app.static_folder, folder)
    filepath = safe_join(markdown_dir, filename)
    if filepath is None or not os.path.isfile(filepath):
        print(f"Markdown file not found or path issue: {filename}")
        abort(404)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Render markdown to HTML
        html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'codehilite'])

        # Basic styling and theme link (adjust paths as needed)
        layout_style = """
            body { padding: 30px 40px; max-width: 850px; margin: 20px auto; line-height: 1.7; overflow: auto !important; }
            img { max-width: 100%; height: auto; margin: 1em 0; }
            table { width: 100%; margin: 1.5em 0; border-collapse: collapse; } th, td { border: 1px solid var(--base01, #586e75); padding: 8px; } th { background-color: var(--base02, #073642); }
            blockquote { border-left: 4px solid var(--base01, #586e75); padding-left: 15px; margin-left: 0; color: var(--base0, #839496); font-style: italic; }
            hr { border: none; border-top: 1px solid var(--base01, #586e75); margin: 2em 0; }
            a { border:none; color: var(--blue, #268bd2); text-decoration: underline; }
            pre { border: 1px solid var(--base01, #586e75); border-radius: 4px; padding: 10px; overflow-x: auto; }
            /* Add other specific styles as needed */
        """
        theme_css_path = url_for('static', filename='solarized.css') # Use url_for for flexibility
        return render_template_string(f"""
        <!DOCTYPE html>
        <html>
            <head>
            <meta charset="UTF-8">
            <title>{Markup.escape(filename)}</title>
            <link rel="stylesheet" href="{theme_css_path}">
            <link href="https://fonts.googleapis.com/css2?family=Fira+Code&family=Share+Tech+Mono&display=swap" rel="stylesheet">
            <style>{layout_style}</style>
            </head>
            <body>
                {Markup(html)}
            </body>
        </html>
        """, filename=Markup.escape(filename), theme_css_path=theme_css_path, layout_style=layout_style) # Pass variables to template

    except Exception as e:
        print(f"Error rendering markdown {filename}: {e}")
        abort(500)

@app.cli.command("init-db")
def init_db_command():
    # --- Keep init-db logic ---
    try:
        with app.app_context(): db.create_all()
        print("Initialized the database.")
        # --- Populate Cache After Init ---
        print("Attempting to populate static definition cache...")
        _get_cached_static_definitions() # Attempt to pre-populate cache after DB init
        # --- End Cache Population ---
    except Exception as e: print(f"Error initializing database: {e}")


if __name__ == "__main__":
    # --- Keep main execution block ---
    # --- Populate Cache At Startup ---
    print("Attempting initial population of static definition cache...")
    _get_cached_static_definitions() # Attempt to pre-populate cache at startup
    # --- End Cache Population ---
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"Starting Flask app: host={host}, port={port}, debug={debug_mode}")
    app.run(host=host, port=port, debug=debug_mode)

# Helper function to handle potential NoneType in cache population log message
