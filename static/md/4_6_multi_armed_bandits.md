
## Subtopic 4.6: Multi-Armed Bandits (MAB) for Optimization

**Goal:** To understand the explore-exploit dilemma in sequential decision-making and implement simple Multi-Armed Bandit algorithms like Epsilon-Greedy and Upper Confidence Bound (UCB) to balance exploration and exploitation.

**Resources:**

  * MAB Introduction:
      * Book Chapter: "Reinforcement Learning: An Introduction" by Sutton and Barto - Chapter 2: Multi-armed Bandits (Available online)
      * Blog Post/Tutorial: [Introduction to Multi-Armed Bandits](https://www.google.com/search?q=https://towardsdatascience.com/multi-armed-bandits-an-introduction-and-simple-python-implementation-954f069f278a)
  * Algorithms:
      * Epsilon-Greedy: Explanation and pseudo-code.
      * UCB: Explanation (e.g., UCB1 algorithm) and pseudo-code.
  * Regret Analysis (Conceptual): Understanding how cumulative regret measures MAB performance.

-----

### Exercise 1: The Explore-Exploit Dilemma

**Goal:** Explain the fundamental trade-off faced by Multi-Armed Bandit algorithms.
**Instructions:**

1.  Describe the "Multi-Armed Bandit" problem setup. What are the "arms"? What action does the agent take at each step? What feedback (reward) does the agent receive? What is the overall goal? (Hint: Maximize cumulative reward over time).
2.  Define **Exploitation**. What does it mean for the agent to exploit its current knowledge?
3.  Define **Exploration**. What does it mean for the agent to explore? Why is exploration necessary?
4.  Explain the **Explore-Exploit Dilemma**. Why can't the agent simply always exploit the arm that looks best so far? Why can't it always explore randomly? What is the challenge?

### Exercise 2: Implement the Epsilon-Greedy Algorithm

**Goal:** Implement the simple Epsilon-Greedy strategy for balancing exploration and exploitation.
**Instructions:**

1.  Describe the **Epsilon-Greedy** algorithm:
      * How does it choose an arm to pull at each step?
      * What role does the parameter **epsilon (ε)** play (typically a value between 0 and 1)?
      * How does the algorithm learn (update its estimates of arm values)? (Hint: Typically uses sample averages).
2.  Write a Python function `epsilon_greedy(arm_values, epsilon)` that simulates one step of the algorithm. It should:
      * Take a list/array `arm_values` (current estimated value for each arm) and `epsilon` as input.
      * Generate a random number.
      * With probability `epsilon`, choose a random arm (explore).
      * With probability `1 - epsilon`, choose the arm with the highest current estimated value (exploit - handle ties, e.g., randomly).
      * Return the index of the chosen arm.
3.  Write a simple simulation loop:
      * Define true probabilities for several simulated "arms" (e.g., Bernoulli bandits where each arm `i` returns reward 1 with probability `p_i` and 0 otherwise).
      * Initialize estimated values (`Q`) and pull counts (`N`) for each arm to zero.
      * Loop for a fixed number of steps (e.g., 1000).
      * In each step, choose an arm using your `epsilon_greedy` function (with a fixed `epsilon`, e.g., 0.1).
      * Simulate pulling the chosen arm (get a reward based on its true probability).
      * Update the pull count (`N`) and the estimated value (`Q`) for the chosen arm using the sample average method: `Q[arm] = Q[arm] + (reward - Q[arm]) / N[arm]`.
4.  After the loop, print the final estimated values (`Q`) and compare them to the true probabilities (`p_i`).

### Exercise 3: Implement the UCB1 Algorithm

**Goal:** Implement the Upper Confidence Bound (UCB) algorithm, which uses uncertainty estimates to guide exploration.
**Instructions:**

1.  Describe the core idea behind the **Upper Confidence Bound (UCB)** strategy. How does it balance exploration and exploitation? (Hint: It favors arms that have high estimated value *and/or* high uncertainty/haven't been pulled often).
2.  Write down the formula for the UCB1 selection criterion at time step `t`: Choose arm `a` that maximizes `Q_t(a) + c * sqrt(ln(t) / N_t(a))`.
      * Define `Q_t(a)` (estimated value of arm `a` at time `t`).
      * Define `N_t(a)` (number of times arm `a` has been pulled up to time `t`).
      * Define `t` (current time step/total pulls so far).
      * Explain the role of the exploration parameter `c`. What happens if `c` is large vs. small?
3.  Write a Python function `ucb1(Q_values, N_counts, t, c)` that simulates one step of UCB1. It should:
      * Take current value estimates `Q_values`, pull counts `N_counts`, the current step `t` (starting from 1), and parameter `c` (e.g., `c=2`) as input.
      * Handle the initial steps where some `N_counts` might be 0 (e.g., pull each arm once initially).
      * Calculate the UCB score for each arm using the formula.
      * Return the index of the arm with the highest UCB score.
4.  Modify your simulation loop from Exercise 2 to use the `ucb1` function instead of `epsilon_greedy`. Run the simulation and compare the final estimated values to the true probabilities.

### Exercise 4: Comparing Algorithm Performance (Regret)

**Goal:** Understand the concept of regret and compare the performance of Epsilon-Greedy and UCB through simulation.
**Instructions:**

1.  Define **Cumulative Regret**. How is it typically calculated in a bandit simulation? (Hint: Sum over time of the difference between the reward from the *optimal* arm and the reward from the *chosen* arm). What does lower cumulative regret indicate?
2.  Modify your simulation loops for both Epsilon-Greedy (using a reasonable fixed epsilon like 0.1) and UCB1 (using a reasonable c like 2).
3.  In each simulation loop, keep track of the cumulative reward obtained by the algorithm and calculate the cumulative regret at each time step `t`. Assume you know the optimal arm's expected reward (`max(p_i)`).
4.  Run both simulations several times (e.g., 10-20 runs each) for a larger number of steps (e.g., 5000) to average out randomness.
5.  Plot the *average* cumulative regret over time for both Epsilon-Greedy and UCB1 on the same graph.
6.  Analyze the plot. Which algorithm typically achieves lower cumulative regret in the long run? Explain intuitively why this might be the case based on how they handle exploration.
    **Challenge:** Implement a decaying epsilon schedule for the Epsilon-Greedy algorithm (e.g., `epsilon = 1/t` or similar) and compare its regret to fixed epsilon and UCB.

### Project: MAB Simulation and Analysis

**Goal:** Implement and compare the performance (cumulative reward and regret) of Epsilon-Greedy and UCB algorithms on a simulated multi-armed bandit problem.
**Instructions:**

1.  Set up a simulation environment in Python. Define a Bernoulli multi-armed bandit problem with a specific number of arms (e.g., 5 or 10) and define their true reward probabilities (e.g., `[0.1, 0.3, 0.8, 0.5, 0.2]`). Identify the optimal arm.
2.  Implement the Epsilon-Greedy algorithm (with a fixed epsilon, e.g., 0.1).
3.  Implement the UCB1 algorithm (with a chosen exploration parameter `c`, e.g., 2).
4.  Run multiple simulations (e.g., 100 runs) for each algorithm over a significant number of time steps (e.g., 1000 or more).
5.  For each algorithm, record:
      * Average cumulative reward over time.
      * Average cumulative regret over time.
      * (Optional) Percentage of times the optimal arm was chosen over time.
6.  Plot the average cumulative reward and average cumulative regret curves for both algorithms on separate graphs.
    **Portfolio Guidance:**

  * Structure your code clearly in a Python script or Jupyter Notebook.
  * Define the bandit problem parameters clearly.
  * Include the implementations of Epsilon-Greedy and UCB1.
  * Show the plots comparing the performance metrics (reward, regret).
  * Add a discussion interpreting the plots and explaining the observed performance differences between the algorithms based on their exploration/exploitation strategies.
  * Mention any parameter tuning experiments (e.g., different epsilon or c values) if performed.
  * Upload the code/notebook and README to GitHub.

