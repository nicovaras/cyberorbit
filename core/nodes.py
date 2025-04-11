# tmp/core/nodes.py
import collections
from models import db, Node, NodeRelationship, UserNodeStatus, UserExerciseCompletion, Exercise
from core import data as core_data
from core.utils import build_child_map

UNLOCK_PERCENT = 50



def compute_user_graph_state(user_id, graph_id, static_nodes_list, static_links_list, user_node_status_map, completed_exercise_ids):
    """
    Computes the complete graph state for a specific user and graph,
    using pre-fetched static data and user progress data.
    Updates user node status (percent, unlocked, discovered) in the database based on new logic.

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

        # --- Pre-computation ---
        static_node_map = {node['id']: node for node in static_nodes_list}
        static_node_map["Start"] = {"id": "Start", "type": "start", "title": "Start"} # Add Start node

        # Build relationship maps
        child_map = collections.defaultdict(list)
        prereq_map = collections.defaultdict(list)
        node_parents = collections.defaultdict(list) # Stores immediate parents based on CHILD links
        for link in static_links_list:
            if link['type'] == 'CHILD':
                child_map[link['source']].append(link['target'])
                node_parents[link['target']].append(link['source'])
            elif link['type'] == 'PREREQUISITE':
                prereq_map[link['target']].append(link['source'])

        # --- Calculate Node Percentages ---
        node_percentages = {}
        # Calculate percentages for 'sub' nodes based on exercises
        for node_id, node_data in static_node_map.items():
            if node_data.get('type') == 'sub':
                exercises = node_data.get('popup', {}).get('exercises', [])
                total_exercises = len(exercises)
                if total_exercises == 0:
                    node_percentages[node_id] = 0 # Or 100 if empty sub node means complete? Assuming 0.
                else:
                    completed_count = sum(1 for ex in exercises if ex['id'] in completed_exercise_ids)
                    node_percentages[node_id] = round((completed_count / total_exercises) * 100)

        # Calculate percentages for 'main' nodes based on descendant 'sub' nodes
        for node_id, node_data in static_node_map.items():
             if node_data.get('type') == 'main':
                total_percent_sum = 0
                sub_node_count = 0
                # Use BFS/DFS to find all descendant sub-nodes, avoiding cycles
                queue = collections.deque(child_map.get(node_id, []))
                visited_in_calc = {node_id} # Prevent infinite loops in cyclic graphs
                while queue:
                    descendant_id = queue.popleft()
                    if descendant_id in visited_in_calc: continue
                    visited_in_calc.add(descendant_id)

                    descendant_node_data = static_node_map.get(descendant_id)
                    if not descendant_node_data: continue

                    if descendant_node_data.get('type') == 'sub':
                        # Found a sub-node descendant
                        total_percent_sum += node_percentages.get(descendant_id, 0)
                        sub_node_count += 1
                        # Continue traversal from sub-nodes as well (Rule 3 dependency)
                        for child_id in child_map.get(descendant_id, []):
                           if child_id not in visited_in_calc: queue.append(child_id)
                    elif descendant_node_data.get('type') != 'main': # Traverse through other intermediate nodes if needed
                         for child_id in child_map.get(descendant_id, []):
                            if child_id not in visited_in_calc: queue.append(child_id)
                # Calculate average percentage from descendant sub-nodes
                node_percentages[node_id] = round(total_percent_sum / sub_node_count) if sub_node_count else 0


        # --- Calculate Unlocked Status (Iterative based on new rules) ---
        # This logic remains the same as the previous version which user confirmed was OK.
        unlocked_map = {"Start": True} # Start node is always unlocked
        changed_in_pass = True
        max_passes = len(static_node_map) + 2 # Allow extra passes for complex dependencies
        current_pass = 0

        while changed_in_pass and current_pass < max_passes:
            changed_in_pass = False
            current_pass += 1

            for node_id, node_data in static_node_map.items():
                if node_id == "Start": continue
                if unlocked_map.get(node_id, False): continue # Skip if already unlocked

                current_status = False
                node_type = node_data.get('type')
                parents = node_parents.get(node_id, [])
                prerequisites = prereq_map.get(node_id, [])

                prereqs_unlocked = True
                if prerequisites:
                    for prereq_id in prerequisites:
                        if not unlocked_map.get(prereq_id, False):
                            prereqs_unlocked = False
                            break
                elif not parents and not prerequisites:
                     prereqs_unlocked = unlocked_map.get("Start", False)

                if not prereqs_unlocked: continue

                potential_unlock_status = False

                if node_type == 'main':
                    if not prerequisites:
                         potential_unlock_status = True
                    else:
                         all_prereqs_sufficient_percent = True
                         for prereq_id in prerequisites:
                             prereq_percent = node_percentages.get(prereq_id, 0)
                             if prereq_percent < UNLOCK_PERCENT:
                                 all_prereqs_sufficient_percent = False
                                 break
                         potential_unlock_status = all_prereqs_sufficient_percent

                elif node_type == 'sub':
                    if not parents:
                         if not prerequisites:
                             potential_unlock_status = unlocked_map.get("Start", False)
                    else:
                        for parent_id in parents:
                            parent_node_data = static_node_map.get(parent_id)
                            if not parent_node_data: continue

                            parent_unlocked = unlocked_map.get(parent_id, False)
                            parent_type = parent_node_data.get('type')

                            if parent_type == 'main' and parent_unlocked:
                                potential_unlock_status = True; break
                            elif parent_type == 'sub':
                                parent_percent = node_percentages.get(parent_id, 0)
                                if parent_unlocked and parent_percent >= UNLOCK_PERCENT:
                                    potential_unlock_status = True; break
                            elif parent_type == 'start' and parent_unlocked:
                                potential_unlock_status = True; break

                if potential_unlock_status and not unlocked_map.get(node_id, False):
                    unlocked_map[node_id] = True
                    changed_in_pass = True
            # End of loop through nodes

        if current_pass == max_passes and changed_in_pass:
            print(f"Warning: Unlock status did not stabilize within {max_passes} passes for user {user_id}, graph {graph_id}.")


        # --- Calculate Discovered Status (Fog of War - REVISED) ---
        # Use the newly computed unlock_map
        discovered_ids = compute_discovered_nodes(unlocked_map, static_links_list, static_node_map)


        # --- Update Database ---
        # Check if any status needs updating in the DB
        node_status_updates = {}
        for node_id, node_data in static_node_map.items():
            if node_id == "Start": continue # Don't store status for pseudo-node 'Start'

            current_db_status = user_node_status_map.get(node_id) # Get from initially fetched map
            new_percent = node_percentages.get(node_id, 0)
            new_unlocked = unlocked_map.get(node_id, False)
            new_discovered = node_id in discovered_ids # Use the result from revised function

            needs_update = False
            if not current_db_status:
                 if new_percent > 0 or new_unlocked or new_discovered:
                     needs_update = True
            elif (current_db_status.percent_complete != new_percent or
                  current_db_status.unlocked != new_unlocked or
                  current_db_status.discovered != new_discovered): # Check discovered status too
                  needs_update = True

            if needs_update:
                 node_status_updates[node_id] = {
                    'percent_complete': new_percent,
                    'unlocked': new_unlocked,
                    'discovered': new_discovered
                 }

        # Perform bulk update if changes are needed
        if node_status_updates:
             print(f"Updating node statuses in DB for user {user_id}: {len(node_status_updates)} nodes")
             update_success = core_data.update_user_node_status_bulk(user_id, node_status_updates)
             if not update_success:
                 print(f"ERROR: Failed to update node statuses for user {user_id}")
             # OPTIONAL: Re-fetch user_node_status_map after update for consistency in returned data
             # user_node_status_map, _ = core_data.get_user_progress(user_id, graph_id)


        # --- Format Final Output ---
        final_nodes = []
        final_links = []

        # Add 'Start' node to the list if it's used in links
        if "Start" in static_node_map:
            final_nodes.append({
                'id': 'Start', 'title': 'Start', 'type': 'start',
                'percent': 100, 'unlocked': True, 'discovered': True, # Start is always discovered
                'popup': {'text': '', 'pdf_link': '', 'userNotes': '', 'exercises': []}
            })


        for node_data in static_nodes_list: # Iterate original list, excluding Start initially
            node_id = node_data['id']
            user_status = user_node_status_map.get(node_id)

            percent = node_percentages.get(node_id, 0)
            is_unlocked = unlocked_map.get(node_id, False)
            is_discovered = node_id in discovered_ids # Use result from revised function
            notes = user_status.user_notes if user_status else ''


            final_node = {
                'id': node_id, 'title': node_data['title'], 'type': node_data.get('type','sub'),
                'percent': percent,
                'unlocked': is_unlocked,
                'discovered': is_discovered, # Reflect the new discovered status
                'popup': {
                    'text': node_data.get('popup',{}).get('text',''),
                    'pdf_link': node_data.get('popup',{}).get('pdf_link',''),
                    'userNotes': notes,
                    'exercises': [
                        {**ex, 'completed': ex['id'] in completed_exercise_ids}
                        for ex in node_data.get('popup', {}).get('exercises', [])
                    ]
                }
            }
            final_nodes.append(final_node)

        # Format links (only CHILD relationships for the graph visualization)
        for link in static_links_list:
             if link['type'] == 'CHILD':
                 # Optional: Only include links where BOTH source and target are discovered?
                 # if link['source'] in discovered_ids and link['target'] in discovered_ids:
                 final_links.append({'source': link['source'], 'target': link['target']})

        # Add links from Start to root nodes
        root_nodes = {n['id'] for n in static_nodes_list if not node_parents.get(n['id']) and not prereq_map.get(n['id'])}
        for root_id in root_nodes:
            # Optional: Only link Start to discovered root nodes?
            # if root_id in discovered_ids:
            final_links.append({'source': 'Start', 'target': root_id})

        # Remove duplicate links
        final_links = [dict(t) for t in {tuple(sorted(d.items())) for d in final_links}]

        # for testing...
        if user_id == 1:
            for n in final_nodes:
                unlocked_map[n['id']] = True
                discovered_ids.add(n['id'])
        return final_nodes, final_links, unlocked_map, discovered_ids

    except Exception as e:
        print(f"FATAL Error computing user graph state for user {user_id}, graph {graph_id}: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return [], [], {"Start": True}, {"Start"}



def compute_abilities(user_id, completed_exercise_ids, user_ctf_completions, exercises_with_cats):
    """Computes ability scores based *only* on provided arguments."""
    # This function remains unchanged.
    try:
        abilities = collections.defaultdict(int)
        for ex in exercises_with_cats:
            if ex.id in completed_exercise_ids and not ex.optional:
                for cat in ex.categories:
                    abilities[cat.name] += 1
        abilities["CTFs"] = sum(user_ctf_completions.values())
        return dict(abilities)
    except Exception as e:
        print(f"Error computing abilities for user {user_id} (using passed data): {e}")
        return {"CTFs": 0}



def compute_discovered_nodes(unlocked_map, links_list_of_dicts, static_node_map):
    """
    Determines discovered nodes based on Fog of War logic for a tree structure:
    Starts with unlocked nodes. Explores via CHILD links, but STOPS exploration
    down a path if it encounters a locked node.
    """
    discovered = set()
    nodes_to_process = collections.deque()

    # Initialize discovered set ONLY with currently unlocked nodes.
    # These are the only nodes initially visible.
    for node_id, is_unlocked in unlocked_map.items():
        # Ensure the node actually exists in the graph data we have
        if is_unlocked and node_id in static_node_map:
            if node_id not in discovered:
                discovered.add(node_id)
                # Add these initially discovered (unlocked) nodes to start the traversal.
                nodes_to_process.append(node_id)

    # Build adjacency list ONLY for CHILD links (both directions needed for traversal)
    # Since it's a tree (mostly), target -> source might represent the parent link visually.
    adj = collections.defaultdict(list)
    for link in links_list_of_dicts:
        source, target = link.get('source'), link.get('target')
        link_type = link.get('type')
        # Only consider CHILD links for discovery spread
        # Ensure both source and target nodes are valid before adding edge
        if link_type == 'CHILD' and source in static_node_map and target in static_node_map:
             adj[source].append(target)
             # For tree traversal, we need to go parent -> child and child -> parent along the CHILD link type
             adj[target].append(source)

    # --- BFS Traversal - STOPS at Locked Nodes ---
    # Use 'processed' set to keep track of nodes already added to the queue, preventing cycles (though less likely in a tree) and redundant work.
    processed = set(discovered) # Initialize with the starting unlocked nodes

    while nodes_to_process:
        current_node_id = nodes_to_process.popleft()

        # Explore neighbors via CHILD links
        for neighbor_id in adj.get(current_node_id, []):
            # CRUCIAL CHECK: Is the neighbor UNLOCKED?
            is_neighbor_unlocked = unlocked_map.get(neighbor_id, False)

            # Check if neighbor exists in our map (sanity check)
            if neighbor_id not in static_node_map: continue

            # Only proceed if the neighbor is UNLOCKED and not already processed/queued
            if is_neighbor_unlocked and neighbor_id not in processed:
                discovered.add(neighbor_id) # Discover the unlocked neighbor
                processed.add(neighbor_id)   # Mark as processed (i.e., added to queue)
                nodes_to_process.append(neighbor_id) # Add to queue to explore *its* neighbors

            # If neighbor is LOCKED or already processed, WE DO NOTHING.
            # The traversal down this path stops here.

    # Ensure Start is always discovered (it should be added initially if unlocked)
    if "Start" in static_node_map:
         discovered.add("Start")

    return discovered