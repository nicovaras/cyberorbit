# cyberorbit/core/nodes.py
import collections
from models import db, Node, NodeRelationship, UserNodeStatus, UserExerciseCompletion, Exercise, Ctf, UserCtfCompletion # Import necessary models
from core import data as core_data # Use functions from refactored core/data.py
from core import ctfs as core_ctfs # Use functions from refactored core/ctfs.py
from core.utils import build_child_map # Keep utility if still needed
from core.data import get_cached_static_graph_data # Use function from refactored core/data.py
from sqlalchemy.orm import joinedload, selectinload # Add selectinload


UNLOCK_PERCENT = 50

# --- User-Specific State Computation ---

def compute_user_graph_state(user_id, graph_id):
    """
    Computes the complete graph state for a specific user and graph,
    including node percentages, unlocked status, and discovered status,
    fetching data from the database.
    """
    try:
        # 1. Fetch static graph structure and user progress
        static_nodes_list, static_links_list = get_cached_static_graph_data(graph_id)
        user_node_status_map, user_completed_exercise_ids = core_data.get_user_progress(user_id, graph_id)

        if not static_nodes_list:
            print(f"Warning: No static nodes found for graph_id {graph_id}")
            return {}, [], {}, set() # Return empty state

        # Build helper maps from static data
        static_node_map = {node['id']: node for node in static_nodes_list}
        # Build parent/prereq maps from relationships
        child_map = collections.defaultdict(list)
        prereq_map = collections.defaultdict(list)
        node_parents = collections.defaultdict(list) # node_id -> list of parent_ids
        for link in static_links_list:
            if link['type'] == 'CHILD':
                child_map[link['source']].append(link['target'])
                node_parents[link['target']].append(link['source'])
            elif link['type'] == 'PREREQUISITE':
                # Store as target_node -> list of prerequisite_nodes
                prereq_map[link['target']].append(link['source'])

        # Add Start node conceptually for calculations
        static_node_map["Start"] = {"id": "Start", "type": "start", "title": "Start"}
        user_node_status_map["Start"] = UserNodeStatus(unlocked=True, discovered=True, percent_complete=100) # Treat Start as always complete/unlocked/discovered


        # 2. Calculate user-specific percentages for each node
        node_percentages = {} # node_id -> calculated percentage for this user

        # Calculate sub-node percentages first
        for node_id, node_data in static_node_map.items():
            if node_data['type'] == 'sub':
                exercises = node_data.get('popup', {}).get('exercises', [])
                total_exercises = len(exercises)
                if total_exercises == 0:
                    node_percentages[node_id] = 0
                else:
                    completed_count = sum(1 for ex in exercises if ex['id'] in user_completed_exercise_ids)
                    node_percentages[node_id] = round((completed_count / total_exercises) * 100)

        # Calculate main-node percentages (BFS based on *user-specific* sub-node percentages)
        for node_id, node_data in static_node_map.items():
             if node_data['type'] == 'main':
                total_percent_sum = 0
                sub_node_count = 0
                queue = collections.deque(child_map.get(node_id, []))
                visited_in_calc = {node_id} # Prevent cycles within percentage calc

                while queue:
                    descendant_id = queue.popleft()
                    if descendant_id in visited_in_calc: continue
                    visited_in_calc.add(descendant_id)

                    descendant_node_data = static_node_map.get(descendant_id)
                    if not descendant_node_data: continue

                    if descendant_node_data['type'] == 'sub':
                        # Use the user-specific percentage calculated above
                        total_percent_sum += node_percentages.get(descendant_id, 0)
                        sub_node_count += 1
                        # Continue traversal from sub-nodes
                        for child_id in child_map.get(descendant_id, []):
                            if child_id not in visited_in_calc: queue.append(child_id)
                    elif descendant_node_data['type'] == 'main':
                         # Stop traversal at the next main node for percentage calculation
                        continue
                    else: # Start or other types? Continue traversal if needed
                         for child_id in child_map.get(descendant_id, []):
                            if child_id not in visited_in_calc: queue.append(child_id)

                # Average the percentages of the descendant sub-nodes found
                node_percentages[node_id] = round(total_percent_sum / sub_node_count) if sub_node_count else 0

        # 3. Determine user-specific unlocked status iteratively
        unlocked_map = {"Start": True} # node_id -> bool
        changed_in_pass = True
        max_passes = len(static_node_map) + 1
        current_pass = 0

        while changed_in_pass and current_pass < max_passes:
            changed_in_pass = False
            current_pass += 1

            for node_id, node_data in static_node_map.items():
                if node_id == "Start": continue

                current_status = unlocked_map.get(node_id, False)
                # Default to locked unless proven otherwise
                new_status = False

                # --- Logic based on original description ---
                if node_data['type'] == 'main':
                    # Main nodes unlock ONLY if all prerequisites are unlocked AND meet percentage.
                    prereqs_fully_met = True
                    node_prereqs = prereq_map.get(node_id, [])
                    if not node_prereqs: # If no prereqs (should link to Start)
                        prereqs_fully_met = unlocked_map.get("Start", False) # Depends only on Start
                    else:
                        for prereq_id in node_prereqs:
                            prereq_unlocked = unlocked_map.get(prereq_id, False)
                            # Fetch percent calculated earlier for this user
                            prereq_percent = node_percentages.get(prereq_id, 0)
                            if not prereq_unlocked or prereq_percent < UNLOCK_PERCENT:
                                prereqs_fully_met = False
                                break
                    new_status = prereqs_fully_met

                elif node_data['type'] == 'sub':
                    # Sub-nodes unlock if parent is unlocked AND all prerequisites are met
                    # (ignoring % for direct main parent prereq - simplified here: ALL prereqs must be met generally).
                    # Let's first check if *any* parent is unlocked.
                    parents_unlocked = False
                    direct_parent_ids = node_parents.get(node_id, [])
                    if not direct_parent_ids: # Should not happen for sub-nodes usually
                        parents_unlocked = False
                    else:
                        parents_unlocked = any(unlocked_map.get(p_id, False) for p_id in direct_parent_ids)

                    # Then check if *all* prerequisites are met (basic unlocked check here, % check implicitly handled by prereqs needing unlock first)
                    prereqs_ok_for_sub = True
                    node_prereqs = prereq_map.get(node_id, [])
                    if node_prereqs:
                         for prereq_id in node_prereqs:
                            if not unlocked_map.get(prereq_id, False):
                                 prereqs_ok_for_sub = False
                                 break

                    new_status = parents_unlocked and prereqs_ok_for_sub

                # --- End Logic based on original description ---

                # Update status if changed
                if new_status != current_status:
                    unlocked_map[node_id] = new_status
                    changed_in_pass = True

            if current_pass == max_passes and changed_in_pass:
                print(f"Warning: User {user_id} unlock status did not stabilize.")

        # 4. Determine user-specific discovered status
        discovered_ids = compute_discovered_nodes(unlocked_map, static_links_list)


        # 5. Prepare data for DB update
        node_status_updates = {}
        for node_id in static_node_map:
            if node_id == "Start": continue # Don't save Start node status

            current_db_status = user_node_status_map.get(node_id)
            new_percent = node_percentages.get(node_id, 0)
            new_unlocked = unlocked_map.get(node_id, False)
            new_discovered = node_id in discovered_ids

            # Check if an update is needed
            needs_update = False
            if not current_db_status:
                needs_update = True
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

        # 6. Bulk update user node status in DB if changes occurred
        if node_status_updates:
             print(f"Updating node statuses for user {user_id}: {node_status_updates}")
             core_data.update_user_node_status_bulk(user_id, node_status_updates)
             # Refresh user_node_status_map after update
             user_node_status_map, _ = core_data.get_user_progress(user_id, graph_id)


        # 7. Format the final state for the frontend
        final_nodes = []
        final_links = [] # Links based only on CHILD relationships for graph drawing

        for node_data in static_nodes_list: # Iterate original list to preserve order somewhat
            node_id = node_data['id']
            user_status = user_node_status_map.get(node_id)

            final_node = {
                'id': node_id,
                'title': node_data['title'],
                'type': node_data['type'],
                'percent': user_status.percent_complete if user_status else 0,
                'popup': {
                    'text': node_data.get('popup',{}).get('text',''),
                    'pdf_link': node_data.get('popup',{}).get('pdf_link',''),
                    'userNotes': user_status.user_notes if user_status else '', # Include notes
                    'exercises': [ # Add completion status from user data
                        {**ex, 'completed': ex['id'] in user_completed_exercise_ids}
                        for ex in node_data.get('popup', {}).get('exercises', [])
                    ]
                }
                # Add children/prerequisites if needed by frontend, derived from static_links_list
            }
            final_nodes.append(final_node)

        # Format links for d3 (source/target)
        for link in static_links_list:
            if link['type'] == 'CHILD':
                final_links.append({'source': link['source'], 'target': link['target']})
            # Add prerequisite links if desired by frontend visualization
            # elif link['type'] == 'PREREQUISITE':
            #     final_links.append({'source': link['source'], 'target': link['target'], 'type': 'prereq'}) # Example


        # Add Start node to final output
        final_nodes.append({
             'id': 'Start', 'title': 'Start', 'type': 'start', 'percent': 100,
             'popup': {'text': 'Start.', 'exercises': []}
        })
        # Add links from Start to root nodes (nodes with no CHILD parents and no PREREQUISITEs)
        root_nodes = {n['id'] for n in static_nodes_list if not node_parents.get(n['id']) and not prereq_map.get(n['id'])}
        for root_id in root_nodes:
            final_links.append({'source': 'Start', 'target': root_id})


        return final_nodes, final_links, unlocked_map, discovered_ids

    except Exception as e:
        # Log the error appropriately
        print(f"Error computing user graph state for user {user_id}, graph {graph_id}: {e}")
        db.session.rollback() # Rollback any partial changes if an error occurred mid-process
        # Return an empty or default state
        return [], [], {"Start": True}, {"Start"}


def compute_abilities(user_id, graph_id):
    """Computes ability scores based on user's completed exercises and CTFs."""
    try:
        # Fetch user's completed exercise IDs
        _, completed_exercise_ids = core_data.get_user_progress(user_id, graph_id)

        # Fetch exercises with categories for the given graph, using selectinload
        exercises_with_cats = db.session.query(Exercise).options(
             selectinload(Exercise.categories), # Use selectinload
             # No need to load node if only using graph_id in filter
             # joinedload(Exercise.node).load_only(Node.graph_id) # Original - can simplify filter
        ).join(Node).filter( # Join with Node to filter by graph_id
            Node.graph_id == graph_id
        ).all()


        abilities = collections.defaultdict(int)
        for ex in exercises_with_cats:
            # Only count non-optional completed exercises
            if ex.id in completed_exercise_ids and not ex.optional:
                for cat in ex.categories: # Categories are loaded due to selectinload
                    abilities[cat.name] += 1

        # Fetch user's CTF completions
        user_ctf_completions = core_ctfs.get_user_ctf_completions(user_id)
        abilities["CTFs"] = sum(user_ctf_completions.values())

        return dict(abilities)
    except Exception as e:
        print(f"Error computing abilities for user {user_id}: {e}")
        return {"CTFs": 0}

def compute_discovered_nodes(unlocked_map, links):
    """
    Determines all nodes reachable from the initially unlocked set.
    :param unlocked_map: Dict {node_id: bool} indicating initially unlocked nodes.
    :param links: List of {'source': id, 'target': id} dictionaries representing connections.
    :return: Set of discovered node IDs.
    """
    discovered = set(node_id for node_id, is_unlocked in unlocked_map.items() if is_unlocked)
    nodes_to_process = collections.deque(discovered)
    processed = set() # Keep track of nodes whose neighbors we've already added

    # Build adjacency list for efficient lookup
    adj = collections.defaultdict(list)
    for link in links:
        # Ensure both directions are added if links are undirected for discovery
        adj[link['source']].append(link['target'])
        adj[link['target']].append(link['source'])

    while nodes_to_process:
        current_node = nodes_to_process.popleft()
        if current_node in processed:
            continue
        processed.add(current_node)

        for neighbor in adj.get(current_node, []):
            if neighbor not in discovered:
                discovered.add(neighbor)
                # If a node allows discovery of neighbors even if locked, add all neighbors
                # If discovery stops at locked nodes, only add if unlocked_map.get(neighbor, False):
                nodes_to_process.append(neighbor) # Add neighbor to check its neighbors later

    return discovered

# Remove old compute_node_states function if it still exists