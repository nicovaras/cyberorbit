# cyberorbit/core/nodes.py
import collections
from models import db, Node, NodeRelationship, UserNodeStatus, UserExerciseCompletion, Exercise # Import necessary models
from core import data as core_data # Still needed for update_user_node_status_bulk
from core.utils import build_child_map # Keep utility if still needed

UNLOCK_PERCENT = 50

# --- Refactored User-Specific State Computation ---

def compute_user_graph_state(user_id, graph_id, static_nodes_list, static_links_list, user_node_status_map, completed_exercise_ids):
    """
    Computes the complete graph state for a specific user and graph,
    using pre-fetched static data and user progress data.
    Updates user node status (percent, unlocked, discovered) in the database.

    Args:
        user_id (int): The ID of the user.
        graph_id (int): The ID of the graph.
        static_nodes_list (list): List of node dictionaries (including exercises) from get_static_graph_data.
        static_links_list (list): List of link dictionaries from get_static_graph_data.
        user_node_status_map (dict): Dict {node_id: UserNodeStatus obj} for the user from get_user_progress.
        completed_exercise_ids (set): Set of completed exercise IDs for the user from get_user_progress.

    Returns:
        tuple: (final_nodes_list, final_links_list, unlocked_map, discovered_ids)
               - final_nodes_list: List of node dicts formatted for frontend.
               - final_links_list: List of link dicts formatted for frontend.
               - unlocked_map: Dict {node_id: bool} of unlocked status for the user.
               - discovered_ids: Set of discovered node IDs for the user.
    """
    try:
        if not static_nodes_list:
            print(f"Warning: No static nodes provided for graph_id {graph_id}")
            return [], [], {}, set()

        # Build helper maps from static data
        static_node_map = {node['id']: node for node in static_nodes_list}
        # Build parent/prereq maps from relationships
        child_map = collections.defaultdict(list)
        prereq_map = collections.defaultdict(list)
        node_parents = collections.defaultdict(list)
        for link in static_links_list:
            if link['type'] == 'CHILD':
                child_map[link['source']].append(link['target'])
                node_parents[link['target']].append(link['source'])
            elif link['type'] == 'PREREQUISITE':
                prereq_map[link['target']].append(link['source'])

        # Add Start node conceptually for calculations
        static_node_map["Start"] = {"id": "Start", "type": "start", "title": "Start"}
        # User status map already fetched, add Start conceptually if needed
        # (Ensure Start node handling doesn't rely on DB UserNodeStatus)

        # --- 1. Calculate user-specific percentages ---
        node_percentages = {} # node_id -> calculated percentage for this user

        # Calculate sub-node percentages using provided completed_exercise_ids
        for node_id, node_data in static_node_map.items():
            if node_data.get('type') == 'sub': # Check type safely
                exercises = node_data.get('popup', {}).get('exercises', [])
                total_exercises = len(exercises)
                if total_exercises == 0:
                    node_percentages[node_id] = 0
                else:
                    completed_count = sum(1 for ex in exercises if ex['id'] in completed_exercise_ids)
                    node_percentages[node_id] = round((completed_count / total_exercises) * 100)

        # Calculate main-node percentages using calculated sub-node percentages
        for node_id, node_data in static_node_map.items():
             if node_data.get('type') == 'main':
                # ... (BFS logic for main node percentage calculation remains the same, using node_percentages map) ...
                total_percent_sum = 0; sub_node_count = 0
                queue = collections.deque(child_map.get(node_id, [])); visited_in_calc = {node_id}
                while queue:
                    descendant_id = queue.popleft();
                    if descendant_id in visited_in_calc: continue; visited_in_calc.add(descendant_id)
                    descendant_node_data = static_node_map.get(descendant_id);
                    if not descendant_node_data: continue
                    if descendant_node_data.get('type') == 'sub':
                        total_percent_sum += node_percentages.get(descendant_id, 0); sub_node_count += 1
                        for child_id in child_map.get(descendant_id, []):
                            if child_id not in visited_in_calc: queue.append(child_id)
                    elif descendant_node_data.get('type') != 'main':
                         for child_id in child_map.get(descendant_id, []):
                            if child_id not in visited_in_calc: queue.append(child_id)
                node_percentages[node_id] = round(total_percent_sum / sub_node_count) if sub_node_count else 0


        # --- 2. Determine user-specific unlocked status iteratively ---
        unlocked_map = {"Start": True}
        changed_in_pass = True
        max_passes = len(static_node_map) + 1
        current_pass = 0

        while changed_in_pass and current_pass < max_passes:
             # ... (Unlock logic from previous step, using node_percentages map) ...
            changed_in_pass = False; current_pass += 1
            for node_id, node_data in static_node_map.items():
                if node_id == "Start": continue
                current_status = unlocked_map.get(node_id, False); new_status = False
                node_type = node_data.get('type')

                if node_type == 'main':
                    prereqs_fully_met = True
                    node_prereqs = prereq_map.get(node_id, [])
                    if not node_prereqs: prereqs_fully_met = unlocked_map.get("Start", False)
                    else:
                        for prereq_id in node_prereqs:
                            if not unlocked_map.get(prereq_id, False) or node_percentages.get(prereq_id, 0) < UNLOCK_PERCENT:
                                prereqs_fully_met = False; break
                    new_status = prereqs_fully_met
                elif node_type == 'sub':
                    parents_unlocked = False
                    direct_parent_ids = node_parents.get(node_id, [])
                    if direct_parent_ids: parents_unlocked = any(unlocked_map.get(p_id, False) for p_id in direct_parent_ids)

                    prereqs_ok_for_sub = True
                    node_prereqs = prereq_map.get(node_id, [])
                    if node_prereqs:
                         for prereq_id in node_prereqs:
                            if not unlocked_map.get(prereq_id, False): prereqs_ok_for_sub = False; break
                    new_status = parents_unlocked and prereqs_ok_for_sub

                if new_status != current_status: unlocked_map[node_id] = new_status; changed_in_pass = True
            # Check for stabilization failure
            if current_pass == max_passes and changed_in_pass: print(f"Warning: User {user_id} unlock status did not stabilize.")


        # --- 3. Determine user-specific discovered status ---
        # Use the provided static_links_list (contains all relationship types)
        discovered_ids = compute_discovered_nodes(unlocked_map, static_links_list)

        # --- 4. Prepare & execute DB updates for node status ---
        node_status_updates = {}
        for node_id in static_node_map:
            if node_id == "Start": continue

            current_db_status = user_node_status_map.get(node_id) # Use map passed as arg
            new_percent = node_percentages.get(node_id, 0)
            new_unlocked = unlocked_map.get(node_id, False)
            new_discovered = node_id in discovered_ids

            # Check if an update is needed compared to the status fetched at the start
            needs_update = False
            if not current_db_status: needs_update = True
            elif (current_db_status.percent_complete != new_percent or
                  current_db_status.unlocked != new_unlocked or
                  current_db_status.discovered != new_discovered):
                  needs_update = True

            if needs_update:
                 node_status_updates[node_id] = {
                    'percent_complete': new_percent,
                    'unlocked': new_unlocked,
                    'discovered': new_discovered
                 }

        # Bulk update user node status in DB if changes occurred
        if node_status_updates:
             print(f"Updating node statuses for user {user_id}: {node_status_updates}")
             update_success = core_data.update_user_node_status_bulk(user_id, node_status_updates)
             if not update_success:
                 print(f"ERROR: Failed to update node statuses for user {user_id}")
             # Refresh user_node_status_map locally *after* update for consistent return value
             # This requires another DB call, alternatively update the local map directly
             user_node_status_map, _ = core_data.get_user_progress(user_id, graph_id)


        # --- 5. Format the final state for the frontend ---
        final_nodes = []
        final_links = [] # Links based only on CHILD relationships for graph drawing

        # Use the static_nodes_list passed in, includes exercise structure
        all_nodes_to_process = list(static_nodes_list)
        all_nodes_to_process.append(static_node_map["Start"]) # Add Start node

        for node_data in all_nodes_to_process:
            node_id = node_data['id']
            user_status = user_node_status_map.get(node_id) # Use potentially updated map

            # Node status values from computed maps/sets or defaults
            percent = node_percentages.get(node_id, 0) if node_id != "Start" else 100
            notes = user_status.user_notes if user_status else ''
            is_unlocked = unlocked_map.get(node_id, False)
            is_discovered = node_id in discovered_ids

            final_node = {
                'id': node_id, 'title': node_data['title'], 'type': node_data.get('type','sub'),
                'percent': percent,
                'unlocked': is_unlocked,     # Include computed unlock status
                'discovered': is_discovered, # Include computed discovered status
                'popup': {
                    'text': node_data.get('popup',{}).get('text',''),
                    'pdf_link': node_data.get('popup',{}).get('pdf_link',''),
                    'userNotes': notes,
                    'exercises': [ # Add user completion status
                        {**ex, 'completed': ex['id'] in completed_exercise_ids}
                        for ex in node_data.get('popup', {}).get('exercises', [])
                    ]
                }
            }
            final_nodes.append(final_node)

        # Format links for d3 (only CHILD type) using provided static_links_list
        for link in static_links_list:
            if link['type'] == 'CHILD':
                final_links.append({'source': link['source'], 'target': link['target']})

        # Add links from Start (ensure root node calculation is robust if needed)
        root_nodes = {n['id'] for n in static_nodes_list if not node_parents.get(n['id']) and not prereq_map.get(n['id'])}
        for root_id in root_nodes: final_links.append({'source': 'Start', 'target': root_id})
        final_links = [dict(t) for t in {tuple(d.items()) for d in final_links}] # De-duplicate


        return final_nodes, final_links, unlocked_map, discovered_ids

    except Exception as e:
        print(f"Error computing user graph state for user {user_id}, graph {graph_id}: {e}")
        db.session.rollback()
        return [], [], {"Start": True}, {"Start"} # Return default empty state


# --- compute_abilities (Refactored Version) ---
def compute_abilities(user_id, completed_exercise_ids, user_ctf_completions, exercises_with_cats):
    """Computes ability scores based *only* on provided arguments."""
    try:
        abilities = collections.defaultdict(int)
        # Use PASSED-IN exercises_with_cats
        for ex in exercises_with_cats:
            if ex.id in completed_exercise_ids and not ex.optional:
                for cat in ex.categories: # Assumes categories were eager-loaded
                    abilities[cat.name] += 1

        # Use PASSED-IN user_ctf_completions
        abilities["CTFs"] = sum(user_ctf_completions.values())
        return dict(abilities)
    except Exception as e:
        print(f"Error computing abilities for user {user_id} (using passed data): {e}")
        return {"CTFs": 0}


# --- compute_discovered_nodes (Remains the same) ---
def compute_discovered_nodes(unlocked_map, links_list_of_dicts):
    """
    Determines all nodes reachable from the initially unlocked set.
    """
    # ... (Implementation from previous step) ...
    discovered = set(node_id for node_id, is_unlocked in unlocked_map.items() if is_unlocked)
    nodes_to_process = collections.deque(discovered)
    processed = set()
    adj = collections.defaultdict(list)
    for link in links_list_of_dicts:
        if link['type'] == 'CHILD':
            adj[link['source']].append(link['target'])
            adj[link['target']].append(link['source'])
    while nodes_to_process:
        current_node = nodes_to_process.popleft()
        if current_node in processed: continue
        processed.add(current_node)
        for neighbor in adj.get(current_node, []):
            if neighbor not in discovered:
                discovered.add(neighbor)
                nodes_to_process.append(neighbor)
    # Add nodes that are prerequisites OF discovered nodes
    nodes_to_check_prereqs = set(discovered)
    for node_id in nodes_to_check_prereqs:
        for link in links_list_of_dicts:
            if link['type'] == 'PREREQUISITE' and link['target'] == node_id:
                if link['source'] not in discovered: discovered.add(link['source'])
    return discovered