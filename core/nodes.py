import collections
from core.utils import build_child_map

UNLOCK_PERCENT = 50

def compute_node_states(data):
    """
    Computes node percentages and unlocked status.
    - Sub-node percent = based on completed non-optional exercises.
    - Main-node percent = average percent of all descendant sub-nodes *within its branch*
                         (traversal stops at the next main node).
    - Unlock logic:
        - Main nodes unlock ONLY if all prerequisites are unlocked AND meet UNLOCK_PERCENT.
        - Sub-nodes unlock if parent is unlocked AND all prerequisites are met (ignoring % for direct main parent prereq).
    """
    id_to_node = {d["id"]: dict(d, percent=0) for d in data if "id" in d}
    id_to_node["Start"] = {
        "id": "Start", "title": "Start", "type": "start", "percent": 100,
        "popup": {"text": "Start.", "exercises": []},
        "children": [], "prerequisites": []
    }

    # Step 1: Calculate sub-node percentages (same as before)
    for node_id, node in id_to_node.items():
        if node["type"] == "sub":
            exercises = node.get("popup", {}).get("exercises", [])
            required_exercises = [e for e in exercises if not e.get("optional")]
            if not required_exercises:
                node["percent"] = 0
                continue
            total_possible_points = sum(e.get("points", 10) for e in required_exercises)
            earned_points = sum(e.get("points", 10) for e in required_exercises if e.get("completed"))
            node["percent"] = round((earned_points / total_possible_points) * 100) if total_possible_points else (100 if all(e.get("completed") for e in required_exercises) else 0)

    # Step 2: Build child map (same as before)
    child_map = build_child_map(id_to_node.values())

    # Step 3: Calculate main node percentages (BFS stopping at main nodes)
    for node_id, node in id_to_node.items():
        if node["type"] == "main":
            total_percent = 0
            sub_node_count = 0
            queue = collections.deque(child_map.get(node_id, []))
            visited_in_calc = {node_id}
            while queue:
                descendant_id = queue.popleft()
                if descendant_id in visited_in_calc: continue
                visited_in_calc.add(descendant_id)
                descendant_node = id_to_node.get(descendant_id)
                if not descendant_node: continue
                if descendant_node["type"] == "sub":
                    total_percent += descendant_node.get("percent", 0)
                    sub_node_count += 1
                    for child_id in child_map.get(descendant_id, []):
                        if child_id not in visited_in_calc: queue.append(child_id)
                elif descendant_node["type"] == "main":
                    continue
            node["percent"] = round(total_percent / sub_node_count) if sub_node_count else 0

    # --- Step 4: Determine unlocked status (REVISED LOGIC v4) ---
    unlocked = {"Start": True}
    changed_in_pass = True
    max_passes = len(id_to_node) + 1
    current_pass = 0

    while changed_in_pass and current_pass < max_passes:
        changed_in_pass = False
        current_pass += 1

        for node_id, node in id_to_node.items():
            if node_id == "Start":
                continue

            current_status = unlocked.get(node_id, False)
            new_status = False # Assume locked

            prereq_ids = node.get("prerequisites", [])
            parent_ids = [p_id for p_id, children in child_map.items() if node_id in children]

            # --- Determine unlock based on Type ---
            if node["type"] == "main":
                # Main nodes depend *only* on prerequisites meeting the threshold.
                prereqs_met = True
                if not prereq_ids:
                    prereqs_met = True # No prerequisites means OK (unlocked by Start)
                else:
                    for prereq_id in prereq_ids:
                        prereq_node = id_to_node.get(prereq_id)
                        # *** Must exist, be unlocked, AND meet percentage ***
                        if not prereq_node or not unlocked.get(prereq_id, False) or prereq_node.get("percent", 0) < UNLOCK_PERCENT:
                            prereqs_met = False
                            break
                new_status = prereqs_met

            elif node["type"] == "sub":
                # Sub-nodes need parent unlocked AND prerequisites met (with exception for main parent prereq)
                parent_unlocked = any(unlocked.get(p_id, False) for p_id in parent_ids)

                prereqs_met = True # Assume OK unless a non-parent prereq fails
                if not prereq_ids:
                    prereqs_met = True # No specific prerequisites for the sub-node itself
                else:
                    for prereq_id in prereq_ids:
                        prereq_node = id_to_node.get(prereq_id)

                        # Basic check: Prerequisite must exist and be unlocked
                        if not prereq_node or not unlocked.get(prereq_id, False):
                            prereqs_met = False
                            break

                        # Percentage Check: Required ONLY if the prerequisite is NOT a direct main-node parent
                        is_direct_parent = prereq_id in parent_ids
                        prereq_is_main = prereq_node.get("type") == "main"

                        # Check percentage ONLY if it's NOT (a direct parent AND that parent is main)
                        if not (is_direct_parent and prereq_is_main):
                            if prereq_node.get("percent", 0) < UNLOCK_PERCENT:
                                prereqs_met = False
                                break
                # Sub-node unlocks if parent is unlocked AND its own prerequisites are met
                new_status = parent_unlocked and prereqs_met

            # Update status if changed
            if new_status != current_status:
                unlocked[node_id] = new_status
                changed_in_pass = True

        # Safety break log
        if current_pass == max_passes and changed_in_pass:
            print("Warning: Unlock status did not stabilize within max passes.")

    # Step 5: Generate Links (same as before)
    links = []
    unique_links_set = set()
    for node_id, node_data in id_to_node.items():
        for child_id in child_map.get(node_id, []):
             if child_id in id_to_node:
                 link_tuple = tuple(sorted((node_id, child_id)))
                 if link_tuple not in unique_links_set:
                     links.append({"source": node_id, "target": child_id})
                     unique_links_set.add(link_tuple)
        # Add links from Start only to main nodes that have NO prerequisites
        if node_data["type"] == "main" and not node_data.get("prerequisites"):
             if "Start" in id_to_node:
                 link_tuple = tuple(sorted(("Start", node_id)))
                 if link_tuple not in unique_links_set:
                     links.append({"source": "Start", "target": node_id})
                     unique_links_set.add(link_tuple)


    return list(id_to_node.values()), links, unlocked

# --- compute_abilities and compute_discovered_nodes remain the same ---
# (Include the previous versions of these functions here)
def compute_abilities(data, ctfs):
    # ... (same as before) ...
    from collections import defaultdict
    abilities = defaultdict(int)
    for node in data:
        exercises = node.get("popup", {}).get("exercises", [])
        for ex in exercises:
            if ex.get("completed") and not ex.get("optional", False):
                for cat in ex.get("categories", []):
                    abilities[cat] += 1
    abilities["CTFs"] = sum(c.get("completed", 0) for c in ctfs)
    return dict(abilities)


def compute_discovered_nodes(unlocked, links):
    # ... (same as before) ...
    discovered = set(node_id for node_id, is_unlocked in unlocked.items() if is_unlocked)
    link_map = collections.defaultdict(list)
    for link in links:
        link_map[link['source']].append(link['target'])
        link_map[link['target']].append(link['source'])

    nodes_to_check = collections.deque(discovered)
    fully_discovered = set(discovered)
    processed_discovery = set()

    while nodes_to_check:
        node_id = nodes_to_check.popleft()
        if node_id in processed_discovery :
            continue
        processed_discovery.add(node_id)

        for neighbor_id in link_map.get(node_id, []):
            if neighbor_id not in fully_discovered:
                fully_discovered.add(neighbor_id)
                if unlocked.get(node_id, False):
                     nodes_to_check.append(neighbor_id)
    return fully_discovered