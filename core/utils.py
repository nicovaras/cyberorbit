def build_child_map(data):
    child_map = {}
    for d in data:
        for child in d.get("children", []):
            child_map.setdefault(d["id"], []).append(child)
    return child_map

def get_subtree_nodes(root_id, child_map):
    visited = set()
    stack = [root_id]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(child_map.get(node, []))
    visited.remove(root_id)
    return visited
