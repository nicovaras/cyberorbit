## Subtopic 4.3: Introduction to Causal Inference Frameworks

**Goal:** To understand the fundamental concepts differentiating correlation from causation, introduce the Potential Outcomes framework (Rubin Causal Model), define key causal effects (like ATE), and recognize the problem of confounding using basic Directed Acyclic Graphs (DAGs).

**Resources:**

  * Correlation vs Causation: Simple Explanations & Examples (Numerous online articles/videos)
  * Potential Outcomes Framework:
      * Wikipedia: [Rubin Causal Model](https://en.wikipedia.org/wiki/Rubin_causal_model)
      * Book Chapter/Article explaining Potential Outcomes, Counterfactuals, SUTVA (e.g., from "Causal Inference: The Mixtape" or online course notes)
  * Confounding Bias: [Wikipedia - Confounding](https://en.wikipedia.org/wiki/Confounding)
  * Directed Acyclic Graphs (DAGs):
      * Introduction to DAGs for Causal Inference: [Blog Post: A Crash Course in Causality: Inferring Causal Effects from Observational Data](https://www.google.com/search?q=https://towardsdatascience.com/a-crash-course-in-causality-6b1221984694) (Or similar introductory articles)
      * DAG Drawing Tool: [dagitty.net](https://www.google.com/search?q=http://dagitty.net/dags.html)

-----

### Exercise 1: Correlation vs. Causation

**Goal:** Differentiate between correlation and causation using examples.
**Instructions:**

1.  Define **Correlation**. What does it mean for two variables to be correlated? Does correlation imply a specific direction of influence?
2.  Define **Causation**. What does it mean for one variable (A) to cause another variable (B)?
3.  Provide an example of two variables that are likely correlated but where neither causes the other (i.e., correlation due to a common cause or **confounder**). Example: Ice cream sales and crime rates. What might be the common cause?
4.  Provide an example where correlation might exist due to **reverse causation** (B causes A, rather than A causing B). Example: Wearing a helmet and having a head injury (among people who had accidents).
5.  Explain why establishing causation typically requires more than just observing a correlation, often necessitating experimental or quasi-experimental methods.

### Exercise 2: Potential Outcomes Framework

**Goal:** Understand the concepts of potential outcomes, counterfactuals, and the fundamental problem of causal inference.
**Instructions:**

1.  Define the **Potential Outcomes** framework (Rubin Causal Model). For an individual unit `i` and a binary treatment `T` (T=1 for treated, T=0 for control), define `Y_i(1)` and `Y_i(0)`. What do these represent?
2.  Define the **Counterfactual Outcome**. For an individual `i` who actually received the treatment (`T_i = 1`), which potential outcome is observed, and which is the counterfactual (unobserved)?
3.  What is the **Fundamental Problem of Causal Inference** as described by this framework? Why can we typically not observe both potential outcomes for the same unit at the same time?
4.  Define the **Individual Treatment Effect (ITE)** for unit `i` using potential outcomes: `ITE_i = Y_i(1) - Y_i(0)`. Why can we usually not calculate the ITE directly?

### Exercise 3: Defining Average Treatment Effect (ATE)

**Goal:** Define the Average Treatment Effect (ATE) and explain how randomization helps estimate it.
**Instructions:**

1.  Define the **Average Treatment Effect (ATE)** for a population using the expected value of potential outcomes: `ATE = E[Y(1) - Y(0)] = E[Y(1)] - E[Y(0)]`. What does the ATE represent?
2.  In a **randomized controlled trial (RCT)** or a well-designed A/B test, participants are randomly assigned to Treatment (T=1) or Control (T=0). Explain why, under randomization, the observed average outcome in the treatment group `E[Y | T=1]` is a good estimate for `E[Y(1)]`, and the observed average outcome in the control group `E[Y | T=0]` is a good estimate for `E[Y(0)]`. (Hint: Randomization makes the groups comparable on average *before* the treatment is applied).
3.  How can we estimate the ATE using the observable data from an RCT? (Hint: Difference in means between the groups).
4.  What assumption is crucial for this estimation to work (often implied by randomization)? (Hint: Ignorability, Unconfoundedness, or "No unmeasured confounders").

### Exercise 4: Identifying Confounding Variables

**Goal:** Understand confounding bias and identify potential confounders in observational scenarios.
**Instructions:**

1.  Define **Confounding Variable** (or Confounder). What are the key properties of a confounder in relation to the treatment and the outcome? (Hint: Associated with both).
2.  Consider an observational study looking at the relationship between drinking coffee (Treatment) and heart disease (Outcome). We observe that coffee drinkers have a higher rate of heart disease. Identify at least one potential confounding variable that might explain this association, rather than coffee directly causing heart disease. Explain how this variable meets the definition of a confounder. (Example confounder: Smoking).
3.  Explain why failing to account for confounders in observational studies leads to **biased estimates** of the true causal effect of the treatment on the outcome.
4.  How does randomization in an RCT address the problem of confounding (both known and unknown confounders)?

### Exercise 5: Introduction to Directed Acyclic Graphs (DAGs)

**Goal:** Represent causal assumptions using simple DAGs and identify basic paths.
**Instructions:**

1.  What do **nodes** (vertices) represent in a DAG used for causal inference?
2.  What do **directed edges** (arrows) represent? Why must the graph be **acyclic**?
3.  Draw a simple DAG representing the scenario from Exercise 4: Coffee Drinking (T), Heart Disease (Y), and Smoking (C) as a confounder. Show the arrows representing the assumed causal relationships (e.g., C -\> T, C -\> Y, potentially T -\> Y).
4.  Define a **path** between two nodes in a DAG. Define a **directed path**.
5.  In your drawn DAG, identify the directed path (if any) from T to Y. Identify the indirect path from T to Y that goes through the confounder C. This indirect, non-causal path is often called a **backdoor path**. Explain why this backdoor path introduces bias when estimating the effect of T on Y by simply comparing outcomes between coffee drinkers and non-drinkers.
