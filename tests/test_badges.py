# tests/test_badges.py
import json
import pytest
from datetime import datetime
from core.badges import (
    load_badges,
    save_badges,
    check_and_award_badges,
    calculate_level,
    award_badge,
    get_required_exercises
)

# Mock s3 interactions
@pytest.fixture(autouse=True)
def mock_s3(mocker):
    mocker.patch('core.badges.sync_down', return_value=None)
    mocker.patch('core.badges.sync_up', return_value=None)

# --- Helper Data ---
@pytest.fixture
def sample_nodes_for_badges():
    return [
        {"id": "n1", "title": "Node 1", "type": "main", "percent": 100, "popup": {
            "exercises": [
                {"id": "ex1", "completed": True, "points": 50, "optional": False, "categories": ["Web"]},
                {"id": "ex2", "completed": True, "points": 70, "optional": False, "categories": ["Scripting"]},
            ]}},
        {"id": "n2", "title": "Node 2", "type": "main", "percent": 50, "popup": {
            "exercises": [
                {"id": "ex3", "completed": True, "points": 30, "optional": False, "categories": ["System"]},
                {"id": "ex4", "completed": False, "points": 40, "optional": False, "categories": ["System"]},
            ]}},
        {"id": "n3", "title": "Sub Node", "type": "sub", "percent": 100, "popup": {
            "exercises": [
                {"id": "ex5", "completed": True, "points": 10, "optional": True, "categories": ["Web"]}, # Optional
                {"id": "ex6", "completed": True, "points": 20, "optional": False, "categories": ["Web"]},
            ]}},
    ]

@pytest.fixture
def sample_ctfs():
    return [
        {"title": "CTF1", "completed": 5},
        {"title": "CTF2", "completed": 7},
    ]

@pytest.fixture
def sample_streak():
    return {"streak": 15, "last_used": "2023-10-27"}

# --- Tests ---

def test_load_badges(manage_test_json_files):
    """Test loading badge data."""
    badges = load_badges()
    assert isinstance(badges, list)
    assert len(badges) == 1
    assert badges[0]['id'] == "test-badge"

def test_save_badges(manage_test_json_files):
    """Test saving badge data."""
    file_path = manage_test_json_files["badges.json"]
    original_badges = load_badges()
    new_badge = {"id": "new-badge", "title": "New", "description": "N", "earnedAt": "now", "shown": False, "image": "new.png"}
    original_badges.append(new_badge)

    save_badges(original_badges)

    with open(file_path, 'r') as f:
        saved_data = json.load(f)
    assert isinstance(saved_data, list)
    assert len(saved_data) == len(original_badges)
    assert any(b['id'] == "new-badge" for b in saved_data)

def test_load_badges_file_not_found(mocker, tmp_path):
    """Test load_badges returns empty list if file doesn't exist."""
    mocker.patch('core.badges.sync_down', side_effect=FileNotFoundError)
    non_existent_path = tmp_path / "non_existent_badge.json"
    mocker.patch('core.badges.BADGES_PATH', str(non_existent_path))
    mocker.patch('os.path.exists', return_value=False)

    badges = load_badges()
    assert badges == []

def test_calculate_level():
    """Test level calculation based on XP thresholds."""
    assert calculate_level(0) == 0
    assert calculate_level(49) == 0 # Below first threshold
    assert calculate_level(50) == 1 # At first threshold
    assert calculate_level(109) == 1 # Below second threshold (50 + 50 + 1*10 = 110)
    assert calculate_level(110) == 2 # At second threshold
    assert calculate_level(500) == 6 # Example for level 5

def test_get_required_exercises(sample_nodes_for_badges):
    """Test filtering for non-optional exercises."""
    required = get_required_exercises(sample_nodes_for_badges)
    assert len(required) == 5
    assert all(not ex.get("optional") for ex in required)
    assert any(ex["id"] == "ex1" for ex in required)
    assert not any(ex["id"] == "ex5" for ex in required) # ex5 is optional

def test_award_badge_logic():
    """Test the award_badge helper function."""
    badges = []
    awarded_ids = set()
    award_badge(badges, awarded_ids, "b1", "Title 1", "Desc 1", "img1.png")
    assert len(badges) == 1
    assert "b1" in awarded_ids
    assert badges[0]["id"] == "b1"
    assert not badges[0]["shown"]

    # Try awarding the same badge again - should do nothing
    award_badge(badges, awarded_ids, "b1", "Title 1", "Desc 1", "img1.png")
    assert len(badges) == 1

    award_badge(badges, awarded_ids, "b2", "Title 2", "Desc 2", "img2.png")
    assert len(badges) == 2
    assert "b2" in awarded_ids

def test_check_and_award_badges_main_node(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test awarding badge for 100% main node completion."""
    existing_badges = []
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)
    assert any(b["id"] == "main-n1" for b in new_badges)
    main_badge = next(b for b in new_badges if b["id"] == "main-n1")
    assert main_badge["title"] == "Node 1 Completed"
    assert main_badge["image"] == "static/badges/badge_main_n1.png"
    # Node 2 is not 100%
    assert not any(b["id"] == "main-n2" for b in new_badges)

def test_check_and_award_badges_level(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test awarding level badges based on calculated XP."""
    # XP = (50+70+30+20) [required ex] + (5*30 + 7*30) [ctf] = 170 + 150 + 210 = 530 XP
    # Level 5 threshold = 50+110+180+260+350 = 950? Let's recalculate
    # L0=0, L1=50, L2=110 (50+60), L3=180 (110+70), L4=260 (180+80), L5=350 (260+90)
    # XP = 170 + (5+7)*30 = 170 + 12*30 = 170 + 360 = 530 XP -> Level 5 (>=350)
    existing_badges = []
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)
    assert any(b["id"] == "level-5" for b in new_badges)
    assert not any(b["id"] == "level-10" for b in new_badges)

def test_check_and_award_badges_exercises(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test awarding exercise count badges."""
    # 5 required exercises, 4 completed
    existing_badges = []
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)
    # Should not award any exercise badges yet (thresholds 10, 25...)
    assert not any(b["id"].startswith("exercises-") for b in new_badges)

    # Complete the last required exercise
    sample_nodes_for_badges[1]["popup"]["exercises"][1]["completed"] = True # Complete ex4
    sample_nodes_for_badges[1]["percent"] = 100 # Update percent manually for test clarity
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, [])
    # Now 5/5 required exercises completed. Total required = 5.
    # Should award exercises-5 (which uses badge_ex_all.png)
    assert any(b["id"] == "exercises-5" for b in new_badges)
    ex_badge = next(b for b in new_badges if b["id"] == "exercises-5")
    assert ex_badge["description"] == "You completed all exercises."
    assert ex_badge["image"] == "static/badges/badge_ex_all.png"

def test_check_and_award_badges_ctfs(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test awarding CTF count badges."""
    # Total CTF completed = 5 + 7 = 12
    existing_badges = []
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)
    assert any(b["id"] == "ctf-5" for b in new_badges)
    assert any(b["id"] == "ctf-10" for b in new_badges)
    assert not any(b["id"] == "ctf-15" for b in new_badges)

def test_check_and_award_badges_streak(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test awarding streak badges."""
    # Streak = 15
    existing_badges = []
    new_badges = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)
    assert any(b["id"] == "streak-7" for b in new_badges)
    assert any(b["id"] == "streak-14" for b in new_badges)
    assert not any(b["id"] == "streak-21" for b in new_badges)

def test_check_and_award_badges_no_duplicates(sample_nodes_for_badges, sample_ctfs, sample_streak):
    """Test that existing badges are not re-awarded."""
    existing_badges = [{"id": "level-5", "title": "Old Level 5", "shown": True, "earnedAt": "past"}]
    awarded_ids_before = set(b["id"] for b in existing_badges)

    new_badges_list = check_and_award_badges(sample_nodes_for_badges, sample_ctfs, sample_streak, existing_badges)

    level_5_badges = [b for b in new_badges_list if b["id"] == "level-5"]
    assert len(level_5_badges) == 1 # Should still only be one level-5 badge
    assert level_5_badges[0]["title"] == "Old Level 5" # Should be the existing one

    # Check another badge that should be awarded
    assert any(b["id"] == "ctf-10" for b in new_badges_list)