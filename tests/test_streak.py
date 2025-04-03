# tests/test_streak.py
import json
import pytest
from datetime import datetime, timedelta
from core.streak import load_streak, update_streak

# Mock s3 interactions
@pytest.fixture(autouse=True)
def mock_s3(mocker):
    mocker.patch('core.streak.sync_down', return_value=None)
    mocker.patch('core.streak.sync_up', return_value=None)

def test_load_streak(manage_test_json_files):
    """Test loading streak data."""
    streak_data = load_streak()
    assert isinstance(streak_data, dict)
    assert "streak" in streak_data
    assert "last_used" in streak_data
    assert streak_data["streak"] == 5
    assert streak_data["last_used"] == "2023-10-26"

def test_update_streak_today(manage_test_json_files, mocker):
    """Test update_streak when last used was today (no change)."""
    today_str = datetime.utcnow().date().isoformat()
    # Mock load_streak to return 'today's date
    mocker.patch('core.streak.load_streak', return_value={"streak": 10, "last_used": today_str})

    updated_data = update_streak()

    assert updated_data["streak"] == 10 # Streak should not change
    assert updated_data["last_used"] == today_str

def test_update_streak_yesterday(manage_test_json_files, mocker):
    """Test update_streak when last used was yesterday (increment)."""
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    yesterday_str = yesterday.isoformat()
    mocker.patch('core.streak.load_streak', return_value={"streak": 10, "last_used": yesterday_str})

    updated_data = update_streak()

    assert updated_data["streak"] == 11 # Streak should increment
    assert updated_data["last_used"] == datetime.utcnow().date().isoformat()

def test_update_streak_long_ago(manage_test_json_files, mocker):
    """Test update_streak when last used was long ago (reset)."""
    long_ago = datetime.utcnow().date() - timedelta(days=5)
    long_ago_str = long_ago.isoformat()
    mocker.patch('core.streak.load_streak', return_value={"streak": 10, "last_used": long_ago_str})

    updated_data = update_streak()

    assert updated_data["streak"] == 1 # Streak should reset to 1
    assert updated_data["last_used"] == datetime.utcnow().date().isoformat()

def test_update_streak_first_time(manage_test_json_files, mocker):
    """Test update_streak when there's no prior data (start at 1)."""
    mocker.patch('core.streak.load_streak', return_value={"streak": 0, "last_used": ""}) # Simulate empty/new file

    updated_data = update_streak()

    assert updated_data["streak"] == 1 # Streak starts at 1
    assert updated_data["last_used"] == datetime.utcnow().date().isoformat()

def test_update_streak_saves_correctly(manage_test_json_files):
    """Verify the file is updated after streak calculation."""
    file_path = manage_test_json_files["streak.json"]
    # Ensure it resets or increments based on the fixture's date vs today
    update_streak()

    with open(file_path, 'r') as f:
        saved_data = json.load(f)

    assert saved_data["last_used"] == datetime.utcnow().date().isoformat()
    # Streak value depends on when the test is run relative to 2023-10-26
    assert saved_data["streak"] >= 1

def test_load_streak_file_not_found(mocker, tmp_path):
    """Test load_streak behavior when the file doesn't exist."""
    mocker.patch('core.streak.sync_down', side_effect=FileNotFoundError)
    non_existent_path = tmp_path / "non_existent_streak.json"
    mocker.patch('core.streak.STREAK_PATH', str(non_existent_path))

    # Should return default values if os.path.exists is false after sync_down mock
    mocker.patch('os.path.exists', return_value=False)
    streak_data = load_streak()

    assert streak_data == {"streak": 0, "last_used": ""}