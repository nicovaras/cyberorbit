# tests/test_data.py
import json
import os
import pytest
# Import the functions to test
from core.data import load_data, save_data

# Mock s3 interactions - Applying universally to all tests in this file
@pytest.fixture(autouse=True)
def mock_s3(mocker):
    """Mocks s3 sync functions and os.makedirs for all tests in this module."""
    mocker.patch('core.data.sync_down', return_value=None)
    mocker.patch('core.data.sync_up', return_value=None)
    mocker.patch('os.makedirs', return_value=None) # Prevent creating real 'json' dir

def test_load_data_success(tmp_path, mocker):
    """Test loading data successfully from a temporary JSON file."""
    json_dir = tmp_path / "json"
    # <<< Use exist_ok=True >>>
    json_dir.mkdir(parents=True, exist_ok=True)
    test_file = json_dir / "x.json"
    test_data = [{"id": "n_test_1", "title": "Test Node 1"}]
    test_file.write_text(json.dumps(test_data))

    mocker.patch('os.path.join', return_value=str(test_file))

    data = load_data("x.json")
    assert data == test_data
    # core.data.sync_down.assert_called_once_with(str(test_file)) # Optional check

def test_save_data_updates_file(tmp_path, mocker):
    """Test saving data updates the temporary JSON file."""
    json_dir = tmp_path / "json"
    # <<< Use exist_ok=True >>>
    json_dir.mkdir(parents=True, exist_ok=True)
    test_file = json_dir / "x.json"
    initial_data = [{"id": "n_orig_1", "title": "Original"}]
    test_file.write_text(json.dumps(initial_data))

    mocker.patch('os.path.join', return_value=str(test_file))

    data_to_modify = load_data("x.json")
    new_node = {"id": "n_new_1", "title": "New Node"}
    data_to_modify.append(new_node)
    save_data(data_to_modify, "x.json")

    saved_data_raw = json.loads(test_file.read_text())
    assert saved_data_raw == data_to_modify
    assert any(node['id'] == "n_new_1" for node in saved_data_raw)
    # core.data.sync_up.assert_called_once_with(str(test_file)) # Optional check

def test_load_data_file_not_found(tmp_path, mocker):
    """Test load_data returns empty list when the file doesn't exist."""
    json_dir = tmp_path / "json"
    # Directory might not exist, file definitely won't
    test_file = json_dir / "nonexistent.json"

    mocker.patch('os.path.join', return_value=str(test_file))
    mocker.patch('core.data.sync_down', return_value=None)

    data = load_data("nonexistent.json")
    assert data == []

def test_load_data_invalid_json(tmp_path, mocker):
    """Test load_data returns empty list for invalid JSON."""
    json_dir = tmp_path / "json"
    # <<< Use exist_ok=True >>>
    json_dir.mkdir(parents=True, exist_ok=True)
    test_file = json_dir / "bad.json"
    test_file.write_text("this is not json {") # Make it invalid

    mocker.patch('os.path.join', return_value=str(test_file))

    data = load_data("bad.json")
    assert data == []


def test_save_data_creates_file(tmp_path, mocker):
    """Test that save_data creates the file if it doesn't exist."""
    json_dir = tmp_path / "json"
    # <<< Create directory explicitly >>>
    json_dir.mkdir(parents=True, exist_ok=True)
    test_file = json_dir / "new_save.json"

    mocker.patch('os.path.join', return_value=str(test_file))
    # os.makedirs mock is handled by the fixture

    test_data = [{"id": "created_node"}]
    save_data(test_data, "new_save.json")

    assert test_file.exists()
    content = json.loads(test_file.read_text())
    assert content == test_data
    # core.data.sync_up.assert_called_once_with(str(test_file)) # Optional check

def test_load_data_uses_filename(tmp_path, mocker):
    """Test that load_data loads 'y.json' when specified."""
    json_dir = tmp_path / "json"
    # <<< Use exist_ok=True >>>
    json_dir.mkdir(parents=True, exist_ok=True)
    x_file = json_dir / "x.json"
    y_file = json_dir / "y.json"

    x_data = [{"id": "node_x"}]
    y_data = [{"id": "node_y"}]

    x_file.write_text(json.dumps(x_data))
    y_file.write_text(json.dumps(y_data))

    # Mock os.path.join to return the correct temp path based on input filename
    def side_effect_join(*args):
        # args should be (JSON_DIR, filename) -> ('json', 'y.json') etc.
        # Use the mocked JSON_DIR logic if needed, or simplify if path is consistent
        base_dir = tmp_path / "json" # Use the tmp_path json dir
        filename = args[-1]
        return str(base_dir / filename)

    mocker.patch('os.path.join', side_effect=side_effect_join)

    # Load 'y.json'
    data = load_data("y.json")
    assert data == y_data

    # Load default ('x.json')
    data_x = load_data("x.json")
    assert data_x == x_data
    data_default = load_data() # Test default loads x.json via side effect logic
    assert data_default == x_data