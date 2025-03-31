import pytest
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def restore_files():
    originals = {
        "x.json": '[{"id": "n1", "title": "Node 1", "type": "main", "children": [], "popup": {"exercises": []}}]',
        "streak.json": '{"streak": 2, "last_used": "2025-03-28"}',
        "ctfs.json": '[{"title": "CTF1", "completed": 1}]',
        "badges.json": '[]'
    }
    for path, content in originals.items():
        with open(path, "w") as f:
            f.write(content)
    yield
    for path in originals:
        os.remove(path)
