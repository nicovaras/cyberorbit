# test_utils.py
import pytest
from core.utils import build_child_map, get_subtree_nodes

# --- Test Data ---

# Sample data for build_child_map
SAMPLE_NODE_DATA_1 = [
    {"id": "A", "children": ["B", "C"]},
    {"id": "B", "children": ["D"]},
    {"id": "C", "children": []}, # Explicit empty children list
    {"id": "D"},               # Node with no children key
    {"id": "E", "children": ["F", "G"]},
]

# Expected child map for SAMPLE_NODE_DATA_1
EXPECTED_CHILD_MAP_1 = {
    "A": ["B", "C"],
    "B": ["D"],
    "E": ["F", "G"],
    # C and D should not be keys as they have no children
}

SAMPLE_NODE_DATA_EMPTY = []
EXPECTED_CHILD_MAP_EMPTY = {}

SAMPLE_NODE_DATA_NO_CHILDREN = [
    {"id": "X"},
    {"id": "Y"},
]
EXPECTED_CHILD_MAP_NO_CHILDREN = {}


# Sample child maps for get_subtree_nodes
CHILD_MAP_LINEAR = {"A": ["B"], "B": ["C"], "C": ["D"]}
CHILD_MAP_BRANCHING = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]}
CHILD_MAP_ISOLATED = {"A": [], "B": ["C"]} # Root A has no children
CHILD_MAP_CYCLE = {"A": ["B"], "B": ["C"], "C": ["A"]} # Test cycle handling
CHILD_MAP_EMPTY = {}

# --- Tests for build_child_map ---

def test_build_child_map_basic():
    """Test basic functionality with children present."""
    result = build_child_map(SAMPLE_NODE_DATA_1)
    assert result == EXPECTED_CHILD_MAP_1

def test_build_child_map_empty_input():
    """Test with an empty list of node data."""
    result = build_child_map(SAMPLE_NODE_DATA_EMPTY)
    assert result == EXPECTED_CHILD_MAP_EMPTY

def test_build_child_map_no_children():
    """Test with nodes that don't have children."""
    result = build_child_map(SAMPLE_NODE_DATA_NO_CHILDREN)
    assert result == EXPECTED_CHILD_MAP_NO_CHILDREN

def test_build_child_map_nodes_without_children_key():
    """Test nodes missing the 'children' key entirely."""
    data = [{"id": "A", "children": ["B"]}, {"id": "B"}]
    expected = {"A": ["B"]}
    result = build_child_map(data)
    assert result == expected

def test_build_child_map_nodes_with_empty_children_list():
    """Test nodes explicitly having 'children': []."""
    data = [{"id": "A", "children": ["B"]}, {"id": "B", "children": []}]
    expected = {"A": ["B"]}
    result = build_child_map(data)
    assert result == expected

# --- Tests for get_subtree_nodes ---

def test_get_subtree_nodes_linear():
    """Test finding subtree in a linear graph."""
    # Find subtree starting from A
    result = get_subtree_nodes("A", CHILD_MAP_LINEAR)
    assert result == {"B", "C", "D"}
    # Find subtree starting from B
    result = get_subtree_nodes("B", CHILD_MAP_LINEAR)
    assert result == {"C", "D"}
    # Find subtree starting from D (leaf)
    result = get_subtree_nodes("D", CHILD_MAP_LINEAR)
    assert result == set()

def test_get_subtree_nodes_branching():
    """Test finding subtree in a branching graph."""
    # Find subtree starting from A
    result = get_subtree_nodes("A", CHILD_MAP_BRANCHING)
    assert result == {"B", "C", "D", "E", "F"}
    # Find subtree starting from B
    result = get_subtree_nodes("B", CHILD_MAP_BRANCHING)
    assert result == {"D", "E"}
    # Find subtree starting from F (leaf)
    result = get_subtree_nodes("F", CHILD_MAP_BRANCHING)
    assert result == set()

def test_get_subtree_nodes_isolated_root():
    """Test when the root node has no children."""
    result = get_subtree_nodes("A", CHILD_MAP_ISOLATED)
    assert result == set()

def test_get_subtree_nodes_non_root_start():
    """Test starting from a node that isn't the 'true' root."""
    result = get_subtree_nodes("B", CHILD_MAP_ISOLATED)
    assert result == {"C"}

def test_get_subtree_nodes_empty_map():
    """Test with an empty child map."""
    result = get_subtree_nodes("A", CHILD_MAP_EMPTY)
    assert result == set()

def test_get_subtree_nodes_unknown_root():
    """Test when the root_id isn't in the map."""
    result = get_subtree_nodes("Z", CHILD_MAP_LINEAR)
    assert result == set()

def test_get_subtree_nodes_cycle():
    """Test graph with a cycle (should terminate and return reachable nodes)."""
    result = get_subtree_nodes("A", CHILD_MAP_CYCLE)
    # It should visit B and C, and not loop infinitely
    assert result == {"B", "C"}