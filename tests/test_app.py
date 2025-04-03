# tests/test_app.py
import pytest
import json
from flask import url_for
from unittest.mock import patch, MagicMock

# Fixtures 'app', 'client' are provided by tests/conftest.py

# --- Mocking Core Functions Used by Routes ---
@pytest.fixture(autouse=True)
def mock_core_functions(mocker):
    """Mock core logic functions to isolate Flask route tests."""
    # Mock get_computed_state logic to return predictable data
    mocker.patch('app.get_computed_state', return_value={
        "nodes": [{"id": "mock_n1", "title": "Mock Node 1", "type": "main", "percent": 50}],
        "links": [{"source": "Start", "target": "mock_n1"}],
        "unlocked": {"Start": True, "mock_n1": True},
        "discovered": ["Start", "mock_n1"],
        "streak": {"streak": 3, "last_used": "2023-10-27"},
        "ctfs": [{"title": "Mock CTF", "completed": 1}],
        "abilities": {"Test": 1, "CTFs": 1},
        "badges": [{"id": "mock_b1", "title": "Mock Badge", "shown": False}]
    })
    # Mock data saving functions
    mocker.patch('app.save_data', return_value=None)
    mocker.patch('app.save_ctfs', return_value=None)
    mocker.patch('app.save_badges', return_value=None)
    # Mock badge loading for the update_badges route
    mocker.patch('app.load_badges', return_value=[
        {"id": "b1", "title": "Badge 1", "shown": False},
        {"id": "b2", "title": "Badge 2", "shown": True},
    ])
    # Mock markdown rendering if testing that route specifically
    mocker.patch('app.markdown.markdown', return_value='<h1>Mocked HTML</h1>')


# --- Route Tests ---

def test_index_route(client):
    """Test the root route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    # Check for a specific element expected in index.html
    # Note: This checks the *rendered* HTML string from the fixture `app`
    assert b'CyberOrbit Roadmap' in response.data

def test_get_data_route(client, mock_core_functions):
    """Test the GET /data route."""
    response = client.get('/data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'nodes' in data
    assert 'streak' in data
    assert 'ctfs' in data
    assert 'badges' in data
    assert data['nodes'][0]['id'] == "mock_n1" # Check mocked data is returned

def test_post_data_route(client, mock_core_functions):
    """Test the POST /data route."""
    test_payload = [{"id": "mock_n1", "percent": 60}] # Example update payload
    response = client.post('/data', json=test_payload)
    assert response.status_code == 200
    # Verify save_data was called (implicitly by mock)
    # Verify the response contains the *updated* state from get_computed_state mock
    data = json.loads(response.data)
    assert data['streak']['streak'] == 3 # Check some value from the mocked return

    # Test error case during save (requires adjusting mocks)
    with patch('app.save_data', side_effect=Exception("Save Failed")):
        response_fail = client.post('/data', json=test_payload)
        assert response_fail.status_code == 500
        assert b"Failed to process node data update" in response_fail.data

def test_post_ctfs_route(client, mock_core_functions):
    """Test the POST /ctfs route."""
    test_payload = [{"title": "Mock CTF", "completed": 2}] # Example update
    response = client.post('/ctfs', json=test_payload)
    assert response.status_code == 200
    # Verify save_ctfs was called (implicitly by mock)
    # Verify the response contains the *updated* state from get_computed_state mock
    data = json.loads(response.data)
    assert data['nodes'][0]['id'] == "mock_n1" # Check some value from the mocked return

    # Test error case during save
    with patch('app.save_ctfs', side_effect=Exception("CTF Save Failed")):
        response_fail = client.post('/ctfs', json=test_payload)
        assert response_fail.status_code == 500
        assert b"Failed to process CTF data update" in response_fail.data

def test_static_files_route(client):
    """Test serving a known static file (requires static folder setup)."""
    # This test assumes a file exists at 'static/dracula.css' relative to app.py
    # In a real test setup, you might need to create a dummy static file
    # For now, let's assume the file exists from the project structure
    # If app.static_folder isn't correctly resolved, this might fail.
    # We need to ensure the app context correctly finds the static folder.
    response = client.get('/static/dracula.css')
    assert response.status_code == 200
    assert b':root' in response.data # Check for some content known to be in dracula.css
    # Test non-existent file
    response_404 = client.get('/static/nonexistentfile.css')
    assert response_404.status_code == 404

def test_serve_markdown_route(client, mocker): # Add mocker
    """Test the /md/<filename> route."""
    # Mock file system interactions *only for this test*
    mocker.patch('os.path.isfile', return_value=True)
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='# Mock Markdown'))

    response = client.get('/md/test.md')
    assert response.status_code == 200
    assert b'<h1>Mocked HTML</h1>' in response.data # Check mocked markdown output

def test_serve_markdown_not_found(client, mocker): # Add mocker
     """Test the /md/<filename> route when file is not found."""
     # Mock isfile to return False *only for this test*
     mocker.patch('os.path.isfile', return_value=False)
     response = client.get('/md/not_found.md')
     assert response.status_code == 404


def test_update_badges_route(client, mock_core_functions, mocker):
    """Test the POST /update_badges route."""
    mocker.patch('os.path.isfile', return_value=False)
    payload = {"badgeIds": ["b1"]} # Mark badge 'b1' as shown
    response = client.post('/update_badges', json=payload)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["updated"] is True # b1 was initially not shown
    # Verify save_badges was called (implicitly by mock)

def test_update_badges_already_shown(client, mock_core_functions):
    """Test updating a badge that is already shown."""
    payload = {"badgeIds": ["b2"]} # b2 is already shown in mock_load_badges
    response = client.post('/update_badges', json=payload)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["updated"] is False # No change was made

def test_update_badges_invalid_payload(client):
    """Test /update_badges with missing or invalid payload."""
    response_missing = client.post('/update_badges', json={})
    assert response_missing.status_code == 400
    assert b"Missing badgeIds" in response_missing.data

    response_invalid = client.post('/update_badges', json={"badgeIds": "not_a_list"})
    assert response_invalid.status_code == 400
    assert b"Invalid payload format" in response_invalid.data