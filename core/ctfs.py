# cyberorbit/core/ctfs.py
import json
import os
from models import db, Ctf, UserCtfCompletion # Import db and relevant models

# Remove old CTF_PATH and JSON functions

def get_all_ctfs():
    """Fetches all static CTF definitions from the database."""
    try:
        ctfs = Ctf.query.order_by(Ctf.id).all()
        # Convert to dictionary list if needed by frontend/core logic
        ctf_list = [{'id': c.id, 'title': c.title, 'description': c.description, 'link': c.link} for c in ctfs]
        return ctf_list
    except Exception as e:
        print(f"Error fetching CTFs: {e}")
        return []

def get_user_ctf_completions(user_id):
    """Fetches all CTF completion counts for a specific user."""
    try:
        completions = UserCtfCompletion.query.filter_by(user_id=user_id).all()
        # Return a dictionary mapping ctf_id to completed_count for easy lookup
        return {comp.ctf_id: comp.completed_count for comp in completions}
    except Exception as e:
        print(f"Error fetching user CTF completions for user {user_id}: {e}")
        return {}

def update_user_ctf_completion(user_id, ctf_id, delta):
    """Increments or decrements the completion count for a user's CTF."""
    try:
        completion = UserCtfCompletion.query.filter_by(user_id=user_id, ctf_id=ctf_id).first()

        if completion:
            completion.completed_count = max(0, completion.completed_count + delta) # Ensure count doesn't go below 0
        elif delta > 0:
            # If record doesn't exist and we're incrementing, create it
            completion = UserCtfCompletion(user_id=user_id, ctf_id=ctf_id, completed_count=delta)
            db.session.add(completion)
        # If record doesn't exist and delta is <= 0, do nothing

        db.session.commit()
        return True # Indicate success
    except Exception as e:
        db.session.rollback()
        print(f"Error updating CTF completion for user {user_id}, ctf {ctf_id}: {e}")
        return False # Indicate failure

def get_combined_ctf_data_for_user(user_id):
    """
    Fetches all CTFs and merges in the user's completion count.
    This is likely what the frontend/state computation needs.
    """
    all_ctfs = get_all_ctfs() # List of {'id': ..., 'title': ...}
    user_completions = get_user_ctf_completions(user_id) # Dict of {ctf_id: count}

    for ctf_dict in all_ctfs:
        ctf_dict['completed'] = user_completions.get(ctf_dict['id'], 0) # Add count, default 0

    return all_ctfs