# cyberorbit/app.py
import os
import markdown
from flask import (Flask, jsonify, request, send_from_directory, render_template_string,
                   abort, flash, redirect, url_for, render_template) # Added flash, redirect, url_for, render_template
from werkzeug.utils import safe_join
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # Added login functions
from dotenv import load_dotenv
import time
import logging # Import the logging module
from flask import g # Import Flask's application context global
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import joinedload, selectinload # Import selectinload
import datetime
from models import UserBadge
# --- Load Environment Variables ---
load_dotenv()

# --- Initialize Flask App ---
app = Flask(__name__, static_folder="static")

# --- App Configuration ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("DATABASE_URL environment variable not set.")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Database Setup ---
from models import db, User, Graph, Node, Exercise, Ctf, Badge # Import necessary models
db.init_app(app)

# --- Login Manager Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Route name for the login page
login_manager.login_message_category = 'info' # Optional: Category for flash messages

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Import Refactored Core Logic ---
from core import nodes as core_nodes
from core import data as core_data
from core import ctfs as core_ctfs
from core import badges as core_badges
from core import streak as core_streak

# --- Load index.html (Keep as is) ---
try:
    app_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(app_dir, "index.html")
    with open(index_path) as f:
        INDEX_HTML = f.read()
except FileNotFoundError:
    INDEX_HTML = "<!DOCTYPE html><html><head><title>Error</title></head><body><h1>Error</h1><p>index.html not found.</p></body></html>"
    print(f"Error: index.html not found at {index_path}. Serving basic error page.")

# --- Authentication Routes ---

# Placeholder for registration form (can be expanded with Flask-WTF)
REGISTER_HTML = """
<!DOCTYPE html><html><head><title>Register</title></head><body>
<h1>Register</h1><form method="post">
Username: <input type="text" name="username" required><br>
Email: <input type="email" name="email" required><br>
Password: <input type="password" name="password" required><br>
<button type="submit">Register</button></form>
<p><a href="{{ url_for('login') }}">Already have an account? Login</a></p>
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
</body></html>
"""

# Placeholder for login form
LOGIN_HTML = """
<!DOCTYPE html><html><head><title>Login</title></head><body>
<h1>Login</h1><form method="post">
Username: <input type="text" name="username" required><br>
Password: <input type="password" name="password" required><br>
<button type="submit">Login</button></form>
<p><a href="{{ url_for('register') }}">Need an account? Register</a></p>
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
</body></html>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
             flash('All fields are required.', 'warning')
             return redirect(url_for('register'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password) # Hashes the password
        try:
            db.session.add(new_user)
            db.session.commit()
             # Optionally create initial streak record for new user
            core_streak.update_user_streak(new_user.id)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {e}', 'danger')
            print(f"Registration error: {e}")
            return redirect(url_for('register'))

    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user) # Handles session setup
            # Update streak on successful login
            core_streak.update_user_streak(user.id)
            # Redirect to the page they were trying to access, or index
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template_string(LOGIN_HTML)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- Refactored Data Routes ---

@app.route("/")
@login_required # Require login to see the main app
def index():
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(app_dir, "index.html")
        with open(index_path) as f:
             # Render the string using Jinja context (includes current_user)
             return render_template_string(f.read())
    except FileNotFoundError:
         abort(404) # Or render an error template

# cyberorbit/app.py
# ... imports ...

# cyberorbit/app.py
# ... imports ...

def _get_full_user_state(user_id, graph_id):
    """Fetches all data and computes the full user state for the API."""
    try:
        # === Stage 1: Consolidated Data Fetching ===
        streak_data = core_streak.update_user_streak(user_id)
        user_node_status_map, completed_exercise_ids = core_data.get_user_progress(user_id, graph_id)
        user_ctf_completions = core_ctfs.get_user_ctf_completions(user_id)
        user_badge_ids = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).with_entities(UserBadge.badge_id).all()}
        static_nodes_list, static_links_list = core_data.get_cached_static_graph_data(graph_id) # Uses cache
        all_ctfs_list = core_ctfs.get_all_ctfs()
        all_badge_defs_map = {b.id: b for b in Badge.query.all()}
        exercises_with_cats = db.session.query(Exercise).options(selectinload(Exercise.categories)).join(Node).filter(Node.graph_id == graph_id).all()
        required_exercises = [ex for ex in exercises_with_cats if not ex.optional]

        # === Stage 2: Compute State & Stage DB Changes ===
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(
            user_id, graph_id, static_nodes_list, static_links_list,
            user_node_status_map, completed_exercise_ids
        )
        abilities = core_nodes.compute_abilities(user_id, completed_exercise_ids, user_ctf_completions, exercises_with_cats)
        newly_awarded_badge_defs = core_badges.check_and_award_badges(
            user_id, graph_id, streak_data, user_ctf_completions, user_node_status_map,
            completed_exercise_ids, required_exercises, user_badge_ids, all_badge_defs_map
        )

        # === Stage 3: Commit staged changes ===
        db.session.commit() # Commit updates from graph state and badge awards

        # === Stage 4: Assemble Final State ===
        final_user_badges_list = core_badges.get_user_badges(user_id) # Fetch list AFTER commit
        combined_ctfs = [{**ctf_def, 'completed': user_ctf_completions.get(ctf_def['id'], 0)} for ctf_def in all_ctfs_list]
        graph = db.session.get(Graph, graph_id); graph_name = graph.name if graph else 'x'

        state = { # Assemble final state dict ...
            "nodes": nodes, "links": links, "unlocked": {nid: status for nid, status in unlocked.items()},
            "discovered": list(discovered), "streak": streak_data, "ctfs": combined_ctfs,
            "abilities": abilities, "badges": final_user_badges_list, "current_graph": graph_name
        }
        return state

    except Exception as e:
        print(f"Error in _get_full_user_state for user {user_id}, graph {graph_id}: {e}")
        db.session.rollback()
        return {"error": "Failed to compute state"}

    except Exception as e:
        print(f"Error in _get_full_user_state for user {user_id}, graph {graph_id}: {e}")
        db.session.rollback()
        return {"error": "Failed to compute state"}

# --- Ensure all routes call the updated helper ---
# ... (GET /data, POST /data, POST /ctfs) ...

# --- Update Routes to use the helper ---

@app.route("/data", methods=["GET"])
@login_required
def get_data():
    graph_name = request.args.get('graph', 'x')
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1
    state = _get_full_user_state(current_user.id, graph_id)
    if "error" in state:
        return jsonify(state), 500
    return jsonify(state)


@app.route("/data", methods=["POST"])
@login_required
def post_data():
    """Handles updates for exercises or node notes."""
    user_id = current_user.id
    payload = request.json
    graph_name = request.args.get('graph', 'x')
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1

    update_successful = True
    try:
        # --- Perform Update ---
        if 'exercise_update' in payload:
            # ... (logic to call update_user_exercise_completion) ...
            ex_data = payload['exercise_update']
            exercise_id = ex_data.get('exercise_id')
            is_completed = ex_data.get('completed')
            if exercise_id is not None and is_completed is not None:
                 update_successful &= core_data.update_user_exercise_completion(user_id, exercise_id, is_completed)
            else: update_successful = False; print(f"Invalid exercise update payload")

        elif 'notes_update' in payload:
             # ... (logic to call update_user_node_notes) ...
             notes_data = payload['notes_update']
             node_id = notes_data.get('node_id')
             notes = notes_data.get('notes')
             if node_id is not None and notes is not None:
                  update_successful &= core_data.update_user_node_notes(user_id, node_id, notes)
             else: update_successful = False; print(f"Invalid notes update payload")
        else:
             return jsonify({"error": "Unknown or missing update type in payload"}), 400

        if not update_successful:
             # Rollback might have happened in core functions, or do it here
             db.session.rollback()
             return jsonify({"error": "Failed to apply update"}), 400

        state = _get_full_user_state(user_id, graph_id)
        if "error" in state:
            return jsonify(state), 500
        return jsonify(state)

    except Exception as e:
        db.session.rollback()
        print(f"Error processing POST /data for user {user_id}: {e}")
        return jsonify({"error": "Failed to process data update", "details": str(e)}), 500

@app.route("/ctfs", methods=["POST"])
@login_required
def post_ctfs():
    """Handles updates to user's CTF completion counts."""
    user_id = current_user.id
    ctf_updates = request.json
    graph_name = request.args.get('graph', 'x')
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1

    if not isinstance(ctf_updates, list):
        return jsonify({"error": "Invalid payload format, expected a list of CTFs"}), 400

    try:
        # --- Perform Update ---
        current_completions = core_ctfs.get_user_ctf_completions(user_id)
        update_failed = False
        for ctf_data in ctf_updates:
            ctf_id = ctf_data.get('id')
            new_count = ctf_data.get('completed')
            # ... (validation) ...
            current_count = current_completions.get(ctf_id, 0)
            delta = new_count - current_count
            if delta != 0:
                success = core_ctfs.update_user_ctf_completion(user_id, ctf_id, delta)
                if not success: update_failed = True # Track if any update failed

        if update_failed:
             # Decide if partial success is acceptable or rollback / return error
             print(f"Warning: One or more CTF updates failed for user {user_id}")
             # Potentially return an error if strict consistency is needed

        state = _get_full_user_state(user_id, graph_id)
        if "error" in state:
            return jsonify(state), 500
        return jsonify(state)

    except Exception as e:
        db.session.rollback()
        print(f"Error processing POST /ctfs for user {user_id}: {e}")
        return jsonify({"error": "Failed to process CTF data update", "details": str(e)}), 500



@app.route("/update_badges", methods=["POST"])
@login_required
def update_badges_shown_status():
    """Marks specific badges as 'shown' for the logged-in user."""
    user_id = current_user.id
    payload = request.json
    badge_ids_to_mark = payload.get("badgeIds", [])

    if not isinstance(badge_ids_to_mark, list):
         return jsonify({"error": "Invalid payload format, expected list for badgeIds"}), 400

    updated_count = 0
    try:
        for badge_id in badge_ids_to_mark:
            if isinstance(badge_id, str): # Basic validation
                 success = core_badges.mark_user_badge_shown(user_id, badge_id)
                 if success:
                     updated_count += 1
            else:
                 print(f"Skipping invalid badge ID format: {badge_id}")

        return jsonify({"status": "ok", "updated": updated_count > 0})
    except Exception as e:
         # Rollback might have already happened in the core function
         print(f"Error processing POST /update_badges for user {user_id}: {e}")
         return jsonify({"error": "Failed to update badge status", "details": str(e)}), 500

# --- Static & Markdown Routes (Keep as is) ---
@app.route("/static/<path:path>")
def static_files(path):
    # ... (keep existing implementation) ...
    try:
        safe_path = safe_join(app.static_folder, path)
        if safe_path is None: abort(404)
        return send_from_directory(os.path.dirname(safe_path), os.path.basename(safe_path))
    except Exception as e: print(f"Error serving static file {path}: {e}"); abort(500)


@app.route("/md/<path:filename>")
@login_required # Protect markdown too? Optional.
def serve_markdown_md(filename):
    return serve_markdown(filename, "md")

@app.route("/mdml/<path:filename>")
@login_required # Protect markdown too? Optional.
def serve_markdown_mdml(filename):
    return serve_markdown(filename, "mdml")

def serve_markdown(filename, folder):
    # ... (keep existing implementation, ensure it doesn't leak paths) ...
    markdown_dir = os.path.join(app.root_path, app.static_folder, folder)
    filepath = safe_join(markdown_dir, filename)
    if filepath is None or not os.path.isfile(filepath): abort(404)
    try:
        with open(filepath, "r", encoding="utf-8") as f: content = f.read()
        html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'codehilite'])
        # Simplified layout string for brevity
        layout_style = "body { padding: 20px; max-width: 800px; margin: auto; } img {max-width: 100%;}"
        theme_css_path = "/static/dracula.css" # Example
        return render_template_string(f"""...{Markup(html)}...""", filename=filename, theme_css_path=theme_css_path, layout_style=layout_style)
    except Exception as e: print(f"Error rendering markdown {filename}: {e}"); abort(500)


# --- Optional DB Init Command (Keep as is) ---
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    try:
        # Ensure this is run within app context if needed, depends on Flask version
        with app.app_context():
             db.create_all()
        print("Initialized the database.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# --- Main Execution (Keep as is) ---
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1") # Listen on 0.0.0.0 to be accessible externally if needed
    print(f"Starting Flask app: host={host}, port={port}, debug={debug_mode}")
    app.run(host=host, port=port, debug=debug_mode)