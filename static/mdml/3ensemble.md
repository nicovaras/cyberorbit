## 倹 Subtopic 3.5: Ensemble Methods: Bagging & Boosting Deep Dive

**Goal:** Understand the principles behind bagging and boosting, explore variations like Random Forests, and gain practical experience tuning popular gradient boosting libraries (XGBoost, LightGBM, CatBoost).

**Resources:**

* **Scikit-learn Ensemble Methods:** [User Guide](https://scikit-learn.org/stable/modules/ensemble.html) (RandomForest, GradientBoostingClassifier/Regressor, BaggingClassifier/Regressor)
* **XGBoost:** [Documentation](https://xgboost.readthedocs.io/en/stable/), [Key Parameters](https://xgboost.readthedocs.io/en/stable/parameter.html)
* **LightGBM:** [Documentation](https://lightgbm.readthedocs.io/en/latest/), [Key Parameters](https://lightgbm.readthedocs.io/en/latest/Parameters.html)
* **CatBoost:** [Documentation](https://catboost.ai/en/docs/), [Key Parameters](https://catboost.ai/en/docs/concepts/parameter-tuning.html)
* **Gradient Boosting Explained:** [StatQuest Video](https://www.youtube.com/watch?v=3CC4N4z3GJc), [Blog Post](https://explained.ai/gradient-boosting/)

---

### 隼 **Exercise 1: Bagging vs. Random Forest**

**Goal:** Compare standard Bagging (Bootstrap Aggregating) with Random Forests to understand the effect of feature randomization.

**Instructions:**

1.  Load a dataset suitable for classification (e.g., Digits, Breast Cancer).
2.  Train a `sklearn.tree.DecisionTreeClassifier` with default parameters. Evaluate its performance using cross-validation (e.g., accuracy).
3.  Train a `sklearn.ensemble.BaggingClassifier` using the `DecisionTreeClassifier` as the `base_estimator`. Use a reasonable number of estimators (`n_estimators`, e.g., 100). Evaluate using CV.
4.  Train a `sklearn.ensemble.RandomForestClassifier` with the same `n_estimators`. Evaluate using CV.
5.  Compare the performance of the single Decision Tree, Bagging Classifier, and Random Forest.
6.  Explain the key difference between Bagging (with decision trees) and Random Forest. How does the additional randomness introduced by Random Forest (random subspace method) help improve generalization?
7.  **Challenge:** Experiment with the `max_features` parameter in `BaggingClassifier` and `RandomForestClassifier`. How does changing the number of features considered at each split affect performance and potentially the correlation between trees in the ensemble?

---

### 隼 **Exercise 2: Gradient Boosting Machine (GBM) Fundamentals**

**Goal:** Understand the sequential nature of Gradient Boosting by examining the residuals and iterative fitting process (using scikit-learn's GBM).

**Instructions:**

1.  Load a dataset suitable for regression (e.g., Boston Housing, Diabetes).
2.  Train a `sklearn.ensemble.GradientBoostingRegressor` with a small number of estimators (`n_estimators=5`), a small learning rate (`learning_rate=0.1`), and shallow trees (`max_depth=2`). Use `loss='ls'` (least squares).
3.  **Step-by-step Analysis:**
    * Fit the model.
    * Access the initial prediction (usually the mean of the target): `model.init_.predict(X_train)`.
    * Calculate the initial residuals: `y_train - initial_prediction`.
    * Examine the first tree (`model.estimators_[0][0]`). Train this tree *only* on the initial residuals. Its predictions should approximate the residuals.
    * Update the overall prediction: `prediction_1 = initial_prediction + learning_rate * tree_1_prediction`.
    * Calculate the new residuals: `y_train - prediction_1`.
    * Examine the second tree (`model.estimators_[1][0]`). It should be trained on the *new* residuals.
4.  Explain how each subsequent tree tries to correct the errors (residuals) made by the ensemble of preceding trees. How does the `learning_rate` control the contribution of each tree?
5.  **Challenge:** How does changing the `loss` function (e.g., to 'lad' - least absolute deviation, or 'huber') affect the calculation of residuals and potentially the robustness of the model to outliers in the target variable?

---

### 隼 **Exercise 3: Tuning XGBoost**

**Goal:** Practice tuning key hyperparameters of the XGBoost algorithm for optimal performance.

**Instructions:**

1.  Install XGBoost (`pip install xgboost`). Load a classification or regression dataset.
2.  Use the `xgboost.XGBClassifier` or `xgboost.XGBRegressor`.
3.  Focus on tuning these key parameters using a systematic approach (e.g., RandomizedSearch or Bayesian Optimization like Optuna/Hyperopt over cross-validation):
    * `n_estimators`: Number of trees (often tuned first with early stopping).
    * `learning_rate` (or `eta`): Step size shrinkage. Lower values usually require more `n_estimators`.
    * `max_depth`: Maximum depth of individual trees. Controls model complexity.
    * `subsample`: Fraction of training samples used per tree (stochastic gradient boosting).
    * `colsample_bytree`: Fraction of features used per tree.
    * Regularization: `reg_alpha` (L1), `reg_lambda` (L2).
    * `gamma`: Minimum loss reduction required to make a further partition.
4.  Employ **early stopping** during tuning: Use the `eval_set` and `early_stopping_rounds` parameters in the `fit` method to stop training when the validation score stops improving, finding the optimal number of boosting rounds automatically for a given set of other parameters.
5.  Report the best hyperparameter combination found and the corresponding cross-validated performance score.
6.  **Challenge:** Explore tree methods (`tree_method` parameter, e.g., 'hist' vs 'exact'). How does 'hist' (histogram-based algorithm) often lead to faster training on large datasets?

---

### 隼 **Exercise 4: Tuning LightGBM**

**Goal:** Practice tuning key hyperparameters of the LightGBM algorithm, noting its differences from XGBoost (e.g., leaf-wise growth).

**Instructions:**

1.  Install LightGBM (`pip install lightgbm`). Use the same dataset as Exercise 3.
2.  Use `lightgbm.LGBMClassifier` or `lightgbm.LGBMRegressor`.
3.  Focus on tuning key parameters (using RandomizedSearch or Bayesian Optimization with CV and early stopping):
    * `n_estimators`, `learning_rate`.
    * `max_depth`: Maximum tree depth (often less critical than `num_leaves` in LightGBM).
    * `num_leaves`: **Main parameter to control complexity in LightGBM.** Controls the number of leaves in individual trees (leaf-wise growth). Higher values mean more complex trees. Must be less than `2^max_depth`.
    * `feature_fraction` (similar to `colsample_bytree`).
    * `bagging_fraction` (similar to `subsample`), `bagging_freq`.
    * Regularization: `reg_alpha`, `reg_lambda`.
    * `min_child_samples`: Minimum number of data points needed in a child leaf.
4.  Use early stopping (`early_stopping_rounds` callback or parameter in `fit`).
5.  Report the best hyperparameter combination and CV score.
6.  Compare the tuning process and potentially the best score/training time to XGBoost (Exercise 3).
7.  Explain LightGBM's **leaf-wise** tree growth strategy. How does it differ from the **level-wise** growth typically used in XGBoost? What are the potential speed advantages and overfitting risks?
8.  **Challenge:** LightGBM has built-in handling for categorical features. Experiment with passing categorical features directly (using `dtype='category'` in pandas and `categorical_feature` parameter in LightGBM) versus one-hot encoding them. Compare performance and training time.

---

### 隼 **Exercise 5: Tuning CatBoost**

**Goal:** Practice tuning CatBoost, focusing on its strengths in handling categorical features automatically.

**Instructions:**

1.  Install CatBoost (`pip install catboost`). Use a dataset with prominent categorical features.
2.  Use `catboost.CatBoostClassifier` or `catboost.CatBoostRegressor`.
3.  Identify the indices or names of your categorical features and pass them to the `cat_features` parameter during initialization or `fit`.
4.  Focus on tuning key parameters (using HPO methods with CV and early stopping):
    * `iterations` (similar to `n_estimators`), `learning_rate`.
    * `depth`: Maximum tree depth.
    * `l2_leaf_reg`: L2 regularization coefficient.
    * `border_count`: Number of splits for numerical features (quantization).
    * `random_strength`: Adds randomness to scoring splits (regularization).
    * CatBoost-specific parameters related to categorical handling (e.g., `one_hot_max_size`).
5.  Use early stopping (`early_stopping_rounds` parameter in `fit`).
6.  Report the best parameters and CV score.
7.  Explain CatBoost's approach to handling categorical features (ordered boosting and variants of target encoding). How does this aim to prevent target leakage compared to naive target encoding?
8.  Compare the performance and ease of use (especially regarding categorical features) to XGBoost and LightGBM.
9.  **Challenge:** Explore CatBoost's visualization tools (`plot_tree`, feature importance plots).

---