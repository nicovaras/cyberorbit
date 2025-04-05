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

@app.route("/data", methods=["GET"])
@login_required
def get_data():
    """Gets the full graph state for the logged-in user."""
    try:
        user_id = current_user.id
        selected_graph_name = request.args.get('graph', 'x') # Default to 'x'
        graph = Graph.query.filter_by(name=selected_graph_name).first()

        if not graph:
             print(f"Graph '{selected_graph_name}' not found in database.")
             # Maybe load default graph 'x' if graph 1 exists?
             graph = db.session.get(Graph, 1) # Assuming graph 'x' has id=1
             if not graph:
                 return jsonify({"error": f"Default graph not found"}), 404

        print(f"Computing state for user {user_id}, graph {graph.id} ({graph.name})")
        # Update streak *before* calculating state potentially involving badges
        streak_data = core_streak.update_user_streak(user_id)

        # Compute the state (this now also updates DB node status)
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(user_id, graph.id)

        # Fetch other user-specific data
        ctfs = core_ctfs.get_combined_ctf_data_for_user(user_id)
        abilities = core_nodes.compute_abilities(user_id, graph.id)
        user_badges = core_badges.get_user_badges(user_id) # Fetches already earned badges

        # Check for and award *new* badges after state computation
        newly_awarded_badges_defs = core_badges.check_and_award_badges(user_id, graph.id)

        # Combine existing and newly awarded for frontend display
        all_display_badges = user_badges + [
             {**badge_def.__dict__, 'image': badge_def.image_path} # Convert newly awarded model to dict
             for badge_def in newly_awarded_badges_defs
             if badge_def # Filter out None if badge def wasn't found
        ]
        # Remove potential internal SQLAlchemy state from dicts
        for badge in all_display_badges:
            badge.pop('_sa_instance_state', None)


        state = {
            "nodes": nodes,
            "links": links,
            "unlocked": {nid: status for nid, status in unlocked.items()}, # Convert set/map if needed by JS
            "discovered": list(discovered), # Convert set to list for JSON
            "streak": streak_data,
            "ctfs": ctfs,
            "abilities": abilities,
            "badges": all_display_badges, # Combined list
            "current_graph": graph.name # Send back the name of the graph used
        }
        return jsonify(state)

    except Exception as e:
        # Log the error
        print(f"Error in GET /data for user {current_user.id}: {e}")
        # Potentially rollback session if db operations were started
        # db.session.rollback()
        return jsonify({"error": "Failed to retrieve graph data", "details": str(e)}), 500


@app.route("/data", methods=["POST"])
@login_required
def post_data():
    """Handles updates for exercises or node notes."""
    user_id = current_user.id
    payload = request.json
    graph_name = request.args.get('graph', 'x') # Need graph context for recomputing state
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1 # Default to graph 1 if not found

    update_successful = True
    update_type = payload.get('update_type') # Hypothetical field to differentiate updates

    try:
        if 'exercise_update' in payload:
            ex_data = payload['exercise_update']
            exercise_id = ex_data.get('exercise_id')
            is_completed = ex_data.get('completed')
            if exercise_id is not None and is_completed is not None:
                print(f"Updating exercise {exercise_id} for user {user_id} to {is_completed}")
                update_successful &= core_data.update_user_exercise_completion(user_id, exercise_id, is_completed)
            else: update_successful = False; print(f"Invalid exercise update payload")

        elif 'notes_update' in payload: # Use elif if updates are mutually exclusive per request
            notes_data = payload['notes_update']
            node_id = notes_data.get('node_id')
            notes = notes_data.get('notes')
            if node_id is not None and notes is not None:
                print(f"Updating notes for node {node_id} for user {user_id}")
                update_successful &= core_data.update_user_node_notes(user_id, node_id, notes)
            else: update_successful = False; print(f"Invalid notes update payload")
        else:
            # Handle unknown update type or disallow requests with no known update type
            return jsonify({"error": "Unknown or missing update type in payload"}), 400

        if not update_successful:
            return jsonify({"error": "Failed to apply update"}), 400 # Or more specific error

        # Recompute and return the full state after successful update
        # (This logic duplicates GET /data - could be refactored into a helper)
        streak_data = core_streak.update_user_streak(user_id) # Update streak on interaction
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(user_id, graph_id)
        ctfs = core_ctfs.get_combined_ctf_data_for_user(user_id)
        abilities = core_nodes.compute_abilities(user_id, graph_id)
        user_badges = core_badges.get_user_badges(user_id)
        newly_awarded_badges_defs = core_badges.check_and_award_badges(user_id, graph_id)
        all_display_badges = user_badges + [
             {**badge_def.__dict__, 'image': badge_def.image_path}
             for badge_def in newly_awarded_badges_defs if badge_def ]
        for badge in all_display_badges: badge.pop('_sa_instance_state', None)

        state = {
            "nodes": nodes, "links": links, "unlocked": {nid: status for nid, status in unlocked.items()},
            "discovered": list(discovered), "streak": streak_data, "ctfs": ctfs,
            "abilities": abilities, "badges": all_display_badges, "current_graph": graph_name
        }
        return jsonify(state)

    except Exception as e:
        db.session.rollback() # Rollback on error during update
        print(f"Error processing POST /data for user {user_id}: {e}")
        return jsonify({"error": "Failed to process data update", "details": str(e)}), 500


@app.route("/ctfs", methods=["POST"])
@login_required
def post_ctfs():
    """Handles updates to user's CTF completion counts."""
    user_id = current_user.id
    # Assuming payload is the *full list* of CTFs from the frontend,
    # where each item now includes 'id' and the new 'completed' count.
    ctf_updates = request.json
    graph_name = request.args.get('graph', 'x') # Need graph context for recomputing state
    graph = Graph.query.filter_by(name=graph_name).first()
    graph_id = graph.id if graph else 1 # Default to graph 1

    if not isinstance(ctf_updates, list):
        return jsonify({"error": "Invalid payload format, expected a list of CTFs"}), 400

    try:
        # Fetch current completions to calculate delta
        current_completions = core_ctfs.get_user_ctf_completions(user_id)

        for ctf_data in ctf_updates:
            ctf_id = ctf_data.get('id')
            new_count = ctf_data.get('completed')
            if ctf_id is None or new_count is None:
                print(f"Skipping invalid CTF update item for user {user_id}: {ctf_data}")
                continue

            current_count = current_completions.get(ctf_id, 0)
            delta = new_count - current_count
            if delta != 0:
                print(f"Updating CTF {ctf_id} for user {user_id} by delta {delta}")
                success = core_ctfs.update_user_ctf_completion(user_id, ctf_id, delta)
                if not success:
                    # Handle potential individual update failure if needed
                    print(f"Warning: Failed to update completion for CTF {ctf_id}, user {user_id}")

        # Recompute and return the full state
        # (This logic duplicates GET /data - could be refactored into a helper)
        streak_data = core_streak.update_user_streak(user_id) # Update streak on interaction
        nodes, links, unlocked, discovered = core_nodes.compute_user_graph_state(user_id, graph_id)
        ctfs = core_ctfs.get_combined_ctf_data_for_user(user_id) # Fetch updated combined data
        abilities = core_nodes.compute_abilities(user_id, graph_id)
        user_badges = core_badges.get_user_badges(user_id)
        newly_awarded_badges_defs = core_badges.check_and_award_badges(user_id, graph_id)
        all_display_badges = user_badges + [
             {**badge_def.__dict__, 'image': badge_def.image_path}
             for badge_def in newly_awarded_badges_defs if badge_def ]
        for badge in all_display_badges: badge.pop('_sa_instance_state', None)

        state = {
            "nodes": nodes, "links": links, "unlocked": {nid: status for nid, status in unlocked.items()},
            "discovered": list(discovered), "streak": streak_data, "ctfs": ctfs,
            "abilities": abilities, "badges": all_display_badges, "current_graph": graph_name
        }
        return jsonify(state)

    except Exception as e:
        db.session.rollback() # Rollback on error during update
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