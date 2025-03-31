import os
import json
from datetime import datetime, timedelta

STREAK_PATH = "json/streak.json"

def load_streak():
    if not os.path.exists(STREAK_PATH):
        return {"streak": 0, "last_used": ""}
    with open(STREAK_PATH, "r") as f:
        return json.load(f)

def update_streak():
    today = datetime.utcnow().date()
    streak_data = load_streak()
    last = streak_data.get("last_used", "")
    if last:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
        if today == last_date:
            pass
        elif today == last_date + timedelta(days=1):
            streak_data["streak"] += 1
        else:
            streak_data["streak"] = 1
    else:
        streak_data["streak"] = 1
    streak_data["last_used"] = today.isoformat()
    with open(STREAK_PATH, "w") as f:
        json.dump(streak_data, f, indent=2)
    return streak_data
