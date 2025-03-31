from flask import Flask, jsonify, request, send_from_directory, render_template_string
from core.data import load_data, save_data
from core.streak import update_streak
from core.ctfs import load_ctfs, save_ctfs
from core.badges import check_and_award_badges, load_badges, save_badges
from core.nodes import compute_node_states, compute_abilities, compute_discovered_nodes
import markdown
import os
from markupsafe import Markup

app = Flask(__name__, static_folder=".")
with open("index.html") as f:
    INDEX_HTML = f.read()

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/data", methods=["GET"])
def get_data():
    data = load_data()
    nodes, links, unlocked = compute_node_states(data)
    streak = update_streak()
    ctfs = load_ctfs()
    abilities = compute_abilities(data, ctfs)
    badges = load_badges()
    updated_badges = check_and_award_badges(nodes, ctfs, streak, badges)
    save_badges(updated_badges)

    discovered = compute_discovered_nodes(unlocked, links)

    return jsonify({
        "nodes": nodes,
        "links": links,
        "unlocked": unlocked,
        "discovered": list(discovered),
        "streak": streak,
        "ctfs": ctfs,
        "abilities": abilities,
        "badges": updated_badges
    })

@app.route("/data", methods=["POST"])
def post_data():
    save_data(request.json)
    return jsonify({"status": "ok"})

@app.route("/ctfs", methods=["POST"])
def post_ctfs():
    save_ctfs(request.json)
    return jsonify({"status": "ok"})

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

@app.route("/md/<path:filename>")
def serve_markdown(filename):
    path = os.path.join("static", "md", filename)
    if not os.path.exists(path):
        return "Markdown file not found", 404
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
    return render_template_string(f"""
    <html>
      <head>
        <title>{filename}</title>
        <style>
          body {{ background: #0b1120; color: #cceeff; font-family: monospace; padding: 40px; max-width: 800px; margin: auto; }}
          h1,h2,h3 {{ color: #00ffff; }}
          pre {{ background: #111; padding: 10px; border-radius: 8px; overflow-x: auto; }}
          code {{ color: #00ff99; }}
          table {{ border-collapse: collapse; }}
          th, td {{ border: 1px solid #00ffcc; padding: 5px; }}
        </style>
      </head>
      <body>{Markup(html)}</body>
    </html>
    """)

@app.route("/update_badges", methods=["POST"])
def update_badges():
    payload = request.json
    ids = payload.get("badgeIds", [])
    badges = load_badges()
    changed = False
    for b in badges:
        if b["id"] in ids and not b.get("shown", False):
            b["shown"] = True
            changed = True
    if changed:
        save_badges(badges)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
