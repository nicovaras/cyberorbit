
## Subtopic 4.2: Designing Robust A/B/n Tests

**Goal:** To learn the principles and practical considerations for designing statistically sound and reliable A/B/n experiments, including randomization, sample size determination, metric selection, segmentation, and handling common pitfalls.

**Resources:**

  * Experimentation Platform Guides (Conceptual):
      * [Optimizely: Experimentation Strategy](https://www.google.com/search?q=https://www.optimizely.com/optimization-glossary/experimentation-strategy/)
      * [VWO: A/B Testing Guide](https://vwo.com/ab-testing/)
  * Sample Size Calculators: [Evan Miller's Sample Size Calculator](https://www.evanmiller.org/ab-testing/sample-size.html) (Good explanations)
  * Statistical Significance vs Practical Significance: [Blog Post: Statistical Significance vs Practical Significance](https://www.google.com/search?q=https://statisticsbyjim.com/hypothesis-testing/statistical-significance-practical-significance/)
  * Common Pitfalls: [Blog Post: Common A/B Testing Pitfalls](https://www.google.com/search?q=https://vwo.com/blog/common-ab-testing-mistakes/) (Or similar reputable articles)
  * Metrics Selection: [HubSpot Blog: Choosing the Right Metrics for A/B Testing](https://www.google.com/search?q=https://blog.hubspot.com/marketing/metrics-a-b-testing)

-----

### Exercise 1: Randomization Units and Strategies

**Goal:** Understand different units of randomization and the importance of consistent assignment.
**Instructions:**

1.  Define **Randomization Unit** (or Unit of Diversion). Provide examples of common units used in online experiments (e.g., user ID, session ID, cookie ID, device ID, page view).
2.  Discuss the pros and cons of using **User ID** vs. **Session ID** as the randomization unit. Consider consistency of user experience and potential interference effects.
3.  Explain why it's crucial that once a unit (e.g., a user) is assigned to a group (A or B), they consistently see that version for the duration of the experiment (unless the experiment design specifically intends otherwise). What problems can inconsistent assignment cause?
4.  Describe **Stratified Randomization**. When might you use it? (e.g., ensuring balance across key segments like new vs. returning users, or high-value vs. low-value customers).

### Exercise 2: Sample Size Calculation for a Specific Goal

**Goal:** Apply power analysis concepts (from 4.1) to calculate the necessary sample size for a planned A/B test.
**Instructions:**

1.  You plan to test a new feature expected to increase the user conversion rate (e.g., sign-ups). The current baseline conversion rate (BCR) is 5%.
2.  You want to be able to detect a minimum absolute improvement of 1% (i.e., increase the rate to 6%). This is your Minimum Detectable Effect (MDE).
3.  You require a statistical power of 80% (1 - β = 0.80) and will use a significance level of α = 0.05 (two-tailed).
4.  Use an online sample size calculator (like Evan Miller's linked above) or Python's `statsmodels.stats.power` functions (e.g., `zt_ind_solve_power`) to calculate the required sample size per variation (assuming two variations: Control and Treatment).
5.  How does the required sample size change if you only needed to detect a 2% absolute improvement (from 5% to 7%)? Recalculate.
6.  How does the required sample size change if the baseline conversion rate was much higher, say 50%, but you still wanted to detect a 1% absolute improvement (to 51%)? Recalculate and explain the difference.

### Exercise 3: Defining Primary, Secondary, and Guardrail Metrics

**Goal:** Understand the different roles metrics play in evaluating an experiment's success and potential side effects.
**Instructions:**

1.  Define **Primary Metric** (or Key Metric). Why is it crucial to choose *one* primary metric before starting the test? What characteristics should a good primary metric have?
2.  Define **Secondary Metrics**. What is their purpose? How should results for secondary metrics be interpreted, especially if the primary metric doesn't show a significant effect?
3.  Define **Guardrail Metrics** (or Counter Metrics / Health Metrics). What is their purpose? Provide examples of common guardrail metrics for a website experiment (e.g., page load time, error rates, bounce rate, unsubscribe rate). What action should be taken if a guardrail metric shows a significant negative change?
4.  For an experiment testing a change to a website's checkout flow aimed at increasing purchase completion rate: propose one primary metric, two secondary metrics, and two guardrail metrics. Justify your choices.

### Exercise 4: Segmentation and Analyzing Results

**Goal:** Understand the purpose and potential pitfalls of analyzing experiment results across different user segments.
**Instructions:**

1.  Why might you want to analyze A/B test results for specific user segments (e.g., new vs. returning users, users on mobile vs. desktop, users from different geographic regions)?
2.  Explain the potential danger of "p-hacking" or finding spurious significant results if you analyze too many segments after the experiment without pre-specification.
3.  Describe a more statistically sound approach to segmentation analysis (e.g., pre-registering hypotheses for specific key segments before running the test).
4.  If an overall result is non-significant, but a pre-specified key segment shows a large significant positive effect, how might you interpret this and decide on next steps?

### Exercise 5: Identifying and Mitigating Common Issues

**Goal:** Recognize potential problems that can invalidate A/B test results, such as novelty effects or instrumentation errors.
**Instructions:**

1.  Define the **Novelty Effect**. How can it temporarily inflate the apparent positive impact of a new feature? Suggest one way to mitigate or account for the novelty effect when analyzing results (e.g., running the test longer, analyzing cohorts over time).
2.  Define **Instrumentation Bias** or Tracking Errors. Give an example of how incorrect event tracking could lead to misleading A/B test results. What process should be in place before launching an experiment to minimize this risk? (Hint: QA, AA testing).
3.  Explain the purpose of running an **A/A Test**. What results would you expect to see? What might it indicate if an A/A test shows statistically significant differences between the identical groups?
4.  Define the **Primacy Effect** or Learning Effect. How does it differ from the novelty effect? When might it be a concern?

