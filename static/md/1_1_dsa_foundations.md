## Subtopic 1.1: Foundational DS\&A for Coding Interviews

**Goal:** To implement and analyze the performance characteristics of core data structures frequently encountered in coding interviews, including arrays (dynamic arrays/lists in Python), strings, hash maps (dictionaries), linked lists, and basic trees/graphs, focusing on understanding their time and space complexity using Big O notation.

**Resources:**

  * Python Official Documentation: [Data Structures (Lists, Dictionaries, etc.)](https://docs.python.org/3/tutorial/datastructures.html)
  * Python Official Documentation: [`collections` module (e.g., `defaultdict`, `deque`)](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/collections.html%5D\(https://docs.python.org/3/library/collections.html\))
  * Big O Notation Explained: [Big O Cheatsheet](https://www.bigocheatsheet.com/)
  * Tutorial on Data Structures: [GeeksforGeeks Data Structures](https://www.geeksforgeeks.org/data-structures/) (Use specific pages for each structure)
  * Book (Conceptual): "Grokking Algorithms" by Aditya Bhargava (Chapters on Arrays, Linked Lists, Hash Tables, Big O)

-----

### Exercise 1: Dynamic Array/List Operations & Complexity

**Goal:** Implement common list operations and analyze their time complexity.
**Instructions:**

1.  Create a Python list.
2.  Implement functions to:
      * Append an element to the end.
      * Insert an element at the beginning.
      * Access an element by index.
      * Remove an element from the end.
      * Remove an element from the beginning.
3.  For each function, determine and document the average-case time complexity using Big O notation, explaining *why* (consider Python's list implementation as a dynamic array).
4.  Measure the execution time (using `timeit` module) for appending 10,000 elements vs inserting 10,000 elements at the beginning. Compare the results with your complexity analysis.

### Exercise 2: Hash Map (Dictionary) Usage and Collision Handling

**Goal:** Utilize Python dictionaries for common tasks and understand the conceptual basis of hash collisions.
**Instructions:**

1.  Given a list of words, use a Python dictionary (`dict`) to count the frequency of each word.
2.  Implement a function `find_duplicates(nums)` that returns a list of numbers appearing more than once in an input list `nums`, using a dictionary for tracking counts. Analyze its time and space complexity.
3.  Explain conceptually (no implementation needed) what a hash collision is and describe one common strategy for resolving collisions (e.g., chaining or open addressing).
4.  Use `collections.defaultdict(int)` to reimplement the word frequency counter from step 1 and compare its conciseness.

### Exercise 3: Linked List Implementation (Singly Linked)

**Goal:** Implement a basic singly linked list data structure from scratch.
**Instructions:**

1.  Define a `Node` class with `data` and `next` attributes.
2.  Define a `SinglyLinkedList` class.
3.  Implement the following methods within `SinglyLinkedList`:
      * `append(data)`: Adds a node to the end.
      * `prepend(data)`: Adds a node to the beginning.
      * `find(data)`: Returns the first node containing the given data, or `None`.
      * `delete(data)`: Removes the first node containing the given data.
      * `__str__()`: Returns a string representation of the list (e.g., "A -\> B -\> C").
4.  Analyze the time complexity (Big O) of each implemented method.

### Exercise 4: String Manipulation and Immutability

**Goal:** Perform common string operations efficiently and understand string immutability in Python.
**Instructions:**

1.  Implement a function `is_palindrome(s)` that checks if a string `s` is a palindrome (reads the same forwards and backwards), ignoring case and non-alphanumeric characters. Optimize for efficiency.
2.  Explain why strings are immutable in Python.
3.  Describe the potential inefficiency of concatenating strings using the `+` operator in a loop (e.g., building a long string piece by piece).
4.  Demonstrate the preferred way to build a string from multiple parts in Python (e.g., using `"".join()`). Analyze the time complexity difference compared to loop concatenation.

### Exercise 5: Basic Tree Traversal (Conceptual Binary Tree)

**Goal:** Understand and implement basic tree traversal algorithms (Pre-order, In-order, Post-order) for a binary tree.
**Instructions:**

1.  Assume a simple `TreeNode` class exists with `value`, `left` (child), and `right` (child) attributes. You don't need to implement the full tree structure, just the traversal logic.
2.  Implement recursive functions for:
      * `pre_order_traversal(node)`
      * `in_order_traversal(node)`
      * `post_order_traversal(node)`
3.  Each function should print the `value` of the node when visited according to the traversal order.
4.  Given a simple example binary tree structure (you can define it manually with nested `TreeNode` objects), trace the output of each traversal function.

### Exercise 6: Representing Graphs (Adjacency List)

**Goal:** Represent a graph data structure using an adjacency list in Python.
**Instructions:**

1.  Choose a simple, undirected graph with 4-5 nodes and a few edges (draw it out).
2.  Represent this graph using a Python dictionary where keys are nodes and values are lists of their neighbors (adjacency list).
3.  Implement a function `add_edge(graph, u, v)` that adds an edge between nodes `u` and `v` in the adjacency list representation (remembering it's undirected).
4.  Implement a function `get_neighbors(graph, node)` that returns the list of neighbors for a given node.
5.  Discuss the space complexity of the adjacency list representation in terms of V (vertices) and E (edges).
