## 倹 Subtopic 3.4: Hyperparameter Optimization Strategies

**Goal:** Implement and compare advanced hyperparameter optimization (HPO) techniques like Bayesian Optimization, TPE, and ASHA, moving beyond basic Grid Search and Random Search for efficiency and effectiveness.

**Resources:**

* **Bayesian Optimization Primer:** [Towards Data Science Article](https://towardsdatascience.com/a-conceptual-explanation-of-bayesian-optimization-algorithm-4a445054751a)
* **HPO Libraries:**
    * **Optuna:** [Documentation](https://optuna.readthedocs.io/en/stable/), [Key Features](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/001_key_features.html) (Samplers like TPE, Median Pruner, Integration)
    * **Hyperopt:** [Documentation](http://hyperopt.github.io/hyperopt/), [Basic Tutorial](http://hyperopt.github.io/hyperopt/tutorial/trivial_example/) (TPE sampler)
    * **Scikit-optimize:** [Documentation](https://scikit-optimize.github.io/stable/) (GP, Random Forest, Gradient Boosting based optimizers)
* **Asynchronous Successive Halving (ASHA):** [Optuna Documentation](https://optuna.readthedocs.io/en/stable/reference/pruners.html#optuna.pruners.SuccessiveHalvingPruner), [Original Paper Blog Post](https://blog.ml.cmu.edu/2018/12/12/massively-parallel-hyperparameter-optimization/)

---

### 隼 **Exercise 1: Limitations of Grid/Random Search**

**Goal:** Demonstrate the inefficiency of Grid Search and the potential limitations of Random Search, especially in high-dimensional hyperparameter spaces.

**Instructions:**

1.  Define a simple objective function (e.g., training a small model like Logistic Regression or k-NN on Iris/Digits) with 3-4 hyperparameters to tune (e.g., `C`, `penalty` for LR; `n_neighbors`, `weights`, `p` for k-NN). Include at least one continuous parameter.
2.  Define a search space for Grid Search (e.g., 5 values per hyperparameter). Calculate the total number of combinations Grid Search would evaluate.
3.  Define the same search space for Random Search.
4.  Perform **Grid Search** using `sklearn.model_selection.GridSearchCV` with 3-fold CV. Record the best score found and the total time taken (or number of fits).
5.  Perform **Random Search** using `sklearn.model_selection.RandomizedSearchCV` with 3-fold CV. Set `n_iter` to a reasonable budget (e.g., 20% of the total Grid Search combinations, or a fixed number like 50). Record the best score and time taken.
6.  Run Random Search again with a larger `n_iter` budget (e.g., 50% of Grid Search).
7.  Compare the best scores found and time taken by Grid Search vs. Random Search (with different budgets). Discuss why Random Search often finds a good solution faster than Grid Search, especially when some hyperparameters are more important than others.
8.  Discuss the "curse of dimensionality" in the context of Grid Search – how does the number of evaluations explode as you add more hyperparameters or more values per hyperparameter?
9.  **Challenge:** Visualize the search path of Random Search compared to the grid points explored by Grid Search (for a 2D hyperparameter space).

---

### 隼 **Exercise 2: Bayesian Optimization with Gaussian Processes (Conceptual)**

**Goal:** Understand the core concepts behind Bayesian Optimization using Gaussian Processes (GP) as the surrogate model.

**Instructions:**

1.  Describe the two main components of Bayesian Optimization:
    * **Surrogate Model:** What is its purpose? Why is a Gaussian Process often used? What does the GP model estimate for unseen hyperparameter combinations (Hint: mean and variance/uncertainty)?
    * **Acquisition Function:** What is its purpose? How does it use the predictions (mean and uncertainty) from the surrogate model to decide which hyperparameter combination to try next?
2.  Explain common acquisition functions like:
    * **Expected Improvement (EI):** How does it balance exploiting known good regions vs. exploring uncertain regions?
    * **Probability of Improvement (PI):** How does it differ from EI?
    * **Upper Confidence Bound (UCB):** How does it use the predicted mean and standard deviation directly?
3.  Illustrate the iterative process: Evaluate point -> Update surrogate model -> Use acquisition function to choose next point -> Repeat.
4.  Why is Bayesian Optimization generally more sample-efficient (requires fewer objective function evaluations) than Random Search, especially for expensive objective functions (like training large deep learning models)?
5.  **Challenge:** What are some potential limitations or challenges when using GP-based Bayesian Optimization (e.g., computational cost of GP, handling conditional parameters)?

---

### 隼 **Exercise 3: HPO with Optuna (TPE Sampler)**

**Goal:** Use the Optuna library with its default Tree-structured Parzen Estimator (TPE) sampler to perform hyperparameter optimization.

**Instructions:**

1.  Install Optuna (`pip install optuna`).
2.  Choose a model and dataset (e.g., LightGBM/XGBoost on a classification/regression task). Select 3-5 hyperparameters to tune (e.g., `learning_rate`, `n_estimators`, `max_depth`, `lambda`, `alpha`).
3.  Define an **objective function** compatible with Optuna:
    * It should accept an `optuna.trial.Trial` object as input.
    * Use `trial.suggest_float`, `trial.suggest_int`, `trial.suggest_categorical` to define the search space *within* the function based on the trial object.
    * Train the model using the suggested hyperparameters (use cross-validation inside the objective function for robustness).
    * Return the performance metric to be optimized (e.g., return validation accuracy, or negative validation log-loss).
4.  Create an Optuna `study` object (`study = optuna.create_study(direction='maximize' or 'minimize')`).
5.  Run the optimization using `study.optimize(objective, n_trials=100)`. Set a reasonable number of trials (e.g., 50-200).
6.  Retrieve the best trial found: `study.best_trial.value`, `study.best_trial.params`.
7.  Compare the results (best score, number of trials) to potentially running Random Search for the same number of trials.
8.  **Challenge:** Use Optuna's visualization functions (`optuna.visualization.plot_optimization_history`, `plot_param_importances`, `plot_slice`) to analyze the optimization process and hyperparameter importance.

---

### 隼 **Exercise 4: HPO with Hyperopt (TPE Sampler)**

**Goal:** Use the Hyperopt library with its TPE sampler to perform hyperparameter optimization.

**Instructions:**

1.  Install Hyperopt (`pip install hyperopt`).
2.  Choose a model/dataset/hyperparameters similar to Exercise 3.
3.  Define an **objective function** compatible with Hyperopt:
    * It should accept a dictionary of hyperparameters as input.
    * Train the model using these hyperparameters (use CV inside).
    * Return a dictionary containing the `loss` (value to minimize) and `status: hyperopt.STATUS_OK`.
4.  Define the **search space** using Hyperopt's functions (`hp.uniform`, `hp.loguniform`, `hp.quniform`, `hp.choice`).
5.  Run the optimization using `hyperopt.fmin`:
    * Pass the objective function (`fn`).
    * Pass the search space (`space`).
    * Specify the algorithm (`algo=hyperopt.tpe.suggest`).
    * Set the maximum number of evaluations (`max_evals`).
    * Use a `hyperopt.Trials` object to store results.
6.  Retrieve the best hyperparameters found (`best = fmin(...)`).
7.  Compare the user experience and results to Optuna (Exercise 3).
8.  **Challenge:** How does Hyperopt's search space definition differ from Optuna's approach (defined within the objective)? Discuss pros and cons.

---

### 隼 **Exercise 5: Early Stopping / Pruning with ASHA**

**Goal:** Implement an early stopping strategy like Asynchronous Successive Halving Algorithm (ASHA) during hyperparameter optimization to quickly discard unpromising trials.

**Instructions:**

1.  This exercise is best done with a library that integrates pruning, like **Optuna**. Use the setup from Exercise 3 (Optuna HPO).
2.  Modify the Optuna objective function:
    * Inside the training loop (or after each epoch), calculate an intermediate validation score.
    * Report this intermediate score to Optuna using `trial.report(intermediate_value, step)`.
    * Check if the trial should be pruned using `trial.should_prune()`. If it returns `True`, raise an `optuna.TrialPruned` exception to stop training for this trial early.
3.  When creating the Optuna study, configure a pruner, specifically the `optuna.pruners.SuccessiveHalvingPruner` or `optuna.pruners.HyperbandPruner` (which often uses ASHA internally). Configure its parameters (e.g., `min_resource`, `reduction_factor`).
4.  Run the optimization using `study.optimize()` again.
5.  Observe the study results. You should see many trials being pruned (stopped early). How does this affect the total time taken for the `n_trials` compared to running without pruning? Did it still find a good set of hyperparameters?
6.  Explain how ASHA (or successive halving) works: How does it allocate budgets to different trials and decide which ones to stop early based on intermediate results?
7.  **Challenge:** Compare the `SuccessiveHalvingPruner` with the `MedianPruner` in Optuna. How do their pruning strategies differ?

---