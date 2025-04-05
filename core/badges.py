# cyberorbit/core/badges.py
import os
import json
from datetime import datetime
from models import db, Badge, UserBadge, UserExerciseCompletion, UserCtfCompletion, UserStreak, UserNodeStatus, Node, Exercise # Import models
from core import streak as core_streak # Import the streak module
from core import data as core_data # Keep existing imports if any
from core import ctfs as core_ctfs # Keep existing imports if any
from sqlalchemy.orm import joinedload

# --- Database Functions ---

def get_all_badges():
    """Fetches all static badge definitions."""
    try:
        badges = Badge.query.order_by(Badge.id).all()
        # Convert to dictionary list
        return [
            {'id': b.id, 'title': b.title, 'description': b.description, 'image_path': b.image_path}
            for b in badges
        ]
    except Exception as e:
        print(f"Error fetching all badges: {e}")
        return []


def get_user_badges(user_id):
    """Fetches all badges earned by a specific user, eager loading Badge details."""
    try: # Wrap in try/except
        user_badges = UserBadge.query.options(
            joinedload(UserBadge.badge) # Eager load the Badge definition
        ).filter_by(user_id=user_id).all()

        # Convert to dictionary list
        return [
            {
                'id': ub.badge.id, # Access via loaded relationship
                'title': ub.badge.title,
                'description': ub.badge.description,
                'image': ub.badge.image_path, # Use correct attribute name
                'earnedAt': ub.earned_at.isoformat() if ub.earned_at else None,
                'shown': ub.shown
            }
            for ub in user_badges if ub.badge # Check if badge relationship loaded correctly
        ]
    except Exception as e:
        print(f"Error fetching badges for user {user_id}: {e}")
        return []

def mark_user_badge_shown(user_id, badge_id):
    """Marks a specific badge as shown for a user."""
    try:
        user_badge = UserBadge.query.filter_by(user_id=user_id, badge_id=badge_id).first()
        if user_badge and not user_badge.shown:
            user_badge.shown = True
            db.session.commit()
            return True
        return False # No update needed or badge not found
    except Exception as e:
        db.session.rollback()
        print(f"Error marking badge shown for user {user_id}, badge {badge_id}: {e}")
        return False

def award_badge(user_id, badge_id, existing_badge_ids_set, awarded_in_this_run_set):
    """
    Adds a badge to the session if the user doesn't already have it in the DB
    and it hasn't been added in this run.
    """
    if badge_id in awarded_in_this_run_set or badge_id in existing_badge_ids_set:
        return False # Already processed or already exists in DB

    try:
        # Fetch badge definition to ensure it exists before creating UserBadge entry
        badge_def = db.session.get(Badge, badge_id)
        if badge_def:
            new_user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
            db.session.add(new_user_badge) # Add to session, NO commit here
            awarded_in_this_run_set.add(badge_id)
            print(f"Staging badge '{badge_id}' for user {user_id}")
            return True
        else:
            print(f"Warning: Badge definition '{badge_id}' not found. Cannot award.")
            return False
    except Exception as e:
        print(f"Error trying to award badge {badge_id} to user {user_id}: {e}")
        return False

# --- Badge Awarding Logic (Needs User Context) ---

def calculate_level(xp):
    # Keep the existing logic, it's independent of DB
    thresholds = [0]
    current_threshold = 0
    for i in range(1, 50): # Calculate more levels
        level_xp = 50 + (i - 1) * 10
        current_threshold += level_xp
        thresholds.append(current_threshold)

    for i in range(len(thresholds)):
        if xp < thresholds[i]:
            return i - 1 # Return 0-based level index
    return len(thresholds) - 1 # Max level achieved

def get_required_exercises_db(graph_id):
    """Fetches required exercises for a graph from DB."""
    try:
        exercises = Exercise.query.join(Node).filter(
            Node.graph_id == graph_id,
            Exercise.optional == False
        ).all()
        return exercises
    except Exception as e:
        print(f"Error fetching required exercises for graph {graph_id}: {e}")
        return []

def check_and_award_badges(
    user_id,
    graph_id, # Still needed? Maybe only if required_exercises is not passed?
    user_streak_data,
    user_ctf_completions,
    user_node_status_map,
    completed_exercise_ids,
    required_exercises,     # Passed from helper
    existing_badge_ids,     # Passed from helper (set)
    all_badge_defs_map      # Passed from helper {badge_id: Badge obj}
    ):
    """Checks criteria and stages badge awards using only passed arguments."""
    newly_awarded_badge_defs = []
    awarded_in_this_run = set() # Track badges added to session now
    try:
        # REMOVED internal fetches for badge defs, required exercises, user badges

        # Calculate XP and Level (using passed-in data)
        exercise_xp = sum(ex.points for ex in required_exercises if ex.id in completed_exercise_ids)
        ctf_xp = sum(count * 30 for count in user_ctf_completions.values())
        total_xp = exercise_xp + ctf_xp
        level = calculate_level(total_xp)

        # --- Badge Awarding Logic (uses passed arguments) ---

        # 1. Main node completions
        for node_id, status in user_node_status_map.items():
            node = db.session.get(Node, node_id) # Still need node type - potentially slow?
            if node and node.type == "main" and status.percent_complete == 100:
                badge_id = f"main-{node_id}"
                # Use passed existing_badge_ids set
                if award_badge(user_id, badge_id, existing_badge_ids, awarded_in_this_run):
                     badge_def = all_badge_defs_map.get(badge_id) # Use passed map
                     if badge_def: newly_awarded_badge_defs.append(badge_def)

        # 2. Level milestones
        for lvl in [5, 10, 15, 20, 25, 30]:
            if level >= lvl:
                badge_id = f"level-{lvl}"
                if award_badge(user_id, badge_id, existing_badge_ids, awarded_in_this_run):
                     badge_def = all_badge_defs_map.get(badge_id)
                     if badge_def: newly_awarded_badge_defs.append(badge_def)

        # 3. Exercise milestones (use passed required_exercises list)
        completed_count = len(completed_exercise_ids.intersection({ex.id for ex in required_exercises}))
        total_req_count = len(required_exercises)
        # ... (rest of exercise badge logic using award_badge) ...
        ex_milestones = [10, 25, 50, 75, 100]
        if total_req_count > 0: ex_milestones.append(total_req_count)
        for count in sorted(list(set(ex_milestones))):
             if count == 0: continue
             if completed_count >= count:
                badge_id = f"exercises-{count}"
                if award_badge(user_id, badge_id, existing_badge_ids, awarded_in_this_run):
                     badge_def = all_badge_defs_map.get(badge_id)
                     if badge_def: newly_awarded_badge_defs.append(badge_def)


        # 4. CTF milestones (use passed user_ctf_completions dict)
        total_ctf_completed = sum(user_ctf_completions.values())
        # ... (rest of ctf badge logic using award_badge) ...
        for count in [5, 10, 15, 20, 25, 30]:
            if total_ctf_completed >= count:
                badge_id = f"ctf-{count}"
                if award_badge(user_id, badge_id, existing_badge_ids, awarded_in_this_run):
                     badge_def = all_badge_defs_map.get(badge_id)
                     if badge_def: newly_awarded_badge_defs.append(badge_def)

        # 5. Streak milestones (use passed user_streak_data dict)
        current_streak = user_streak_data.get("streak", 0)
        # ... (rest of streak badge logic using award_badge) ...
        for days in [7, 14, 21, 28]:
            if current_streak >= days:
                badge_id = f"streak-{days}"
                if award_badge(user_id, badge_id, existing_badge_ids, awarded_in_this_run):
                     badge_def = all_badge_defs_map.get(badge_id)
                     if badge_def: newly_awarded_badge_defs.append(badge_def)

        # NO COMMIT HERE - Changes are staged in the session

    except Exception as e:
        print(f"Error during check_and_award_badges (staging) for user {user_id}: {e}")
        return []

    # Return definitions of badges staged for adding
    return newly_awarded_badge_defs