## 倹 Subtopic 1.3: Cost-Sensitive Learning Evaluation

**Goal:** Evaluate classification models by incorporating explicit costs associated with different types of misclassifications, aligning model selection with real-world consequences.

**Resources:**

* **Confusion Matrix:** [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix)
* **Cost-Sensitive Learning Overview:** [Machine Learning Mastery Article](https://machinelearningmastery.com/cost-sensitive-learning-for-imbalanced-classification/)
* **Expected Cost Calculation:** [Conceptual Explanation](https://towardsdatascience.com/expected-cost-a-model-evaluation-metric-you-should-consider-using-c2a973b5d6a1)

---

### 隼 **Exercise 1: Defining and Using a Cost Matrix**

**Goal:** Define a cost matrix representing asymmetric misclassification costs and calculate the total cost of a classifier's predictions.

**Instructions:**

1.  Consider a binary classification problem (e.g., fraud detection: Class 0=Not Fraud, Class 1=Fraud).
2.  Define a cost matrix as a 2x2 NumPy array. Assign costs based on a hypothetical scenario:
    * Cost of True Negative (Correctly predicting Not Fraud): 0
    * Cost of True Positive (Correctly predicting Fraud): 0 (or a small cost associated with investigation)
    * Cost of False Positive (Predicting Fraud when it's Not Fraud - Type I Error): e.g., 1 (cost of investigation)
    * Cost of False Negative (Predicting Not Fraud when it's Fraud - Type II Error): e.g., 10 (cost of missed fraud)
3.  Train a classifier on a suitable dataset (use `make_classification` or a real-world dataset).
4.  Generate predictions on a test set.
5.  Calculate the confusion matrix for the predictions using scikit-learn (`confusion_matrix`).
6.  Using the confusion matrix and your defined cost matrix, calculate the **total cost** of the classifier on the test set. (Hint: Element-wise multiplication and sum).
7.  **Challenge:** Define a different cost matrix where False Positives are much more expensive than False Negatives. Recalculate the total cost. How does the optimal decision threshold likely change under this new cost structure?

---

### 隼 **Exercise 2: Weighted Metrics based on Cost**

**Goal:** Calculate weighted versions of standard metrics (like accuracy or F1-score) using misclassification costs.

**Instructions:**

1.  Use the classifier, predictions, and the cost matrix (where False Negatives cost 10, False Positives cost 1) from Exercise 1.
2.  Calculate the standard accuracy.
3.  Calculate a **weighted accuracy** where each prediction's contribution to the accuracy score is inversely proportional to its associated cost if incorrect. (Conceptually: `Weighted Accuracy = Sum(Correct_Prediction_Weights) / Sum(All_Weights)` where weights reflect costs). *This often requires manual calculation based on the confusion matrix and costs.* A simpler approach is to focus on total cost minimization instead.
4.  Alternatively, focus on modifying the decision threshold. Obtain predicted probabilities from your classifier.
5.  Calculate the total cost (using the cost matrix from Exercise 1) for a range of different classification thresholds (e.g., from 0.1 to 0.9).
6.  Identify the threshold that minimizes the total cost. How does this threshold compare to the default 0.5?
7.  **Challenge:** Create a weighted F-beta score function that incorporates the cost matrix elements directly into the calculation of weighted precision and recall.

---

### 隼 **Exercise 3: Evaluating with Expected Cost**

**Goal:** Calculate the expected cost per prediction, incorporating prediction probabilities and the cost matrix.

**Instructions:**

1.  Use the classifier, cost matrix (FN=10, FP=1), and test set from Exercise 1.
2.  Obtain the predicted probabilities `P(class=1 | x)` for each instance `x` in the test set. Let `P(class=0 | x) = 1 - P(class=1 | x)`.
3.  For a *single* test instance `x` with true label `y`:
    * Calculate the **expected cost** of predicting class 0: `Cost(Predict=0 | True=0) * P(class=0 | x) + Cost(Predict=0 | True=1) * P(class=1 | x)`
    * Calculate the **expected cost** of predicting class 1: `Cost(Predict=1 | True=0) * P(class=0 | x) + Cost(Predict=1 | True=1) * P(class=1 | x)`
    (Note: `Cost(Predict=0 | True=1)` is the cost of a False Negative, `Cost(Predict=1 | True=0)` is the cost of a False Positive).
4.  The optimal decision for instance `x` is to predict the class with the lower expected cost.
5.  Implement a function that calculates the expected cost for predicting class 0 and class 1 for *all* test instances based on their predicted probabilities and the cost matrix.
6.  Determine the optimal prediction for each instance by comparing expected costs.
7.  Calculate the total cost on the test set using these optimal predictions derived from expected cost minimization. Compare this to the total cost calculated using the default 0.5 threshold in Exercise 1.
8.  **Challenge:** The threshold where the expected cost of predicting class 0 equals the expected cost of predicting class 1 defines the optimal threshold for minimizing expected cost. Derive the formula for this threshold in terms of the costs and the predicted probability `P(class=1 | x)`.

---

### 隼 **Exercise 4: Visualizing Cost on ROC/PR Curves**

**Goal:** Understand how cost considerations can influence the choice of operating point on ROC or PR curves.

**Instructions:**

1.  Generate the ROC curve and the PR curve for your classifier from Exercise 1.
2.  Superimpose iso-cost lines or visualize the cost associated with different points on the curves (this is conceptually challenging to plot directly but can be understood through analysis).
3.  Consider the cost matrix (FN=10, FP=1). On the ROC curve (plotting True Positive Rate vs False Positive Rate):
    * Where on the curve would operating points minimize False Negatives (high TPR)? What is the implication for False Positives (FPR)? What is the likely cost implication?
    * Where on the curve would operating points minimize False Positives (low FPR)? What is the implication for True Positives (TPR)? What is the likely cost implication?
4.  Repeat the analysis for the PR curve (Precision vs Recall):
    * Where on the curve would points minimize False Negatives (high Recall)? What is the implication for Precision? What is the likely cost implication?
    * Where on the curve would points minimize False Positives (high Precision)? What is the implication for Recall? What is the likely cost implication?
5.  Discuss how the optimal operating point (threshold choice) shifts depending on the relative costs of FP and FN errors.
6.  **Challenge:** Research methods like "Cost Curves" which explicitly plot expected cost versus probability thresholds, providing a more direct way to visualize cost-sensitive decision making.

---