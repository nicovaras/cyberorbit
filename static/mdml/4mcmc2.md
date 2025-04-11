## 倹 Subtopic 4.3: Advanced MCMC & Diagnostics

**Goal:** Explore more advanced MCMC algorithms like Gibbs Sampling and HMC/NUTS (primarily through PPLs), and learn how to assess MCMC convergence and efficiency using standard diagnostics.

**Resources:**

* **Probabilistic Programming Languages (PPLs):**
    * **PyMC:** [Documentation](https://www.pymc.io/projects/docs/en/stable/index.html)
    * **Stan (via CmdStanPy or PyStan):** [Documentation](https://mc-stan.org/users/documentation/)
    * **NumPyro:** [Documentation](http://num.pyro.ai/en/stable/)
* **MCMC Diagnostics Libraries:**
    * **ArviZ:** [Documentation](https://python.arviz.org/en/stable/) (Works with PyMC, Stan, NumPyro outputs)
* **Gibbs Sampling:** [Explanation](https://en.wikipedia.org/wiki/Gibbs_sampling)
* **Hamiltonian Monte Carlo (HMC) / NUTS:** [Conceptual Explanation](https://arxiv.org/abs/1701.02434), [NUTS Paper](http://www.stat.columbia.edu/~gelman/research/published/nuts.pdf)
* **Convergence Diagnostics:** `R-hat` ([Gelman-Rubin statistic](https://en.wikipedia.org/wiki/Gelman%E2%80%93Rubin_diagnostic)), Effective Sample Size (ESS).

---

### 隼 **Exercise 1: Gibbs Sampling (Simple Bivariate Case)**

**Goal:** Implement Gibbs sampling for a simple two-parameter problem where the conditional distributions are easy to sample from.

**Instructions:**

1.  **Target Distribution:** Consider a Bivariate Normal distribution for parameters `(theta_1, theta_2)` with a known covariance matrix. The key is that the *conditional distributions* `P(theta_1 | theta_2)` and `P(theta_2 | theta_1)` are also Normal and can be derived analytically.
    * Example: Target `N([0, 0], [[1, 0.8], [0.8, 1]])`.
    * Conditional `theta_1 | theta_2 ~ N(rho * theta_2, 1 - rho^2)`
    * Conditional `theta_2 | theta_1 ~ N(rho * theta_1, 1 - rho^2)` (Where `rho = 0.8`)
2.  **Gibbs Sampler Implementation:**
    * Initialize `theta_1` and `theta_2` (e.g., `theta_1 = 0, theta_2 = 0`).
    * Set number of iterations (e.g., 10000).
    * Loop:
        * Sample `theta_1_new` from `P(theta_1 | theta_2_current)` using the derived conditional Normal distribution.
        * Sample `theta_2_new` from `P(theta_2 | theta_1_new)` using the derived conditional Normal distribution.
        * Update `theta_1_current = theta_1_new`, `theta_2_current = theta_2_new`.
        * Store the pair `(theta_1_current, theta_2_current)`.
3.  Implement this in Python using `numpy.random.normal`.
4.  Discard burn-in samples.
5.  Plot a scatter plot of the sampled `(theta_1, theta_2)` pairs. Does it resemble the target Bivariate Normal distribution (an ellipse)? Plot histograms for the marginal distributions of `theta_1` and `theta_2`.
6.  **Challenge:** Explain why Gibbs sampling works. How does iteratively sampling from full conditional distributions lead to samples from the joint distribution? In what scenarios is Gibbs sampling preferred over Metropolis-Hastings?

---

### 隼 **Exercise 2: Using a PPL for Posterior Sampling (PyMC/Stan)**

**Goal:** Define a simple Bayesian model (e.g., estimating coin bias) using a PPL and use its built-in MCMC sampler (often NUTS) to draw samples from the posterior.

**Instructions:**

1.  Choose a PPL (e.g., PyMC or Stan via CmdStanPy). Install it.
2.  **Define the Model (Beta-Binomial):**
    * Specify the prior for the bias parameter `theta`: `theta ~ Beta(alpha=1, beta=1)`.
    * Specify the likelihood for the observed data `h` (number of heads) given `n` (number of trials): `h ~ Binomial(n, theta)`.
3.  Provide simulated or real data (`n`, `h`).
4.  Use the PPL's functions to:
    * Define the model structure (using PPL syntax, e.g., `with pm.Model(): ...` or Stan language).
    * Run the MCMC sampler (e.g., `pm.sample()`, `CmdStanModel.sample()`). Let it run multiple chains (e.g., 4 chains). The default sampler is often NUTS (an advanced form of HMC).
5.  The sampler returns an object containing the MCMC samples (the "trace"). Extract the samples for the parameter `theta`.
6.  Plot a histogram or density plot of the samples for `theta`. Does it match the analytical posterior `Beta(alpha+h, beta+n-h)` you calculated in Subtopic 4.1?
7.  **Challenge:** Use the PPL to define the Normal-Normal model from Subtopic 4.1 (Exercise 3) and sample from the posterior of `mu`. Compare the sampled posterior to the analytical one.

---

### 隼 **Exercise 3: Interpreting Trace Plots**

**Goal:** Visually inspect MCMC trace plots to assess chain convergence and mixing.

**Instructions:**

1.  Generate MCMC samples for a parameter using a PPL (as in Exercise 2) or your own sampler, making sure to run **multiple independent chains** (e.g., 4 chains).
2.  Use a library like ArviZ (`az.plot_trace`) or plot manually: For a specific parameter (e.g., `theta` from Exercise 2), create **trace plots**. These show the sampled value of the parameter at each MCMC iteration, plotted separately for each chain.
3.  Examine the trace plots:
    * **Convergence:** Do all chains seem to converge to the same general area (stationary distribution)? Or are some chains stuck in different regions?
    * **Mixing:** Does each chain explore the parameter space well (moving around rapidly), or does it move very slowly or get stuck at certain values for long periods? Good mixing looks like a "fuzzy caterpillar".
    * **Burn-in:** Can you visually identify an initial "warm-up" or "burn-in" phase before the chains reach stationarity?
4.  Generate trace plots for a "bad" MCMC run (e.g., use a very poor proposal distribution in Metropolis-Hastings, or a model with strong multi-modality/identifiability issues). How do the trace plots differ in appearance?
5.  **Challenge:** Besides the trace plot itself, what other information is typically shown by functions like `az.plot_trace` (e.g., posterior density plot)? How does the density plot complement the trace plot?

---

### 隼 **Exercise 4: Calculating and Interpreting R-hat (Gelman-Rubin)**

**Goal:** Compute the R-hat statistic to quantitatively assess convergence across multiple MCMC chains.

**Instructions:**

1.  Use the MCMC samples generated from multiple chains (e.g., 4 chains) in Exercise 2 or 3.
2.  Calculate (or use a library function like ArviZ's `az.summary` or `az.rhat`) the R-hat statistic (potential scale reduction factor) for your parameter(s) of interest.
3.  Understand the calculation conceptually: R-hat compares the **variance between chains** to the **variance within chains**.
4.  Interpret the R-hat value:
    * What does an R-hat value close to 1.0 (e.g., < 1.01 or < 1.05 depending on convention) indicate about convergence?
    * What does a high R-hat value (e.g., > 1.1) suggest?
5.  If you generated a "bad" MCMC run in Exercise 3, calculate R-hat for that run. Is it significantly higher than 1.0?
6.  **Challenge:** Why is running multiple chains essential for calculating R-hat? What potential convergence issues might be missed if you only run a single chain?

---

### 隼 **Exercise 5: Calculating and Interpreting Effective Sample Size (ESS)**

**Goal:** Compute the Effective Sample Size (ESS) to understand the efficiency of the MCMC sampler and account for autocorrelation between samples.

**Instructions:**

1.  Use the MCMC samples from a *single* chain (after discarding burn-in) or combined samples from multiple chains (after verifying convergence with R-hat).
2.  Calculate (or use a library function like ArviZ's `az.summary` or `az.ess`) the Effective Sample Size (ESS) for your parameter(s) of interest.
3.  Understand the concept: MCMC samples are often autocorrelated (nearby samples are not independent). ESS estimates the number of *independent* samples that would contain the same amount of information as the autocorrelated MCMC samples.
4.  Interpret the ESS value:
    * If you have `N` total MCMC samples (post-burn-in), what does an ESS much smaller than `N` indicate about the autocorrelation and efficiency of your sampler?
    * What constitutes a "good" or acceptable ESS value (often depends on the goal, but higher is better, e.g., > 400 sometimes cited for stable estimates)?
5.  If you generated samples using different proposal widths in Metropolis-Hastings (Exercise 3, Challenge), calculate ESS for each run. How did the proposal width affect sampling efficiency (ESS)?
6.  **Challenge:** Plot the autocorrelation function (ACF) for your MCMC samples (e.g., using `arviz.plot_autocorr`). How does high autocorrelation (slow decay in the ACF plot) relate to low ESS?

---

### 隼 **Exercise 6: HMC/NUTS Conceptual Understanding**

**Goal:** Grasp the intuition behind Hamiltonian Monte Carlo (HMC) and the No-U-Turn Sampler (NUTS) used by modern PPLs.

**Instructions:**

1.  Research HMC. Explain the physical analogy used: simulating a particle moving over a potential energy surface (related to the negative log posterior).
    * What roles do the "position" (parameters) and "momentum" play?
    * How does simulating Hamiltonian dynamics propose new states that are potentially far away but still have high probability?
    * What is the Metropolis acceptance step used for at the end of a trajectory simulation?
2.  Research NUTS. Explain the problem with basic HMC that NUTS tries to solve (sensitivity to the number of simulation steps `L` and step size `epsilon`).
3.  How does NUTS automatically adapt the trajectory length (number of steps) to avoid random walks and U-turns, making it less sensitive to tuning?
4.  Why are HMC and NUTS generally much more efficient than standard Metropolis-Hastings or Gibbs sampling for complex, high-dimensional models (especially those with correlated parameters)?
5.  **Challenge:** What are some potential difficulties or failure modes when using HMC/NUTS (e.g., issues with discrete parameters, challenging geometries like "funnels")?

---