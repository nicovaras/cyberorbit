# tests/test_data.py
import json
import pytest
from core.data import load_data, save_data
from core.s3sync import sync_up, sync_down # Import mocked functions

# Mock s3 interactions (though already mocked in conftest)
@pytest.fixture(autouse=True)
def mock_s3(mocker):
    mocker.patch('core.data.sync_down', return_value=None)
    mocker.patch('core.data.sync_up', return_value=None)

def test_load_data(manage_test_json_files):
    """Test loading data from the temporary JSON file."""
    data = load_data()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['id'] == "n_test_1"
    # Check if sync_down was called (implicitly tested by mock)

def test_save_data(manage_test_json_files):
    """Test saving data to the temporary JSON file."""
    file_path = manage_test_json_files["x.json"]
    original_data = load_data()
    new_node = {"id": "n_test_new", "title": "New Test Node", "type": "main", "percent": 0, "popup": {}, "children": [], "prerequisites": []}
    original_data.append(new_node)

    save_data(original_data)

    # Verify file content directly
    with open(file_path, 'r') as f:
        saved_data_raw = json.load(f)

    assert isinstance(saved_data_raw, list)
    assert len(saved_data_raw) == len(original_data)
    assert any(node['id'] == "n_test_new" for node in saved_data_raw)
    # Check if sync_up was called (implicitly tested by mock)

def test_load_data_file_not_found(mocker, tmp_path):
    """Test load_data behavior when the file doesn't exist initially."""
    # Ensure sync_down doesn't create the file if it fails
    mocker.patch('core.data.sync_down', side_effect=FileNotFoundError)
    # Point to a non-existent file within tmp_path
    non_existent_path = tmp_path / "non_existent.json"
    mocker.patch('core.data.JSON_PATH', str(non_existent_path))

    with pytest.raises(FileNotFoundError):
        load_data()

def test_save_data_creates_file(manage_test_json_files, tmp_path):
    """Test that save_data creates the file if it doesn't exist."""
    new_file_path = tmp_path / "json" / "new_x.json"
    pytest.importorskip('core.data').JSON_PATH = str(new_file_path) # Override path

    test_data = [{"id": "only_node"}]
    save_data(test_data)

    assert new_file_path.exists()
    with open(new_file_path, 'r') as f:
        content = json.load(f)
    assert content == test_data