## 倹 Subtopic 4.2: Markov Chain Monte Carlo (MCMC) Methods

**Goal:** Understand the need for sampling methods like MCMC when analytical solutions for posteriors are unavailable, grasp the core concepts of Markov chains, and implement a basic Metropolis-Hastings sampler.

**Resources:**

* **MCMC Introduction:** [Blog post explaining the basics](https://towardsdatascience.com/markov-chain-monte-carlo-in-python-44f7e40979b4)
* **Metropolis-Hastings:** [Wikipedia Article](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm)
* **Target Distributions:** Define simple distributions to sample from (e.g., mixture of Gaussians, strangely shaped distributions).
* **NumPy/SciPy:** For random number generation, probability density calculations.

---

### 隼 **Exercise 1: The Need for Sampling**

**Goal:** Understand why we often need numerical methods like MCMC to analyze posterior distributions.

**Instructions:**

1.  Recall Bayes' Theorem: `Posterior = (Likelihood * Prior) / Evidence`.
2.  Explain the role of the **Evidence** (also called Marginal Likelihood or Normalizing Constant): `Evidence = Integral over all parameters [ Likelihood(Data|Parameters) * Prior(Parameters) ]`.
3.  Describe scenarios where calculating this integral analytically is difficult or impossible:
    * Non-conjugate prior/likelihood pairs.
    * High-dimensional parameter spaces (many parameters).
    * Complex model structures.
4.  Explain how MCMC methods allow us to approximate the posterior distribution *without* explicitly calculating the evidence term. How does focusing on the *ratio* of posterior densities help (as used in Metropolis-Hastings)?
5.  **Challenge:** Consider Bayesian logistic regression. Why is the posterior distribution for the regression coefficients typically intractable analytically?

---

### 隼 **Exercise 2: Simulating a Simple Markov Chain**

**Goal:** Implement a basic discrete-state Markov chain to understand state transitions and equilibrium.

**Instructions:**

1.  Define a simple 3-state system (e.g., Weather: Sunny, Cloudy, Rainy).
2.  Define a **transition probability matrix** `P`, where `P[i, j]` is the probability of transitioning from state `i` to state `j` in one step. Ensure rows sum to 1.
    * Example `P`:
      ```
      #   Sunny Cloudy Rainy (To)
      [[0.7,  0.2,   0.1],  # Sunny (From)
       [0.3,  0.5,   0.2],  # Cloudy (From)
       [0.4,  0.4,   0.2]]  # Rainy (From)
      ```
3.  Write a Python simulation:
    * Start in an initial state (e.g., Sunny).
    * Simulate 1000 steps: In each step, determine the next state by sampling randomly according to the transition probabilities defined in the current state's row in `P` (e.g., use `np.random.choice`). Record the sequence of states visited.
4.  Calculate the proportion of time spent in each state over the 1000 steps.
5.  Calculate the **stationary distribution** `pi` of the Markov chain (the eigenvector corresponding to the eigenvalue 1 of the transpose of `P`, normalized to sum to 1). You can use `numpy.linalg.eig` or look up analytical solutions for small matrices.
6.  Compare the simulated proportions from step 4 to the calculated stationary distribution `pi` from step 5. Do they converge?
7.  **Challenge:** Run the simulation starting from different initial states. Does the chain still converge to the same stationary distribution (assuming the chain is irreducible and aperiodic)?

---

### 隼 **Exercise 3: Metropolis-Hastings Sampler (Symmetric Proposal)**

**Goal:** Implement the basic Metropolis-Hastings algorithm with a symmetric proposal distribution to sample from a known target distribution.

**Instructions:**

1.  **Target Distribution:** Choose a 1D target distribution whose density we can evaluate (proportionality is enough), but which might be hard to sample from directly. Example: A standard Normal distribution `N(0, 1)`. Let `target_pdf(x)` be its probability density function (use `scipy.stats.norm.pdf`).
2.  **Proposal Distribution:** Choose a symmetric proposal distribution `Q(x' | x)` to suggest the next state `x'` given the current state `x`. A common choice is a Normal distribution centered at the current state: `x' ~ N(x, proposal_sigma^2)`. Choose a `proposal_sigma` (e.g., 1.0).
3.  **Metropolis-Hastings Algorithm:**
    * Initialize the chain at a starting point `x_current`.
    * Set a number of iterations (e.g., 10000).
    * Loop:
        * Propose a new state `x_proposed` by sampling from `Q(x_proposed | x_current)`.
        * Calculate the acceptance ratio `alpha = min(1, target_pdf(x_proposed) / target_pdf(x_current))`. (Note: Since the proposal is symmetric, `Q(x|x') = Q(x'|x)`, the proposal densities cancel out).
        * Generate a random number `u` from Uniform(0, 1).
        * If `u < alpha`, accept the proposal: `x_current = x_proposed`.
        * Else (if `u >= alpha`), reject the proposal: `x_current` remains unchanged.
        * Store `x_current`.
4.  Implement this algorithm in Python.
5.  Discard an initial portion of the samples as "burn-in" (e.g., first 1000 samples).
6.  Plot a histogram of the remaining samples. Does it approximate the target Normal distribution? Overlay the true target PDF for comparison.
7.  **Challenge:** Experiment with different values of `proposal_sigma`. What happens if it's too small or too large? How does it affect the acceptance rate and the exploration of the target distribution (visualize the trace plot of samples)?

---

### 隼 **Exercise 4: Metropolis-Hastings Sampler (Asymmetric Proposal)**

**Goal:** Adapt the Metropolis-Hastings algorithm for an asymmetric proposal distribution.

**Instructions:**

1.  **Target Distribution:** Use the same target distribution `target_pdf(x)` as in Exercise 3 (e.g., `N(0, 1)`).
2.  **Asymmetric Proposal:** Choose an asymmetric proposal, e.g., a log-normal distribution or a Gamma distribution where the proposed `x'` depends on `x`. For simplicity, let's simulate a Random Walk on positive reals where proposal depends on current state variance. (A better example might be sampling variance where proposal scales with current value). Let's stick to a conceptual modification for now: Assume you have `Q(x'|x)` and `Q(x|x')` which are *not* equal.
3.  **Modified Acceptance Ratio:** The acceptance ratio now includes the proposal densities:
    `alpha = min(1, [target_pdf(x_proposed) * Q(x_current | x_proposed)] / [target_pdf(x_current) * Q(x_proposed | x_current)])`
4.  Modify your Python implementation from Exercise 3 to calculate this full acceptance ratio, assuming you have functions `proposal_pdf(new_state, old_state)` and `proposal_sampler(old_state)`.
5.  Run the simulation. (You might need to carefully design the proposal to make this work well).
6.  Discuss why the proposal density ratio `Q(x_current | x_proposed) / Q(x_proposed | x_current)` is necessary to ensure the chain converges to the correct target distribution when the proposal is asymmetric (Hint: Detailed balance condition).
7.  **Challenge:** Implement a concrete example with an asymmetric proposal, e.g., sampling a variance parameter `sigma^2` (which must be positive) where the proposal `sigma_proposed^2` is drawn from a distribution whose scale depends on `sigma_current^2`.

---

### 隼 **Exercise 5: Markov Chain Properties (Conceptual)**

**Goal:** Understand the theoretical properties required for an MCMC chain to converge to the target distribution.

**Instructions:**

1.  Define the following Markov chain properties in the context of MCMC sampling:
    * **Irreducibility:** What does it mean for the chain to be irreducible? Why is this necessary for exploring the entire target distribution? How might a poor proposal distribution violate this?
    * **Aperiodicity:** What does it mean for the chain to be aperiodic? Why is this condition usually satisfied by standard MCMC algorithms like Metropolis-Hastings with continuous state spaces?
    * **Stationary Distribution:** What is the desired stationary distribution for an MCMC chain designed to sample from a posterior `P(theta|Data)`?
    * **Detailed Balance (Reversibility):** State the detailed balance condition: `pi(x) * P(x' | x) = pi(x') * P(x | x')`, where `pi` is the stationary distribution and `P` is the transition kernel. Explain how satisfying detailed balance guarantees that `pi` is the stationary distribution. Show how the Metropolis-Hastings acceptance probability is constructed to satisfy detailed balance for the target distribution `pi`.
2.  **Challenge:** Can an MCMC algorithm that does *not* satisfy detailed balance still converge to the correct stationary distribution? (Hint: Research Gibbs sampling or other MCMC variants).

---