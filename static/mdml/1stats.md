## 倹 Subtopic 1.1: Statistical Foundations for Model Comparison

**Goal:** Understand and apply statistical methods to rigorously compare the performance of different machine learning models, moving beyond simple point estimates of metrics.

**Resources:**

* **Scipy Stats Library:** [scipy.stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) (t-tests, etc.)
* **Scikit-learn Metrics:** [Metrics Documentation](https://scikit-learn.org/stable/modules/model_evaluation.html)
* **Confidence Intervals:** [Blog Post on CIs for ML Metrics](https://machinelearningmastery.com/confidence-intervals-for-machine-learning/)
* **Hypothesis Testing:** [Tutorial on Hypothesis Testing in Python](https://towardsdatascience.com/hypothesis-testing-in-machine-learning-using-python-a0dc89e169ce)
* **Statistical Power:** [Understanding Statistical Power](https://effectsizefaq.com/2010/05/31/understanding-statistical-power/)

---

### 隼 **Exercise 1: Confidence Intervals for Accuracy**

**Goal:** Calculate and interpret confidence intervals for a model's accuracy using bootstrapping.

**Instructions:**

1.  Train a simple classifier (e.g., Logistic Regression) on a standard dataset (e.g., Iris, Breast Cancer).
2.  Evaluate the classifier on a held-out test set and calculate the point estimate for accuracy.
3.  Implement bootstrap resampling on the test set predictions:
    * Repeatedly (e.g., 1000 times) sample the test set predictions *with replacement*.
    * For each bootstrap sample, calculate the accuracy score.
4.  Collect the accuracy scores from all bootstrap samples.
5.  Calculate the 95% confidence interval for the accuracy using the percentiles of the bootstrap scores distribution (e.g., the 2.5th and 97.5th percentiles).
6.  Print the point estimate of accuracy and the calculated confidence interval. Interpret what the interval means.
7.  **Challenge:** Compare the bootstrap confidence interval to a confidence interval calculated using the normal approximation (if appropriate for the metric and sample size).

---

### 隼 **Exercise 2: Comparing Two Models with Paired t-test**

**Goal:** Use a paired statistical test to determine if the difference in performance between two models on the same dataset is statistically significant.

**Instructions:**

1.  Choose a dataset and train two different classifiers (e.g., Logistic Regression vs. k-Nearest Neighbors) using k-fold cross-validation (e.g., k=10).
2.  For each fold, record the performance metric (e.g., accuracy or F1-score) for *both* models on the *same* test fold. This gives you k pairs of scores.
3.  Calculate the differences in scores between Model A and Model B for each fold.
4.  Perform a paired t-test (e.g., using `scipy.stats.ttest_rel`) on the k score differences.
5.  Interpret the resulting p-value. Assuming a significance level (alpha) of 0.05, can you conclude that there is a statistically significant difference between the two models' performance on this dataset?
6.  **Challenge:** Research and discuss the assumptions of the paired t-test. Are they likely met in this cross-validation scenario? What non-parametric alternative could be used (e.g., Wilcoxon signed-rank test)?

---

### 隼 **Exercise 3: Understanding p-value Pitfalls**

**Goal:** Demonstrate how p-values can be misinterpreted, especially when conducting multiple comparisons.

**Instructions:**

1.  Generate two sets of random data representing "model scores" drawn from the *same* normal distribution (implying no real difference). Create, for example, 20 "models" each with 30 "scores".
2.  Perform pairwise t-tests comparing every possible pair of your 20 "models" (190 comparisons).
3.  Count how many of these comparisons yield a p-value less than 0.05, suggesting a "statistically significant" difference.
4.  Discuss the results. Given that all scores came from the same distribution (null hypothesis is true), what does this experiment demonstrate about the risk of false positives when performing multiple comparisons without correction?
5.  **Challenge:** Research common methods for correcting p-values in multiple comparisons (e.g., Bonferroni correction, Holm-Bonferroni method). Briefly explain how one of these methods works.

---

### 隼 **Exercise 4: Statistical Power Estimation (Conceptual)**

**Goal:** Understand the concept of statistical power and its importance in model comparison experiments.

**Instructions:**

1.  Assume you are planning an experiment to compare two models (A and B). You hypothesize Model B is slightly better.
2.  Define the key components needed to estimate statistical power:
    * Significance level (alpha, e.g., 0.05).
    * Effect size (the magnitude of the difference between models you want to be able to detect, e.g., a difference of 0.02 in AUC).
    * Sample size (e.g., the number of cross-validation folds or independent test sets).
    * Desired statistical power (e.g., 0.80, meaning an 80% chance of detecting the effect if it exists).
3.  Using a statistical power calculator tool (online or libraries like `statsmodels` in Python), explore the relationship between these components.
    * How does required sample size change if you want to detect a smaller effect size?
    * How does power change if you decrease the sample size but keep the effect size constant?
    * How does power change if you make alpha stricter (e.g., 0.01)?
4.  Explain why performing a power analysis *before* running extensive model comparison experiments can be beneficial.
5.  **Challenge:** Describe a scenario where low statistical power might lead to incorrectly concluding that two models have equivalent performance.

---