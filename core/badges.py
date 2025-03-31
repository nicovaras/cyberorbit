import os
import json
from datetime import datetime
from core.s3sync import sync_down, sync_up

BADGES_PATH = "json/badges.json"


def load_badges():
    sync_down(BADGES_PATH)
    if not os.path.exists(BADGES_PATH):
        return []
    with open(BADGES_PATH, "r") as f:
        return json.load(f)


def save_badges(badges):
    with open(BADGES_PATH, "w") as f:
        json.dump(badges, f, indent=2)
    sync_up(BADGES_PATH)        


def calculate_level(xp):
    thresholds = [0]
    points = 50
    for i in range(1, 25):
        thresholds.append(points)
        points += 50 + i * 10
    for i in range(len(thresholds) - 1):
        if xp < thresholds[i + 1]:
            return i
    return len(thresholds) - 1


def award_badge(badges, awarded_ids, bid, title, desc, image):
    if bid in awarded_ids:
        return
    badges.append({
        "id": bid,
        "title": title,
        "description": desc,
        "earnedAt": datetime.utcnow().isoformat(),
        "shown": False,
        "image": image
    })
    awarded_ids.add(bid)


def get_required_exercises(nodes):
    return [
        e for n in nodes
        for e in n.get("popup", {}).get("exercises", [])
        if not e.get("optional")
    ]


def check_and_award_badges(nodes, ctfs, streak, existing_badges):
    badges = existing_badges[:]
    awarded_ids = set(b["id"] for b in badges)

    required_exercises = get_required_exercises(nodes)
    exercise_xp = sum(e.get("points", 10) for e in required_exercises if e.get("completed"))
    ctf_xp = sum(c.get("completed", 0) * 30 for c in ctfs)
    total_xp = exercise_xp + ctf_xp
    level = calculate_level(total_xp)

    # Main node completions
    for n in nodes:
        if n["type"] == "main" and n["percent"] == 100:
            award_badge(
                badges, awarded_ids,
                f"main-{n['id']}",
                f"{n['title']} Completed",
                f"Completed {n['title']}",
                f"static/badges/badge_main_{n['id']}.png" 
            )

    # Level milestones
    for lvl in [5, 10, 15, 20, 25, 30]:
        if level + 1 >= lvl:
            award_badge(
                badges, awarded_ids,
                f"level-{lvl}",
                f"Level {lvl} Achieved",
                f"You reached level {lvl}",
                f"static/badges/badge_level_{lvl}.png"
            )

    # Exercise milestones
    completed_count = sum(1 for e in required_exercises if e.get("completed"))
    total_count = len(required_exercises)
    for count in [10, 25, 50, 75, 100, total_count]:
        if completed_count >= count and count != 0:
            desc = "You completed all exercises." if count == total_count else f"You completed {count} exercises."
            award_badge(
                badges, awarded_ids,
                f"exercises-{count}",
                f"{count} Exercises Completed",
                desc,
                f"static/badges/badge_ex_{count}.png" if count < total_count else "static/badges/badge_ex_all.png"
            )

    # CTF milestones
    total_ctf_completed = sum(c.get("completed", 0) for c in ctfs)
    for count in [5, 10, 15, 20, 25, 30]:
        if total_ctf_completed >= count:
            award_badge(
                badges, awarded_ids,
                f"ctf-{count}",
                f"{count} CTFs Completed",
                f"You completed {count} CTF challenges.",
                f"static/badges/badge_ctf_{count}.png"
            )

    # Streak milestones
    for days in [ 7, 14, 21, 28]:
        if streak.get("streak", 0) >= days:
            award_badge(
                badges, awarded_ids,
                f"streak-{days}",
                f"{days} Days Streak",
                f"You maintained a streak of {days} days.",
                f"static/badges/badge_streak_{days}.png"
            )

    print(badges)
    return badges
