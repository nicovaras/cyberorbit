# cyberorbit/core/data.py
import json
import os
from models import db, Node, Exercise, NodeRelationship, UserExerciseCompletion, UserNodeStatus # Import db and models
# Remove s3sync imports if they are no longer needed globally here
# from core.s3sync import sync_down, sync_up

# Remove old JSON_DIR and file loading/saving functions (load_data, save_data)

# --- New Database Interaction Functions ---

def get_static_graph_data(graph_id):
    """
    Fetches static data for a given graph_id from the database.
    Returns nodes (including their exercises) and relationships.
    """
    # Fetch nodes belonging to the specified graph, including their exercises
    nodes_with_exercises = db.session.query(Node).options(
        db.joinedload(Node.exercises).options(
           db.joinedload(Exercise.categories) # Also load exercise categories if needed later
        )
    ).filter(Node.graph_id == graph_id).all()

    # Fetch all relationships relevant to the nodes in this graph
    node_ids = {node.id for node in nodes_with_exercises}
    relationships = db.session.query(NodeRelationship).filter(
        (NodeRelationship.parent_node_id.in_(node_ids)) |
        (NodeRelationship.child_node_id.in_(node_ids))
    ).all()

    # Convert node objects to dictionaries (similar to old JSON structure if needed by downstream logic)
    # This might be adjusted depending on how core/nodes.py is refactored
    nodes_dict_list = []
    for node in nodes_with_exercises:
        node_dict = {
            'id': node.id,
            'graph_id': node.graph_id,
            'title': node.title,
            'type': node.type,
            'popup': { # Reconstruct popup structure
                'text': node.popup_text,
                'pdf_link': node.pdf_link,
                'exercises': [
                    {
                        'id': ex.id,
                        'label': ex.label,
                        'points': ex.points,
                        'optional': ex.optional,
                        'categories': [cat.name for cat in ex.categories] # Assuming categories are loaded
                    } for ex in node.exercises
                ]
            }
            # Note: Children/Prerequisites are handled via relationships table now
            # We might add them back here if needed, or handle in core/nodes.py
        }
        nodes_dict_list.append(node_dict)

    # Convert relationships to simple source/target dictionaries if needed
    links_dict_list = [
        {'source': rel.parent_node_id, 'target': rel.child_node_id, 'type': rel.relationship_type}
        for rel in relationships
    ]

    return nodes_dict_list, links_dict_list

def get_user_progress(user_id, graph_id):
    """
    Fetches all user-specific progress data for a given graph.
    """
    # Fetch node statuses (unlocked, discovered, percent, notes) for the user and graph
    node_statuses = db.session.query(UserNodeStatus).join(Node).filter(
        UserNodeStatus.user_id == user_id,
        Node.graph_id == graph_id
    ).all()
    node_status_map = {status.node_id: status for status in node_statuses}

    # Fetch completed exercise IDs for the user (can filter by graph indirectly via nodes later if needed)
    completed_exercises = db.session.query(UserExerciseCompletion.exercise_id).filter(
        UserExerciseCompletion.user_id == user_id
    ).all()
    # Convert list of tuples to a set for faster lookup
    completed_exercise_ids = {ex_id[0] for ex_id in completed_exercises}

    return node_status_map, completed_exercise_ids


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

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error bulk updating node status for user {user_id}: {e}")
        return False

# Add other necessary functions as needed, e.g., fetching a single node's static data.