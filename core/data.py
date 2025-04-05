# cyberorbit/core/data.py
import json
import os
from models import db, Node, Exercise, NodeRelationship, UserExerciseCompletion, UserNodeStatus # Import db and models
from sqlalchemy.orm import joinedload, selectinload # Import selectinload

# Remove s3sync imports if they are no longer needed globally here
# from core.s3sync import sync_down, sync_up

# Remove old JSON_DIR and file loading/saving functions (load_data, save_data)

# --- New Database Interaction Functions ---
from threading import Lock
_static_cache = {}
_cache_lock = Lock()

def get_cached_static_graph_data(graph_id):
    cache_key = f"graph_{graph_id}"
    # Check cache first
    if cache_key in _static_cache:
        print(f"CACHE HIT for {cache_key}")
        return _static_cache[cache_key]

    # If not in cache, acquire lock, fetch from DB, store in cache
    with _cache_lock:
        # Double-check cache inside lock (another thread might have populated it)
        if cache_key in _static_cache:
            return _static_cache[cache_key]

        print(f"CACHE MISS for {cache_key}. Fetching from DB...")
        # Call the actual DB fetching function (use the optimized one)
        # Ensure get_static_graph_data uses the optimized query with eager loading
        nodes_list, links_list = get_static_graph_data(graph_id) # Assuming function is in 
        if nodes_list: # Only cache if data was successfully fetched
             _static_cache[cache_key] = (nodes_list, links_list)
        return nodes_list, links_list
    
def get_static_graph_data(graph_id):
    """
    Fetches static data for a given graph_id from the database.
    Uses eager loading for exercises and categories.
    """
    try: # Wrap in try/except
        nodes_with_exercises = db.session.query(Node).options(
            selectinload(Node.exercises).options( # Use selectinload for Node->Exercises
               selectinload(Exercise.categories) # Use selectinload for Exercise->Categories (many-to-many)
            )
        ).filter(Node.graph_id == graph_id).all()

        # Fetch relationships (query seems okay, ensure indexes exist on foreign keys)
        node_ids = {node.id for node in nodes_with_exercises}
        if not node_ids: return [], [] # Handle case where no nodes found for graph

        relationships = db.session.query(NodeRelationship).filter(
            (NodeRelationship.parent_node_id.in_(node_ids)) |
            (NodeRelationship.child_node_id.in_(node_ids))
        ).all()

        # Convert nodes to dicts (simplified, adapt if needed)
        nodes_dict_list = []
        for node in nodes_with_exercises:
             node_dict = {
                 'id': node.id, 'graph_id': node.graph_id, 'title': node.title,
                 'type': node.type, 'popup_text': node.popup_text, 'pdf_link': node.pdf_link,
                 # Embed exercises directly if structure is simple
                 'popup': {
                      'text': node.popup_text,
                      'pdf_link': node.pdf_link,
                      'exercises': [
                           { 'id': ex.id, 'label': ex.label, 'points': ex.points,
                             'optional': ex.optional,
                             'categories': [cat.name for cat in ex.categories] # Categories are now loaded
                           } for ex in node.exercises # Access directly
                      ]
                 }
             }
             nodes_dict_list.append(node_dict)

        # Convert relationships to simple source/target dictionaries
        links_dict_list = [
            {'source': rel.parent_node_id, 'target': rel.child_node_id, 'type': rel.relationship_type}
            for rel in relationships
        ]

        return nodes_dict_list, links_dict_list
    except Exception as e:
        print(f"Error in get_static_graph_data for graph {graph_id}: {e}")
        return [], [] # Return empty on error

def get_user_progress(user_id, graph_id):
    """
    Fetches user-specific progress data for a given graph.
    Loads related Node data for filtering.
    """
    try: # Wrap in try/except
        # Fetch node statuses, joining and loading Node to filter by graph_id
        node_statuses = db.session.query(UserNodeStatus).options(
            joinedload(UserNodeStatus.node) # Eager load the related Node
        ).filter(UserNodeStatus.user_id == user_id).all() # Fetch all for user first

        # Filter in Python (simpler than complex join filter if UserNodeStatus doesn't have graph_id)
        node_status_map = {
            status.node_id: status
            for status in node_statuses
            # Ensure status.node is not None before accessing graph_id
            if status.node and status.node.graph_id == graph_id
        }

        # Fetch completed exercise IDs (query is likely fine as is)
        completed_exercises = db.session.query(UserExerciseCompletion.exercise_id).filter(
            UserExerciseCompletion.user_id == user_id
        ).all()
        completed_exercise_ids = {ex_id[0] for ex_id in completed_exercises}

        return node_status_map, completed_exercise_ids
    except Exception as e:
        print(f"Error in get_user_progress for user {user_id}, graph {graph_id}: {e}")
        return {}, set() # Return defaults on error


def update_user_exercise_completion(user_id, exercise_id, completed):
    """Updates the completion status for a user's exercise."""
    try:
        if completed:
            # If completed is True, try to add a new completion record
            # Use merge to handle potential unique constraint violation if already completed
            completion = UserExerciseCompletion(user_id=user_id, exercise_id=exercise_id)
            db.session.merge(completion)
        else:
            # If completed is False, delete the record if it exists
            UserExerciseCompletion.query.filter_by(user_id=user_id, exercise_id=exercise_id).delete()

        db.session.commit()
        return True # Indicate success
    except Exception as e:
        db.session.rollback()
        print(f"Error updating exercise completion for user {user_id}, exercise {exercise_id}: {e}")
        return False # Indicate failure

def update_user_node_notes(user_id, node_id, notes):
    """Updates the user's notes for a specific node."""
    try:
        status = UserNodeStatus.query.filter_by(user_id=user_id, node_id=node_id).first()
        if status:
            status.user_notes = notes
        else:
            # If status record doesn't exist, create it (might happen if node just unlocked)
            status = UserNodeStatus(user_id=user_id, node_id=node_id, user_notes=notes)
            db.session.add(status)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating notes for user {user_id}, node {node_id}: {e}")
        return False

def update_user_node_status_bulk(user_id, node_status_updates):
    """
    Updates multiple node statuses (unlocked, discovered, percent) for a user.
    `node_status_updates` should be a dictionary like:
    { node_id: {'unlocked': True, 'discovered': True, 'percent_complete': 50}, ... }
    """
    try:
        existing_statuses = UserNodeStatus.query.filter(
            UserNodeStatus.user_id == user_id,
            UserNodeStatus.node_id.in_(node_status_updates.keys())
        ).all()
        existing_map = {s.node_id: s for s in existing_statuses}

        for node_id, updates in node_status_updates.items():
            status = existing_map.get(node_id)
            if not status:
                # Create new status if it doesn't exist
                status = UserNodeStatus(user_id=user_id, node_id=node_id)
                db.session.add(status)

            # Apply updates from the dictionary
            if 'unlocked' in updates:
                status.unlocked = updates['unlocked']
            if 'discovered' in updates:
                status.discovered = updates['discovered']
            if 'percent_complete' in updates:
                status.percent_complete = updates['percent_complete']
            # Notes are handled separately by update_user_node_notes

        return True
    except Exception as e:
        print(f"Error bulk updating node status for user {user_id}: {e}")
        return False

# Add other necessary functions as needed, e.g., fetching a single node's static data.