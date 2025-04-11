## 倹 Subtopic 4.4: Variational Inference (VI)

**Goal:** Understand the core concepts of Variational Inference as an alternative to MCMC for approximating posterior distributions, focusing on the KL divergence, the Evidence Lower Bound (ELBO), and the optimization process.

**Resources:**

* **Variational Inference Review:** [Paper by Blei, Kucukelbir & McAuliffe](https://arxiv.org/abs/1601.00670)
* **KL Divergence:** [Wikipedia Article](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
* **ELBO (Evidence Lower Bound):** Derivations and explanations in VI review papers or tutorials.
* **PPL Documentation for VI:** (PyMC, Stan, NumPyro all have VI capabilities)
    * **PyMC:** [Variational Inference](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/variational_inference.html)
    * **NumPyro:** [VI Tutorial](http://num.pyro.ai/en/stable/tutorials/bayesian_regression_vi.html)
    * **Stan:** [Variational Inference Algorithms](https://mc-stan.org/docs/reference-manual/variational-inference-algorithms.html)

---

### 隼 **Exercise 1: KL Divergence Calculation (Simple Case)**

**Goal:** Calculate the Kullback-Leibler (KL) divergence between two simple, known probability distributions (e.g., two Normal distributions) to understand it as a measure of difference.

**Instructions:**

1.  Define two univariate Normal distributions using `scipy.stats.norm`:
    * `P = Normal(mu=0, sigma=1)`
    * `Q = Normal(mu=1, sigma=1.5)`
2.  Recall the formula for KL divergence (continuous case): `KL(P || Q) = Integral[ p(x) * log(p(x) / q(x)) dx ]`.
3.  For the specific case of two Normal distributions `P = N(mu_p, sigma_p^2)` and `Q = N(mu_q, sigma_q^2)`, the KL divergence has an analytical solution:
    `KL(P || Q) = log(sigma_q / sigma_p) + (sigma_p^2 + (mu_p - mu_q)^2) / (2 * sigma_q^2) - 1/2`
4.  Calculate `KL(P || Q)` using this formula and the parameters defined in step 1.
5.  Calculate `KL(Q || P)` using the formula (swap the roles of P and Q).
6.  Implement these calculations in Python. Are `KL(P || Q)` and `KL(Q || P)` the same? What does this tell you about KL divergence as a distance metric?
7.  **Challenge:** Use numerical integration (e.g., `scipy.integrate.quad`) to approximate `KL(P || Q)` by evaluating the integral definition directly over a reasonable range of `x`. Compare the numerical result to the analytical result.

---

### 隼 **Exercise 2: Understanding the ELBO**

**Goal:** Conceptually understand the Evidence Lower Bound (ELBO) and its relationship to KL divergence and the marginal likelihood (evidence).

**Instructions:**

1.  Let `p(theta|D)` be the true posterior distribution we want to approximate, and `q(theta; phi)` be the variational approximation (from a chosen family, parameterized by `phi`). Let `p(D, theta)` be the joint distribution (`likelihood * prior`).
2.  The ELBO is defined as: `ELBO(phi) = E_q [ log p(D, theta) ] - E_q [ log q(theta; phi) ]`
    * The first term is the expected log joint probability under the variational approximation.
    * The second term is the negative entropy of the variational approximation.
3.  It can be shown that maximizing the ELBO with respect to `phi` is equivalent to minimizing the KL divergence `KL(q(theta; phi) || p(theta|D))`. Write down the equation relating the log marginal likelihood `log p(D)`, the ELBO, and this KL divergence:
    `log p(D) = ELBO(phi) + KL(q || p)`
4.  Explain why, since `KL(q || p) >= 0`, the ELBO is a *lower bound* on the log marginal likelihood (log evidence).
5.  Explain the objective of VI: We choose a family for `q` and then find the parameters `phi` within that family that maximize the ELBO, thereby minimizing the KL divergence to the true posterior.
6.  **Challenge:** Compare the KL divergence minimized in VI (`KL(q || p)`) with the "reverse" KL divergence `KL(p || q)`. How might minimizing one versus the other lead to different types of approximations `q` (e.g., mode-seeking vs. mean-seeking, variance characteristics)? (Hint: Consider where `q` must be zero if `p` is zero, and vice-versa).

---

### 隼 **Exercise 3: VI Approximation vs. MCMC (Simple Model)**

**Goal:** Use a PPL to approximate a posterior distribution using both MCMC and Variational Inference (mean-field ADVI) and compare the results.

**Instructions:**

1.  Use the same simple Beta-Binomial model (estimating coin bias `theta`) from Subtopic 4.2 Exercise 2, defined within your chosen PPL (PyMC, NumPyro, or Stan). Use the same data.
2.  **MCMC:** Run the PPL's MCMC sampler (e.g., NUTS) to get a high-quality approximation of the posterior for `theta`. Treat this as the "ground truth" posterior.
3.  **VI:** Use the PPL's Variational Inference functionality (e.g., `pm.fit(method='advi')`, `pyro.infer.SVI`, `CmdStanModel.variational()`). This typically performs Automatic Differentiation Variational Inference (ADVI) using a mean-field approximation (factorized Normal distributions).
4.  Extract the approximate posterior distribution for `theta` obtained from VI. PPLs often provide a way to sample from this approximate variational posterior.
5.  **Comparison:**
    * Plot the density estimate from the MCMC samples.
    * Plot the density of the analytical posterior (`Beta(alpha+h, beta+n-h)`).
    * Plot the density estimate from samples drawn from the VI approximation.
    * Compare the three plots. How well does the VI approximation match the MCMC/analytical posterior in this simple conjugate case? Compare the means and variances.
6.  **Challenge:** Report the final ELBO value achieved by the VI optimization.

---

### 隼 **Exercise 4: VI for a Non-Conjugate Model**

**Goal:** Apply VI to a model where the posterior is not analytically tractable (e.g., Bayesian Logistic Regression) and compare to MCMC.

**Instructions:**

1.  Define a simple Bayesian Logistic Regression model in your PPL:
    * Priors for intercept (`beta_0`) and slope (`beta_1`), e.g., `Normal(0, 10)`.
    * Likelihood: `y ~ Bernoulli(sigmoid(beta_0 + beta_1 * x))`.
2.  Generate simple synthetic data `(x, y)` suitable for logistic regression.
3.  **MCMC:** Run MCMC (NUTS) to sample from the posterior distributions of `beta_0` and `beta_1`.
4.  **VI:** Run ADVI using your PPL's VI functionality to get an approximate posterior for `beta_0` and `beta_1`.
5.  **Comparison:**
    * Create scatter plots (or 2D density plots) of the posterior samples for `(beta_0, beta_1)` obtained from MCMC vs. VI.
    * Create marginal density plots for `beta_0` and `beta_1` comparing MCMC and VI results.
    * How well does the VI approximation capture the shape (including correlations) and location of the MCMC posterior in this non-conjugate case? Discuss potential discrepancies.
6.  **Challenge:** Train the logistic regression model using standard frequentist methods (`sklearn.linear_model.LogisticRegression`). Compare the point estimates obtained from the frequentist approach to the means/modes of the posterior distributions obtained from MCMC and VI.

---

### 隼 **Exercise 5: Speed vs. Accuracy Trade-off (VI vs. MCMC)**

**Goal:** Compare the execution time and approximation quality of VI versus MCMC for a given model.

**Instructions:**

1.  Use the Bayesian Logistic Regression model and data from Exercise 4.
2.  Time the execution of the MCMC sampler (e.g., 4 chains, 1000 draws + 1000 tuning steps). Ensure convergence (check R-hat).
3.  Time the execution of the VI algorithm (e.g., ADVI for 20000 iterations).
4.  Compare the run times. Which method is significantly faster?
5.  Qualitatively (by comparing posterior plots as in Exercise 4) and potentially quantitatively (e.g., comparing posterior means/medians), assess the accuracy of the VI approximation relative to the MCMC "ground truth".
6.  Discuss the trade-off: In what scenarios might the speed advantage of VI be worth accepting a potentially less accurate approximation of the posterior compared to MCMC? When might the accuracy of MCMC be essential despite its longer runtime?
7.  **Challenge:** Experiment with the number of iterations for VI and the number of samples/tuning steps for MCMC. How does increasing the computational budget affect the runtime and results for each method?

---