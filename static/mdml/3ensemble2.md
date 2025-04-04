## 倹 Subtopic 3.6: Ensemble Methods: Stacking & Blending

**Goal:** Implement stacking and blending techniques to combine predictions from multiple diverse base models using a meta-learner, aiming for improved performance over individual models.

**Resources:**

* **Scikit-learn Ensemble Methods:** [StackingCVClassifier/Regressor](https://raschka-mlxtend.github.io/mlxtend-ref/user_guide/classifier/StackingCVClassifier/) (from mlxtend library, common example), [StackingRegressor/Classifier](https://scikit-learn.org/stable/modules/ensemble.html#stacking) (built-in)
* **Stacking Explained:** [Blog Post with Code Example](https://machinelearningmastery.com/stacking-ensemble-machine-learning-with-python/)
* **Blending Explanation:** [Difference between Stacking and Blending](https://vitalflux.com/stacking-vs-blending-ensemble-learning-explained/)

---

### 隼 **Exercise 1: Stacking Workflow (Manual Implementation)**

**Goal:** Manually implement the stacking procedure using cross-validation to generate meta-features and train a meta-learner.

**Instructions:**

1.  Load a dataset (classification or regression). Split into training and test sets.
2.  Choose several diverse **base models** (Level 0 models), e.g., Logistic Regression, Random Forest, LightGBM, k-NN.
3.  Choose a **meta-learner** (Level 1 model), often a simple model like Logistic Regression, Ridge, or Linear SVM.
4.  **Generate Meta-Features:**
    * Set up K-Fold cross-validation (e.g., 5 folds) on the **training set**.
    * Initialize empty arrays (out-of-fold predictions) to store meta-features for the training data, one array per base model.
    * Initialize empty arrays/lists to store test set predictions from each base model trained on different folds.
    * Loop through the CV folds:
        * Split the training data into inner-train and inner-validation folds.
        * Train each base model on the inner-train fold.
        * Generate predictions from each trained base model on the corresponding inner-validation fold. Store these predictions in the correct rows of the out-of-fold prediction arrays.
        * Generate predictions from each trained base model on the **entire original test set**. Store these test set predictions (you'll average them later).
5.  You now have out-of-fold predictions for the training set (these are your meta-features for training the meta-learner). Average the test set predictions made by each base model across the different folds.
6.  **Train Meta-Learner:** Train the chosen meta-learner using the generated out-of-fold predictions (meta-features) as input `X` and the original training set target `y` as the target.
7.  **Final Prediction:** Use the trained meta-learner to make predictions on the averaged test set predictions obtained in step 5. Evaluate performance on the test set labels.
8.  **Challenge:** Compare the stacking ensemble's performance to the performance of the best individual base model. Did stacking provide an improvement?

---

### 隼 **Exercise 2: Stacking with Scikit-learn (`StackingClassifier`/`StackingRegressor`)**

**Goal:** Use scikit-learn's built-in stacking implementation for convenience.

**Instructions:**

1.  Load the same dataset as Exercise 1.
2.  Choose your list of base models (`estimators`) – provide them as a list of tuples `[('name1', model1), ('name2', model2), ...]`.
3.  Choose your meta-learner (`final_estimator`).
4.  Instantiate `sklearn.ensemble.StackingClassifier` or `StackingRegressor`:
    * Pass the `estimators` list.
    * Pass the `final_estimator`.
    * Specify the cross-validation strategy to use for generating meta-features (`cv`, e.g., 5 or a CV object).
    * Specify how predictions are passed to the meta-learner (`passthrough=True` to include original features, `passthrough=False` to use only base model predictions).
5.  Train the stacking model directly using `fit(X_train, y_train)`.
6.  Generate predictions using `predict(X_test)`.
7.  Evaluate the performance. Compare the ease of implementation to the manual approach in Exercise 1.
8.  **Challenge:** Experiment with the `stack_method` parameter ('auto', 'predict_proba', 'decision_function', 'predict'). How does using probabilities vs. direct predictions as meta-features affect the performance, especially if the meta-learner is linear?

---

### 隼 **Exercise 3: Blending Implementation**

**Goal:** Implement the blending ensemble technique, which uses a separate holdout set to train the meta-learner.

**Instructions:**

1.  Load a dataset. Split it into three sets: Training set, Validation set (Holdout set for meta-learner training, e.g., 15-20% of original data), and Test set.
2.  Choose diverse base models and a meta-learner.
3.  **Train Base Models:** Train each base model on the **Training set**.
4.  **Generate Meta-Features:**
    * Generate predictions from each trained base model on the **Validation set**. These predictions form the input features (`X_meta_train`) for the meta-learner.
    * Generate predictions from each trained base model on the **Test set**. These predictions form the input features (`X_meta_test`) for the final prediction step.
5.  **Train Meta-Learner:** Train the meta-learner using `X_meta_train` as input and the true labels of the **Validation set** (`y_validation`) as the target.
6.  **Final Prediction:** Use the trained meta-learner to make predictions on `X_meta_test`. Evaluate performance on the test set labels.
7.  Compare blending's performance and implementation complexity to stacking (Exercise 1 or 2).
8.  Discuss the pros and cons of blending vs. stacking. Why might blending be simpler to implement but potentially use less data effectively for training base models?
9.  **Challenge:** How sensitive is blending performance to the size of the validation (holdout) set used for training the meta-learner?

---

### 隼 **Exercise 4: Multi-Level Stacking**

**Goal:** Conceptualize and potentially implement a stacking ensemble with more than two levels.

**Instructions:**

1.  Describe the concept of **Multi-Level Stacking** (e.g., 3 levels):
    * Level 0: Base models trained on original data, generate out-of-fold predictions (Meta-Features 1).
    * Level 1: Meta-learners trained on Meta-Features 1, generate out-of-fold predictions (Meta-Features 2).
    * Level 2: Final meta-learner trained on Meta-Features 2.
2.  Discuss the potential benefits (capturing more complex interactions between model predictions) and drawbacks (increased complexity, risk of overfitting, diminishing returns) of adding more stacking levels.
3.  **Implementation (Optional/Conceptual):** Outline the steps required to implement a 3-level stacking ensemble manually, focusing on how cross-validation and out-of-fold prediction generation would work at each level to prevent leakage.
4.  **Challenge:** What kind of diversity would you aim for when selecting models for different levels in a multi-level stack? Should Level 1 models be different from Level 0 models?

---

### 隼 **Exercise 5: Choosing Base Models and Meta-Learner**

**Goal:** Develop intuition for selecting appropriate base models and meta-learners for stacking/blending ensembles.

**Instructions:**

1.  Discuss the importance of **diversity** among base models in an ensemble. Why does combining predictions from accurate but *different* models often lead to better performance than combining predictions from similar models? List ways to achieve diversity (different algorithms, different hyperparameters, different feature subsets, different training data subsets).
2.  What are the characteristics of a good **base model** for stacking/blending? (Should generally be as accurate as possible, but diversity is key).
3.  What are the characteristics of a good **meta-learner**? Why are simple, stable models (like Logistic Regression, Ridge, Linear SVM) often preferred? What are the risks of using a very complex meta-learner?
4.  Consider a scenario where your base models include a Tree-based model (Random Forest), a Linear model (Logistic Regression), and a k-NN model. Would a Linear Regression meta-learner be a reasonable choice? Why? Would a complex Gradient Boosting model as a meta-learner be risky? Why?
5.  **Challenge:** How might you use feature importance from the *meta-learner* to understand which base models are contributing most effectively to the final stacked prediction?

---