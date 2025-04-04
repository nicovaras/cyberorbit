## 倹 Subtopic 2.4: Regularization Techniques Deep Dive

**Goal:** Understand the mechanisms and implementation details of common regularization techniques like L1/L2 weight decay and various forms of Dropout, analyzing their impact on model generalization.

**Resources:**

* **L1/L2 Regularization:** [Scikit-learn Documentation (e.g., LogisticRegression 'penalty' parameter)](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression), [Deep Learning Book Chapter](https://www.deeplearningbook.org/contents/regularization.html)
* **Dropout Paper:** [Srivastava et al., 2014](http://jmlr.org/papers/v15/srivastava14a.html)
* **PyTorch Dropout Layers:** [Dropout](https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html), [Dropout2d](https://pytorch.org/docs/stable/generated/torch.nn.Dropout2d.html)
* **TensorFlow Dropout Layers:** [Dropout](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout), [SpatialDropout2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/SpatialDropout2D)

---

### 隼 **Exercise 1: L1 vs L2 Regularization Effects**

**Goal:** Compare the effects of L1 (Lasso) and L2 (Ridge) regularization on model weights and feature selection in a linear model context.

**Instructions:**

1.  Choose a dataset suitable for linear regression or logistic regression, preferably one with many features, some potentially irrelevant (e.g., use `make_classification` with informative and redundant features).
2.  Train a Logistic Regression model (or Linear Regression) with **no regularization**. Examine the learned coefficients/weights.
3.  Train the same model using **L2 regularization** (Ridge). Experiment with different regularization strengths (e.g., `C` parameter in scikit-learn LogisticRegression, which is inverse strength, so try small values like 0.1, 0.01). Examine the learned weights. How do they compare to the unregularized model?
4.  Train the same model using **L1 regularization** (Lasso). Experiment with different regularization strengths. Examine the learned weights. How do they compare to L2 and the unregularized model?
5.  Discuss the key difference: How does L1 regularization promote sparsity (driving some weights to exactly zero) compared to L2 regularization (which tends to shrink weights towards zero but not exactly to zero)? What are the implications for feature selection?
6.  **Challenge:** Plot the coefficient values for each feature for the unregularized, L2-regularized, and L1-regularized models (at a chosen regularization strength). Visually compare the weight magnitudes and sparsity.

---

### 隼 **Exercise 2: Weight Decay Implementation Nuances**

**Goal:** Understand how L2 regularization (weight decay) is typically implemented in deep learning optimizers and differentiate it from adding an L2 penalty term directly to the loss function.

**Instructions:**

1.  Review the standard update rule for SGD with momentum: `velocity = momentum * velocity + learning_rate * gradient`, `weights = weights - velocity`.
2.  Review the update rule for an optimizer implementing **weight decay** (like AdamW or SGD with `weight_decay` parameter): `gradient = gradient + weight_decay * weights`, `velocity = ...`, `weights = weights - velocity`. (Note: Sometimes decay is applied directly to weights after velocity step).
3.  Review the concept of adding an **L2 penalty to the loss**: `Loss_total = Loss_original + (lambda / 2) * sum(weights^2)`. The gradient of this total loss would include an extra `lambda * weights` term.
4.  Discuss the difference: When using adaptive optimizers like Adam, the effective learning rate changes per parameter. Show (conceptually or with a simple example) how applying decay directly to the weights (as in weight decay) differs from adding the `lambda * weights` term to the gradient *before* it gets scaled by Adam's adaptive learning rates. (Reference the AdamW paper).
5.  Explain why the "weight decay" approach (decoupled from the gradient scaling) is often preferred with adaptive optimizers.
6.  **Challenge:** Implement both approaches manually for a simple linear model update using SGD and Adam. Compare the resulting weight updates over a few steps.

---

### 隼 **Exercise 3: Implementing and Evaluating Standard Dropout**

**Goal:** Add Dropout layers to a neural network and evaluate its effect on overfitting.

**Instructions:**

1.  Choose a dataset/model prone to overfitting (e.g., train a moderately large MLP or CNN on a relatively small dataset like CIFAR-10 without data augmentation, for enough epochs to see overfitting).
2.  Train the model **without Dropout**. Plot the training loss/accuracy and validation loss/accuracy curves over epochs. Observe the gap indicating overfitting. Record the best validation accuracy.
3.  Add standard `Dropout` layers after activation functions (or between linear/convolutional layers) in your network architecture. Choose a dropout rate `p` (e.g., 0.25 or 0.5).
4.  **Important:** Ensure Dropout is active during training but **disabled** during evaluation/testing (frameworks usually handle this automatically via `model.train()` and `model.eval()`).
5.  Train the model **with Dropout** for the same number of epochs. Plot the new training and validation curves.
6.  Compare the curves and the best validation accuracy with and without Dropout. Did Dropout reduce the gap between training and validation performance? Did it improve the best validation accuracy?
7.  **Challenge:** Experiment with different dropout rates `p`. How does the rate affect regularization strength and potentially training speed or final performance? Try placing dropout layers in different positions in the network.

---

### 隼 **Exercise 4: Spatial Dropout (Dropout2d)**

**Goal:** Understand and apply Spatial Dropout (Dropout2d) for convolutional layers.

**Instructions:**

1.  Use a CNN architecture on an image dataset (e.g., CIFAR-10).
2.  Train the model without any dropout as a baseline, observing overfitting as in Exercise 3.
3.  Modify the architecture by adding `SpatialDropout2D` (TensorFlow) or `Dropout2d` (PyTorch) layers *after* convolutional layers (typically after activation). This type of dropout drops entire feature maps rather than individual pixels/activations. Choose a dropout rate `p`.
4.  Train the model with Spatial Dropout. Plot training/validation curves.
5.  Compare the performance (overfitting reduction, final accuracy) to the baseline model without dropout.
6.  Discuss the rationale behind Spatial Dropout: Why might dropping entire feature maps be more effective for regularizing convolutional layers compared to dropping individual units (standard Dropout)? (Hint: Consider spatial correlation in feature maps).
7.  **Challenge:** Compare the effect of using standard `Dropout` (applied after flattening the feature maps before a dense layer) versus using `SpatialDropout2D` earlier in the convolutional blocks of the same network. Which seems more effective for regularizing the CNN?

---

### 隼 **(Optional) Exercise 5: Exploring DropConnect**

**Goal:** Understand the concept of DropConnect as an alternative to Dropout.

**Instructions:**

1.  Research the DropConnect regularization technique. Read the original paper or summary articles.
2.  Explain the key difference between Dropout (which drops neuron activations/outputs) and DropConnect (which drops connections/weights within the network).
3.  Draw a small diagram illustrating where connections are dropped in DropConnect versus where activations are dropped in Dropout for a simple fully connected layer.
4.  Discuss the potential advantages and disadvantages of DropConnect compared to Dropout (e.g., potentially stronger regularization, computational cost during training).
5.  **Challenge:** If framework support is available (might require custom implementation or specific libraries), try applying DropConnect to a simple network and compare its performance to standard Dropout.

---