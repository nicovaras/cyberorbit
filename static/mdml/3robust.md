## 倹 Subtopic 3.1: Robust Cross-Validation & Leakage Detection

**Goal:** Implement and understand advanced cross-validation techniques suited for complex data dependencies (time series, groups) and develop strategies to detect and prevent target leakage.

**Resources:**

* **Scikit-learn Cross-validation:** [User Guide](https://scikit-learn.org/stable/modules/cross_validation.html) (See TimeSeriesSplit, GroupKFold, StratifiedGroupKFold)
* **Kaggle Course on Leakage:** [Data Leakage](https://www.kaggle.com/code/alexisbcook/data-leakage)
* **Adversarial Validation Explanation:** [FastML Article](https://fastml.com/adversarial-validation-part-one/)
* **Target Encoding Leakage:** [Explanation of risks](https://medium.com/@pouryaayria/kfold-target-encoding-dfe9a594874b)

---

### 隼 **Exercise 1: Time Series Cross-Validation**

**Goal:** Implement cross-validation for time series data ensuring that validation folds always come *after* training folds to prevent lookahead bias.

**Instructions:**

1.  Create or load a time series dataset (e.g., stock prices, sales data). Ensure it has a time index.
2.  Instantiate scikit-learn's `TimeSeriesSplit` cross-validator. Configure the number of splits (`n_splits`).
3.  Use the `split()` method of `TimeSeriesSplit` on your data (you might only need the indices or can pass dummy `y`). Visualize the indices generated for training and validation in each split.
4.  Observe how the validation set always comes after the training set in each fold.
5.  Train a simple time series forecasting model (e.g., ARIMA, Prophet, or even a simple lagged feature regression) using this cross-validation scheme. Evaluate the performance metric (e.g., MAE, RMSE) on each validation fold and average the results.
6.  Compare this approach to using standard `KFold`. Why would standard `KFold` be inappropriate for most time series forecasting tasks?
7.  **Challenge:** Implement a "sliding window" or "rolling forecast origin" cross-validation scheme manually or using framework features if available. How does this differ from `TimeSeriesSplit`?

---

### 隼 **Exercise 2: Group-Aware Cross-Validation**

**Goal:** Use GroupKFold or StratifiedGroupKFold to ensure that observations from the same group (e.g., same patient, same customer) do not appear in both the training and validation sets within a fold, preventing unrealistic evaluation.

**Instructions:**

1.  Create or load a dataset where multiple rows belong to the same logical group (e.g., multiple sensor readings from the same device, multiple transactions from the same user). Add a 'group_id' column.
2.  Instantiate scikit-learn's `GroupKFold`.
3.  Use the `split()` method, passing your features `X`, target `y`, and the `groups` array (your 'group_id' column). Visualize the training/validation indices for a few splits. Verify that all entries for a specific group end up in *either* the training or the validation set for any given split, never both.
4.  Train a classifier or regressor using this `GroupKFold` strategy within a cross-validation loop (e.g., `cross_val_score`).
5.  Compare the estimated performance to using standard `KFold` or `StratifiedKFold` (which would ignore the group structure). Why might ignoring the group structure lead to an overly optimistic performance estimate?
6.  **Challenge:** When would you use `StratifiedGroupKFold` instead of `GroupKFold`? Create a scenario and dataset where `StratifiedGroupKFold` is necessary to maintain class distribution *and* respect group boundaries.

---

### 隼 **Exercise 3: Identifying Target Leakage**

**Goal:** Recognize common sources of target leakage in feature engineering and validation design.

**Instructions:**

1.  Describe **target leakage** in your own words. Why is it detrimental to building a reliable model?
2.  Analyze the following scenarios and identify the potential source of leakage:
    * **Scenario A:** Creating features like "average user spending in the *next* 30 days" to predict current user churn.
    * **Scenario B:** Calculating aggregate statistics (e.g., mean encoding) for a feature based on the *entire* dataset (including the validation/test set target values) before splitting into train/validation.
    * **Scenario C:** Using future information (e.g., product return status determined *after* a sale) as a feature to predict the likelihood of that sale occurring.
    * **Scenario D:** Performing feature selection using methods that evaluate feature importance based on the *entire* dataset before cross-validation.
3.  For each scenario identified with leakage, propose a correction to prevent it (e.g., use time-based splits, calculate encodings only on training data within CV folds, use features available *at prediction time*, perform feature selection within CV folds).
4.  **Challenge:** Research "subtle" forms of leakage. Can leakage occur even if you use proper time-based or grouped cross-validation (e.g., through external data sources)?

---

### 隼 **Exercise 4: Implementing Adversarial Validation**

**Goal:** Use adversarial validation to check if the training data distribution is significantly different from the test data distribution, which can indicate potential issues like dataset drift or non-representative sampling.

**Instructions:**

1.  Load a training dataset and a separate test dataset (e.g., from a Kaggle competition or by simulating dataset drift).
2.  Combine the training and test datasets. Create a new target variable: assign `0` to all rows originally from the training set and `1` to all rows originally from the test set. Drop the original target variable.
3.  Train a simple, fast binary classification model (e.g., Logistic Regression, LightGBM) to predict this new target variable (i.e., distinguish between training and test set rows) using the original features.
4.  Evaluate this classifier's performance using AUC ROC on a hold-out portion of the combined data (using standard stratified CV).
5.  Interpret the AUC score:
    * An AUC close to 0.5 suggests the training and test distributions are similar (the classifier cannot distinguish them).
    * An AUC significantly higher than 0.5 (e.g., > 0.8) suggests the distributions are different, and the classifier can easily tell them apart. This indicates potential problems for generalizing a model trained on the training set to the test set.
6.  If the AUC is high, examine the feature importances of the adversarial validation classifier. Which features were most helpful in distinguishing train from test? This can highlight features with drifting distributions.
7.  **Challenge:** How could you use the *predictions* of the adversarial validation classifier as weights or features in your main model training to potentially mitigate the train-test distribution shift?

---

### 隼 **Exercise 5: Cross-Validation for Target Encoding**

**Goal:** Implement target encoding within a cross-validation framework to prevent leakage from the target variable into the encoded features.

**Instructions:**

1.  Choose a dataset with a categorical feature and a target variable (classification or regression).
2.  Implement standard **Target Encoding (Mean Encoding)** *incorrectly*: Calculate the mean of the target for each category using the *entire* training dataset. Create the new feature and train a model using standard KFold CV. Record performance. Why is this leaky?
3.  Implement **Target Encoding within Cross-Validation**:
    * Set up a KFold cross-validation loop on the training data.
    * *Inside* each fold:
        * Take the *training portion* of the fold. Calculate the target mean for each category *using only this training portion*.
        * Apply this encoding to the *validation portion* of the fold. Handle potential new categories in validation (e.g., use global mean).
        * Train your model on the training portion (with the encoded feature) and evaluate on the validation portion (with the encoded feature).
    * Average the validation scores across folds.
4.  Compare the cross-validated performance estimate from the leaky method (step 2, evaluated properly via CV itself) vs. the correct CV-based encoding method (step 3). Which provides a more realistic estimate?
5.  **Challenge:** Implement **smoothing** for target encoding within the cross-validation loop. How does smoothing help, especially for categories with few samples? (`TargetEncoder` in `category_encoders` library often handles this).

---