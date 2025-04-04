## 倹 Subtopic 1.2: Metrics for Imbalanced Data Deep Dive

**Goal:** Understand, calculate, and interpret evaluation metrics specifically designed for classification tasks where class distributions are skewed, moving beyond simple accuracy.

**Resources:**

* **Scikit-learn Metrics:** [Classification Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics) (Precision, Recall, F-beta, MCC, Balanced Accuracy, PR Curve, Average Precision)
* **Precision-Recall Curve:** [Scikit-learn Documentation](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)
* **Matthews Correlation Coefficient (MCC):** [Wikipedia Article](https://en.wikipedia.org/wiki/Phi_coefficient) (MCC is the Phi coefficient for binary classification)
* **Balanced Accuracy:** [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#balanced-accuracy-score)

---

### 隼 **Exercise 1: Accuracy vs. Precision/Recall/F1**

**Goal:** Demonstrate why accuracy is a misleading metric on imbalanced datasets and calculate more informative metrics.

**Instructions:**

1.  Create or load a highly imbalanced binary classification dataset (e.g., use `make_classification` from scikit-learn with weights parameter like `weights=[0.98, 0.02]`).
2.  Train a simple classifier (e.g., Logistic Regression) on this data.
3.  Implement a "dummy" classifier that always predicts the majority class.
4.  Evaluate both the trained classifier and the dummy classifier on a test set using the following metrics:
    * Accuracy
    * Precision (for the minority class)
    * Recall (for the minority class)
    * F1-Score (for the minority class)
5.  Compare the results. Why does the dummy classifier achieve high accuracy? How do precision, recall, and F1 reveal the poor performance of the dummy classifier on the minority class compared to the trained model (even if the trained model isn't perfect)?
6.  **Challenge:** Calculate the metrics specifically for the *majority* class as well. How do they compare between the dummy and trained classifiers?

---

### 隼 **Exercise 2: Plotting and Interpreting Precision-Recall Curves**

**Goal:** Generate and analyze Precision-Recall (PR) curves to understand the trade-off between precision and recall at different classification thresholds.

**Instructions:**

1.  Use the imbalanced dataset and trained classifier from Exercise 1.
2.  Obtain the predicted probabilities for the positive (minority) class from your classifier for the test set (e.g., using `model.predict_proba(X_test)[:, 1]`).
3.  Use scikit-learn functions (`precision_recall_curve`, `PrecisionRecallDisplay`) to calculate and plot the PR curve for your classifier.
4.  Calculate the Average Precision (AP) score, which summarizes the PR curve.
5.  Plot the PR curve for a "no-skill" classifier. What does this baseline represent on a PR curve? (Hint: It relates to the prevalence of the positive class).
6.  Interpret the shape of your model's PR curve. What does a curve closer to the top-right corner signify? How does the AP score relate to this?
7.  **Challenge:** Manually select a few points on the PR curve and identify the corresponding classification thresholds. Explain what classification outcome you would expect at a threshold resulting in high recall but low precision, versus one resulting in high precision but low recall.

---

### 隼 **Exercise 3: Calculating Balanced Accuracy and MCC**

**Goal:** Compute and understand Balanced Accuracy and Matthews Correlation Coefficient (MCC) as robust metrics for imbalanced data.

**Instructions:**

1.  Use the imbalanced dataset, trained classifier, and dummy classifier from Exercise 1.
2.  Calculate the Balanced Accuracy for both classifiers using scikit-learn (`balanced_accuracy_score`). Compare these scores to the standard accuracy calculated earlier. How does Balanced Accuracy account for imbalance?
3.  Calculate the Matthews Correlation Coefficient (MCC) for both classifiers using scikit-learn (`matthews_corrcoef`).
4.  Interpret the MCC scores. What do values close to +1, -1, and 0 indicate? Why is MCC considered a particularly informative metric for imbalanced classification? Compare the MCC scores of the trained classifier and the dummy classifier.
5.  **Challenge:** Consider a scenario where your classifier predicts *only* the minority class correctly and *none* of the majority class. Calculate Accuracy, Balanced Accuracy, Precision (minority), Recall (minority), and MCC for this scenario. Which metrics best reflect the model's performance?

---

### 隼 **Exercise 4: Using the F-beta Score**

**Goal:** Understand how the F-beta score allows weighting the importance of precision versus recall.

**Instructions:**

1.  Use the imbalanced dataset and trained classifier from Exercise 1.
2.  Calculate the F1-score (which is the F-beta score with beta=1).
3.  Now, imagine a scenario where **recall is twice as important as precision** (e.g., medical diagnosis where missing a positive case is very costly). Calculate the F-beta score with beta=2 using scikit-learn (`fbeta_score`).
4.  Next, imagine a scenario where **precision is twice as important as recall** (e.g., spam detection where misclassifying a non-spam email is very disruptive). Calculate the F-beta score with beta=0.5.
5.  Compare the F1, F2, and F0.5 scores. Explain how changing the beta value adjusts the score based on the relative importance of precision and recall.
6.  **Challenge:** Plot the F-beta score for your classifier across a range of beta values (e.g., from 0.1 to 10). How does the score change as beta increases?

---