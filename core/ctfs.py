
import json
import os
from models import db, Ctf, UserCtfCompletion 



def get_all_ctfs():
    """Fetches all static CTF definitions from the database."""
    try:
        ctfs = Ctf.query.order_by(Ctf.id).all()
        
        ctf_list = [{'id': c.id, 'title': c.title, 'description': c.description, 'link': c.link} for c in ctfs]
        return ctf_list
    except Exception as e:
        print(f"Error fetching CTFs: {e}")
        return []

def get_user_ctf_completions(user_id):
    """Fetches all CTF completion counts for a specific user."""
    try:
        completions = UserCtfCompletion.query.filter_by(user_id=user_id).all()
        
        return {comp.ctf_id: comp.completed_count for comp in completions}
    except Exception as e:
        print(f"Error fetching user CTF completions for user {user_id}: {e}")
        return {}

def update_user_ctf_completion(user_id, ctf_id, delta):
    """Increments or decrements the completion count for a user's CTF."""
    try:
        completion = UserCtfCompletion.query.filter_by(user_id=user_id, ctf_id=ctf_id).first()

        if completion:
            completion.completed_count = max(0, completion.completed_count + delta) 
        elif delta > 0:
            
            completion = UserCtfCompletion(user_id=user_id, ctf_id=ctf_id, completed_count=delta)
            db.session.add(completion)
        

        db.session.commit()
        return True 
    except Exception as e:
        db.session.rollback()
        print(f"Error updating CTF completion for user {user_id}, ctf {ctf_id}: {e}")
        return False 

def get_combined_ctf_data_for_user(user_id):
    """
    Fetches all CTFs and merges in the user's completion count.
    This is likely what the frontend/state computation needs.
    """
    all_ctfs = get_all_ctfs() 
    user_completions = get_user_ctf_completions(user_id) 

    for ctf_dict in all_ctfs:
        ctf_dict['completed'] = user_completions.get(ctf_dict['id'], 0) 

    return all_ctfs