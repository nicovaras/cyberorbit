# cyberorbit/core/badges.py
import os
import json
from datetime import datetime
from models import db, Badge, UserBadge, UserExerciseCompletion, UserCtfCompletion, UserStreak, UserNodeStatus, Node, Exercise # Import models
from core import streak as core_streak # Import the streak module
from core import data as core_data # Keep existing imports if any
from core import ctfs as core_ctfs # Keep existing imports if any

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
    """Fetches all badges earned by a specific user."""
    try:
        user_badges = UserBadge.query.filter_by(user_id=user_id).all()
        # Convert to dictionary list including earned_at and shown status
        return [
            {
                'id': ub.badge_id,
                'title': ub.badge.title, # Access title via relationship
                'description': ub.badge.description,
                'image': ub.badge.image_path, # Assuming 'image' is used in frontend
                'earnedAt': ub.earned_at.isoformat() if ub.earned_at else None,
                'shown': ub.shown
            }
            for ub in user_badges
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

def award_badge(user_id, badge_id, awarded_ids_set):
    """
    Helper function to add a badge to the UserBadge table if not already present.
    `awarded_ids_set` contains badge_ids already processed in this check run.
    Returns True if a new badge was added, False otherwise.
    """
    if badge_id in awarded_ids_set:
        return False # Already processed in this check

    # Check if user already has this badge in the DB
    exists = db.session.query(UserBadge.query.filter_by(user_id=user_id, badge_id=badge_id).exists()).scalar()

    if not exists:
        try:
            # Fetch badge definition to ensure it exists (optional but good practice)
            badge_def = db.session.get(Badge, badge_id)
            if badge_def:
                new_user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
                db.session.add(new_user_badge)
                awarded_ids_set.add(badge_id) # Mark as processed for this run
                # Commit happens at the end of check_and_award_badges
                print(f"Awarding badge '{badge_id}' to user {user_id}")
                return True
            else:
                print(f"Warning: Badge definition for '{badge_id}' not found in DB. Cannot award.")
                return False
        except Exception as e:
            # Rollback might happen later, just log here
            print(f"Error trying to award badge {badge_id} to user {user_id}: {e}")
            return False
    else:
        awarded_ids_set.add(badge_id) # Mark as processed even if existing
        return False # Badge already exists in DB

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

def check_and_award_badges(user_id, graph_id):
    """Checks all criteria and awards badges for a specific user."""
    newly_awarded_badges = [] # Keep track of badges awarded *in this run*
    try:
        # Fetch user's progress data
        user_streak_data = core_streak.get_user_streak(user_id) # Assumes get_user_streak exists in streak.py
        user_ctf_completions = core_ctfs.get_user_ctf_completions(user_id) # From ctfs.py
        user_node_statuses, completed_exercise_ids = core_data.get_user_progress(user_id, graph_id) # From data.py

        # Fetch definitions
        all_badge_defs = {b.id: b for b in Badge.query.all()} # Fetch all badge defs once
        required_exercises = get_required_exercises_db(graph_id) # Fetch required exercises for this graph

        # Fetch IDs of badges already earned by the user from DB
        existing_badge_ids = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).all()}
        awarded_in_this_run = set() # Track badges awarded *now* to avoid duplicates if criteria overlap

        # Calculate XP and Level
        exercise_xp = sum(ex.points for ex in required_exercises if ex.id in completed_exercise_ids)
        ctf_xp = sum(count * 30 for count in user_ctf_completions.values()) # Assuming 30 points per completion
        total_xp = exercise_xp + ctf_xp
        level = calculate_level(total_xp)

        # 1. Main node completions
        for node_id, status in user_node_statuses.items():
            node = db.session.get(Node, node_id) # Get the node object
            if node and node.type == "main" and status.percent_complete == 100:
                badge_id = f"main-{node_id}"
                if badge_id not in existing_badge_ids: # Only award if not already in DB
                    if award_badge(user_id, badge_id, awarded_in_this_run):
                         newly_awarded_badges.append(all_badge_defs.get(badge_id))

        # 2. Level milestones
        for lvl in [5, 10, 15, 20, 25, 30]: # Check against 0-based level index
            if level >= lvl:
                badge_id = f"level-{lvl}"
                if badge_id not in existing_badge_ids:
                     if award_badge(user_id, badge_id, awarded_in_this_run):
                         newly_awarded_badges.append(all_badge_defs.get(badge_id))

        # 3. Exercise milestones
        completed_count = len(completed_exercise_ids.intersection({ex.id for ex in required_exercises}))
        total_req_count = len(required_exercises)
        ex_milestones = [10, 25, 50, 75, 100]
        if total_req_count > 0:
            ex_milestones.append(total_req_count) # Add 'all' milestone

        for count in sorted(list(set(ex_milestones))): # Ensure unique and sorted
             if count == 0: continue
             if completed_count >= count:
                badge_id = f"exercises-{count}"
                if badge_id not in existing_badge_ids:
                     if award_badge(user_id, badge_id, awarded_in_this_run):
                         newly_awarded_badges.append(all_badge_defs.get(badge_id))

        # 4. CTF milestones
        total_ctf_completed = sum(user_ctf_completions.values())
        for count in [5, 10, 15, 20, 25, 30]:
            if total_ctf_completed >= count:
                badge_id = f"ctf-{count}"
                if badge_id not in existing_badge_ids:
                     if award_badge(user_id, badge_id, awarded_in_this_run):
                         newly_awarded_badges.append(all_badge_defs.get(badge_id))

        # 5. Streak milestones
        current_streak = user_streak_data.get("streak", 0)
        for days in [7, 14, 21, 28]:
            if current_streak >= days:
                badge_id = f"streak-{days}"
                if badge_id not in existing_badge_ids:
                     if award_badge(user_id, badge_id, awarded_in_this_run):
                         newly_awarded_badges.append(all_badge_defs.get(badge_id))

        # Commit all new badges awarded in this run
        if awarded_in_this_run - existing_badge_ids: # Check if any truly new badges were added
             db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Error during check_and_award_badges for user {user_id}: {e}")

    # Return newly awarded badges (convert SQLAlchemy objects to dicts if needed)
    return [
         {
             'id': b.id, 'title': b.title, 'description': b.description,
             'image': b.image_path, 'shown': False, # Newly awarded are always not shown yet
             'earnedAt': datetime.utcnow().isoformat() # Approximate time
         } for b in newly_awarded_badges if b # Filter out None if badge def wasn't found
    ]