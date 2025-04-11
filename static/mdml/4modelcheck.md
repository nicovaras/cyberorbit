## 倹 Subtopic 4.7: Bayesian Model Checking & Selection

**Goal:** Learn how to evaluate the goodness-of-fit of Bayesian models using posterior predictive checks (PPCs) and compare different models using information criteria (LOO, WAIC) and Bayes Factors.

**Resources:**

* **ArviZ Library:** [Documentation](https://python.arviz.org/en/stable/) (For PPCs, LOO, WAIC, model comparison plots)
* **PPL Documentation:** PyMC, NumPyro, Stan sections on posterior predictive sampling and model comparison utilities.
* **Information Criteria:** [Vehtari et al. - Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC](https://arxiv.org/abs/1507.04544) (Detailed explanation of LOO-CV and WAIC)
* **Bayes Factors:** [Wikipedia Article](https://en.wikipedia.org/wiki/Bayes_factor), [More detailed explanation](https://statswithr.github.io/book/bayesian-model-choice.html)

---

### 隼 **Exercise 1: Graphical Posterior Predictive Checks (PPCs)**

**Goal:** Visually assess model fit by comparing simulated data generated from the posterior predictive distribution to the actual observed data.

**Instructions:**

1.  Fit a Bayesian model to data using a PPL (e.g., the Bayesian Linear Regression from Subtopic 4.6 Exercise 1). Obtain the MCMC trace (posterior samples).
2.  Use your PPL or ArviZ (`arviz.plot_ppc`) to generate posterior predictive samples. This involves:
    * Drawing parameter samples (`beta_0`, `beta_1`, `sigma`) from the posterior trace.
    * For each parameter sample, simulate a new dataset `y_rep` from the likelihood function (`Normal(beta_0 + beta_1 * x, sigma^2)`).
3.  Generate graphical PPC plots provided by ArviZ:
    * Plot the density estimate of the observed data `y` overlaid with density estimates from multiple simulated datasets `y_rep`. Does the overall shape match?
    * Plot specific summary statistics (e.g., mean, standard deviation, min, max) calculated from the observed data `y` compared to the distribution of the same statistics calculated from the `y_rep` datasets. Do the observed statistics look plausible under the model?
4.  Interpret the plots. Do they indicate any major discrepancies between the model's predictions and the real data?
5.  **Challenge:** Implement a PPC for a different type of model (e.g., the Bayesian Logistic Regression) comparing the distribution of observed binary outcomes to simulated binary outcomes.

---

### 隼 **Exercise 2: Test Statistics for PPCs**

**Goal:** Quantify model fit using numerical posterior predictive checks based on specific test statistics relevant to the modeling goal.

**Instructions:**

1.  Use the same fitted model and posterior predictive samples (`y_rep`) from Exercise 1.
2.  Choose specific test statistics `T(y)` that capture aspects of the data you care about (beyond simple mean/variance). Examples for regression:
    * Skewness of `y`.
    * Kurtosis of `y`.
    * Number of outliers (e.g., points beyond 3 standard deviations from the mean).
    * Autocorrelation (if time series).
3.  Calculate the test statistic for the *observed* data: `T(y_obs)`.
4.  Calculate the test statistic for *each* simulated dataset in your posterior predictive samples: `T(y_rep_i)`.
5.  Calculate the **Bayesian p-value** for the test statistic: This is the proportion of simulated statistics `T(y_rep_i)` that are greater than or equal to (or less than or equal to, depending on the statistic) the observed statistic `T(y_obs)`.
    * `p_value = mean(T(y_rep) >= T(y_obs))`
6.  Interpret the Bayesian p-value:
    * Values close to 0.5 suggest the observed statistic is plausible under the model.
    * Values close to 0 or 1 suggest the model struggles to replicate that specific aspect of the data (misfit).
7.  Calculate Bayesian p-values for several different test statistics. Does the model fit well according to some statistics but poorly according to others?
8.  **Challenge:** Use ArviZ's `plot_bpv` (Bayesian p-value plot) function to visualize this comparison.

---

### 隼 **Exercise 3: Calculating LOO-CV and WAIC with ArviZ**

**Goal:** Use the ArviZ library to compute estimated out-of-sample predictive fit using Leave-One-Out Cross-Validation (LOO-CV) and the Widely Applicable Information Criterion (WAIC).

**Instructions:**

1.  Fit two competing Bayesian models to the same dataset using a PPL (e.g., Model 1: Linear regression with only `x1`; Model 2: Linear regression with `x1` and `x2`). Obtain the ArviZ `InferenceData` object containing the trace and posterior predictive distributions for both models.
2.  Use ArviZ functions to compute LOO-CV and WAIC:
    * `loo1 = az.loo(trace_model_1, pointwise=True)`
    * `waic1 = az.waic(trace_model_1, pointwise=True)`
    * Repeat for Model 2.
3.  Examine the output for each model:
    * Look for the estimated Expected Log Predictive Density (`elpd_loo` or `elpd_waic`). Higher is better.
    * Look for the effective number of parameters (`p_loo` or `p_waic`).
    * Look for warning messages regarding Pareto k diagnostic values (for LOO) or p_waic values, which might indicate unreliable estimates.
4.  Report the `elpd_loo` and `elpd_waic` for both models. Which model appears to have better out-of-sample predictive performance according to these metrics?
5.  **Challenge:** Why are LOO-CV and WAIC generally preferred over simpler information criteria like AIC or BIC in a Bayesian context? (Hint: Averaging over the posterior vs. using point estimates).

---

### 隼 **Exercise 4: Comparing Models with `az.compare`**

**Goal:** Use ArviZ's `compare` function to formally compare models based on their LOO or WAIC scores, accounting for uncertainty.

**Instructions:**

1.  Using the computed LOO or WAIC results (ArviZ `InferenceData` objects or the dictionaries returned by `az.loo`/`az.waic`) from Exercise 3 for Model 1 and Model 2.
2.  Create a dictionary mapping model names to their LOO/WAIC results: `compare_dict = {"Model 1": loo1, "Model 2": loo2}`.
3.  Use `az.compare(compare_dict, ic='loo')` (or `ic='waic'`) to generate a comparison table.
4.  Interpret the output table:
    * The models are usually ranked from best (top) to worst based on the chosen IC (information criterion).
    * `elpd_diff`: Difference in ELPD compared to the best model.
    * `se_diff`: Standard error of the ELPD difference. Provides uncertainty estimate.
    * `dse`: Standard error of the difference itself.
    * `warning`: Indicates if IC calculation might be unreliable.
    * `weight`: LOO Akaike weights, representing the probability that each model will make the best predictions on future data, assuming one of the compared models is the true model.
5.  Based on the `elpd_diff` and its standard error `dse`, can you confidently say that the top-ranked model is significantly better than the second-ranked model? (A common rule of thumb is if `elpd_diff` is more than several times `dse`).
6.  **Challenge:** What does a high Pareto k diagnostic value (reported by `az.loo`) indicate about a specific data point's influence on the LOO-CV calculation? Why might this suggest the model is sensitive or that LOO might be unreliable for that model/data?

---

### 隼 **Exercise 5: Bayes Factors (Conceptual & Simple Cases)**

**Goal:** Understand the concept of Bayes Factors for model comparison and how they relate to posterior model probabilities.

**Instructions:**

1.  Define the Bayes Factor `BF_12` comparing Model 1 (`M1`) to Model 2 (`M2`): `BF_12 = p(Data | M1) / p(Data | M2)`. What does `p(Data | M)` represent (the marginal likelihood or evidence)?
2.  Explain how the Bayes Factor relates to posterior model odds and prior model odds:
    `Posterior Odds (M1 vs M2) = Bayes Factor (BF_12) * Prior Odds (M1 vs M2)`
    Where `Odds = Probability / (1 - Probability)`.
3.  If you assume equal prior probabilities for both models (`P(M1) = P(M2) = 0.5`), how does the Bayes Factor directly relate to the posterior probabilities `P(M1 | Data)` and `P(M2 | Data)`?
4.  Discuss the major practical challenge in calculating Bayes Factors for complex models. (Hint: Calculating the marginal likelihood `p(Data|M)` is often very difficult).
5.  Research common interpretations or scales for Bayes Factors (e.g., Jeffreys' scale). What magnitude of `BF_12` might be considered "strong" or "decisive" evidence in favor of Model 1?
6.  **Challenge:** For very simple models with conjugate priors where the marginal likelihood *can* be calculated analytically (e.g., comparing two different Beta priors for the Beta-Binomial model), calculate the Bayes Factor manually or using library functions if available.

---