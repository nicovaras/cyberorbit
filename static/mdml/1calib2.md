## 倹 Subtopic 1.5: Calibration Methods Implementation

**Goal:** Apply common calibration techniques (Platt Scaling, Isotonic Regression, Temperature Scaling) to improve the calibration of poorly calibrated classifiers.

**Resources:**

* **Scikit-learn Calibration:** [Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html) (Covers Platt and Isotonic)
* **Temperature Scaling:** [Paper explaining concept](https://arxiv.org/abs/1706.04599) (Section 2.2)
* **PyTorch Temperature Scaling Implementation:** [Example Code](https://github.com/gpleiss/temperature_scaling) (Or implement based on paper)

---

### 隼 **Exercise 1: Platt Scaling (Sigmoid Calibration)**

**Goal:** Apply Platt scaling to calibrate the output of a classifier, typically one like an SVM or boosted trees whose outputs aren't well-calibrated probabilities.

**Instructions:**

1.  Train a classifier known to produce poorly calibrated scores (e.g., Support Vector Classifier with `probability=False` or default, or Gradient Boosting). Use a dataset like Iris or Breast Cancer.
2.  Split your *training* data into a smaller training set and a calibration set (e.g., 80% train, 20% calibration). Train the main classifier on the smaller training set.
3.  Obtain the decision function scores (or non-probabilistic outputs) from the trained classifier on the *calibration set*.
4.  Train a Logistic Regression model where the input features are the decision function scores from step 3, and the target is the true labels of the calibration set. This Logistic Regression model *is* the Platt scaler.
5.  Obtain predicted probabilities from the original classifier on the *test set*. Pass these through your trained Platt scaler (the Logistic Regression model's `predict_proba`) to get calibrated probabilities.
6.  Alternatively, use scikit-learn's `CalibratedClassifierCV` with `method='sigmoid'` which automates this cross-validated process. Train it on the full training data. Obtain calibrated probabilities on the test set.
7.  Evaluate the calibration of the *original* model and the *Platt-calibrated* model using reliability diagrams and ECE scores on the test set. Did Platt scaling improve calibration?
8.  **Challenge:** Why is it crucial to train the calibrator (the Logistic Regression model) on a separate calibration set (or using cross-validation as in `CalibratedClassifierCV`) rather than the same data used to train the original classifier?

---

### 隼 **Exercise 2: Isotonic Regression Calibration**

**Goal:** Apply Isotonic Regression, a non-parametric method, to calibrate classifier probabilities.

**Instructions:**

1.  Train a classifier whose probabilities might be miscalibrated but not necessarily in a simple sigmoid way (e.g., Random Forest, or use the Naive Bayes from previous exercises). Use standard dataset.
2.  Split data into train/calibration/test sets as in Exercise 1 OR use `CalibratedClassifierCV`.
3.  If doing manually: Train the main classifier on the training set. Obtain predicted probabilities on the calibration set. Train an `IsotonicRegression` model (from scikit-learn) where the input (`y` parameter in `fit`) is the true labels and the sample weights (`X` parameter in `fit`) are the predicted probabilities from the calibration set.
4.  Obtain predicted probabilities from the original classifier on the *test set*. Use the `predict` method of the fitted Isotonic Regression model to transform these probabilities into calibrated ones.
5.  Alternatively, use scikit-learn's `CalibratedClassifierCV` with `method='isotonic'`. Train it on the full training data. Obtain calibrated probabilities on the test set.
6.  Evaluate the calibration of the *original* model and the *Isotonic-calibrated* model using reliability diagrams and ECE scores on the test set.
7.  Compare the results of Isotonic calibration to Platt scaling (if applied to the same original model). Which worked better?
8.  **Challenge:** Isotonic Regression is non-parametric. What are the potential advantages and disadvantages of this compared to the parametric Platt scaling (Logistic Regression)? Consider overfitting risk and the shapes of calibration curves they can correct.

---

### 隼 **Exercise 3: Temperature Scaling for Neural Networks**

**Goal:** Implement and apply Temperature Scaling, a simple extension of Platt scaling often used for deep neural networks.

**Instructions:**

1.  Train a simple neural network (e.g., a small MLP or CNN using PyTorch/TensorFlow) for a classification task. Ensure the final layer provides logits (outputs *before* the final Softmax/Sigmoid).
2.  Split data into train/calibration/test sets. Train the NN on the training set.
3.  Obtain the logits from the trained network for the *calibration set*.
4.  Implement the Temperature Scaling optimization:
    * Define a single scalar parameter `T` (temperature), initialized to 1.
    * The scaled probabilities are obtained by applying Softmax (or Sigmoid for binary) to `logits / T`.
    * Define a loss function suitable for calibration, often Negative Log Likelihood (NLL), calculated between the scaled probabilities and the true labels of the calibration set.
    * Optimize *only* the temperature `T` (keeping network weights fixed) to minimize the NLL on the calibration set. This can be done using simple gradient descent on `T`.
5.  Obtain the logits from the network for the *test set*. Apply the optimal temperature `T` found in step 4 (`scaled_logits = logits / T`) and then apply the Softmax/Sigmoid function to get calibrated probabilities.
6.  Evaluate the calibration of the *original* network (using standard Softmax/Sigmoid on logits, T=1) and the *Temperature-scaled* network using reliability diagrams and ECE on the test set. Did Temperature Scaling improve calibration?
7.  **Challenge:** How does Temperature Scaling preserve the ranking of predictions (i.e., the `argmax` of the probabilities) compared to the original model? Why is this often a desirable property?

---

### 隼 **Exercise 4: Comparing Calibration Methods**

**Goal:** Systematically compare the effectiveness of different calibration methods on various base models.

**Instructions:**

1.  Choose a dataset suitable for binary classification.
2.  Select several different classification models (e.g., Logistic Regression, Naive Bayes, SVM, Random Forest, Gradient Boosting, a simple Neural Network).
3.  For each base model:
    * Train the model on the training data.
    * Evaluate its *original* calibration (ECE, Brier score, Reliability Diagram) on the test set.
    * Apply Platt Scaling (using `CalibratedClassifierCV` method='sigmoid'). Evaluate its calibration.
    * Apply Isotonic Regression (using `CalibratedClassifierCV` method='isotonic'). Evaluate its calibration.
    * (If applicable) Apply Temperature Scaling (requires logits and manual implementation or specialized libraries). Evaluate its calibration.
4.  Create a table summarizing the ECE and Brier scores for the original and calibrated versions of each model using each applicable calibration method.
5.  Analyze the results: Which calibration methods worked best for which types of models? Were already well-calibrated models (like Logistic Regression) significantly affected? Did any method make calibration worse?
6.  **Challenge:** Does calibration significantly impact the model's discriminative performance (e.g., AUC ROC)? Calculate and compare AUC ROC scores before and after calibration for each model/method combination. Discuss why calibration primarily affects probability scores rather than ranking ability.

---