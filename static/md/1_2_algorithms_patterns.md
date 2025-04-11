## Subtopic 1.2: Key Algorithms & Problem-Solving Patterns

**Goal:** To implement fundamental algorithms like sorting and searching, understand recursion, perform graph traversals, and apply common problem-solving patterns (Two Pointers, Sliding Window) often required in coding interviews.

**Resources:**

  * Sorting Algorithms Visualized: [VisuAlgo - Sorting](https://visualgo.net/en/sorting)
  * Binary Search: Python [`bisect` module](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/bisect.html%5D\(https://docs.python.org/3/library/bisect.html\))
  * Recursion Explained: [GeeksforGeeks - Recursion](https://www.geeksforgeeks.org/recursion/)
  * Graph Traversal (BFS/DFS): [GeeksforGeeks - BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/), [GeeksforGeeks - DFS](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)
  * Two Pointers Technique: [LeetCode Explore Card - Two Pointers](https://www.google.com/search?q=https://leetcode.com/explore/learn/card/leetcodes-interview-crash-course-data-structures-and-algorithms/703/arraystrings/4501/) (Requires LeetCode account, or search for tutorials)
  * Sliding Window Technique: [GeeksforGeeks - Sliding Window](https://www.geeksforgeeks.org/window-sliding-technique/)

-----

### Exercise 1: Implement Binary Search

**Goal:** Implement the binary search algorithm and understand its prerequisites and complexity.
**Instructions:**

1.  Implement a function `binary_search(sorted_list, target)` that returns the index of `target` in `sorted_list` if found, otherwise returns -1.
2.  Do **not** use Python's built-in `bisect` module for the core logic (implement it manually using loops or recursion).
3.  Clearly state the prerequisite for the input list for binary search to work correctly.
4.  Analyze the time complexity (Big O) of your binary search implementation.
5.  Test your function with various cases (target present, target absent, target at boundaries).

### Exercise 2: Recursive Factorial Calculation

**Goal:** Implement a classic recursive function and identify its base case and recursive step.
**Instructions:**

1.  Implement a function `recursive_factorial(n)` that calculates the factorial of a non-negative integer `n` using recursion.
2.  Identify and clearly comment on the **base case** within your function.
3.  Identify and clearly comment on the **recursive step** within your function.
4.  Trace the execution flow for `recursive_factorial(4)`.
5.  Discuss the potential risk associated with deep recursion (e.g., stack overflow).

### Exercise 3: Graph Traversal - Breadth-First Search (BFS)

**Goal:** Implement BFS to traverse a graph represented by an adjacency list.
**Instructions:**

1.  Use the adjacency list graph representation from Subtopic 1.1 (Exercise 6) or create a similar one.
2.  Implement a function `bfs(graph, start_node)` that performs a BFS traversal starting from `start_node`.
3.  The function should return a list of nodes in the order they were visited.
4.  Use a queue (e.g., `collections.deque`) to manage the nodes to visit.
5.  Keep track of visited nodes to avoid cycles and redundant processing.
6.  Analyze the time complexity of BFS in terms of V (vertices) and E (edges).

### Exercise 4: Graph Traversal - Depth-First Search (DFS)

**Goal:** Implement DFS recursively to traverse a graph represented by an adjacency list.
**Instructions:**

1.  Use the same adjacency list graph representation as in the BFS exercise.
2.  Implement a function `dfs(graph, start_node)` that performs a DFS traversal starting from `start_node`. You can implement this recursively.
3.  The function should return a list of nodes in the order they were visited (pre-order DFS).
4.  Keep track of visited nodes to avoid cycles.
5.  Analyze the time complexity of DFS in terms of V (vertices) and E (edges).
    **Challenge:** Implement an iterative version of DFS using a stack.

### Exercise 5: Two Pointers - Check for Pair Sum

**Goal:** Apply the Two Pointers technique to efficiently find if a pair sums to a target value in a sorted array.
**Instructions:**

1.  Implement a function `has_pair_with_sum(sorted_arr, target_sum)` that takes a **sorted** array of integers and a target sum.
2.  The function should return `True` if there exists any pair of distinct elements in the array that add up to `target_sum`, and `False` otherwise.
3.  Use the Two Pointers technique (one pointer starting at the beginning, one at the end) to solve this efficiently.
4.  Analyze the time complexity of your solution. Explain why sorting is crucial for this approach.

### Exercise 6: Sliding Window - Maximum Sum Subarray of Size K

**Goal:** Apply the Sliding Window technique to find the maximum sum of a subarray of a fixed size.
**Instructions:**

1.  Implement a function `max_subarray_sum(arr, k)` that takes an array of integers `arr` and an integer `k`.
2.  The function should find the maximum sum of any contiguous subarray of size `k`.
3.  Use the Sliding Window technique to achieve a time complexity better than O(N\*k).
4.  Initialize the window sum, then slide the window one element at a time, updating the sum efficiently.
5.  Analyze the time complexity of your sliding window solution.