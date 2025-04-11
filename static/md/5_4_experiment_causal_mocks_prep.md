
## Subtopic 5.4: Complex Experiment Design & Causal Inference Mocks Prep

**Goal:** To prepare for mock interview rounds focused on designing experiments for complex situations (e.g., network effects, marketplaces, long-term effects) and applying causal inference methods when A/B testing is infeasible.

**Resources:**

  * Advanced Experimentation Concepts:
      * Interference in A/B Testing: [Articles/papers on network effects, interference, cluster randomization](https://www.google.com/search?q=https://booking.ai/understanding-interference-in-online-experiments-a-guide-for-practitioners-9b2080297537) (Or similar resources)
      * CUPED Technique: [Microsoft Blog: Improving Experiment Sensitivity with CUPED](https://www.google.com/search?q=https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/improving-experiment-power-through-control-using-cuped/)
      * Long-term effects: [Articles discussing challenges and methods for measuring long-term impact](https://www.google.com/search?q=https://towardsdatascience.com/measuring-long-term-impact-in-a-b-tests-cd8d69b62d8a)
  * Causal Inference Application:
      * Module 4 Resources (DiD, RDD, IV).
      * Case studies applying quasi-experimental methods (search academic/industry blogs).
  * Interview Question Examples: Search for "Staff Data Scientist Experiment Design Interview Questions".

-----

### Exercise 1: Designing Experiments with Network Effects/Interference

**Goal:** Prepare to design experiments for products where users' experiences influence each other (e.g., social networks, marketplaces).
**Instructions:**

1.  Define **Interference** (or spillover/network effects) in the context of A/B testing. Why does standard user-level randomization often lead to biased results when interference is present?
2.  Describe at least two alternative randomization strategies to mitigate interference. Examples:
      * **Cluster Randomization:** Randomizing groups of connected users (e.g., by geography, by social clusters). What are the trade-offs (e.g., reduced statistical power)?
      * **Ego-Cluster Randomization / Graph-Based Randomization:** More complex methods involving network structure. (Conceptual understanding is sufficient).
3.  Consider designing an experiment to test a new feed ranking algorithm on a social media app. Outline the challenges posed by network effects (e.g., seeing a friend's engaging post might affect your own engagement, regardless of which algorithm ranked it for you). Propose a suitable randomization strategy and justify your choice. Discuss how you would measure the effect.

### Exercise 2: Designing Experiments for Two-Sided Marketplaces

**Goal:** Prepare to design experiments in platforms connecting two distinct user groups (e.g., ride-sharing, e-commerce marketplaces, food delivery).
**Instructions:**

1.  Describe the challenges of experimenting in a two-sided marketplace (e.g., ride-sharing app testing a new pricing algorithm for drivers). How might a change affecting one side (drivers) impact the other side (riders) and the overall platform health (liquidity)?
2.  Propose an experimental design for the ride-sharing pricing example. Consider:
      * **Randomization Unit:** User, driver, trip, geographic region? Justify your choice.
      * **Metrics:** What primary metric(s) would you track for drivers? For riders? For the platform overall (e.g., completed trips, wait times, surge pricing frequency)? Identify key guardrail metrics for both sides.
      * **Potential Interference:** How might interference occur (e.g., drivers moving between treated/control areas)? How might you mitigate or measure it?
      * **Analysis:** How would you analyze the results considering impacts on both sides of the marketplace?

### Exercise 3: Handling Long-Term Effects & Sequential Testing

**Goal:** Prepare to discuss approaches for measuring long-term impact and the pitfalls of sequential testing if not done correctly.
**Instructions:**

1.  Why might the short-term effect measured in a standard 2-week A/B test differ from the long-term impact of a change? Give examples (e.g., novelty effects wearing off, users adapting behavior, impact on retention/LTV).
2.  Describe one strategy for estimating longer-term effects. Examples:
      * Running experiments for longer durations (pros/cons?).
      * Using surrogate metrics highly correlated with long-term outcomes.
      * Using causal inference methods on observational data post-launch (mention limitations).
      * Analyzing specific user cohorts over time after the initial experiment ends.
3.  Explain **Sequential Testing** (e.g., using sequential probability ratio test - SPRT, or Bayesian methods). What is the potential benefit compared to fixed-horizon tests?
4.  Why is naively "peeking" at p-values repeatedly during a fixed-horizon test statistically invalid? How do formal sequential testing methods properly adjust for this? (Conceptual understanding).

### Exercise 4: Applying Causal Inference in Mock Scenarios

**Goal:** Prepare to propose and defend the use of quasi-experimental methods when A/B testing is not feasible in an interview setting.
**Instructions:**

1.  Consider a scenario: A competitor launched a major marketing campaign in specific cities last month. You want to estimate the impact of their campaign on your company's user sign-ups in those cities using only your internal data (you cannot run an A/B test on their campaign).
      * Which quasi-experimental method (DiD, RDD, IV) seems most applicable? Justify your choice.
      * What data would you need? What would be your treatment and control groups? What is the "pre" and "post" period?
      * What is the key identifying assumption you would need to make? How could you gather evidence to support (or refute) this assumption using data from *before* the competitor's campaign launch?
      * Outline the analysis steps.
2.  Consider another scenario: A new data privacy law went into effect on a specific date, requiring users above a certain age threshold (e.g., 18) to give extra consent, potentially impacting engagement. You want to estimate the causal impact of this law/consent requirement on user engagement (e.g., time spent).
      * Which quasi-experimental method seems most applicable? Identify the running variable, cutoff, and treatment.
      * What is the key assumption? How would you visually test it?
      * What are potential threats to the validity of this approach?

### Exercise 5: Critiquing Experimental Designs

**Goal:** Prepare to analyze and critique potentially flawed experimental designs presented during an interview.
**Instructions:**

1.  Review common A/B testing pitfalls (from Subtopic 4.2) and quasi-experimental assumptions (from 4.4 and 4.3).
2.  Consider the following hypothetical design: "To test our new recommendation algorithm, we deployed it to all users in California (treatment) for one week and compared their engagement metrics to users in Oregon (control) during the same week."
      * Identify at least three major flaws or questionable assumptions in this design. Explain *why* they are problematic for inferring the causal effect of the algorithm. (Hint: Selection bias, non-random assignment, confounding variables, short duration).
      * Suggest a more robust experimental design (e.g., randomized rollout within states, longer duration, A/A test first).
3.  Consider another design: "We ran an A/B test for 4 weeks. After week 1, the p-value was 0.04 so we stopped the test and declared victory."
      * Explain why this approach ("peeking") inflates the Type I error rate and is statistically invalid.
4.  Prepare to articulate critiques clearly and constructively, focusing on the underlying assumptions being violated.

### Portfolio/Practice Guidance: Documenting Practice Scenarios

**Goal:** Structure detailed analyses of complex experiment design or causal inference scenarios for review.
**Instructions:**

1.  For each scenario practiced (network effects, marketplace, long-term, causal inference applications, critiques):
      * Clearly state the problem/scenario.
      * Document your proposed design or analysis plan step-by-step.
      * Justify your methodological choices (e.g., why cluster randomization? why DiD?).
      * Explicitly state the key assumptions required for your approach to be valid.
      * Discuss potential limitations, threats to validity, and how you might mitigate them or check assumptions.
      * Include diagrams where helpful.
2.  Organize these documented scenarios for review, focusing on the reasoning process.


