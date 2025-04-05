# test_models.py (REVISED AND SAFER VERSION)
import pytest
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# --- IMPORTANT: Create db instance OUTSIDE factory/fixture ---
# This allows importing models that might reference 'db'
from models import db as original_db # Import your original db instance
from models import User # Import necessary models

# --- Fixtures ---

@pytest.fixture(scope='module')
def test_app():
    """Creates and configures a new Flask app for testing."""
    # Create a new Flask app instance for testing
    app = Flask(__name__)

    # --- Essential Test Configuration ---
    # Use an in-memory SQLite database FOR TESTING ONLY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing-secret-key' # Use a distinct test secret key
    app.config['WTF_CSRF_ENABLED'] = False # Often useful for testing forms
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize extensions with the test app ---
    # Crucially, initialize YOUR db instance with THIS test app
    original_db.init_app(app)
    # Initialize LoginManager if your tests need login functionality
    # from app import login_manager # Assuming login_manager is defined globally in app.py
    # login_manager.init_app(app)

    with app.app_context():
        # Create tables in the in-memory database
        original_db.create_all()

        yield app # provide the test app instance

        # --- Cleanup ---
        # No db.drop_all() here for extra safety.
        # The in-memory DB is ephemeral anyway.
        original_db.session.remove()
        # If you were using a file-based test DB, you'd os.remove() it here.


@pytest.fixture(scope='module')
def test_client(test_app):
    """Creates a test client for the test Flask app."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def db_session(test_app):
    """Provides a DB session for the test function context."""
    with test_app.app_context():
        yield original_db.session # Use your imported db instance's session
        original_db.session.rollback() # Rollback any changes after each test


@pytest.fixture(scope='function')
def new_user():
    """Creates a sample User object."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    return user

# --- Test Cases (using revised fixtures) ---

def test_new_user_creation(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and password hashing are correct
    """
    assert new_user.username == 'testuser'
    assert new_user.email == 'test@example.com'
    assert new_user.password_hash != 'password123'
    assert new_user.check_password('password123')
    assert not new_user.check_password('wrongpassword')

def test_add_user_to_db(db_session, new_user):
    """
    GIVEN a test DB session and a new user
    WHEN the user is added to the session and committed
    THEN check the user is retrieved correctly from the test DB
    """
    db_session.add(new_user)
    db_session.commit()

    retrieved_user = User.query.filter_by(username='testuser').first()
    assert retrieved_user is not None
    assert retrieved_user.email == 'test@example.com'
    assert retrieved_user.check_password('password123')

def test_unique_username_constraint(db_session):
    """
    GIVEN a test DB session
    WHEN two users with the same username are added
    THEN check that an IntegrityError occurs on commit
    """
    user1 = User(username='duplicate', email='user1@example.com')
    user1.set_password('pass1')
    user2 = User(username='duplicate', email='user2@example.com')
    user2.set_password('pass2')

    db_session.add(user1)
    db_session.commit() # Commit the first user successfully

    db_session.add(user2)
    with pytest.raises(Exception): # Or specific sqlalchemy.exc.IntegrityError
        db_session.commit()
    db_session.rollback() # Important to rollback after expected error

# --- Add more tests for other models and constraints as needed ---