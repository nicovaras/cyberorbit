# test_ctfs.py (REVISED AGAIN to remove commits from tests)
import pytest

# Assuming test fixtures (test_app, db_session) are defined in conftest.py
# or accessible otherwise.

# --- Imports for the module being tested ---
from core.ctfs import (
    get_all_ctfs,
    get_user_ctf_completions,
    update_user_ctf_completion,
    get_combined_ctf_data_for_user
)
from models import User, Ctf, UserCtfCompletion, db as original_db

# --- Test Data ---
USER_ID_1 = 1
USER_ID_2 = 2
CTF_ID_1 = 101
CTF_ID_2 = 102
CTF_ID_3 = 103

# --- Helper Functions (Unchanged) ---

def setup_user(db_session, user_id):
    """Adds a user to the session if they don't exist, flushes."""
    user = db_session.get(User, user_id)
    if not user:
        user = User(id=user_id, username=f'ctf_user{user_id}', email=f'ctf_user{user_id}@test.com')
        user.set_password('password')
        db_session.add(user)
        db_session.flush()
    return user

def setup_ctf_defs(db_session, ctf_data):
    """Adds CTF definitions to the session, flushes."""
    ctf_objects = []
    for ctf_id, title, desc, link in ctf_data:
        ctf = Ctf(id=ctf_id, title=title, description=desc, link=link)
        db_session.add(ctf)
        ctf_objects.append(ctf)
    db_session.flush()
    return ctf_objects

def setup_user_completion(db_session, user_id, ctf_id, count):
    """Adds a UserCtfCompletion record to the session, flushes."""
    completion = UserCtfCompletion(user_id=user_id, ctf_id=ctf_id, completed_count=count)
    db_session.add(completion)
    db_session.flush()
    return completion

# --- Tests for get_all_ctfs ---

def test_get_all_ctfs_empty(db_session):
    # No setup needed, just call the function
    result = get_all_ctfs()
    # Assertion relies on the db_session fixture ensuring a clean state initially
    assert result == []

def test_get_all_ctfs_populated(db_session):
    # Setup CTF defs (adds and flushes)
    ctf_defs = [
        (CTF_ID_1, 'Linux Basics', 'Desc 1', 'link1'),
        (CTF_ID_2, 'Web XSS', 'Desc 2', 'link2'),
    ]
    setup_ctf_defs(db_session, ctf_defs)
    # --- NO COMMIT HERE ---
    # get_all_ctfs performs its own query, which should see the flushed data
    # within the transaction managed by db_session fixture.

    result = get_all_ctfs()
    result.sort(key=lambda x: x['id'])
    assert len(result) == 2
    assert result[0] == {'id': CTF_ID_1, 'title': 'Linux Basics', 'description': 'Desc 1', 'link': 'link1'}
    assert result[1] == {'id': CTF_ID_2, 'title': 'Web XSS', 'description': 'Desc 2', 'link': 'link2'}
    # Rollback happens automatically after test via fixture

# --- Tests for get_user_ctf_completions ---

def test_get_user_completions_empty(db_session):
    # Setup user (adds and flushes)
    setup_user(db_session, USER_ID_1)
    # --- NO COMMIT HERE ---

    result = get_user_ctf_completions(USER_ID_1)
    assert result == {}
    # Rollback happens automatically

def test_get_user_completions_populated(db_session):
    # Setup user, ctfs, completions (adds and flushes)
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1'), (CTF_ID_2, 'T2', 'D2', 'L2')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 3)
    setup_user_completion(db_session, USER_ID_1, CTF_ID_2, 1)
    # --- NO COMMIT HERE ---

    result = get_user_ctf_completions(USER_ID_1)
    # Function runs its own query, sees flushed data
    assert result == {CTF_ID_1: 3, CTF_ID_2: 1}
    # Rollback happens automatically

# --- Tests for update_user_ctf_completion ---
# This function commits internally, so tests verify state *after* call

def test_update_completion_new(db_session):
    # Setup user and ctf defs (adds and flushes)
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    # --- NO COMMIT HERE ---

    # Call the function, which performs its own commit
    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, 2)
    assert success is True

    # Verify DB state AFTER the function's internal commit
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp is not None
    assert comp.completed_count == 2
    # Rollback happens automatically

def test_update_completion_increment(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 3)
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, 2) # Commits internally
    assert success is True
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp.completed_count == 5
    # Rollback happens automatically

def test_update_completion_decrement(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 5)
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, -2) # Commits internally
    assert success is True
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp.completed_count == 3
    # Rollback happens automatically

def test_update_completion_decrement_to_zero(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 2)
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, -2) # Commits internally
    assert success is True
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp.completed_count == 0
    # Rollback happens automatically

def test_update_completion_decrement_below_zero(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 2)
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, -5) # Commits internally
    assert success is True
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp.completed_count == 0
    # Rollback happens automatically

def test_update_completion_zero_delta(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 3)
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, 0) # Commits internally
    assert success is True
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp.completed_count == 3 # Should be unchanged
    # Rollback happens automatically

def test_update_completion_negative_delta_new(db_session):
    setup_user(db_session, USER_ID_1)
    setup_ctf_defs(db_session, [(CTF_ID_1, 'T1', 'D1', 'L1')])
    # --- NO COMMIT HERE ---

    success = update_user_ctf_completion(USER_ID_1, CTF_ID_1, -2) # Commits internally
    assert success is True
    # Record should not exist
    comp = db_session.query(UserCtfCompletion).filter_by(user_id=USER_ID_1, ctf_id=CTF_ID_1).first()
    assert comp is None
    # Rollback happens automatically

# --- Tests for get_combined_ctf_data_for_user ---

def test_get_combined_data_no_ctfs(db_session):
    # Setup user (adds and flushes)
    setup_user(db_session, USER_ID_1)
    # --- NO COMMIT HERE ---

    # Call function - it uses get_all_ctfs and get_user_ctf_completions
    # which query the (empty of CTFs) database state
    result = get_combined_ctf_data_for_user(USER_ID_1)
    # Assertion should now pass because no CTFs were created/committed
    assert result == []
    # Rollback happens automatically

def test_get_combined_data_no_completions(db_session):
    # Setup user and CTF defs (adds and flushes)
    setup_user(db_session, USER_ID_1)
    ctf_defs = [(CTF_ID_1, 'T1', 'D1', 'L1'), (CTF_ID_2, 'T2', 'D2', 'L2')]
    setup_ctf_defs(db_session, ctf_defs)
    # --- NO COMMIT HERE ---

    result = get_combined_ctf_data_for_user(USER_ID_1)
    result.sort(key=lambda x: x['id'])
    assert len(result) == 2
    assert result[0] == {'id': CTF_ID_1, 'title': 'T1', 'description': 'D1', 'link': 'L1', 'completed': 0}
    assert result[1] == {'id': CTF_ID_2, 'title': 'T2', 'description': 'D2', 'link': 'L2', 'completed': 0}
    # Rollback happens automatically

def test_get_combined_data_with_completions(db_session):
    # Setup user, CTF defs, and completions (adds and flushes)
    setup_user(db_session, USER_ID_1)
    ctf_defs = [
        (CTF_ID_1, 'T1', 'D1', 'L1'),
        (CTF_ID_2, 'T2', 'D2', 'L2'),
        (CTF_ID_3, 'T3', 'D3', 'L3'),
    ]
    setup_ctf_defs(db_session, ctf_defs)
    setup_user_completion(db_session, USER_ID_1, CTF_ID_1, 5)
    setup_user_completion(db_session, USER_ID_1, CTF_ID_3, 1)
    # --- NO COMMIT HERE ---

    result = get_combined_ctf_data_for_user(USER_ID_1)
    expected_result = [
        {'id': CTF_ID_1, 'title': 'T1', 'description': 'D1', 'link': 'L1', 'completed': 5},
        {'id': CTF_ID_2, 'title': 'T2', 'description': 'D2', 'link': 'L2', 'completed': 0},
        {'id': CTF_ID_3, 'title': 'T3', 'description': 'D3', 'link': 'L3', 'completed': 1},
    ]
    assert sorted(result, key=lambda x: x['id']) == sorted(expected_result, key=lambda x: x['id'])
    # Rollback happens automatically