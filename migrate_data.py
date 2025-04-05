# migrate_data.py
import json
import os
from dotenv import load_dotenv

# --- Flask App and DB Setup (for context) ---
# We need the app context to interact with the database defined in models.py
# This assumes your Flask app instance is named 'app' in 'app.py'
# and your models/db are defined in 'models.py'

# Important: Ensure this script can import your app and models correctly.
# You might need to adjust Python path depending on your structure.
try:
    from app import app, db
    from models import (Graph, Node, Exercise, ExerciseCategory,
                        NodeRelationship, Ctf, Badge, exercise_category_map)
except ImportError as e:
    print(f"Error importing Flask app or models: {e}")
    print("Make sure this script is run from the project root directory")
    print("or adjust the Python path if necessary.")
    exit(1)

from sqlalchemy.dialects.postgresql import insert as pg_insert


# --- Configuration ---
JSON_DIR = "json"
NODE_FILES = ["x.json", "y.json"] # Add other node files if they exist
CTF_FILE = os.path.join(JSON_DIR, "ctfs.json")
# BADGE_FILE = os.path.join(JSON_DIR, "badges.json") # Existing badges.json is empty
# Define static badges directly based on core/badges.py logic
BADGE_DEFINITIONS = [
    # Levels
    {"id": "level-5", "title": "Level 5 Achieved", "desc": "You reached level 5", "img": "static/badges/badge_level_5.png"},
    {"id": "level-10", "title": "Level 10 Achieved", "desc": "You reached level 10", "img": "static/badges/badge_level_10.png"},
    {"id": "level-15", "title": "Level 15 Achieved", "desc": "You reached level 15", "img": "static/badges/badge_level_15.png"},
    {"id": "level-20", "title": "Level 20 Achieved", "desc": "You reached level 20", "img": "static/badges/badge_level_20.png"},
    {"id": "level-25", "title": "Level 25 Achieved", "desc": "You reached level 25", "img": "static/badges/badge_level_25.png"},
    {"id": "level-30", "title": "Level 30 Achieved", "desc": "You reached level 30", "img": "static/badges/badge_level_30.png"},
    # Exercises
    {"id": "exercises-10", "title": "10 Exercises Completed", "desc": "You completed 10 exercises.", "img": "static/badges/badge_ex_10.png"},
    {"id": "exercises-25", "title": "25 Exercises Completed", "desc": "You completed 25 exercises.", "img": "static/badges/badge_ex_25.png"},
    {"id": "exercises-50", "title": "50 Exercises Completed", "desc": "You completed 50 exercises.", "img": "static/badges/badge_ex_50.png"},
    {"id": "exercises-75", "title": "75 Exercises Completed", "desc": "You completed 75 exercises.", "img": "static/badges/badge_ex_75.png"},
    {"id": "exercises-100", "title": "100 Exercises Completed", "desc": "You completed 100 exercises.", "img": "static/badges/badge_ex_100.png"},
    # CTFs
    {"id": "ctf-5", "title": "5 CTFs Completed", "desc": "You completed 5 CTF challenges.", "img": "static/badges/badge_ctf_5.png"},
    {"id": "ctf-10", "title": "10 CTFs Completed", "desc": "You completed 10 CTF challenges.", "img": "static/badges/badge_ctf_10.png"},
    {"id": "ctf-15", "title": "15 CTFs Completed", "desc": "You completed 15 CTF challenges.", "img": "static/badges/badge_ctf_15.png"},
    {"id": "ctf-20", "title": "20 CTFs Completed", "desc": "You completed 20 CTF challenges.", "img": "static/badges/badge_ctf_20.png"},
    {"id": "ctf-25", "title": "25 CTFs Completed", "desc": "You completed 25 CTF challenges.", "img": "static/badges/badge_ctf_25.png"},
    {"id": "ctf-30", "title": "30 CTFs Completed", "desc": "You completed 30 CTF challenges.", "img": "static/badges/badge_ctf_30.png"},
    # Add other ctf counts (15, 20, 25, 30...)
    # Streaks
    {"id": "streak-7", "title": "7 Days Streak", "desc": "You maintained a streak of 7 days.", "img": "static/badges/badge_streak_7.png"},
    {"id": "streak-14", "title": "14 Days Streak", "desc": "You maintained a streak of 14 days.", "img": "static/badges/badge_streak_14.png"},
    {"id": "streak-21", "title": "21 Days Streak", "desc": "You maintained a streak of 21 days.", "img": "static/badges/badge_streak_21.png"},
    {"id": "streak-28", "title": "28 Days Streak", "desc": "You maintained a streak of 28 days.", "img": "static/badges/badge_streak_28.png"},
    # Add other streak counts (21, 28...)
    # Main Node Badges will be dynamically generated IDs like 'main-<node_id>'
]


# --- Helper Functions ---
def load_json_file(filepath):
    """Loads data from a JSON file."""
    if not os.path.exists(filepath):
        print(f"Warning: File not found - {filepath}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return None
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

# --- Migration Functions ---

def migrate_graphs():
    """Creates entries for the known graphs."""
    print("Migrating graphs...")
    graphs_to_create = []
    for filename in NODE_FILES:
        graph_name = filename.replace('.json', '')
        existing = Graph.query.filter_by(name=graph_name).first()
        if not existing:
            graphs_to_create.append(Graph(name=graph_name, description=f"Roadmap {graph_name.upper()}"))
        else:
            print(f"- Graph '{graph_name}' already exists.")

    if graphs_to_create:
        db.session.add_all(graphs_to_create)
        db.session.flush() # Flush to get IDs if needed later in same transaction
        print(f"+ Added {len(graphs_to_create)} new graphs.")
    else:
        print("  No new graphs to add.")

def migrate_nodes_and_exercises():
    """Migrates nodes, exercises, categories, and relationships."""
    print("\nMigrating nodes, exercises, and relationships...")
    all_node_data = []
    graph_map = {g.name: g.id for g in Graph.query.all()} # Get graph names and IDs

    for filename in NODE_FILES:
        graph_name = filename.replace('.json', '')
        graph_id = graph_map.get(graph_name)
        if not graph_id:
            print(f"Error: Graph '{graph_name}' not found in database. Skipping {filename}.")
            continue

        print(f" Processing {filename} for graph_id {graph_id}...")
        filepath = os.path.join(JSON_DIR, filename)
        node_list = load_json_file(filepath)
        if node_list is None:
            continue

        for node_json in node_list:
            if 'id' not in node_json or node_json['id'] == 'Start': # Skip Start node placeholder
                 continue
            node_json['graph_id'] = graph_id # Add graph_id association
            all_node_data.append(node_json)

    nodes_to_add = []
    exercises_to_add = []
    relationships_to_add = []
    exercise_category_mappings = [] # Store tuples (exercise_id, category_name)
    existing_categories = {cat.name: cat.category_id for cat in ExerciseCategory.query.all()}
    categories_to_add = {} # name -> ExerciseCategory object

    for node_json in all_node_data:
        node_id = node_json['id']
        # Create Node object
        existing_node = db.session.get(Node, node_id)
        if not existing_node:
            nodes_to_add.append(Node(
                id=node_id,
                graph_id=node_json['graph_id'],
                title=node_json.get('title', 'Untitled Node'),
                type=node_json.get('type', 'sub'),
                popup_text=node_json.get('popup', {}).get('text'),
                pdf_link=node_json.get('popup', {}).get('pdf_link')
            ))
        else:
             # Optionally update existing nodes if needed
             pass

        # Create Exercise objects and map categories
        for ex_json in node_json.get('popup', {}).get('exercises', []):
            ex_id = ex_json.get('id')
            if not ex_id: continue
            existing_ex = db.session.get(Exercise, ex_id)
            if not existing_ex:
                exercises_to_add.append(Exercise(
                    id=ex_id,
                    node_id=node_id,
                    label=ex_json.get('label', 'Exercise'),
                    points=ex_json.get('points', 10),
                    optional=ex_json.get('optional', False)
                ))
                # Handle categories for the new exercise
                for cat_name in ex_json.get('categories', []):
                    if cat_name not in existing_categories and cat_name not in categories_to_add:
                         categories_to_add[cat_name] = ExerciseCategory(name=cat_name)
                    exercise_category_mappings.append((ex_id, cat_name))
            else:
                 # Optionally update existing exercises
                 pass

        # Create NodeRelationship objects
        for child_id in node_json.get('children', []):
            relationships_to_add.append({'parent': node_id, 'child': child_id, 'type': 'CHILD'})
        for prereq_id in node_json.get('prerequisites', []):
             # Ensure prereq isn't 'Start' before adding relationship to DB model
            if prereq_id != 'Start':
                 relationships_to_add.append({'parent': prereq_id, 'child': node_id, 'type': 'PREREQUISITE'})


    # Add new objects in dependency order
    if categories_to_add:
        db.session.add_all(categories_to_add.values())
        db.session.flush() # Get IDs for newly added categories
        # Update existing_categories map
        existing_categories.update({cat.name: cat.category_id for cat in categories_to_add.values()})
        print(f"+ Added {len(categories_to_add)} new categories.")

    if nodes_to_add:
        db.session.add_all(nodes_to_add)
        print(f"+ Added {len(nodes_to_add)} new nodes.")

    if exercises_to_add:
        db.session.add_all(exercises_to_add)
        print(f"+ Added {len(exercises_to_add)} new exercises.")
        db.session.flush()

    # Add exercise category mappings (handle potential duplicates if script run multiple times)
    print(f"  Processing {len(exercise_category_mappings)} exercise-category links...")

    mappings_to_insert = []
    processed_mapping_links = 0
    for ex_id, cat_name in exercise_category_mappings:
         cat_id = existing_categories.get(cat_name)
         if cat_id:
             # Check if mapping already exists might be needed depending on DB/ORM
             # For bulk insert, rely on UNIQUE constraint and IGNORE/ON CONFLICT
             mappings_to_insert.append({'exercise_id': ex_id, 'category_id': cat_id})
             processed_mapping_links += 1
         else:
             print(f"Warning: Category ID not found for '{cat_name}' when mapping exercise '{ex_id}'.")
    if mappings_to_insert:
        stmt = pg_insert(exercise_category_map).values(mappings_to_insert)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['exercise_id', 'category_id'] 
        )
        db.session.execute(stmt) 
        print(f"+ Added/Ignored {processed_mapping_links} exercise-category mappings.")

    # Add relationships (handle potential duplicates)
    print(f"  Processing {len(relationships_to_add)} relationships...")
    rel_added_count = 0
    for rel in relationships_to_add:
         # Check if relationship already exists
        exists = NodeRelationship.query.filter_by(
            parent_node_id=rel['parent'],
            child_node_id=rel['child'],
            relationship_type=rel['type']
        ).first()
        if not exists:
             # Ensure parent and child nodes actually exist in the DB before adding rel
             # Using get() is efficient if nodes were flushed or already committed
            parent_exists = db.session.get(Node, rel['parent']) is not None
            child_exists = db.session.get(Node, rel['child']) is not None
            if parent_exists and child_exists:
                 db.session.add(NodeRelationship(
                     parent_node_id=rel['parent'],
                     child_node_id=rel['child'],
                     relationship_type=rel['type']
                 ))
                 rel_added_count += 1
            else:
                 print(f"Warning: Skipping relationship {rel['parent']} -> {rel['child']} ({rel['type']}) due to missing node.")

    print(f"+ Added {rel_added_count} new relationships.")



def migrate_ctfs():
    """Migrates CTF definitions."""
    print("\nMigrating CTFs...")
    ctf_list = load_json_file(CTF_FILE)
    if not ctf_list:
        print("  No CTF data found or error loading.")
        return

    ctfs_to_add = []
    for ctf_json in ctf_list:
        existing = Ctf.query.filter_by(title=ctf_json.get('title')).first()
        if not existing:
            ctfs_to_add.append(Ctf(
                title=ctf_json.get('title', 'Untitled CTF'),
                description=ctf_json.get('description'),
                link=ctf_json.get('link')
            ))
        else:
            print(f"- CTF '{ctf_json.get('title')}' already exists.")

    if ctfs_to_add:
        db.session.add_all(ctfs_to_add)
        print(f"+ Added {len(ctfs_to_add)} new CTFs.")
    else:
        print("  No new CTFs to add.")

def migrate_badges():
    """Creates badge definitions based on hardcoded list."""
    print("\nMigrating Badges...")
    badges_to_add = []
    # Add main node badges dynamically based on nodes in DB
    main_nodes = Node.query.filter_by(type='main').all()
    dynamic_badge_defs = list(BADGE_DEFINITIONS) # Copy static list
    for node in main_nodes:
        badge_id = f"main-{node.id}"
        dynamic_badge_defs.append({
             "id": badge_id,
             "title": f"{node.title} Completed",
             "desc": f"Completed {node.title}",
             "img": f"static/badges/badge_main_{node.id}.png" # Assumes image exists
        })
        # Add 'all exercises' badge if needed, requires knowing total count
        # total_req_exercises = Exercise.query.join(Node).filter(Node.graph_id == node.graph_id, Exercise.optional == False).count()
        # if total_req_exercises > 0:
        #    badge_id = f"exercises-{total_req_exercises}"
        #     # Add logic to avoid duplicate 'all' badges if multiple graphs exist
        #     if not any(b['id'] == badge_id for b in dynamic_badge_defs):
        #          dynamic_badge_defs.append({
        #              "id": badge_id, "title": "All Exercises Completed", ...
        #          })


    for badge_def in dynamic_badge_defs:
        existing = db.session.get(Badge, badge_def['id'])
        if not existing:
            badges_to_add.append(Badge(
                id=badge_def['id'],
                title=badge_def['title'],
                description=badge_def['desc'],
                image_path=badge_def['img']
            ))
        else:
             print(f"- Badge '{badge_def['id']}' already exists.")

    if badges_to_add:
        db.session.add_all(badges_to_add)
        print(f"+ Added {len(badges_to_add)} new Badges.")
    else:
        print("  No new Badges to add.")

# --- Main Execution ---
if __name__ == "__main__":
    load_dotenv() # Load .env for DATABASE_URL

    # Ensure we have app context to use db.session
    with app.app_context():
        print("Starting database migration...")

        # Optional: Clear existing static data if running multiple times?
        # Be careful with this in production!
        # print("Clearing existing static data (Nodes, Exercises, CTFs, Badges)...")
        # NodeRelationship.query.delete()
        # exercise_category_map.delete() # Need to use db.session.execute(exercise_category_map.delete())
        # ExerciseCategory.query.delete()
        # Exercise.query.delete()
        # Node.query.delete()
        # Ctf.query.delete()
        # Badge.query.delete()
        # Graph.query.delete()
        # db.session.commit()

        migrate_graphs()
        db.session.commit() # Commit after graph creation

        migrate_nodes_and_exercises()
        db.session.commit() # Commit after nodes/exercises/rels

        migrate_ctfs()
        db.session.commit() # Commit after ctfs

        migrate_badges()
        db.session.commit() # Commit after badges

        print("\nMigration completed.")