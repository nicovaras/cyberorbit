# -*- coding: utf-8 -*-
import os
import markdown
from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
    render_template_string,
    abort,
    flash,
    redirect,
    url_for,
    render_template,
)
from werkzeug.utils import safe_join
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from dotenv import load_dotenv
import time
import logging
from flask import g
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import joinedload, selectinload
import datetime
from models import UserBadge  # Keep specific imports if needed elsewhere
from threading import Lock  # Import Lock for thread safety
from sqlalchemy.orm import aliased
from collections import defaultdict

load_dotenv()

app = Flask(__name__, static_folder="static")


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default-fallback-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
if not app.config["SQLALCHEMY_DATABASE_URI"]:
    raise ValueError("DATABASE_URL environment variable not set.")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Import all models needed for caching/operations
from models import (
    db,
    User,
    Graph,
    Node,
    Exercise,
    Ctf,
    Badge,
    UserNodeStatus,
    NodeRelationship,
)

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


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

    with _cache_lock:  # Ensure thread safety when checking/updating cache
        if _ALL_CTFS_CACHE is None or _ALL_BADGES_CACHE is None:
            print("CACHE MISS: Populating static CTF and Badge definitions...")
            try:
                with app.app_context():  # Need app context for DB queries
                    # Fetch CTFs
                    all_ctfs_db = Ctf.query.order_by(Ctf.id).all()
                    _ALL_CTFS_CACHE = [
                        {
                            "id": c.id,
                            "title": c.title,
                            "description": c.description,
                            "link": c.link,
                        }
                        for c in all_ctfs_db
                    ]

                    # Fetch Badges
                    all_badges_db = Badge.query.order_by(Badge.id).all()
                    _ALL_BADGES_CACHE = {
                        b.id: {
                            "id": b.id,
                            "title": b.title,
                            "description": b.description,
                            "image_path": b.image_path,
                        }
                        for b in all_badges_db
                    }
                    print(
                        f"CACHE POPULATED: {_len(_ALL_CTFS_CACHE)} CTFs, {_len(_ALL_BADGES_CACHE)} Badges."
                    )
            except Exception as e:
                # Log error but potentially allow app to continue without cache
                print(f"CRITICAL: Failed to populate static definition cache: {e}")
                # Set to empty lists/dicts to avoid repeated attempts on error?
                _ALL_CTFS_CACHE = []
                _ALL_BADGES_CACHE = {}

    return _ALL_CTFS_CACHE, _ALL_BADGES_CACHE


# --- End Caching Setup ---


REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - CyberOrbit</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='solarized.css') }}">
    <style>
        body { padding: 20px; max-width: 500px; margin: 40px auto; font-family: sans-serif; }
        .form-container { padding: 30px; border: 1px solid var(--base01); border-radius: 8px; background-color: var(--base03); }
        h1 { text-align: center; color: var(--base1); margin-bottom: 25px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: var(--base0); }
        input[type="text"], input[type="email"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid var(--base01);
            border-radius: 4px;
            box-sizing: border-box;
            background-color: var(--base02);
            color: var(--base1);
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: var(--blue);
            color: var(--base3);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover { background-color: var(--cyan); }
        .alert { padding: 10px; margin-bottom: 15px; border-radius: 4px; }
        .alert-danger { background-color: var(--red); color: var(--base3); }
        .alert-success { background-color: var(--green); color: var(--base3); }
        .alert-info { background-color: var(--blue); color: var(--base3); }
        .login-link { text-align: center; margin-top: 20px; }
        .login-link a { color: var(--violet); text-decoration: none; }
        .login-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Register New Account</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('register') }}">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
        <div class="login-link">
            <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
        </div>
    </div>
</body>
</html>
"""
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - CyberOrbit</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='solarized.css') }}">
     <style>
        /* Using the same styles as REGISTER_HTML for consistency */
        body { padding: 20px; max-width: 500px; margin: 40px auto; font-family: sans-serif; }
        .form-container { padding: 30px; border: 1px solid var(--base01); border-radius: 8px; background-color: var(--base03); }
        h1 { text-align: center; color: var(--base1); margin-bottom: 25px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: var(--base0); }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid var(--base01);
            border-radius: 4px;
            box-sizing: border-box;
            background-color: var(--base02);
            color: var(--base1);
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: var(--blue);
            color: var(--base3);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover { background-color: var(--cyan); }
        .alert { padding: 10px; margin-bottom: 15px; border-radius: 4px; }
        .alert-danger { background-color: var(--red); color: var(--base3); }
        .alert-success { background-color: var(--green); color: var(--base3); }
        .alert-info { background-color: var(--blue); color: var(--base3); }
        .register-link { text-align: center; margin-top: 20px; }
        .register-link a { color: var(--violet); text-decoration: none; }
        .register-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Login</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('login') }}{% if request.args.get('next') %}?next={{ request.args.get('next') }}{% endif %}">
             <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
         <div class="register-link">
            <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
        </div>
    </div>
</body>
</html>
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    # --- Keep register logic ---
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        # ... (form processing) ...
        existing_user = User.query.filter(
            (User.username == request.form.get("username"))
            | (User.email == request.form.get("email"))
        ).first()
        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("register"))
        new_user = User(
            username=request.form.get("username"), email=request.form.get("email")
        )
        new_user.set_password(request.form.get("password"))
        try:
            db.session.add(new_user)
            db.session.commit()
            core_streak.update_user_streak(new_user.id)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error during registration: {e}", "danger")
            print(f"Registration error: {e}")
            return redirect(url_for("register"))
    return render_template_string(REGISTER_HTML)


@app.route("/login", methods=["GET", "POST"])
def login():
    # --- Keep login logic ---
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and user.check_password(request.form.get("password")):
            login_user(user)
            core_streak.update_user_streak(user.id)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template_string(LOGIN_HTML)


@app.route("/logout")
@login_required
def logout():
    # --- Keep logout logic ---
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    # --- Keep index logic ---
    try:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(app_dir, "index.html")
        with open(index_path) as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        abort(404)


# --- MODIFIED State Calculation ---
def _get_full_user_state(user_id, graph_id):
    """Fetches all data and computes the full user state for the API."""
    try:
        # --- Use Cached Static Definitions ---
        all_ctfs_list_cached, all_badge_defs_map_cached = (
            _get_cached_static_definitions()
        )
        if all_ctfs_list_cached is None or all_badge_defs_map_cached is None:
            # Handle case where cache failed to populate
            print("Warning: Static definitions cache not ready.")
            # Fallback to direct query (or return error if cache is critical)
            all_ctfs_list_cached = core_ctfs.get_all_ctfs()  # Direct fetch as fallback
            badges_db = Badge.query.all()
            all_badge_defs_map_cached = {
                b.id: {
                    "id": b.id,
                    "title": b.title,
                    "description": b.description,
                    "image_path": b.image_path,
                }
                for b in badges_db
            }
        # --- End Cache Usage ---

        # --- Fetch user-specific and graph-specific data ---
        streak_data = core_streak.update_user_streak(
            user_id
        )  # Updates and returns streak
        user_node_status_map, completed_exercise_ids = core_data.get_user_progress(
            user_id, graph_id
        )
        user_ctf_completions = core_ctfs.get_user_ctf_completions(user_id)
        user_badge_ids = {
            ub.badge_id
            for ub in UserBadge.query.filter_by(user_id=user_id)
            .with_entities(UserBadge.badge_id)
            .all()
        }
        static_nodes_list, static_links_list = core_data.get_cached_static_graph_data(
            graph_id
        )  # Graph-specific cache

        # Fetch exercises (already graph-specific)
        exercises_with_cats = (
            db.session.query(Exercise)
            .options(selectinload(Exercise.categories))
            .join(Node)
            .filter(Node.graph_id == graph_id)
            .all()
        )
        required_exercises = [ex for ex in exercises_with_cats if not ex.optional]

        # --- Compute dynamic state ---
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(
            user_id,
            graph_id,
            static_nodes_list,
            static_links_list,
            user_node_status_map,
            completed_exercise_ids,
        )
        abilities = core_nodes.compute_abilities(
            user_id, completed_exercise_ids, user_ctf_completions, exercises_with_cats
        )

        # Pass cached badge definitions to badge check function
        newly_awarded_badge_defs_list = core_badges.check_and_award_badges(
            user_id,
            graph_id,
            streak_data,
            user_ctf_completions,
            user_node_status_map,
            completed_exercise_ids,
            required_exercises,
            user_badge_ids,
            all_badge_defs_map_cached,  # Pass cached map
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
            {**ctf_def, "completed": user_ctf_completions.get(ctf_def["id"], 0)}
            for ctf_def in all_ctfs_list_cached  # Use cached list
        ]
        graph = db.session.get(Graph, graph_id)
        graph_name = graph.name if graph else "x"

        # Assemble the final state dictionary
        state = {
            "nodes": nodes,
            "links": links,
            "unlocked": {nid: status for nid, status in unlocked.items()},
            "discovered": list(discovered),
            "streak": streak_data,
            "ctfs": combined_ctfs,
            "abilities": abilities,
            "badges": final_user_badges_list,
            "current_graph": graph_name,
            # Add newly awarded badges for popup?
            # "newly_awarded_badges": newly_awarded_badge_defs_list # Pass badge *objects* or just IDs? Frontend needs details.
        }
        return state

    except Exception as e:
        print(
            f"Error in _get_full_user_state for user {user_id}, graph {graph_id}: {e}"
        )
        db.session.rollback()  # Rollback on error
        return {"error": "Failed to compute state"}


# --- End MODIFIED State Calculation ---


@app.route("/data", methods=["GET"])
@login_required
def get_data():
    # --- Keep get_data logic (calls the optimized _get_full_user_state) ---
    graph_name = request.args.get("graph", "x")
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1
    state = _get_full_user_state(current_user.id, graph_id)
    if "error" in state:
        return jsonify(state), 500
    return jsonify(state)


@app.route("/data", methods=["POST"])
@login_required
def post_data():
    # --- Use the refactored version from Step 1 ---
    user_id = current_user.id
    payload = request.json
    update_successful = True
    try:
        if "exercise_update" in payload:
            ex_data = payload["exercise_update"]
            exercise_id = ex_data.get("exercise_id")
            is_completed = ex_data.get("completed")
            if exercise_id is not None and is_completed is not None:
                update_successful &= core_data.update_user_exercise_completion(
                    user_id, exercise_id, is_completed
                )
            else:
                update_successful = False
                print(f"Invalid exercise update payload")
        elif "notes_update" in payload:
            notes_data = payload["notes_update"]
            node_id = notes_data.get("node_id")
            notes = notes_data.get("notes")
            if node_id is not None and notes is not None:
                update_successful &= core_data.update_user_node_notes(
                    user_id, node_id, notes
                )
            else:
                update_successful = False
                print(f"Invalid notes update payload")
        else:
            return jsonify({"error": "Unknown or missing update type in payload"}), 400

        if not update_successful:
            db.session.rollback()
            return jsonify({"error": "Failed to apply update"}), 400
        db.session.commit()  # Commit successful update
        return jsonify({"status": "ok"})  # Return minimal confirmation

    except Exception as e:
        db.session.rollback()
        print(f"Error processing POST /data for user {user_id}: {e}")
        return (
            jsonify({"error": "Failed to process data update", "details": str(e)}),
            500,
        )


@app.route("/ctfs", methods=["POST"])
@login_required
def post_ctfs():
    # --- Use the refactored version from Step 1 ---
    user_id = current_user.id
    ctf_updates = request.json
    if not isinstance(ctf_updates, list):
        return (
            jsonify({"error": "Invalid payload format, expected a list of CTFs"}),
            400,
        )
    try:
        current_completions = core_ctfs.get_user_ctf_completions(user_id)
        update_failed = False
        any_updates_made = False
        for ctf_data in ctf_updates:
            ctf_id = ctf_data.get("id")
            new_count = ctf_data.get("completed")
            if ctf_id is None or new_count is None:
                continue
            current_count = current_completions.get(ctf_id, 0)
            delta = new_count - current_count
            if delta != 0:
                success = core_ctfs.update_user_ctf_completion(user_id, ctf_id, delta)
                if success:
                    any_updates_made = True
                else:
                    update_failed = True
                    print(f"Failed to update CTF {ctf_id}...")
        if update_failed:
            print(
                f"Warning: One or more CTF updates failed..."
            )  # Decide on rollback/partial commit
        if any_updates_made:
            db.session.commit()  # Commit if changes were made
        return jsonify({"status": "ok"})  # Return minimal confirmation

    except Exception as e:
        db.session.rollback()
        print(f"Error processing POST /ctfs for user {user_id}: {e}")
        return (
            jsonify({"error": "Failed to process CTF data update", "details": str(e)}),
            500,
        )


@app.route("/update_badges", methods=["POST"])
@login_required
def update_badges_shown_status():
    # --- Keep update_badges logic ---
    user_id = current_user.id
    payload = request.json
    badge_ids_to_mark = payload.get("badgeIds", [])
    if not isinstance(badge_ids_to_mark, list):
        return jsonify({"error": "Invalid payload format..."}), 400
    updated_count = 0
    try:
        for badge_id in badge_ids_to_mark:
            if isinstance(badge_id, (str, int)):  # Allow int or string IDs
                # Pass cached map if core_badges.mark_user_badge_shown is adapted, otherwise it queries anyway
                success = core_badges.mark_user_badge_shown(user_id, str(badge_id))
                if success:
                    updated_count += 1
        if updated_count > 0:
            db.session.commit()  # Commit only if changes were made
        return jsonify({"status": "ok", "updated": updated_count > 0})
    except Exception as e:
        db.session.rollback()
        print(f"Error processing POST /update_badges...")
        return (
            jsonify({"error": "Failed to update badge status", "details": str(e)}),
            500,
        )


@app.route("/notes")
@login_required
def get_all_notes():
    graph_name = request.args.get("graph", "x")  # Get graph name from query param
    user_id = current_user.id

    try:
        # 1. Find the graph_id
        graph = Graph.query.filter_by(name=graph_name).first()
        if not graph:
            return jsonify({"error": f"Graph '{graph_name}' not found"}), 404
        graph_id = graph.id

        # 2. Find all nodes with non-empty notes for this user and graph
        # We still need this map to know *which* nodes have notes and what they are.
        nodes_with_notes_statuses = (
            db.session.query(UserNodeStatus)
            .join(Node)
            .filter(
                UserNodeStatus.user_id == user_id,
                Node.graph_id == graph_id,
                UserNodeStatus.user_notes != None,  # Check for NULL
                UserNodeStatus.user_notes != "",  # Check for empty string
            )
            .options(joinedload(UserNodeStatus.node))  # Eager load node details
            .all()
        )

        # Create a map for quick lookup: node_id -> {title, notes, type} ONLY for nodes WITH notes
        notes_map = {
            status.node_id: {
                "title": status.node.title,
                "notes": status.user_notes,
                "type": status.node.type,
            }
            for status in nodes_with_notes_statuses
            if status.node  # Ensure node was loaded
        }
        # Create a map of ONLY SubNodes that have notes, used in the BFS check
        sub_nodes_with_notes_map = {
            nid: data for nid, data in notes_map.items() if data["type"] == "sub"
        }

        # 3. Get ALL Main Nodes for this graph (regardless of whether they have notes)
        all_main_nodes_in_graph = (
            db.session.query(Node.id, Node.title)
            .filter(Node.graph_id == graph_id, Node.type == "main")
            .all()
        )
        # Store details: node_id -> title
        all_main_node_details = {nid: title for nid, title in all_main_nodes_in_graph}

        if not all_main_node_details:
            return jsonify([])  # No main nodes in this graph

        # 4. Find relationships to determine hierarchy (within this graph)
        # Build a full parent -> children map for traversal
        relationships = (
            db.session.query(
                NodeRelationship.parent_node_id, NodeRelationship.child_node_id
            )
            .join(
                Node,
                NodeRelationship.parent_node_id
                == Node.id,  # Join to filter by graph_id implicitly via Node
            )
            .filter(
                Node.graph_id == graph_id, NodeRelationship.relationship_type == "CHILD"
            )
            .all()
        )

        full_children_map = defaultdict(list)
        for parent_id, child_id in relationships:
            full_children_map[parent_id].append(child_id)

        # 5. Structure the data hierarchically and filter
        result_data = []

        # Iterate through ALL main nodes of the graph
        for main_node_id, main_node_title in all_main_node_details.items():

            # Perform BFS/DFS to find if this main_node has any descendant SubNode WITH notes
            found_sub_nodes_with_notes = []
            queue = list(
                full_children_map.get(main_node_id, [])
            )  # Start BFS with direct children
            visited = {main_node_id}  # Track visited nodes during BFS traversal

            while queue:
                current_id = queue.pop(0)
                if current_id in visited:
                    continue
                visited.add(current_id)

                # Check if this node is a SUB-NODE and HAS NOTES
                if current_id in sub_nodes_with_notes_map:
                    node_data = sub_nodes_with_notes_map[current_id]
                    found_sub_nodes_with_notes.append(
                        {
                            "sub_node_title": node_data["title"],
                            "notes": node_data["notes"],
                        }
                    )
                    # Note: We could potentially stop the search for *this branch* once one is found,
                    # but continuing allows collecting *all* sub-nodes with notes under the main node.

                # Continue traversal regardless of type, to find potentially deeper sub-nodes
                for next_child_id in full_children_map.get(current_id, []):
                    if next_child_id not in visited:
                        queue.append(next_child_id)

            # Condition for inclusion: MUST have found at least one sub-node with notes
            if found_sub_nodes_with_notes:
                # Get the main node's own notes (if they exist) using the original notes_map
                main_node_notes_content = notes_map.get(main_node_id, {}).get(
                    "notes"
                )  # Safely get notes, default None

                main_node_entry = {
                    "main_node_title": main_node_title,  # Use title fetched earlier
                    "main_node_notes": main_node_notes_content,  # Will be None if main node has no notes
                    "sub_nodes": sorted(
                        found_sub_nodes_with_notes, key=lambda x: x["sub_node_title"]
                    ),
                }
                result_data.append(main_node_entry)

        # Sort final list by main node title
        result_data.sort(key=lambda x: x["main_node_title"])

        return jsonify(result_data)

    except Exception as e:
        print(f"Error fetching notes for user {user_id}, graph {graph_name}: {e}")
        import traceback

        traceback.print_exc()  # Print detailed error traceback to Flask console
        db.session.rollback()
        return (
            jsonify({"error": "An internal error occurred while fetching notes."}),
            500,
        )


@app.route("/static/<path:path>")
def static_files(path):
    # --- Keep static_files logic ---
    try:
        safe_path = safe_join(app.static_folder, path)
        if safe_path is None:
            abort(404)
        return send_from_directory(
            os.path.dirname(safe_path), os.path.basename(safe_path)
        )
    except Exception as e:
        print(f"Error serving static file {path}: {e}")
        abort(500)


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
        html = markdown.markdown(
            content, extensions=["fenced_code", "tables", "codehilite"]
        )

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
        theme_css_path = url_for(
            "static", filename="solarized.css"
        )  # Use url_for for flexibility
        return render_template_string(
            f"""
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
        """,
            filename=Markup.escape(filename),
            theme_css_path=theme_css_path,
            layout_style=layout_style,
        )  # Pass variables to template

    except Exception as e:
        print(f"Error rendering markdown {filename}: {e}")
        abort(500)


@app.cli.command("init-db")
def init_db_command():
    # --- Keep init-db logic ---
    try:
        with app.app_context():
            db.create_all()
        print("Initialized the database.")
        # --- Populate Cache After Init ---
        print("Attempting to populate static definition cache...")
        _get_cached_static_definitions()  # Attempt to pre-populate cache after DB init
        # --- End Cache Population ---
    except Exception as e:
        print(f"Error initializing database: {e}")


import json
import os
import uuid  # Import the uuid module
import click  # Ensure click is imported for the CLI command
from flask import Flask  # Assuming your app instance might be created differently
from models import Graph, Node, NodeRelationship  # Import your specific models


def process_node_uuid(node_data, graph_id, parent_node_id=None):
    """
    Recursively processes a node and its children from the JSON data,
    generating a UUID for each new node and creating Node and
    NodeRelationship entries in the database session.
    """
    title = node_data.get("title")
    node_type = node_data.get("type")
    children = node_data.get("children", [])

    if not title or not node_type:
        print(f"Warning: Node data missing title or type: {node_data}. Skipping.")
        return

    # --- Generate a unique ID for the new node ---
    # Use uuid4 for random UUIDs, hex for a plain string representation
    generated_node_id = uuid.uuid4().hex

    # --- Create and Add New Node (Simpler version without title check) ---
    print(
        f"Creating Node: ID='{generated_node_id}', Title='{title}', Type='{node_type}'"
    )
    new_node = Node(
        id=generated_node_id,  # Use the generated UUID as the primary key
        graph_id=graph_id,
        title=title,
        type=node_type,
        popup_text=node_data.get("popup_text", None),
        pdf_link=node_data.get("pdf_link", None),
    )
    db.session.add(new_node)
    current_node_id_for_children = generated_node_id  # Use new ID for children

    # --- Create Relationship if it has a parent ---
    if parent_node_id:
        print(
            f"  Creating Relationship: Parent='{parent_node_id}' -> Child='{generated_node_id}'"
        )
        relationship = NodeRelationship(
            parent_node_id=parent_node_id,
            child_node_id=generated_node_id,  # Link to the newly generated child ID
            relationship_type="CHILD",
        )
        db.session.add(relationship)

    # --- Recursively process children ---
    for child_data in children:
        # Pass the *generated* ID of the current node as the parent_id for its children
        process_node_uuid(
            child_data, graph_id, parent_node_id=current_node_id_for_children
        )


@app.cli.command("upload-graph-uuid")
@click.argument("json_filepath")
@click.argument("graph_name")
def upload_graph_data_uuid(json_filepath, graph_name):
    """
    Uploads graph data from JSON to the database, generating UUIDs for nodes.

    JSON_FILEPATH: Path to the input JSON file (e.g., data.json).
    GRAPH_NAME: The unique name of the graph (e.g., w).
    """
    print(
        f"Starting graph upload from '{json_filepath}' for graph '{graph_name}' (generating UUIDs)..."
    )

    # --- 1. Load JSON data ---
    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Error: JSON data must be a list of node objects.")
            return
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_filepath}'")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON file '{json_filepath}': {e}")
        return
    except Exception as e:
        print(f"Error reading file '{json_filepath}': {e}")
        return

    # --- 2. Find or Create the Graph ---
    graph = Graph.query.filter_by(name=graph_name).first()
    if not graph:
        print(f"Graph '{graph_name}' not found. Creating...")
        try:
            graph = Graph(name=graph_name, description=f"Graph for {graph_name}")
            db.session.add(graph)
            # Flush is needed here to ensure graph.id is populated before being used
            db.session.flush()
            print(f"Graph '{graph_name}' created with ID: {graph.id}")
        except Exception as e:
            db.session.rollback()
            print(f"Error: Could not create graph '{graph_name}': {e}")
            return
    else:
        print(f"Found existing graph '{graph_name}' with ID: {graph.id}")

    graph_id = graph.id

    # --- 3. Process Nodes Recursively ---
    try:
        for root_node_data in data:
            # Start recursion, no parent for root nodes
            process_node_uuid(root_node_data, graph_id, parent_node_id=None)

        # --- 4. Commit Changes ---
        print("Committing changes to the database...")
        db.session.commit()
        print("Database upload completed successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"\nError during node processing: {e}")
        print("Database transaction rolled back. No changes were saved.")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # --- Keep main execution block ---
    # --- Populate Cache At Startup ---
    print("Attempting initial population of static definition cache...")
    _get_cached_static_definitions()  # Attempt to pre-populate cache at startup
    # --- End Cache Population ---
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"Starting Flask app: host={host}, port={port}, debug={debug_mode}")
    app.run(host=host, port=port, debug=debug_mode)

# Helper function to handle potential NoneType in cache population log message
