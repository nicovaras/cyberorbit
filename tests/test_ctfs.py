# tests/test_ctfs.py
import json
import pytest
from core.ctfs import load_ctfs, save_ctfs

# Mock s3 interactions
@pytest.fixture(autouse=True)
def mock_s3(mocker):
    mocker.patch('core.ctfs.sync_down', return_value=None)
    mocker.patch('core.ctfs.sync_up', return_value=None)

def test_load_ctfs(manage_test_json_files):
    """Test loading CTF data."""
    ctfs = load_ctfs()
    assert isinstance(ctfs, list)
    assert len(ctfs) == 1
    assert ctfs[0]['title'] == "TestCTF"
    assert ctfs[0]['completed'] == 2

def test_save_ctfs(manage_test_json_files):
    """Test saving CTF data."""
    file_path = manage_test_json_files["ctfs.json"]
    original_ctfs = load_ctfs()
    new_ctf = {"title": "NewCTF", "description": "New one", "link": "http://new.com", "completed": 0}
    original_ctfs.append(new_ctf)

    save_ctfs(original_ctfs)

    # Verify file content
    with open(file_path, 'r') as f:
        saved_data = json.load(f)

    assert isinstance(saved_data, list)
    assert len(saved_data) == len(original_ctfs)
    assert any(ctf['title'] == "NewCTF" for ctf in saved_data)

def test_load_ctfs_file_not_found(mocker, tmp_path):
    """Test load_ctfs returns empty list if file doesn't exist."""
    mocker.patch('core.ctfs.sync_down', side_effect=FileNotFoundError)
    non_existent_path = tmp_path / "non_existent_ctf.json"
    mocker.patch('core.ctfs.CTF_PATH', str(non_existent_path))
    mocker.patch('os.path.exists', return_value=False) # Mock os.path.exists check

    ctfs = load_ctfs()
    assert ctfs == []

def test_save_ctfs_creates_file(manage_test_json_files, tmp_path):
    """Test save_ctfs creates the file if it doesn't exist."""
    new_file_path = tmp_path / "json" / "new_ctfs.json"
    pytest.importorskip('core.ctfs').CTF_PATH = str(new_file_path) # Override path

    test_data = [{"title": "OnlyCTF", "completed": 1}]
    save_ctfs(test_data)

    assert new_file_path.exists()
    with open(new_file_path, 'r') as f:
        content = json.load(f)
    assert content == test_data