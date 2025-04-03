# tests/test_utils.py
import pytest
from core.utils import build_child_map, get_subtree_nodes

@pytest.fixture
def sample_data_for_utils():
    return [
        {"id": "root", "children": ["a", "b"]},
        {"id": "a", "children": ["c"]},
        {"id": "b", "children": ["d", "e"]},
        {"id": "c", "children": []},
        {"id": "d", "children": []},
        {"id": "e", "children": ["f"]}, # f is not in the main data list
        {"id": "g", "children": []} # Unconnected node
    ]

def test_build_child_map(sample_data_for_utils):
    child_map = build_child_map(sample_data_for_utils)
    assert child_map == {
        "root": ["a", "b"],
        "a": ["c"],
        "b": ["d", "e"],
        "e": ["f"]
        # c, d, g have no children, so they shouldn't be keys
    }
    assert "c" not in child_map
    assert "d" not in child_map
    assert "g" not in child_map

def test_build_child_map_empty():
    assert build_child_map([]) == {}

def test_build_child_map_no_children():
    data = [{"id": "1"}, {"id": "2"}]
    assert build_child_map(data) == {}

def test_get_subtree_nodes(sample_data_for_utils):
    child_map = build_child_map(sample_data_for_utils)
    subtree = get_subtree_nodes("root", child_map)
    # Should include a, b, c, d, e, f but NOT root itself or g
    assert subtree == {"a", "b", "c", "d", "e", "f"}

def test_get_subtree_nodes_leaf(sample_data_for_utils):
    child_map = build_child_map(sample_data_for_utils)
    # Subtree of a leaf node is empty
    assert get_subtree_nodes("c", child_map) == set()
    assert get_subtree_nodes("d", child_map) == set()
    # Subtree of an unconnected node is empty
    assert get_subtree_nodes("g", child_map) == set()

def test_get_subtree_nodes_intermediate(sample_data_for_utils):
    child_map = build_child_map(sample_data_for_utils)
    # Subtree of 'b' includes 'd', 'e', 'f'
    assert get_subtree_nodes("b", child_map) == {"d", "e", "f"}

def test_get_subtree_nodes_missing_root(sample_data_for_utils):
    child_map = build_child_map(sample_data_for_utils)
    # If root_id doesn't exist in map keys or data, should handle gracefully (empty set)
    assert get_subtree_nodes("nonexistent", child_map) == set()