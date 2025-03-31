from core.nodes import compute_node_states, compute_abilities

def test_node_states_unlock_logic():
    data = [{"id": "a", "title": "A", "type": "main", "children": []}]
    nodes, links, unlocked = compute_node_states(data)
    ids = [n["id"] for n in nodes]
    assert "a" in ids
    assert unlocked["a"] in [True, False]

def test_compute_abilities():
    nodes = [{
        "id": "x", "popup": {
            "exercises": [
                {"completed": True, "optional": False, "categories": ["Web", "CTFs"]},
                {"completed": False, "optional": False, "categories": ["Web"]}
            ]
        }
    }]
    ctfs = [{"solved": 2}]
    result = compute_abilities(nodes, ctfs)
    assert result["Web"] == 1
    assert result["CTFs"] == 2
