# test_streak.py (REVISED TO FIX UNIQUE CONSTRAINT ERRORS)
import pytest
from datetime import datetime, date, timedelta

# Assuming test fixtures (test_app, db_session) are defined in conftest.py
# or accessible otherwise.

# --- Imports for the module being tested ---
from core.streak import get_user_streak, update_user_streak
from models import User, UserStreak, db as original_db # Import necessary models and db

# --- Test Data ---
USER_ID_1 = 1
USER_ID_2 = 2
USER_ID_NEW = 99

TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)
TWO_DAYS_AGO = TODAY - timedelta(days=2)

# --- MODIFIED Helper function to set up streaks ---
def setup_streak_entry(db_session, user_id, streak_count, last_date):
    """
    Helper to add User and UserStreak records to the session WITHOUT committing.
    Relies on the db_session fixture to handle rollback/commit boundaries.
    """
    # Ensure user exists in the session or add them
    user = db_session.get(User, user_id)
    if not user:
        user = User(id=user_id, username=f'user{user_id}', email=f'user{user_id}@test.com')
        user.set_password('password')
        db_session.add(user)
        # Flush to ensure user is queryable within the same transaction if needed,
        # but DON'T commit.
        db_session.flush()

    # Create streak and add to session, DON'T commit.
    streak = UserStreak(user_id=user_id, current_streak=streak_count, last_used_date=last_date)
    db_session.add(streak)
    # Flush again if streak object needs to be read back immediately before test logic
    db_session.flush()
    return streak


# --- Tests for get_user_streak ---

def test_get_streak_no_record(db_session):
    """Test getting streak for a user with no streak record."""
    result = get_user_streak(USER_ID_NEW)
    assert result == {"streak": 0, "last_used": ""}

def test_get_streak_existing_record(db_session):
    """Test getting streak for a user with an existing record."""
    # Setup adds to session, but doesn't commit. get_user_streak queries session.
    setup_streak_entry(db_session, USER_ID_1, 5, YESTERDAY)
    result = get_user_streak(USER_ID_1)
    assert result == {"streak": 5, "last_used": YESTERDAY.isoformat()}

def test_get_streak_existing_record_no_date(db_session):
    """Test getting streak for a user with record but null date (edge case)."""
    # Setup adds to session.
    setup_streak_entry(db_session, USER_ID_1, 3, None)
    result = get_user_streak(USER_ID_1)
    assert result == {"streak": 3, "last_used": ""} # Correctly handles None date


# --- Tests for update_user_streak ---
# These tests now rely on setup_streak_entry adding data to the session,
# and update_user_streak potentially modifying it within that same session.
# The db_session fixture rollback will clear everything afterwards.

def test_update_streak_new_user(db_session):
    """Test updating streak for a user with no prior record."""
    result = update_user_streak(USER_ID_NEW)
    assert result == {"streak": 1, "last_used": TODAY.isoformat()}
    # Verify DB state (within the uncommitted session)
    # Use db_session.get() or query directly
    streak_record = db_session.query(UserStreak).filter_by(user_id=USER_ID_NEW).first()
    assert streak_record is not None
    assert streak_record.current_streak == 1
    assert streak_record.last_used_date == TODAY

def test_update_streak_same_day(db_session):
    """Test updating streak when last used was today."""
    setup_streak_entry(db_session, USER_ID_1, 5, TODAY)
    result = update_user_streak(USER_ID_1)
    assert result == {"streak": 5, "last_used": TODAY.isoformat()}
    # Verify DB state (within the uncommitted session)
    streak_record = db_session.query(UserStreak).filter_by(user_id=USER_ID_1).first()
    assert streak_record.current_streak == 5
    assert streak_record.last_used_date == TODAY

def test_update_streak_consecutive_day(db_session):
    """Test updating streak when last used was yesterday."""
    setup_streak_entry(db_session, USER_ID_1, 5, YESTERDAY)
    result = update_user_streak(USER_ID_1)
    assert result == {"streak": 6, "last_used": TODAY.isoformat()}
    # Verify DB state (within the uncommitted session)
    streak_record = db_session.query(UserStreak).filter_by(user_id=USER_ID_1).first()
    assert streak_record.current_streak == 6
    assert streak_record.last_used_date == TODAY

def test_update_streak_gap_day(db_session):
    """Test updating streak when last used was >= 2 days ago (streak resets)."""
    setup_streak_entry(db_session, USER_ID_1, 5, TWO_DAYS_AGO)
    result = update_user_streak(USER_ID_1)
    assert result == {"streak": 1, "last_used": TODAY.isoformat()}
    # Verify DB state (within the uncommitted session)
    streak_record = db_session.query(UserStreak).filter_by(user_id=USER_ID_1).first()
    assert streak_record.current_streak == 1
    assert streak_record.last_used_date == TODAY

def test_update_streak_multiple_updates_same_day(db_session):
    """Test calling update multiple times on the same day."""
    # First call (new user)
    result1 = update_user_streak(USER_ID_NEW)
    assert result1 == {"streak": 1, "last_used": TODAY.isoformat()}

    # Second call (same day) - should read the state from the session
    result2 = update_user_streak(USER_ID_NEW)
    assert result2 == {"streak": 1, "last_used": TODAY.isoformat()}

    # Third call (same day)
    result3 = update_user_streak(USER_ID_NEW)
    assert result3 == {"streak": 1, "last_used": TODAY.isoformat()}

    # Final check on session state before rollback
    streak_record = db_session.query(UserStreak).filter_by(user_id=USER_ID_NEW).first()
    assert streak_record.current_streak == 1 # Streak should not have incremented