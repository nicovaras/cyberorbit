## 倹 Subtopic 1.7: Model Selection Strategies Beyond Grid/Random Search

**Goal:** Implement and understand advanced model selection and hyperparameter optimization techniques like Nested Cross-Validation and Bayesian Optimization, and learn to evaluate models against business-specific KPIs.

**Resources:**

* **Nested Cross-Validation:** [Scikit-learn Example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html), [Explanation Blog Post](https://machinelearningmastery.com/nested-cross-validation-for-machine-learning-with-python/)
* **Bayesian Optimization Libraries:**
    * **Hyperopt:** [Documentation](http://hyperopt.github.io/hyperopt/)
    * **Optuna:** [Documentation](https://optuna.readthedocs.io/en/stable/)
    * **Scikit-optimize:** [Documentation](https://scikit-optimize.github.io/stable/)
* **Business KPIs:** Focus on defining custom metrics based on hypothetical scenarios.

---

### 隼 **Exercise 1: Implementing Nested Cross-Validation**

**Goal:** Perform hyperparameter tuning and model evaluation using nested cross-validation to get an unbiased estimate of generalization performance.

**Instructions:**

1.  Choose a dataset (e.g., Breast Cancer) and a model with hyperparameters to tune (e.g., SVC with `C` and `gamma`).
2.  Set up the **Outer Loop** of cross-validation (e.g., 5-fold CV). This loop splits the data into training/test folds *for final evaluation*.
3.  Inside the Outer Loop:
    * Take the outer training fold.
    * Set up an **Inner Loop** of cross-validation (e.g., 3-fold CV) *on this outer training fold*.
    * Inside the Inner Loop, perform hyperparameter search (e.g., GridSearchCV or RandomizedSearchCV) to find the best hyperparameters *using only the outer training fold data*.
    * Select the best hyperparameters found in the Inner Loop for this outer fold.
    * Train a *new* model using these best hyperparameters on the *entire* outer training fold.
    * Evaluate this model on the corresponding *outer test fold*. Store the score.
4.  After the Outer Loop completes, you will have a set of scores (one from each outer test fold). Calculate the average and standard deviation of these scores.
5.  Compare this average score to the score you might get from a *non-nested* approach (e.g., running GridSearchCV on the whole dataset and reporting `best_score_`). Why is the nested CV score considered a less biased estimate of generalization performance?
6.  **Challenge:** Implement this process using scikit-learn's `GridSearchCV` or `RandomizedSearchCV` within a manual outer `KFold` loop, or explore if libraries provide direct support for nested CV evaluation.

---

### 隼 **Exercise 2: Introduction to Bayesian Optimization with Optuna/Hyperopt**

**Goal:** Use a Bayesian optimization library to efficiently search for optimal hyperparameters for a given model.

**Instructions:**

1.  Choose a dataset and a model with several hyperparameters (e.g., Gradient Boosting with `n_estimators`, `learning_rate`, `max_depth`, `subsample`).
2.  Select a Bayesian Optimization library (e.g., Optuna or Hyperopt). Install it.
3.  Define an **objective function** that:
    * Takes a set of hyperparameters as input (e.g., Optuna's `trial` object or Hyperopt's dictionary).
    * Trains the model using these hyperparameters on the training data (potentially using cross-validation within the objective function for robustness).
    * Evaluates the model on a validation set (or returns the average CV score).
    * Returns the score to be *minimized* or *maximized* (e.g., return validation error to minimize, or validation accuracy to maximize).
4.  Define the **search space** for the hyperparameters (e.g., ranges for continuous values, choices for categorical values) using the library's syntax.
5.  Run the Bayesian optimization process using the library's functions (e.g., `optuna.create_study`, `study.optimize` or `hyperopt.fmin`), specifying the objective function, search space, and the number of trials (iterations).
6.  Retrieve the best hyperparameters found and the corresponding best score.
7.  Compare the efficiency (number of function evaluations needed) and the best score found by Bayesian optimization to what you might expect from Grid Search or Random Search over the same space.
8.  **Challenge:** Visualize the optimization process using the library's plotting functions (if available, e.g., Optuna's `plot_optimization_history`, `plot_param_importances`). What insights do these plots provide?

---

### 隼 **Exercise 3: Defining and Evaluating Custom Business KPIs**

**Goal:** Translate a business objective into a custom evaluation metric and use it to select a model or threshold.

**Instructions:**

1.  Consider a binary classification scenario like customer churn prediction.
2.  Hypothesize a business context:
    * Cost of attempting to retain a customer (offer discount): $5
    * Cost of losing a customer (lost revenue): $100
    * Benefit of retaining a customer who would have churned: $100 (avoided loss)
    * Benefit/Cost of correctly identifying a non-churner: $0
3.  Define a **custom KPI function** `calculate_profit(y_true, y_pred)` that takes true labels and predicted labels and calculates the total profit/loss based on the above costs/benefits and the resulting confusion matrix counts (TP, TN, FP, FN where Positive=Churn).
4.  Train a classifier that predicts churn probability.
5.  Obtain predicted probabilities on a test set.
6.  Evaluate the *total profit* using your custom KPI function for different decision thresholds applied to the probabilities (e.g., thresholds from 0.1 to 0.9).
7.  Identify the threshold that maximizes the total profit according to your custom KPI. How does this threshold compare to one optimized for standard metrics like Accuracy or F1?
8.  **Challenge:** Modify the custom KPI to incorporate the predicted probability. For example, maybe the retention offer is only successful 30% of the time. How would you calculate the *expected* profit per customer based on predicted probability and costs?

---

### 庁 **Project: Automated Model Selection Framework**

**Goal:** Build a framework that uses Nested Cross-Validation for unbiased evaluation and Bayesian Optimization for efficient hyperparameter search to compare multiple algorithms.

**Instructions:**

1.  Choose a dataset suitable for classification or regression.
2.  Select a few different model types to compare (e.g., Logistic Regression, Random Forest, Gradient Boosting, SVM).
3.  For each model type, define a hyperparameter search space.
4.  Implement a Nested Cross-Validation structure (Outer loop for evaluation, Inner loop for HPO).
5.  Inside the Inner Loop (for each outer train fold), use a Bayesian Optimization library (Optuna/Hyperopt) to find the best hyperparameters for the current model type *using only that outer train fold data*. The objective function for Bayesian Optimization should perform cross-validation *within* the inner loop fold.
6.  After finding the best inner hyperparameters, train the model on the full outer train fold and evaluate on the outer test fold. Store this score.
7.  After the Outer Loop finishes for a given model type, calculate the average and standard deviation of its outer test scores.
8.  Repeat steps 4-7 for all selected model types.
9.  Compare the final (outer loop) performance distributions (mean and std dev) of the different model types. Report which model performed best based on this unbiased evaluation.
10. **Portfolio Guidance:** Create a GitHub repository for this framework. Include:
    * Well-documented code.
    * `requirements.txt` (including scikit-learn, numpy, and your chosen Bayesian Optimization library).
    * A `README.md` explaining the importance of unbiased evaluation (Nested CV), efficient HPO (Bayesian Opt), how the framework combines them, instructions for running it, and a summary of results on a sample dataset. This demonstrates advanced model selection practices.

---