# tests/test_nodes.py
import pytest
from core.nodes import compute_node_states, compute_abilities, compute_discovered_nodes

# --- Sample Data ---
@pytest.fixture
def sample_node_data():
    # Structure: main -> sub1 -> sub2, main -> sub3
    # sub1 has 2 exercises, 1 done
    # sub2 has 1 exercise, 0 done
    # sub3 has 1 exercise, 1 done
    return [
        {"id": "m1", "title": "Main 1", "type": "main", "children": ["s1", "s3", "m2"], "prerequisites": ["Start"], "popup": {}},
        {"id": "s1", "title": "Sub 1", "type": "sub", "children": ["s2"], "prerequisites": ["m1"], "popup": {
            "exercises": [
                {"id": "ex1", "completed": True, "points": 10, "categories": ["CatA"]},
                {"id": "ex2", "completed": False, "points": 10, "categories": ["CatA"]},
            ]}},
        {"id": "s2", "title": "Sub 2", "type": "sub", "children": [], "prerequisites": ["s1"], "popup": {
            "exercises": [
                {"id": "ex3", "completed": False, "points": 20, "categories": ["CatB"]},
            ]}},
        {"id": "s3", "title": "Sub 3", "type": "sub", "children": [], "prerequisites": ["m1"], "popup": {
            "exercises": [
                {"id": "ex4", "completed": True, "points": 30, "categories": ["CatB"]},
            ]}},
         {"id": "m2", "title": "Main 2", "type": "main", "children": ["s4"], "prerequisites": ["m1"], "popup": {}}, # Depends on m1
         {"id": "s4", "title": "Sub 4", "type": "sub", "children": [], "prerequisites": ["m2"], "popup": { "exercises": []}} # No exercises
    ]

@pytest.fixture
def sample_ctf_data():
    return [{"title": "CTF1", "completed": 3}]

# --- Tests for compute_node_states ---

def test_compute_sub_node_percentage(sample_node_data):
    """Test percentage calculation for sub nodes based on exercises."""
    nodes, _, _ = compute_node_states(sample_node_data)
    node_map = {n['id']: n for n in nodes}

    assert node_map['s1']['percent'] == 50 # 1 of 2 exercises done
    assert node_map['s2']['percent'] == 0  # 0 of 1 exercise done
    assert node_map['s3']['percent'] == 100 # 1 of 1 exercise done
    assert node_map['s4']['percent'] == 0 # 0 of 0 exercises done

def test_compute_main_node_percentage(sample_node_data):
    """Test percentage calculation for main nodes based on descendant sub nodes."""
    nodes, _, _ = compute_node_states(sample_node_data)
    node_map = {n['id']: n for n in nodes}

    # m1 depends on s1(50%), s2(0%), s3(100%) -> Avg = (50+0+100)/3 = 150/3 = 50%
    assert node_map['m1']['percent'] == 50
    # m2 depends on s4(0%) -> Avg = 0/1 = 0%
    assert node_map['m2']['percent'] == 0

def test_compute_unlocked_status_initial(sample_node_data):
    """Test initial unlock status (Start and direct children)."""
    _, _, unlocked = compute_node_states(sample_node_data)
    assert unlocked.get("Start", False) is True
    assert unlocked.get("m1", False) is True # Depends only on Start
    assert unlocked.get("s1", False) is True # Child of unlocked m1
    assert unlocked.get("s3", False) is True # Child of unlocked m1
    assert unlocked.get("s2", False) is True # Child of unlocked s1
    # m2 requires m1 at 50% (UNLOCK_PERCENT). m1 is 50% in this data.
    assert unlocked.get("m2", False) is True
    assert unlocked.get("s4", False) is True # Child of unlocked m2

def test_compute_unlocked_status_prereq_percent(sample_node_data):
    """Test unlock status when a prerequisite percentage is not met."""
    # Modify s1 and s3 to be incomplete, lowering m1's percentage
    sample_node_data[1]["popup"]["exercises"][0]["completed"] = False # s1 ex1 incomplete
    sample_node_data[3]["popup"]["exercises"][0]["completed"] = False # s3 ex4 incomplete

    nodes, _, unlocked = compute_node_states(sample_node_data)
    node_map = {n['id']: n for n in nodes}

    # Recalculate m1 percent: s1=0%, s2=0%, s3=0% -> m1=0%
    assert node_map['m1']['percent'] == 0
    assert unlocked.get("m1", False) is True # Still unlocked as child of Start

    # m2 depends on m1 meeting UNLOCK_PERCENT (50). m1 is now 0%.
    assert unlocked.get("m2", False) is False # Should now be locked
    assert unlocked.get("s4", False) is False # Child of locked m2

def test_compute_links(sample_node_data):
    """Test that links are generated correctly."""
    _, links, _ = compute_node_states(sample_node_data)
    link_pairs = set(tuple(sorted((l['source'], l['target']))) for l in links)

    assert tuple(sorted(("m1", "s1"))) in link_pairs
    assert tuple(sorted(("m1", "s3"))) in link_pairs
    assert tuple(sorted(("s1", "s2"))) in link_pairs
    assert tuple(sorted(("m1", "m2"))) in link_pairs # Link between main nodes based on prereq
    assert tuple(sorted(("m2", "s4"))) in link_pairs
    assert len(links) == 5 # Check total number of unique links

# --- Tests for compute_abilities ---

def test_compute_abilities_calculation(sample_node_data, sample_ctf_data):
    """Test calculation of ability points."""
    # In sample_node_data:
    # ex1 (done, req): CatA -> +1
    # ex2 (not done)
    # ex3 (not done)
    # ex4 (done, req): CatB -> +1
    # CTFs: 3 completed
    abilities = compute_abilities(sample_node_data, sample_ctf_data)

    assert abilities.get("CatA", 0) == 1
    assert abilities.get("CatB", 0) == 1
    assert abilities.get("CTFs", 0) == 3
    assert abilities.get("NonExistentCategory", 0) == 0

def test_compute_abilities_empty():
    """Test abilities with empty inputs."""
    abilities = compute_abilities([], [])
    assert abilities == {"CTFs": 0} # CTFs key might still be added

# --- Tests for compute_discovered_nodes ---

def test_compute_discovered_nodes_basic(sample_node_data):
    """Test basic node discovery."""
    _, links, unlocked = compute_node_states(sample_node_data)
    # Default unlocked: Start, m1, s1, s2, s3, m2, s4
    discovered = compute_discovered_nodes(unlocked, links)

    # All nodes should be discovered because they are linked and unlocked
    all_node_ids = set(n['id'] for n in sample_node_data)
    all_node_ids.add("Start")
    assert discovered == all_node_ids

def test_compute_discovered_nodes_locked_branch(sample_node_data):
    """Test discovery when a branch is locked."""
     # Modify s1 and s3 to be incomplete, lowering m1's percentage -> locks m2/s4
    sample_node_data[1]["popup"]["exercises"][0]["completed"] = False
    sample_node_data[3]["popup"]["exercises"][0]["completed"] = False
    _, links, unlocked = compute_node_states(sample_node_data)

    # unlocked should now be: Start, m1, s1, s2, s3 (m2 and s4 are locked)
    assert unlocked.get("m2") is None
    assert unlocked.get("s4") is None

    discovered = compute_discovered_nodes(unlocked, links)
    expected_discovered = {"Start", "m1", "s1", "s2", "s3", "m2", "s4"}
    print(discovered)
    assert discovered == expected_discovered