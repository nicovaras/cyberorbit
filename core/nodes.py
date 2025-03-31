from core.utils import build_child_map, get_subtree_nodes

def compute_node_states(data):
    id_to_node = {d["id"]: dict(d, percent=0) for d in data if d["id"]}
    id_to_node["Start"] = {
        "id": "Start",
        "title": "Start",
        "type": "start",
        "percent": 100,
        "popup": {"text": "This is the beginning of your journey.", "pdf_link": "", "exercises": []},
    }

    for node in id_to_node.values():
        if node["type"] not in ("main", "start"):
            ex = node.get("popup", {}).get("exercises", [])
            required = [e for e in ex if not e.get("optional")]
            total_points = sum(e.get("points", 10) for e in required)
            done_points = sum(e.get("points", 10) for e in required if e.get("completed"))
            node["percent"] = round((done_points / total_points) * 100) if total_points else 0

    child_map = build_child_map(data)

    for node in id_to_node.values():
        if node["type"] == "main":
            all_sub_ids = get_subtree_nodes(node["id"], child_map)
            sub_nodes = [id_to_node[sid] for sid in all_sub_ids if sid in id_to_node and id_to_node[sid]["type"] != "main"]
            node["percent"] = round(sum(n["percent"] for n in sub_nodes) / len(sub_nodes)) if sub_nodes else 0

    unlocked = {"Start": True}
    for node in id_to_node.values():
        if node["id"] == "Start":
            continue
        raw = next((d for d in data if d["id"] == node["id"]), {})
        prereqs = raw.get("prerequisites", [])
        parents = [d["id"] for d in data if node["id"] in d.get("children", [])]
        if node["type"] == "main":
            unlocked[node["id"]] = all(id_to_node[p]["percent"] >= 60 for p in prereqs)
        else:
            main_parent = next((id_to_node[p] for p in parents if id_to_node[p]["type"] == "main"), None)
            if main_parent:
                unlocked[node["id"]] = unlocked.get(main_parent["id"], False)
            else:
                unlocked[node["id"]] = all(id_to_node[p]["percent"] >= 60 for p in parents)

    links = []
    for d in data:
        for c in d.get("children", []):
            links.append({"source": d["id"], "target": c})
        for p in d.get("prerequisites", []):
            links.append({"source": p, "target": d["id"]})
        if d["type"] == "main" and not d.get("prerequisites"):
            links.append({"source": "Start", "target": d["id"]})

    return list(id_to_node.values()), links, unlocked

def compute_abilities(data, ctfs):
    from collections import defaultdict
    abilities = defaultdict(int)
    for node in data:
        exercises = node.get("popup", {}).get("exercises", [])
        for ex in exercises:
            if ex.get("completed") and not ex.get("optional", False):
                for cat in ex.get("categories", []):
                    abilities[cat] += 1
    abilities["CTFs"] = sum(c.get("solved", 0) for c in ctfs)
    return dict(abilities)

def compute_discovered_nodes(unlocked, links):
    discovered = set(node_id for node_id, is_unlocked in unlocked.items() if is_unlocked)
    for link in links:
        source, target = link['source'], link['target']
        if unlocked.get(source) or unlocked.get(target):
            discovered.update([source, target])
    return discovered
