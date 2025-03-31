from core.badges import check_and_award_badges, load_badges, save_badges

def test_awards_main_node_completion():
    nodes = [{"id": "x", "type": "main", "title": "NodeX", "percent": 100}]
    ctfs = []
    streak = {"streak": 1}
    badges = check_and_award_badges(nodes, ctfs, streak, [])
    ids = [b["id"] for b in badges]
    assert "main-x" in ids
    assert any(b["image"] for b in badges)

def test_awards_streak_badges():
    badges = check_and_award_badges([], [], {"streak": 14}, [])
    assert any(b["id"] == "streak-14" for b in badges)

def test_awards_level_badge():
    nodes = []
    ctfs = []
    exercises = [{"completed": True, "points": 500, "optional": False}]
    nodes.append({"id": "y", "popup": {"exercises": exercises}, "type":"main", "percent":100, "title": "NodeY"})
    badges = check_and_award_badges(nodes, ctfs, {"streak": 0}, [])
    assert any(b["id"] == "level-5" for b in badges)

def test_persistence():
    save_badges([{"id": "test", "title": "T", "description": "D", "earnedAt": "now", "shown": False, "image": "i.png"}])
    loaded = load_badges()
    assert loaded[0]["id"] == "test"
