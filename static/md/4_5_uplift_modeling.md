
## Subtopic 4.5: Uplift Modeling Techniques and Evaluation

**Goal:** To understand the objective of uplift modeling (estimating heterogeneous treatment effects or CATE), learn basic techniques like the two-model approach, and understand specific evaluation metrics like the Qini curve.

**Resources:**

  * Uplift Modeling Introduction:
      * [Wikipedia - Uplift Modelling](https://en.wikipedia.org/wiki/Uplift_modelling)
      * [Paperspace Blog: Introduction to Uplift Modeling](https://www.google.com/search?q=https://blog.paperspace.com/uplift-modeling/)
  * Two-Model Approach Explained: [Tutorial or article explaining the two-model/separate model approach](https://www.google.com/search?q=https://towardsdatascience.com/a-quick-uplift-modeling-introduction-6e14de7ac73_ "or similar")
  * Evaluation Metrics:
      * Qini/Uplift Curves Explained: [Blog Post: Evaluating Uplift Models: Qini and Uplift Curves](https://www.google.com/search?q=https://towardsdatascience.com/evaluating-uplift-models-f38274757155)
  * Python Libraries (Explore documentation, usage might be advanced):
      * `CausalML`: [CausalML Documentation](https://causalml.readthedocs.io/en/latest/)
      * `pylift`: [pylift Documentation (Wayfair)](https://pylift.readthedocs.io/en/latest/)

-----

### Exercise 1: Define Uplift and CATE

**Goal:** Understand the target quantity estimated by uplift models.
**Instructions:**

1.  Define **Uplift** (also known as Conditional Average Treatment Effect - CATE, Incremental Impact, Net Lift, True Lift). How does it differ from simply predicting the outcome itself?
2.  Using the Potential Outcomes notation (`Y(1)`, `Y(0)`), write the formula for the uplift (CATE) for an individual (or group) with specific characteristics `X`: `Uplift(X) = E[Y(1) | X] - E[Y(0) | X]`.
3.  Explain in practical terms what a positive uplift score for a customer segment means in a marketing campaign context (e.g., targeting with an offer vs. not targeting). What does a negative uplift score (sometimes called "sleeping dogs") imply? What does a near-zero uplift imply ("sure things" or "lost causes")?
4.  Why is estimating uplift more valuable for targeted interventions (like marketing or personalized medicine) than simply predicting the outcome `E[Y|X]` or the average treatment effect (ATE)?

### Exercise 2: The Two-Model Approach (TMA)

**Goal:** Understand and implement the logic of the simple Two-Model Approach for uplift estimation.
**Instructions:**

1.  Describe the **Two-Model Approach** (or Separate Model Approach). What are the two models that are trained?
      * Model 1: Trained on which group (Treatment or Control)? What does it predict (`P(Outcome | X, Treated)`)?
      * Model 2: Trained on which group (Treatment or Control)? What does it predict (`P(Outcome | X, Control)`)?
2.  How is the uplift score for a new individual with characteristics `X` calculated using the predictions from these two models? `Uplift(X) = Prediction_Model1(X) - Prediction_Model2(X)`.
3.  Assume you have A/B test data (or observational data where treatment assignment is conditionally random given X) with features `X`, a binary treatment indicator `T`, and a binary outcome `Y`. Outline the steps to implement the TMA:
      * Split data into Treatment (T=1) and Control (T=0) subsets.
      * Choose a base ML algorithm (e.g., Logistic Regression, RandomForestClassifier).
      * Train Model 1 on the Treatment subset to predict Y.
      * Train Model 2 on the Control subset to predict Y.
      * For prediction on new data, get scores from both models and subtract.
4.  What is a potential drawback of this approach? (Hint: Errors from two separate models might compound).

### Exercise 3: Data Requirements for Uplift Modeling

**Goal:** Understand the type of data needed to train and evaluate uplift models.
**Instructions:**

1.  What is the ideal type of data for training an uplift model? Why? (Hint: Randomized Experiment / A/B Test data).
2.  Explain why simply having observational data (where treatment assignment wasn't random) is problematic for training unbiased uplift models. What issue arises? (Hint: Confounding).
3.  What specific information must the dataset contain to train an uplift model using methods like the Two-Model Approach? List the essential columns (e.g., features `X`, treatment indicator `T`, outcome `Y`).
4.  For *evaluating* uplift models using metrics like the Qini curve, why is it essential to have data where the outcome is observed for *both* treated and control individuals (even if for different, comparable groups)?

### Exercise 4: Evaluating Uplift Models - Qini/Uplift Curves (Conceptual)

**Goal:** Understand the purpose and interpretation of uplift evaluation curves like the Qini curve.
**Instructions:**

1.  Why can't standard classification metrics (like Accuracy, Precision, Recall, AUC) be directly used to evaluate how well a model ranks individuals by their *uplift*?
2.  Describe the process of generating an **Uplift Curve** or **Qini Curve** conceptually:
      * Take a validation dataset with known treatment assignments and outcomes.
      * Use the trained uplift model to score all individuals in the validation set.
      * Sort the individuals in descending order based on their predicted uplift scores.
      * Iterate through the sorted population (e.g., by deciles or percentiles).
      * For each percentile, calculate the cumulative actual incremental gain (e.g., `(Outcome Count in Treat Group - Outcome Count in Control Group)` within that percentile, scaled appropriately).
      * Plot this cumulative gain against the population percentile.
3.  How do you interpret the Uplift/Qini curve? What does a curve that rises steeply and then flattens indicate? What does a curve close to the diagonal (random targeting) indicate? What does a curve going below the diagonal indicate?
4.  Define the **Qini coefficient**. How does it summarize the uplift curve, similar to how AUC summarizes the ROC curve? What does a higher Qini coefficient imply?

### Project: Implement and Evaluate Two-Model Uplift

**Goal:** Build a simple uplift model using the Two-Model Approach and evaluate it conceptually using predicted scores.
**Instructions:**

1.  Find or simulate a dataset suitable for uplift modeling (requires features X, treatment T, outcome Y, ideally from an A/B test). You might need to simulate this, ensuring some features influence the treatment effect.
2.  Implement the Two-Model Approach (Exercise 2):
      * Split data into train/test sets.
      * Split the training set into treatment and control groups.
      * Train two separate classification models (e.g., `LogisticRegression` or `RandomForestClassifier` from scikit-learn) on the respective groups.
      * Predict probabilities (`predict_proba`) for the *test* set using *both* models.
      * Calculate the predicted uplift score for each instance in the test set (P(Y=1|X,T=1) - P(Y=1|X,T=0)).
3.  Analyze the distribution of predicted uplift scores (e.g., histogram).
4.  (Conceptual Evaluation) Sort the test set by predicted uplift score in descending order. Examine the actual outcomes (Y) and treatment assignments (T) for the top \~10% of individuals (highest predicted uplift) versus the bottom \~10% (lowest predicted uplift). Does the top group appear to have a higher actual treatment effect (higher outcome rate difference between treated and control) than the bottom group? This provides a basic sanity check, though a proper Qini curve requires more calculation.
    **Portfolio Guidance:**


  * Structure your work in a Jupyter Notebook.
  * Clearly describe the dataset (or simulation process).
  * Show the code for implementing the Two-Model Approach.
  * Include the histogram of predicted uplift scores.
  * Provide the qualitative analysis comparing the top vs. bottom predicted uplift groups.
  * Discuss the limitations of the TMA and the conceptual evaluation performed.
  * Upload the notebook and any data/simulation code to GitHub.

