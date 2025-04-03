# tests/conftest.py (Ensure this exists, content provided for context)
import pytest
import os
import json
import sys
from app import app as flask_app # Import the Flask app instance

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Fixtures ---

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    flask_app.config.update({
        "TESTING": True,
        # Add other test configurations if needed, e.g., mock database URI
    })
    # TODO: Add any other app setup logic here (e.g., database initialization for tests)
    yield flask_app
    # TODO: Add any app teardown logic here (e.g., database cleanup)

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """A test command runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='function', autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("FLASK_DEBUG", "False")
    # Mock BUCKET_NAME if s3sync were active
    monkeypatch.setenv("BUCKET_NAME", "test-cyberorbit-bucket")

@pytest.fixture(scope='function', autouse=True)
def manage_test_json_files(tmp_path):
    """Creates temporary JSON files for tests and cleans them up."""
    # Define original content or structure for test files
    # Use tmp_path provided by pytest for temporary file creation
    base_dir = tmp_path / "json"
    base_dir.mkdir()

    files_content = {
        "x.json": [{"id": "n_test_1", "title": "Test Node 1", "type": "main", "percent": 0, "popup": {"exercises": []}, "children": ["n_test_2"], "prerequisites": ["Start"]}, {"id": "n_test_2", "title": "Sub Node", "type": "sub", "percent": 50, "popup": {"exercises": [{"id": "ex1", "completed": True, "points": 10, "categories": ["Test"]}, {"id": "ex2", "completed": False, "points": 10, "categories": ["Test"]}]}, "children": [], "prerequisites": ["n_test_1"]}],
        "streak.json": {"streak": 5, "last_used": "2023-10-26"}, # Use a fixed past date
        "ctfs.json": [{"title": "TestCTF", "description": "A test", "link": "http://example.com", "completed": 2}],
        "badges.json": [{"id": "test-badge", "title": "Test Badge", "description": "Desc", "earnedAt": "2023-10-26T10:00:00", "shown": True, "image": "img.png"}]
    }

    original_paths = {}
    for filename, content in files_content.items():
        file_path = base_dir / filename
        original_paths[filename] = file_path
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)

    # --- Mocking file paths within modules ---
    # This is crucial: tell the core modules to use the temp files
    pytest.importorskip('core.data').JSON_PATH = str(original_paths["x.json"])
    pytest.importorskip('core.streak').STREAK_PATH = str(original_paths["streak.json"])
    pytest.importorskip('core.ctfs').CTF_PATH = str(original_paths["ctfs.json"])
    pytest.importorskip('core.badges').BADGES_PATH = str(original_paths["badges.json"])
    # Mock s3sync to do nothing during tests
    pytest.importorskip('core.s3sync').sync_down = lambda x: None
    pytest.importorskip('core.s3sync').sync_up = lambda x: None
    # Mock app's sync paths as well, if they are module-level constants
    # (They seem to be hardcoded strings in app.py, patching might be needed if complex)

    yield original_paths # Provide the paths to the tests if needed

    # Cleanup happens automatically due to tmp_path fixture