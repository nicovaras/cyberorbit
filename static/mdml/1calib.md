## 倹 Subtopic 1.4: Calibration of Probabilistic Models

**Goal:** Understand why predicted probabilities from classifiers may not reflect true likelihoods (calibration), how to measure miscalibration using reliability diagrams and metrics like ECE, and the components of the Brier score.

**Resources:**

* **Scikit-learn Calibration:** [Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html)
* **Reliability Diagrams:** [Paper explaining concepts](https://arxiv.org/abs/1706.04599) (Figure 1 is key)
* **Expected Calibration Error (ECE):** Definition and calculation methods.
* **Brier Score:** [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/model_evaluation.html#brier-score-loss), [Wikipedia Article](https://en.wikipedia.org/wiki/Brier_score)

---

### 隼 **Exercise 1: Visualizing Calibration with Reliability Diagrams**

**Goal:** Create and interpret reliability diagrams to visually assess model calibration.

**Instructions:**

1.  Train two different binary classifiers on a dataset (e.g., Naive Bayes and Logistic Regression). Naive Bayes is often poorly calibrated, while Logistic Regression tends to be better.
2.  Obtain predicted probabilities for the positive class on a test set for both models.
3.  Implement the logic to create a reliability diagram (calibration curve):
    * Bin the predicted probabilities into intervals (e.g., 10 bins: [0.0, 0.1], [0.1, 0.2], ..., [0.9, 1.0]).
    * For each bin, calculate the **average predicted probability** of the instances falling into that bin.
    * For each bin, calculate the **actual fraction of positive instances** among those falling into that bin.
    * Plot the actual fraction of positives (y-axis) against the average predicted probability (x-axis).
4.  Use scikit-learn's `CalibrationDisplay` or plot manually. Include a diagonal line representing perfect calibration.
5.  Plot the reliability diagrams for both the Naive Bayes and Logistic Regression models.
6.  Interpret the diagrams: Which model appears better calibrated? How does deviation from the diagonal line indicate miscalibration (over-confidence or under-confidence)? Include histograms of predicted probabilities in the plots.
7.  **Challenge:** Experiment with different numbers of bins for the reliability diagram. How does the number of bins affect the appearance and interpretation of the curve?

---

### 隼 **Exercise 2: Quantifying Calibration with ECE**

**Goal:** Calculate the Expected Calibration Error (ECE) to get a single numerical score for model calibration.

**Instructions:**

1.  Use the binned data (average predicted probability and actual fraction of positives per bin) generated for the reliability diagrams in Exercise 1.
2.  For each bin `i`:
    * Let `avg_prob(i)` be the average predicted probability in bin `i`.
    * Let `frac_pos(i)` be the fraction of positive instances in bin `i`.
    * Let `n(i)` be the number of instances in bin `i`.
    * Let `N` be the total number of instances.
3.  Calculate the ECE using the formula: `ECE = sum over all bins [ (n(i) / N) * |frac_pos(i) - avg_prob(i)| ]`
4.  Calculate the ECE for both the Naive Bayes and Logistic Regression models.
5.  Compare the ECE scores. Does the ECE score align with your visual interpretation of the reliability diagrams? Lower ECE indicates better calibration.
6.  **Challenge:** Implement the Maximum Calibration Error (MCE), which is simply the maximum absolute difference `|frac_pos(i) - avg_prob(i)|` across all bins. How does MCE differ from ECE in what it measures?

---

### 隼 **Exercise 3: Calculating the Brier Score**

**Goal:** Compute the Brier score, a proper scoring rule that measures both calibration and refinement (discrimination).

**Instructions:**

1.  Use the predicted probabilities and true labels from the test set for both classifiers (Naive Bayes, Logistic Regression) from Exercise 1.
2.  Calculate the Brier score for each model using the formula: `Brier Score = (1/N) * sum over all instances [(predicted_prob_i - true_label_i)^2]`, where `true_label_i` is 0 or 1.
3.  Use scikit-learn's `brier_score_loss` function to verify your calculation.
4.  Compare the Brier scores of the two models. Lower Brier scores are better.
5.  Calculate the Brier score for a "no-skill" baseline model that always predicts the base rate (overall prevalence) of the positive class. How do the models compare to this baseline?
6.  **Challenge:** Does a lower Brier score always mean better calibration? Discuss the relationship between the Brier score and calibration (Hint: Consider the Brier score decomposition).

---

### 隼 **Exercise 4: Brier Score Decomposition (Conceptual)**

**Goal:** Understand the components of the Brier score: Calibration (Reliability), Refinement (Resolution), and Uncertainty.

**Instructions:**

1.  Research the decomposition of the Brier score, typically expressed as: `Brier Score = Reliability - Resolution + Uncertainty`.
2.  Define each component in your own words:
    * **Uncertainty:** What does this term measure? (Hint: It depends only on the true label distribution). Calculate it for your test set.
    * **Reliability:** How does this term relate to the reliability diagram and ECE? (Hint: It's the weighted average of squared differences between fraction of positives and mean predicted probability per bin, similar to ECE but using squared error). Conceptually calculate or estimate this based on your reliability diagrams.
    * **Resolution:** What does this term measure? (Hint: It measures how much the average predicted probabilities per bin differ from the overall base rate of positives). Conceptually calculate or estimate this based on your reliability diagrams.
3.  Explain how improving calibration (reducing the Reliability term) affects the Brier score.
4.  Explain how improving model discrimination/resolution (increasing the Resolution term) affects the Brier score.
5.  Discuss why optimizing directly for Brier score encourages both good calibration and good discriminatory power.
6.  **Challenge:** If two models have the same Reliability (calibration) term, which one will have a better (lower) Brier score according to the decomposition? The one with higher or lower Resolution?

---