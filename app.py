from flask import Flask, jsonify, request, send_from_directory, render_template_string, abort
from werkzeug.utils import safe_join
# Ensure load_data and save_data are imported correctly if they are not already
from core.data import load_data, save_data
from core.streak import update_streak
from core.ctfs import load_ctfs, save_ctfs
from core.badges import check_and_award_badges, load_badges, save_badges
from core.nodes import compute_node_states # Make sure compute_node_states is imported
from core.nodes import compute_abilities, compute_discovered_nodes
import markdown
import os
from markupsafe import Markup
from core.s3sync import sync_down
from werkzeug.exceptions import HTTPException, NotFound

# --- Initial Setup ---
for f in ["json/ctfs.json", "json/x.json", "json/streak.json", "json/badges.json"]:
    try:
        os.makedirs(os.path.dirname(f), exist_ok=True)
        sync_down(f)
    except Exception as e:
        print(f"Warning: Failed initial sync for {f}. Error: {e}")

app = Flask(__name__, static_folder="static") # Set static_folder to 'static' directly
# Load index.html once
try:
    # Assuming index.html is in the root directory, adjacent to app.py
    app_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(app_dir, "index.html")
    with open(index_path) as f:
        INDEX_HTML = f.read()
except FileNotFoundError:
    INDEX_HTML = "<!DOCTYPE html><html><head><title>Error</title></head><body><h1>Error</h1><p>index.html not found.</p></body></html>"
    print(f"Error: index.html not found at {index_path}. Serving basic error page.")

# --- Helper function to get the full computed state ---
def get_computed_state(graph_filename="x.json"):
    """Loads all data for the SPECIFIED graph, computes derived states, and returns the full state object."""
    try:
        # <<< Pass filename to load_data >>>
        data = load_data(graph_filename) # Load specified nodes data
        if not data: # Handle case where data file is empty or missing
             print(f"Warning: No data loaded from {graph_filename}, returning empty state.")
             return {
                 "nodes": [], "links": [], "unlocked": {}, "discovered": [],
                 "streak": {}, "ctfs": [], "abilities": {}, "badges": []
             }
    
        # Compute states based on the loaded data
        nodes, links, unlocked = compute_node_states(data) # compute_node_states uses the data passed in

        # Other computations remain the same (streak, ctfs, badges are likely global)
        streak = update_streak()
        ctfs = load_ctfs()
        abilities = compute_abilities(nodes, ctfs) # Use computed nodes
        badges = load_badges()
        updated_badges = check_and_award_badges(nodes, ctfs, streak, badges)
        if badges != updated_badges:
             save_badges(updated_badges)
             badges = updated_badges
        discovered = compute_discovered_nodes(unlocked, links)

        # Include the current graph filename in the state for the frontend
        return {
            "nodes": nodes, "links": links, "unlocked": unlocked,
            "discovered": list(discovered), "streak": streak, "ctfs": ctfs,
            "abilities": abilities, "badges": badges,
            "current_graph": graph_filename # <<< Add current graph info
        }
    except Exception as e:
        print(f"Error computing application state for {graph_filename}: {e}")
        # Consider more specific error handling if needed
        return { # Return empty state on error
             "nodes": [], "links": [], "unlocked": {}, "discovered": [],
             "streak": {}, "ctfs": [], "abilities": {}, "badges": [], "current_graph": graph_filename
        }

# --- Routes ---

@app.route("/")
def index():
    """Serves the main index.html page."""
    # No change needed here if using query parameters for graph selection
    return render_template_string(INDEX_HTML)

@app.route("/data", methods=["GET"])
def get_data():
    """Handles initial data load request from frontend, selecting graph via query param."""
    # <<< Get graph selection from query parameter >>>
    selected_graph = request.args.get('graph', 'x') # Default to 'x'
    graph_filename = f"{selected_graph}.json"
    if graph_filename not in ["x.json", "y.json"]: # Validate
         graph_filename = "x.json"

    # <<< Pass filename to state computation >>>
    state = get_computed_state(graph_filename)
    return jsonify(state)

@app.route("/data", methods=["POST"])
def post_data():
    """Handles updates to the main node data (e.g., exercise completion) for the specified graph."""
    # <<< Get graph selection from query parameter >>>
    selected_graph = request.args.get('graph', 'x') # Default to 'x'
    graph_filename = f"{selected_graph}.json"
    if graph_filename not in ["x.json", "y.json"]: # Validate
         graph_filename = "x.json"

    try:
        # <<< Pass filename to save_data >>>
        save_data(request.json, graph_filename) # Save nodes data to the correct file
        # <<< Pass filename to state computation >>>
        updated_state = get_computed_state(graph_filename) # Recompute state for the saved graph
        return jsonify(updated_state)
    except Exception as e:
        print(f"Error processing POST /data for {graph_filename}: {e}")
        return jsonify({"error": "Failed to process node data update", "details": str(e)}), 500


@app.route("/ctfs", methods=["POST"])
def post_ctfs():
    """Handles updates to CTF completion data."""
    try:
        save_ctfs(request.json)
        updated_state = get_computed_state()
        return jsonify(updated_state)
    except Exception as e:
        print(f"Error processing POST /ctfs: {e}")
        return jsonify({"error": "Failed to process CTF data update", "details": str(e)}), 500


# Correctly serve static files from the 'static' folder relative to app.py
# Flask does this automatically if static_folder is set correctly in app = Flask(...)
# So this route might be redundant unless you need custom logic for static files.
# If you keep it, ensure the path logic is robust.
@app.route("/static/<path:path>")
def static_files(path):
    # Use Flask's safe_join to prevent path traversal issues
    try:
        # Assuming static folder is 'static' relative to app.py
        safe_path = safe_join(app.static_folder, path)
        if safe_path is None:
             abort(404)
        return send_from_directory(os.path.dirname(safe_path), os.path.basename(safe_path))
    except NotFound:
         abort(404)
    except Exception as e:
         print(f"Error serving static file {path}: {e}")
         abort(500)


@app.route("/md/<path:filename>")
def serve_markdown_md(filename):
    try:
        return serve_markdown(filename, "md")
    except NotFound:
        print(f"Caught FileNotFoundError for: {filename}")
        abort(404)
    except Exception as e:
        print(f"Error rendering markdown {filename}: {e}")
        abort(500)


@app.route("/mdml/<path:filename>")
def serve_markdown_mdml(filename):
    try:
        return serve_markdown(filename, "mdml")
    except NotFound:
        print(f"Caught FileNotFoundError for: {filename}")
        abort(404)
    except Exception as e:
        print(f"Error rendering markdown {filename}: {e}")
        abort(500)



def serve_markdown(filename, folder):
    """Serves markdown files from the static/md directory rendered as HTML."""
    markdown_dir = os.path.join(app.root_path, app.static_folder, folder)
    filepath = safe_join(markdown_dir, filename)
    if filepath is None or not os.path.isfile(filepath):
        print(f"Markdown file not found or path issue: {filename}")
        abort(404)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Render markdown with code highlighting extensions
    html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'codehilite'])

    # Define minimal layout styles, letting the theme handle colors/code
    # You can adjust padding, max-width as desired
    layout_style = """
        body {
            padding: 30px 40px; /* Adjust padding */
            max-width: 850px; /* Adjust max width */
            margin: 20px auto; /* Center content with top/bottom margin */
            line-height: 1.7; /* Improve readability */
            overflow: auto !important;
        }
        /* Optional: Add specific styles for elements not covered well by theme */
        img { max-width: 100%; height: auto; margin: 1em 0; } /* Responsive images */
        table { width: 100%; margin: 1.5em 0; } /* Full width tables */
        blockquote {
            border-left: 4px solid var(--comment, #6272a4); /* Use theme variable */
            padding-left: 15px;
            margin-left: 0;
            color: var(--base0, #839496); /* Dimmer text for quotes */
            font-style: italic;
        }
        hr {
            border: none;
            border-top: 1px solid var(--current-line, #44475a); /* Theme variable */
            margin: 2em 0;
        }
        a {
        border:none;
        }
    """

    # Render using template string, linking the theme CSS
    # Using Dracula theme as an example default
    theme_css_path = "/static/monokai.css" # Or dynamically choose based on user pref?
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
    """
    )



@app.route("/update_badges", methods=["POST"])
def update_badges_shown_status():
    """Marks specific badges as 'shown'."""
    payload = request.json
    if not payload or "badgeIds" not in payload:
        return jsonify({"error": "Missing badgeIds in payload"}), 400
    ids_to_mark = payload.get("badgeIds", [])
    if not isinstance(ids_to_mark, list):
         return jsonify({"error": "Invalid payload format, expected list for badgeIds"}), 400

    try:
        badges = load_badges()
        changed = False
        for b in badges:
            if b.get("id") in ids_to_mark and not b.get("shown", False):
                b["shown"] = True
                changed = True
        if changed:
            save_badges(badges)
            print(f"Marked badges as shown: {ids_to_mark}")
            return jsonify({"status": "ok", "updated": True})
        else:
             return jsonify({"status": "ok", "updated": False})
    except Exception as e:
         print(f"Error processing POST /update_badges: {e}")
         return jsonify({"error": "Failed to update badge status", "details": str(e)}), 500

# --- Main Execution ---
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"Starting Flask app: host={host}, port={port}, debug={debug_mode}")
    app.run(host=host, port=port, debug=debug_mode)