## 倹 Subtopic 3.7: Post-Processing & Platform Strategies

**Goal:** Learn techniques applied *after* model prediction to optimize for specific competition metrics, calibrate predictions, and understand common strategies used in ML platforms like Kaggle.

**Resources:**

* **Probability Calibration:** (See Subtopic 1.5 resources), [Scikit-learn Guide](https://scikit-learn.org/stable/modules/calibration.html)
* **Threshold Tuning:** [Blog post on finding optimal threshold](https://machinelearningmastery.com/threshold-moving-for-imbalanced-classification/)
* **Ensembling Submissions:** Conceptual understanding (averaging, weighted averaging).
* **Kaggle:** [Competitions](https://www.kaggle.com/competitions), [Discussion Forums](https://www.kaggle.com/discussions) (Search for specific competition post-mortems or metric discussions).

---

### 隼 **Exercise 1: Optimal Threshold Tuning for Classification Metrics**

**Goal:** Find the optimal classification threshold on validation predictions to maximize a specific metric like F1-score, Precision, Recall, or a custom business metric.

**Instructions:**

1.  Train a binary classifier (e.g., LightGBM, Logistic Regression) and obtain predicted probabilities on a validation set.
2.  Calculate the chosen evaluation metric (e.g., F1-score) using the default threshold of 0.5.
3.  Iterate through a range of possible thresholds (e.g., from 0.01 to 0.99 in small steps).
4.  For each threshold:
    * Convert the predicted probabilities into class predictions based on the current threshold.
    * Calculate the chosen evaluation metric using these predictions and the true validation labels.
5.  Keep track of the threshold that yielded the best score for your chosen metric.
6.  Plot the metric score versus the threshold value.
7.  Report the best threshold found and the corresponding best score. How does it compare to the score at the default 0.5 threshold?
8.  **Challenge:** Instead of iterating, use the Precision-Recall curve (`sklearn.metrics.precision_recall_curve`) which returns thresholds. Find the threshold that maximizes F1 = 2 * (P * R) / (P + R) using the precision and recall values returned.

---

### 隼 **Exercise 2: Calibrating Predictions Post-Hoc**

**Goal:** Apply calibration techniques (Platt Scaling, Isotonic Regression) to the *outputs* of already trained models, especially relevant if the competition metric relies on well-calibrated probabilities (e.g., log loss).

**Instructions:**

1.  Train a classifier (potentially one known to be poorly calibrated, like Naive Bayes or Random Forest) on a training set.
2.  Generate predicted probabilities from this trained model on a separate *calibration set* (holdout set).
3.  Train a calibrator model (e.g., `sklearn.calibration.CalibratedClassifierCV` with `method='sigmoid'` or `'isotonic'`, but fit *only* the calibrator part on the calibration set predictions and true labels, OR manually fit Logistic Regression/Isotonic Regression as in Subtopic 1.5 Exercises 1 & 2).
4.  Generate predicted probabilities from the original model on the final *test set*.
5.  Apply the fitted calibrator to these test set probabilities to get calibrated probabilities.
6.  Evaluate the calibration (ECE, Brier score, Reliability Diagram) and the relevant competition metric (e.g., log loss) on the test set using both the *original* and the *calibrated* probabilities. Did calibration improve the metric?
7.  **Challenge:** Why might post-hoc calibration be particularly important for ensembles where probabilities are averaged?

---

### 隼 **Exercise 3: Simple Averaging Ensemble for Submissions**

**Goal:** Combine predictions from multiple models by simple averaging to potentially improve robustness and performance.

**Instructions:**

1.  Train several diverse, well-performing models on the same training data (e.g., LightGBM, XGBoost, CatBoost, a Neural Network). Use cross-validation to ensure they are robust.
2.  Generate predictions (probabilities for classification, direct values for regression) from each of these models on the **test set**. You will have multiple sets of test predictions.
3.  Calculate the **simple average** of these predictions across the models for each test instance.
    * Classification: Average the predicted probabilities for each class. The final prediction can be the class with the highest average probability.
    * Regression: Average the predicted values.
4.  Create a submission file based on these averaged predictions.
5.  (If in a competition) Submit and compare the score to the scores of the individual models. Did averaging help?
6.  Discuss why averaging predictions from diverse, strong models often leads to more robust results.
7.  **Challenge:** Implement **rank averaging**. Convert each model's predictions on the test set into ranks, average the ranks, and then use the order of averaged ranks for the final submission. When might rank averaging be preferred over simple averaging (Hint: models predicting on different scales)?

---

### 隼 **Exercise 4: Weighted Averaging Ensemble**

**Goal:** Combine model predictions using weights, potentially giving higher weight to models that performed better on validation data.

**Instructions:**

1.  Use the same trained models and test set predictions from Exercise 3.
2.  You also need the out-of-fold (OOF) validation predictions generated during cross-validation for each model on the *training* data.
3.  Determine weights for each model. Common strategies include:
    * **Manual Weights:** Assign weights based on intuition or individual model CV scores (e.g., model A gets 0.4, B gets 0.3, C gets 0.3). Ensure weights sum to 1.
    * **Optimization:** Find weights that optimize the ensemble's performance metric directly on the OOF validation predictions. This is like a simple linear regression where the OOF predictions are features and the true validation labels are the target (constrain weights to be positive and sum to 1).
4.  Calculate the weighted average of the **test set predictions** using the determined weights.
5.  Create a submission file based on the weighted average. Compare its potential performance to simple averaging and individual models.
6.  **Challenge:** How does the optimization approach for finding weights relate to the meta-learner concept in stacking/blending?

---

### 隼 **Exercise 5: Understanding Competition Metrics & Leaderboards**

**Goal:** Analyze specific competition metrics and understand leaderboard dynamics like overfitting to the public leaderboard.

**Instructions:**

1.  Choose a past or ongoing Kaggle competition (or similar platform).
2.  Identify the **official evaluation metric** used (e.g., AUC, Log Loss, Accuracy, F1, MAE, RMSE, custom metrics). Understand precisely how it is calculated. Does it require probabilities or hard labels? Is it sensitive to outliers?
3.  Read the competition's overview and data description. Are there any specific data characteristics mentioned (imbalance, time series nature, groups) that would influence model evaluation or validation strategy choices?
4.  Browse the competition's **discussion forum** and **public notebooks (kernels)**. Look for discussions or code related to:
    * Validation strategies used by top participants.
    * Specific post-processing tricks employed (e.g., rounding predictions, fixing common misclassifications).
    * Discussions about the difference between Public Leaderboard (LB) scores and Private LB scores (or final CV scores).
5.  Explain the concept of **overfitting the Public Leaderboard**. How can participants inadvertently tune their models based on the limited public test set feedback, leading to poor performance on the final private test set? How can robust cross-validation help prevent this?
6.  **Challenge:** Find an example of a custom metric used in a competition. Implement its calculation based on its definition.

---