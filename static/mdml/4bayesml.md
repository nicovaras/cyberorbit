## 倹 Subtopic 4.6: Bayesian Approaches to Core ML Models

**Goal:** Implement Bayesian versions of standard machine learning models like Linear Regression and Logistic Regression using Probabilistic Programming Languages, and get introduced to Gaussian Processes.

**Resources:**

* **PPL Documentation:** (PyMC, NumPyro, Stan tutorials on Bayesian Linear/Logistic Regression)
    * **PyMC:** [Bayesian Linear Regression](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_linear.html), [Bayesian Logistic Regression](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_logistic.html)
    * **NumPyro:** [Bayesian Regression](http://num.pyro.ai/en/stable/tutorials/bayesian_regression.html)
    * **Stan:** Examples available in documentation and online.
* **Gaussian Processes:**
    * **Book:** Rasmussen & Williams - "Gaussian Processes for Machine Learning" (Definitive reference)
    * **Scikit-learn:** [Gaussian Processes](https://scikit-learn.org/stable/modules/gaussian_process.html)
    * **GP Libraries:** GPyTorch, GPFlow

---

### 隼 **Exercise 1: Bayesian Linear Regression with PPL**

**Goal:** Implement a Bayesian Linear Regression model using a PPL, estimate the posterior distributions for the coefficients and noise term, and generate posterior predictive distributions.

**Instructions:**

1.  Generate simple synthetic data for linear regression: `y = beta_0 + beta_1 * x + noise`, where noise is `Normal(0, sigma^2)`.
2.  Define the Bayesian Linear Regression model in your chosen PPL (PyMC, NumPyro, Stan):
    * **Priors:** Define priors for the intercept (`beta_0`), slope (`beta_1`), and the noise standard deviation (`sigma`). Use weakly informative priors, e.g., `Normal(0, 10)` for coefficients, `HalfCauchy(1)` or `Exponential(1)` for `sigma`.
    * **Likelihood:** Define the likelihood for the observed `y` values: `y ~ Normal(mu, sigma^2)`, where `mu = beta_0 + beta_1 * x`.
3.  Run MCMC (e.g., NUTS) to sample from the posterior distributions of `beta_0`, `beta_1`, and `sigma`.
4.  Analyze the results using ArviZ or similar tools:
    * Plot the posterior distributions (trace plots, densities) for `beta_0`, `beta_1`, `sigma`.
    * Report summary statistics (mean, median, credible intervals). How do the posterior means compare to the true values used to generate the data?
5.  Use the PPL's posterior predictive sampling capability to generate predictions (`y_pred`) for new `x` values. Plot the mean prediction line and a credible interval band (e.g., 95% HDI) for the predictions, overlaid on the original data.
6.  **Challenge:** Compare the Bayesian credible interval for the coefficients (`beta_0`, `beta_1`) to the frequentist confidence intervals obtained from `sklearn.linear_model.LinearRegression`. How does the interpretation differ?

---

### 隼 **Exercise 2: Bayesian Logistic Regression with PPL**

**Goal:** Implement Bayesian Logistic Regression using a PPL to model binary outcomes and estimate coefficient posteriors.

**Instructions:**

1.  Generate simple synthetic data for binary classification suitable for logistic regression (e.g., two slightly overlapping clusters of points in 2D).
2.  Define the Bayesian Logistic Regression model in your PPL:
    * **Priors:** Define priors for the intercept and coefficients (e.g., `Normal(0, 10)`).
    * **Linear Model:** Calculate the linear predictor `eta = intercept + coef_1 * x1 + coef_2 * x2`.
    * **Likelihood:** Define the likelihood for the observed binary `y` values using the sigmoid (logistic) function: `y ~ Bernoulli(sigmoid(eta))` or `y ~ Bernoulli(logit_p=eta)`.
3.  Run MCMC to sample from the posterior distributions of the intercept and coefficients.
4.  Analyze the results:
    * Plot posterior distributions and report summaries for the parameters.
    * How do you interpret the posterior distribution for a coefficient in logistic regression (e.g., in terms of log-odds)?
5.  Generate posterior predictive samples for the class labels on a grid of new input points. Visualize the decision boundary (e.g., the contour where the probability of class 1 is 0.5) and potentially the uncertainty around the boundary based on the posterior samples.
6.  **Challenge:** Place weakly informative priors on the coefficients. Now, try placing very narrow (informative) priors centered at 0. How does this affect the posterior distributions and the resulting decision boundary, especially if the data is limited? This demonstrates regularization via priors.

---

### 隼 **Exercise 3: Introduction to Gaussian Processes (GP) for Regression**

**Goal:** Use scikit-learn or a dedicated GP library to fit a Gaussian Process regressor, understanding its non-parametric nature and ability to provide uncertainty estimates.

**Instructions:**

1.  Generate simple 1D non-linear data (e.g., `y = sin(x) + noise`). Split into train and test points.
2.  Use `sklearn.gaussian_process.GaussianProcessRegressor`.
3.  Choose a **kernel** (covariance function). Start with a common one like the RBF kernel (`kernels.RBF`) possibly combined with a `WhiteKernel` for noise.
    * `kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2)) + WhiteKernel(0.1, (1e-10, 1e1))` (Example with bounds for hyperparameter optimization).
4.  Instantiate the `GaussianProcessRegressor` with the chosen kernel. Set `alpha` (noise level added to diagonal) or use `WhiteKernel`. Set `n_restarts_optimizer` to >0 to help find good kernel hyperparameters.
5.  Fit the GP model to the training data (`X_train`, `y_train`). The fitting process optimizes the kernel hyperparameters by maximizing the log marginal likelihood.
6.  Use the fitted model to make predictions on the test points (`X_test`). Use `predict(X_test, return_std=True)` to get both the mean prediction and the standard deviation (uncertainty) at each test point.
7.  Plot the original data, the GP mean prediction line, and a shaded region representing the uncertainty (e.g., mean +/- 1.96 * std_dev for a 95% confidence interval).
8.  Analyze the plot: Does the GP capture the non-linear relationship? Where is the prediction uncertainty highest and lowest? (Typically higher further from training data).
9.  **Challenge:** Experiment with different kernels (e.g., Matern, RationalQuadratic). How does the choice of kernel affect the smoothness and fit of the GP model? Examine the optimized kernel hyperparameters (`gp.kernel_.get_params()`).

---

### 隼 **Exercise 4: Bayesian Model Comparison (Conceptual)**

**Goal:** Understand how Bayesian approaches can be used to compare different models, going beyond simple point estimates of performance.

**Instructions:**

1.  Suppose you have fit two different Bayesian models (Model A and Model B) to the same data using MCMC or VI.
2.  **Posterior Predictive Checks (PPCs):** Describe how you would use PPCs to assess the fit of each model. (Generate simulated datasets from the fitted posterior predictive distribution and compare summary statistics of the simulated data to the observed data). If Model A consistently generates simulated data that looks more like the real data than Model B does, what does that suggest?
3.  **Information Criteria (LOO-CV, WAIC):** Explain the purpose of Leave-One-Out Cross-Validation (LOO-CV) and the Widely Applicable Information Criterion (WAIC) in a Bayesian context. How do they estimate the out-of-sample predictive accuracy while penalizing for model complexity? How would you use `az.compare` (ArviZ library) output comparing LOO/WAIC scores for Model A and Model B to choose between them?
4.  **Bayes Factors:** Define the Bayes Factor `BF_AB = p(Data|Model A) / p(Data|Model B)`. What does the evidence (marginal likelihood) `p(Data|Model)` represent? Why is calculating it often difficult? If `BF_AB` is large (e.g., > 10), what does it suggest about the evidence supporting Model A versus Model B?
5.  Compare these Bayesian approaches (PPCs, Information Criteria, Bayes Factors) to frequentist model selection based on metrics like AIC, BIC, or simple cross-validated accuracy/RMSE. What are the philosophical and practical differences?
6.  **Challenge:** If using VI, the ELBO is a lower bound on the log marginal likelihood. Can the ELBO be directly used for model comparison like WAIC or LOO? Why or why not?

---