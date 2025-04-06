# graph_editor_app/editor_app.py
import os
import uuid
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import and_ # Import 'and_' for combined filters
from dotenv import load_dotenv
from flask_cors import CORS # Import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-fallback-secret-key-editor') # Use shared or specific key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("DATABASE_URL environment variable not set in .env file.")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Import Models ---
# This assumes models.py is in the SAME directory as editor_app.py
# If it's elsewhere, adjust the import path accordingly.
try:
    from models import db, Graph, Node, NodeRelationship, Exercise, ExerciseCategory, UserNodeStatus, UserExerciseCompletion
    # Add any other models needed
except ImportError as e:
     print(f"Error importing models: {e}")
     print("Ensure 'models.py' is in the same directory as 'editor_app.py' or adjust the import path.")
     # Depending on your setup, you might need sys.path manipulation if models.py is outside
     # import sys
     # sys.path.append('..') # Example: if models.py is one directory up
     # from models import ...
     exit(1) # Exit if models can't be loaded

db.init_app(app)

# Import the ID generator
from utils import generate_unique_id

# --- Helper Functions ---

def get_node_or_404(node_id):
    """Fetches a node by ID or aborts with 404."""
    # Use db.session.get for primary key lookups if available and efficient
    node = db.session.get(Node, node_id)
    # Fallback or alternative:
    # node = Node.query.get(node_id) # .get() is often shorthand for PK lookup
    if not node:
        abort(404, description=f"Node with id '{node_id}' not found.")
    return node

def get_exercise_or_404(exercise_id):
    """Fetches an exercise by ID or aborts with 404."""
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        abort(404, description=f"Exercise with id '{exercise_id}' not found.")
    return exercise

def get_graph_or_404(graph_id):
    """Fetches a graph by ID or aborts with 404."""
    graph = db.session.get(Graph, graph_id)
    if not graph:
        abort(404, description=f"Graph with id '{graph_id}' not found.")
    return graph

# --- API Routes ---
# Note: No '/api/editor' prefix here unless you add it manually to each route

@app.route('/api/graphs', methods=['GET'])
def list_graphs():
    """Returns a list of all available graphs."""
    try:
        graphs = Graph.query.order_by(Graph.name).all()
        return jsonify([{'id': g.id, 'name': g.name} for g in graphs])
    except Exception as e:
        print(f"Error fetching graphs: {e}")
        abort(500, description="Internal server error fetching graphs.")

@app.route('/api/graphs/<int:graph_id>/nodes', methods=['GET'])
def get_graph_nodes(graph_id):
    """Returns nodes and parent relationships for a specific graph."""
    get_graph_or_404(graph_id) # Ensure graph exists
    try:
        nodes = Node.query.filter_by(graph_id=graph_id).all()
        # Fetch only CHILD relationships where both parent and child are in this graph
        relationships = NodeRelationship.query.filter(
            NodeRelationship.relationship_type == 'CHILD',
            NodeRelationship.child_node_id.in_([n.id for n in nodes])
        ).all()

        parent_map = {rel.child_node_id: rel.parent_node_id for rel in relationships}

        nodes_data = [
            {
                'id': n.id,
                'title': n.title,
                'type': n.type,
                'parent_id': parent_map.get(n.id) # Include parent_id
            } for n in nodes
        ]
        return jsonify(nodes_data)
    except Exception as e:
        print(f"Error fetching nodes for graph {graph_id}: {e}")
        abort(500, description="Internal server error fetching graph nodes.")


@app.route('/api/nodes/<node_id>', methods=['GET'])
def get_node_details(node_id):
    """Returns full details for a single node."""
    # Use a try-except block around the main logic after getting the node
    try:
        # Eager load exercises and their categories
        # Use options() directly on the query for clarity
        node = db.session.query(Node).options(
            selectinload(Node.exercises).selectinload(Exercise.categories)
        ).filter(Node.id == node_id).one_or_none() # Use one_or_none for clarity

        if not node:
             abort(404, description=f"Node with id '{node_id}' not found.")

        # Find the parent relationship (CHILD type)
        parent_rel = NodeRelationship.query.filter_by(
            child_node_id=node.id,
            relationship_type='CHILD'
        ).first()
        parent_id = parent_rel.parent_node_id if parent_rel else None

        node_data = {
            'id': node.id,
            'graph_id': node.graph_id,
            'title': node.title,
            'type': node.type,
            'popup_text': node.popup_text,
            'pdf_link': node.pdf_link,
            'parent_id': parent_id,
            'exercises': [
                {
                    'id': ex.id,
                    'label': ex.label,
                    'points': ex.points,
                    'optional': ex.optional,
                    'categories': [cat.name for cat in ex.categories]
                 } for ex in node.exercises
            ]
        }
        return jsonify(node_data)
    except Exception as e:
        # Rollback is generally handled by Flask-SQLAlchemy at the end of request
        # but can be done explicitly if needed mid-request
        print(f"Error fetching details for node {node_id}: {e}")
        abort(500, description="Internal server error fetching node details.")

@app.route('/api/graphs/<int:graph_id>/nodes', methods=['POST'])
def create_node(graph_id):
    """Creates a new node in the specified graph."""
    graph = get_graph_or_404(graph_id)
    data = request.get_json()

    if not data or not data.get('title') or not data.get('type'):
        abort(400, description="Missing required fields: title, type.")

    new_node_id = generate_unique_id()
    parent_id = data.get('parent_id') # Optional parent ID

    # Check if ID already exists (highly unlikely with UUID, but possible with other schemes)
    existing_node = db.session.get(Node, new_node_id)
    if existing_node:
         abort(409, description=f"Generated Node ID '{new_node_id}' already exists. Please try again.") # 409 Conflict

    try:
        new_node = Node(
            id=new_node_id,
            graph_id=graph_id,
            title=data['title'],
            type=data['type'],
            popup_text=data.get('popup_text', ''),
            pdf_link=data.get('pdf_link')
        )
        db.session.add(new_node)

        # Handle parent relationship if provided
        if parent_id:
            parent_node = db.session.get(Node, parent_id)
            if not parent_node or parent_node.graph_id != graph_id:
                db.session.rollback()
                abort(400, description=f"Parent node '{parent_id}' not found in graph '{graph_id}'.")

            # Check if new node already has a parent (shouldn't happen on create, but good practice)
            existing_parent = NodeRelationship.query.filter_by(child_node_id=new_node_id, relationship_type='CHILD').first()
            if existing_parent:
                 db.session.rollback()
                 abort(409, description=f"Node '{new_node_id}' cannot be created with multiple parents.") # 409 Conflict

            parent_rel = NodeRelationship(
                parent_node_id=parent_id,
                child_node_id=new_node_id,
                relationship_type='CHILD'
            )
            db.session.add(parent_rel)

        db.session.commit()

        # Fetch the created node details to return a complete object
        created_node_data = get_node_details(new_node_id).get_json()
        return jsonify(created_node_data), 201 # 201 Created status code

    except Exception as e:
        db.session.rollback()
        print(f"Error creating node in graph {graph_id}: {e}")
        abort(500, description="Internal server error creating node.")

@app.route('/api/nodes/<node_id>', methods=['PUT'])
def update_node(node_id):
    """Updates an existing node's details and parent relationship."""
    node = get_node_or_404(node_id)
    data = request.get_json()

    if not data:
        abort(400, description="No update data provided.")

    try:
        # Update basic fields
        if 'title' in data: node.title = data['title']
        if 'type' in data: node.type = data['type']
        if 'popup_text' in data: node.popup_text = data['popup_text']
        if 'pdf_link' in data: node.pdf_link = data.get('pdf_link') # Use .get() to handle null properly

        # Handle parent update
        # Check if parent_id is explicitly provided in the payload
        if 'parent_id' in data:
            new_parent_id = data['parent_id'] # Could be an ID or null/None

            current_parent_rel = NodeRelationship.query.filter_by(
                child_node_id=node_id,
                relationship_type='CHILD'
            ).first()
            current_parent_id = current_parent_rel.parent_node_id if current_parent_rel else None

            # Only proceed if parent actually changed
            if new_parent_id != current_parent_id:
                # Remove old relationship if it exists
                if current_parent_rel:
                    print(f"Removing old parent link: {current_parent_id} -> {node_id}")
                    db.session.delete(current_parent_rel)

                # Add new relationship if new parent is specified (and not null/None)
                if new_parent_id:
                    # Prevent self-parenting
                    if new_parent_id == node_id:
                        db.session.rollback()
                        abort(400, description="Node cannot be its own parent.")

                    new_parent_node = db.session.get(Node, new_parent_id)
                    if not new_parent_node or new_parent_node.graph_id != node.graph_id:
                        db.session.rollback()
                        abort(400, description=f"New parent node '{new_parent_id}' not found in graph '{node.graph_id}'.")

                     # Double-check constraint before adding new relationship
                    existing_parent_check = NodeRelationship.query.filter_by(child_node_id=node_id, relationship_type='CHILD').count()
                    if existing_parent_check > 0:
                        # This should not happen if the deletion worked, indicates potential issue
                        db.session.rollback()
                        print(f"Error: Node {node_id} conflict detected when setting new parent {new_parent_id}.")
                        abort(500, description="Internal error: Could not clear previous parent relationship.")


                    print(f"Adding new parent link: {new_parent_id} -> {node_id}")
                    new_rel = NodeRelationship(
                        parent_node_id=new_parent_id,
                        child_node_id=node_id,
                        relationship_type='CHILD'
                    )
                    db.session.add(new_rel)
                else:
                    print(f"Setting node {node_id} as root (parent=None)")


        db.session.commit()

        # Fetch updated node details to return
        updated_node_data = get_node_details(node_id).get_json()
        return jsonify(updated_node_data)

    except Exception as e:
        db.session.rollback()
        print(f"Error updating node {node_id}: {e}")
        # Distinguish between client errors (4xx) and server errors (5xx) if possible
        if isinstance(e, (ValueError, TypeError)): # Example client-side issues
             abort(400, description=f"Invalid data for update: {e}")
        abort(500, description="Internal server error updating node.")


@app.route('/api/nodes/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    """Deletes a node and makes its children root nodes."""
    node = get_node_or_404(node_id)

    try:
        # 1. Find relationships where this node is the PARENT (CHILD type)
        child_relationships = NodeRelationship.query.filter_by(
            parent_node_id=node_id,
            relationship_type='CHILD'
        ).all()
        # Remove these relationships (makes children root nodes)
        for rel in child_relationships:
            print(f"Removing parent link from child {rel.child_node_id} due to parent {node_id} deletion.")
            db.session.delete(rel)

        # 2. Find relationship where this node is the CHILD (its parent link)
        parent_relationship = NodeRelationship.query.filter_by(
            child_node_id=node_id,
            relationship_type='CHILD'
        ).first()
        if parent_relationship:
             print(f"Removing node {node_id}'s own parent link.")
             db.session.delete(parent_relationship)

        # 3. Delete exercises associated with the node (assuming cascade delete works OR handle explicitly)
        # If cascade="all, delete-orphan" is set on Node.exercises relationship, this might be automatic.
        # Explicit deletion is safer if unsure.
        # Exercise.query.filter_by(node_id=node_id).delete() # Uncomment if cascade is not reliable

        # 4. Delete user statuses associated with the node (important!)
        UserNodeStatus.query.filter_by(node_id=node_id).delete()

        # 5. Delete the node itself (Exercises might be deleted via cascade now)
        print(f"Deleting node {node_id}.")
        db.session.delete(node)

        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Node {node_id} deleted successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting node {node_id}: {e}")
        abort(500, description="Internal server error deleting node.")


# --- Exercises Endpoints ---

@app.route('/api/nodes/<node_id>/exercises', methods=['POST'])
def add_exercise_to_node(node_id):
    """Adds a new exercise to the specified node."""
    node = get_node_or_404(node_id)
    data = request.get_json()

    if not data or not data.get('label') or 'points' not in data:
        abort(400, description="Missing required fields: label, points.")

    # Validate categories (assuming they are fixed and passed as names)
    # Consider caching categories if they are truly fixed and DB access is slow
    valid_categories = {cat.name: cat for cat in ExerciseCategory.query.all()} # Fetch fixed categories
    category_names = data.get('categories', [])
    categories_to_add = []
    if not isinstance(category_names, list):
         abort(400, description="Categories must be a list of strings.")

    for cat_name in category_names:
        if not isinstance(cat_name, str) or cat_name not in valid_categories:
            db.session.rollback() # Rollback not strictly needed before commit, but good practice
            abort(400, description=f"Invalid or non-string exercise category: {cat_name}")
        categories_to_add.append(valid_categories[cat_name])


    new_exercise_id = generate_unique_id()
    # Check if ID exists (unlikely with UUID)
    existing_ex = db.session.get(Exercise, new_exercise_id)
    if existing_ex:
        abort(409, description=f"Generated Exercise ID '{new_exercise_id}' already exists. Please try again.")


    try:
        new_exercise = Exercise(
            id=new_exercise_id,
            node_id=node_id,
            label=data['label'],
            points=int(data['points']), # Ensure points are integer
            optional=bool(data.get('optional', False)), # Ensure optional is boolean
            categories=categories_to_add # Assign validated category objects
        )
        db.session.add(new_exercise)
        db.session.commit()

        return jsonify({
            'id': new_exercise.id,
            'node_id': new_exercise.node_id, # Include node_id for context
            'label': new_exercise.label,
            'points': new_exercise.points,
            'optional': new_exercise.optional,
            'categories': [cat.name for cat in new_exercise.categories]
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error adding exercise to node {node_id}: {e}")
        abort(500, description="Internal server error adding exercise.")


@app.route('/api/exercises/<exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    """Updates an existing exercise."""
    exercise = get_exercise_or_404(exercise_id)
    data = request.get_json()

    if not data:
        abort(400, description="No update data provided.")

    try:
        if 'label' in data: exercise.label = data['label']
        if 'points' in data: exercise.points = int(data['points'])
        if 'optional' in data: exercise.optional = bool(data['optional'])

        # Handle category updates
        if 'categories' in data:
            category_names = data['categories']
            if not isinstance(category_names, list):
                abort(400, description="Categories must be a list of strings.")

            valid_categories = {cat.name: cat for cat in ExerciseCategory.query.all()}
            categories_to_set = []
            for cat_name in category_names:
                 if not isinstance(cat_name, str) or cat_name not in valid_categories:
                      db.session.rollback()
                      abort(400, description=f"Invalid or non-string exercise category: {cat_name}")
                 categories_to_set.append(valid_categories[cat_name])
            exercise.categories = categories_to_set # Replace existing categories

        db.session.commit()

        return jsonify({
            'id': exercise.id,
            'node_id': exercise.node_id,
            'label': exercise.label,
            'points': exercise.points,
            'optional': exercise.optional,
            'categories': [cat.name for cat in exercise.categories]
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error updating exercise {exercise_id}: {e}")
        abort(500, description="Internal server error updating exercise.")


@app.route('/api/exercises/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """Deletes an exercise."""
    exercise = get_exercise_or_404(exercise_id)

    try:
        # Manually delete related user completions first if cascade isn't set reliably
        # This is important if users might have completed the exercise
        UserExerciseCompletion.query.filter_by(exercise_id=exercise_id).delete()

        db.session.delete(exercise)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Exercise {exercise_id} deleted successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting exercise {exercise_id}: {e}")
        abort(500, description="Internal server error deleting exercise.")


# --- Main Execution ---
if __name__ == "__main__":
    # Create tables if they don't exist within the app context
    # This is useful for initial setup but might be handled separately
    # in a real deployment (e.g., using Flask-Migrate)
    with app.app_context():
        try:
             # Check if tables exist (optional, depends on workflow)
             # inspector = db.inspect(db.engine)
             # if not inspector.has_table("nodes"): # Check one table
             print("Attempting to create database tables if they don't exist...")
             db.create_all()
             print("Tables checked/created.")
        except Exception as e:
             print(f"Error during initial table creation check: {e}")
             print("Please ensure the database is running and accessible.")


    # Run the app on port 5001
    port = int(os.environ.get("EDITOR_PORT", 5001)) # Use environment variable or default
    host = os.environ.get("HOST", "127.0.0.1")
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    print(f"Starting Graph Editor Flask app: http://{host}:{port}/")
    app.run(host=host, port=port, debug=debug_mode)