
import os
import json
from datetime import datetime, timedelta
from models import db, UserStreak, User 




def get_user_streak(user_id):
    """Fetches the streak data for a specific user."""
    try:
        streak_record = UserStreak.query.filter_by(user_id=user_id).first()
        if streak_record:
            return {
                "streak": streak_record.current_streak,
                "last_used": streak_record.last_used_date.isoformat() if streak_record.last_used_date else ""
            }
        else:
            
            return {"streak": 0, "last_used": ""}
    except Exception as e:
        print(f"Error fetching streak for user {user_id}: {e}")
        return {"streak": 0, "last_used": ""} 

def update_user_streak(user_id):
    """
    Updates the streak for a specific user based on the current date.
    Returns the updated streak data dictionary.
    """
    today = datetime.utcnow().date()
    updated_streak_data = {"streak": 0, "last_used": ""} 

    try:
        streak_record = UserStreak.query.filter_by(user_id=user_id).first()

        if not streak_record:
            
            streak_record = UserStreak(user_id=user_id, current_streak=1, last_used_date=today)
            db.session.add(streak_record)
            updated_streak_data = {"streak": 1, "last_used": today.isoformat()}
        else:
            last_date = streak_record.last_used_date
            if last_date == today:
                
                updated_streak_data = {"streak": streak_record.current_streak, "last_used": today.isoformat()}
            elif last_date == today - timedelta(days=1):
                
                streak_record.current_streak += 1
                streak_record.last_used_date = today
                updated_streak_data = {"streak": streak_record.current_streak, "last_used": today.isoformat()}
            else:
                
                streak_record.current_streak = 1
                streak_record.last_used_date = today
                updated_streak_data = {"streak": 1, "last_used": today.isoformat()}

        
        return updated_streak_data

    except Exception as e:
        db.session.rollback()
        print(f"Error updating streak for user {user_id}: {e}")
        
        return get_user_streak(user_id) 