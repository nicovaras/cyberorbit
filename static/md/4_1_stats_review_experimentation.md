## Subtopic 4.1: Review of Foundational Statistics for Experimentation

**Goal:** To refresh understanding and practical application of core statistical concepts essential for designing and analyzing experiments, including hypothesis testing frameworks, p-value interpretation, confidence intervals, and statistical power analysis.

**Resources:**

  * Hypothesis Testing Overview: [Khan Academy - Significance Tests (Hypothesis testing)](https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample)
  * p-value Explained: [Blog Post: What is a p-value?](https://www.google.com/search?q=https://statisticsbyjim.com/hypothesis-testing/p-values-interpreted-correctly/)
  * Confidence Intervals: [Khan Academy - Confidence Intervals](https://www.khanacademy.org/math/statistics-probability/confidence-intervals-one-sample)
  * Type I/II Errors & Power: [Blog Post: Type I & Type II Errors | Differences, Examples, Visualizations](https://www.google.com/search?q=https://statisticsbyjim.com/hypothesis-testing/type-i-type-ii-errors/)
  * Python Libraries:
      * `scipy.stats`: [Statistical functions documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) (e.g., `ttest_ind`, `norm.interval`)
      * `statsmodels`: [Statistics in Python documentation](https://www.statsmodels.org/stable/index.html), especially [Power and Sample Size Calculation](https://www.google.com/search?q=https://www.statsmodels.org/stable/stats.html%23power-and-sample-size-calculations)

-----

### Exercise 1: Formulating Hypotheses

**Goal:** Practice setting up the null (H0) and alternative (H1) hypotheses for common A/B testing scenarios.
**Instructions:**

1.  Define **Null Hypothesis (H0)** and **Alternative Hypothesis (H1)** in the context of statistical testing. What does each typically represent in an A/B test?
2.  Consider an A/B test where a website changes the color of a "Buy Now" button from blue (Control, Group A) to green (Treatment, Group B). The primary metric is the click-through rate (CTR). Formulate the H0 and H1 for a two-tailed test comparing the CTRs.
3.  Consider an A/B test evaluating if a new recommendation algorithm (Treatment, Group B) increases the average session duration compared to the old algorithm (Control, Group A). Formulate the H0 and H1 for a one-tailed test (specifically testing for an *increase*).
4.  Explain why clearly defining H0 and H1 *before* running the experiment is crucial.

### Exercise 2: Calculating and Interpreting p-values

**Goal:** Calculate p-values for common statistical tests and interpret their meaning correctly.
**Instructions:**

1.  Define **p-value**. What does it represent under the assumption that the null hypothesis (H0) is true?
2.  Assume you ran an A/B test comparing conversion rates. Control group (A): 100 conversions out of 1000 users. Treatment group (B): 125 conversions out of 1000 users.
      * Use Python's `statsmodels.stats.proportion.proportions_ztest` or `scipy.stats` equivalent to perform a two-proportion z-test comparing the conversion rates.
      * Report the calculated p-value.
3.  Set a significance level (alpha) of α = 0.05. Based on the calculated p-value, would you reject or fail to reject the null hypothesis (that the conversion rates are the same)? Explain your reasoning.
4.  Explain common misinterpretations of the p-value (e.g., "the probability that H0 is true", "the probability that H1 is true"). State the correct interpretation.

### Exercise 3: Calculating and Interpreting Confidence Intervals (CIs)

**Goal:** Calculate confidence intervals for means or proportions and interpret their meaning.
**Instructions:**

1.  Define **Confidence Interval**. What does a 95% confidence interval represent in the long run (frequentist interpretation)?
2.  Assume an A/B test measured user engagement scores. Control group (A) mean score = 75, standard deviation = 10, n = 100. Treatment group (B) mean score = 78, standard deviation = 12, n = 100.
      * Calculate the 95% confidence interval for the *difference in means* between Group B and Group A. Use `scipy.stats.ttest_ind` (it returns the p-value, but you can derive the CI using the standard error of the difference) or functions from `statsmodels`.
3.  Interpret the calculated confidence interval. Does it contain zero? What does this suggest about the statistical significance of the difference at the α = 0.05 level?
4.  How does the width of the confidence interval relate to sample size and data variability?

### Exercise 4: Understanding Type I and Type II Errors

**Goal:** Define Type I and Type II errors in hypothesis testing and their relationship with the significance level (alpha).
**Instructions:**

1.  Define **Type I Error**. What is the probability of making a Type I error, denoted by α? What decision is made regarding H0 when a Type I error occurs? Relate this to a "false positive".
2.  Define **Type II Error**. What is the probability of making a Type II error, denoted by β? What decision is made regarding H0 when a Type II error occurs? Relate this to a "false negative".
3.  Consider the A/B test scenario from Exercise 1 (button color change). Describe what would constitute a Type I error in this specific context. Describe what would constitute a Type II error.
4.  How does changing the significance level α (e.g., from 0.05 to 0.01) affect the probability of Type I error (α) and the probability of Type II error (β)?

### Exercise 5: Statistical Power Analysis

**Goal:** Understand statistical power and perform basic power calculations to determine required sample size or minimum detectable effect.
**Instructions:**

1.  Define **Statistical Power (1 - β)**. What does it represent? Why is achieving adequate power (e.g., 80%) important when designing an experiment?
2.  Assume you want to detect a 2% absolute increase in conversion rate (e.g., from a baseline of 10% to 12%) in an A/B test. You require 80% power (β = 0.20) and will use a significance level α = 0.05 (two-tailed).
      * Use Python's `statsmodels.stats.power.NormalIndPower().solve_power` (or specifically `zt_ind_solve_power` for proportions approximation) to calculate the required sample size (`nobs1`, assuming equal size groups `nobs2=nobs1`) per group.
3.  Now assume you only have budget/time for 5000 users per group. Keeping α = 0.05 and power = 0.80, what is the minimum detectable effect (MDE) size (difference in proportions) you can reliably detect? Use `solve_power` again, this time solving for `effect_size`.
4.  Explain qualitatively how baseline conversion rate, desired power, significance level, and minimum detectable effect influence the required sample size.
