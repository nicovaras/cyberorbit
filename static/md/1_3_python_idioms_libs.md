## Subtopic 1.3: Python Idioms & Libraries for Interviews

**Goal:** To effectively use Python's idiomatic constructs (comprehensions, generators, lambdas) and leverage key standard libraries (`collections`, `itertools`, `heapq`) to write concise, efficient, and readable code typical of successful coding interview solutions.

**Resources:**

  * Python Official Documentation: [List Comprehensions](https://www.google.com/search?q=https://docs.python.org/3/tutorial/datastructures.html%23list-comprehensions)
  * Python Official Documentation: [Generator Expressions](https://www.google.com/search?q=https://docs.python.org/3/reference/expressions.html%23generator-expressions) & [Generators (yield)](https://www.google.com/search?q=https://docs.python.org/3/glossary.html%23term-generator)
  * Python Official Documentation: [Lambda Expressions](https://www.google.com/search?q=https://docs.python.org/3/reference/expressions.html%23lambda)
  * Python Official Documentation: [`collections` module (`deque`, `Counter`, `defaultdict`)](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/collections.html%5D\(https://docs.python.org/3/library/collections.html\))
  * Python Official Documentation: [`itertools` module (`combinations`, `permutations`, `product`)](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/itertools.html%5D\(https://docs.python.org/3/library/itertools.html\))
  * Python Official Documentation: [`heapq` module (Priority Queues)](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/heapq.html%5D\(https://docs.python.org/3/library/heapq.html\))
  * Style Guide: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) (Focus on readability principles)

-----

### Exercise 1: List Comprehensions for Data Transformation

**Goal:** Use list comprehensions to create new lists based on existing iterables concisely.
**Instructions:**

1.  Given a list of numbers `nums = [1, 2, 3, 4, 5, 6]`:
      * Use a list comprehension to create a new list containing the squares of the numbers in `nums`.
      * Use a list comprehension to create a new list containing only the even numbers from `nums`.
      * Use a list comprehension to create a list of tuples `(number, square)` for each number in `nums`.
2.  Given a list of strings `words = ["apple", "banana", "cherry"]`, use a list comprehension to create a list containing the length of each word.
3.  Rewrite one of the above list comprehensions using a traditional `for` loop with `.append()` to highlight the difference in conciseness.

### Exercise 2: Generator Expressions for Memory Efficiency

**Goal:** Understand and use generator expressions for lazy evaluation and memory efficiency compared to list comprehensions.
**Instructions:**

1.  Create a list comprehension that generates the squares of numbers from 0 to 999,999.
2.  Create an equivalent generator expression for the same range.
3.  Use Python's `sys.getsizeof()` function to roughly compare the memory footprint of the resulting list object versus the generator object. Explain the difference.
4.  Implement a function `sum_of_squares(n)` that calculates the sum of squares up to `n` using a generator expression within the `sum()` function for efficiency.

### Exercise 3: Using `collections.Counter` for Frequency Analysis

**Goal:** Utilize `collections.Counter` for efficiently counting hashable objects.
**Instructions:**

1.  Given a string `text = "hello world"`, use `collections.Counter` to find the frequency of each character.
2.  Given a list of items `items = ["A", "B", "A", "C", "B", "A"]`, use `collections.Counter` to get the counts of each item.
3.  Explore and demonstrate how to use the `.most_common(n)` method of a `Counter` object.
4.  Implement a function `find_anagrams(s1, s2)` that returns `True` if strings `s1` and `s2` are anagrams (contain the same characters with the same frequencies), using `collections.Counter`.

### Exercise 4: Leveraging `collections.defaultdict`

**Goal:** Use `collections.defaultdict` to simplify code that involves grouping items or initializing default values in dictionaries.
**Instructions:**

1.  Given a list of tuples `pairs = [('a', 1), ('b', 2), ('a', 3), ('c', 4), ('b', 5)]`, use `collections.defaultdict(list)` to create a dictionary where keys are the first elements of the tuples and values are lists of the second elements associated with that key (e.g., `{'a': [1, 3], 'b': [2, 5], 'c': [4]}`).
2.  Compare the implementation using `defaultdict` with an implementation using a standard `dict` and explicit checks (`if key not in dict:`).
3.  Explain how `defaultdict` avoids `KeyError` exceptions during the first insertion for a new key.

### Exercise 5: Using `itertools` for Combinatorics

**Goal:** Apply functions from the `itertools` module for common combinatorial tasks like permutations and combinations.
**Instructions:**

1.  Given a list `elements = ['A', 'B', 'C']`:
      * Use `itertools.combinations()` to generate all unique combinations of size 2. Print the results (they will be tuples).
      * Use `itertools.permutations()` to generate all possible orderings (permutations) of the elements. Print the results.
      * Use `itertools.product()` to generate the Cartesian product of `elements` with `[1, 2]`. Print the results.
2.  Explain the difference between combinations and permutations in the context of these functions.

### Exercise 6: Implementing a Priority Queue with `heapq`

**Goal:** Use the `heapq` module to implement a min-priority queue.
**Instructions:**

1.  Import the `heapq` module.
2.  Create an empty list to represent the heap.
3.  Use `heapq.heappush()` to add the following elements (representing priorities, lower is higher priority) to the heap: `5, 3, 7, 1, 4`.
4.  Observe the internal list representation after pushes (it might not look fully sorted).
5.  Use `heapq.heappop()` repeatedly to extract elements from the heap. Print each element as it's extracted.
6.  Verify that elements are extracted in ascending order (min-heap property).
    **Challenge:** Store tuples `(priority, task_description)` in the heap and demonstrate pushing and popping while maintaining priority order based on the first element of the tuple.
