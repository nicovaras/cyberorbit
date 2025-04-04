## 倹 Subtopic 2.7: Mixed-Precision Training

**Goal:** Utilize Automatic Mixed Precision (AMP) to accelerate training speed and reduce memory usage by using lower-precision floating-point formats (like float16) where appropriate.

**Resources:**

* **NVIDIA Deep Learning Performance Guide:** [Mixed-Precision Training Section](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html)
* **PyTorch AMP:** [Automatic Mixed Precision package - torch.amp](https://pytorch.org/docs/stable/amp.html), [Examples](https://pytorch.org/docs/stable/notes/amp_examples.html)
* **TensorFlow Mixed Precision:** [Mixed precision guide](https://www.tensorflow.org/guide/mixed_precision)

---

### 隼 **Exercise 1: Enabling Automatic Mixed Precision (AMP)**

**Goal:** Use framework utilities (PyTorch `torch.amp` or TensorFlow Keras Mixed Precision API) to enable AMP and observe its impact on training speed and memory consumption. **Requires compatible GPU hardware (NVIDIA Tensor Cores recommended for significant speedup).**

**Instructions:**

1.  Choose a moderately large model (e.g., ResNet, Vision Transformer) and dataset (e.g., ImageNet subset, CIFAR-100) where training time and memory are noticeable.
2.  Establish a baseline: Train the model using standard **float32** precision. Record the training time per epoch and peak GPU memory usage (use tools like `nvidia-smi` or framework profiling utilities). Note the final validation accuracy.
3.  Enable AMP using your framework's recommended practice:
    * **PyTorch:** Use `torch.cuda.amp.autocast()` context manager around your model's forward pass and loss computation. Use `torch.cuda.amp.GradScaler` to scale the loss before `backward()` and unscale gradients before `optimizer.step()`.
    * **TensorFlow:** Set the global policy `tf.keras.mixed_precision.set_global_policy('mixed_float16')`. Keras automatically handles loss scaling within the `model.fit` loop or requires using a `LossScaleOptimizer` wrapper for custom loops.
4.  Train the *exact same* model architecture **with AMP enabled** using the same hyperparameters (learning rate might need adjustment).
5.  Record the training time per epoch and peak GPU memory usage with AMP. Compare these to the float32 baseline. Was training faster? Did memory usage decrease?
6.  Compare the final validation accuracy achieved with AMP to the float32 baseline. Did AMP significantly impact accuracy?
7.  **Challenge:** Monitor the loss scale value used by the `GradScaler` (PyTorch) or `LossScaleOptimizer` (TensorFlow) during training. How does it change over time? What happens if you disable loss scaling when using AMP?

---

### 隼 **Exercise 2: Understanding Loss Scaling**

**Goal:** Understand why loss scaling is crucial for numerical stability when using float16 gradients in mixed-precision training.

**Instructions:**

1.  Explain the limited range and precision of the `float16` (FP16) numerical format compared to `float32` (FP32).
2.  Describe what can happen during the backward pass if gradients computed in FP32 are directly cast to FP16: Which gradients are most likely to become zero (underflow)? (Hint: Small magnitude gradients).
3.  Explain the concept of **Loss Scaling**:
    * How does multiplying the loss by a large scaling factor *before* the backward pass help? (Hint: Affects gradient magnitudes).
    * How are the gradients treated *after* the backward pass but *before* the optimizer update? (Hint: Unscaling).
    * How does this process prevent underflow of small gradient values when they are converted to FP16?
4.  Describe **Dynamic Loss Scaling** (as used by `GradScaler` / `LossScaleOptimizer`): How does the scaler automatically adjust the scaling factor during training based on whether gradient overflows (NaNs/Infs) occur?
5.  **Challenge:** If you disable loss scaling in Exercise 1 (if your framework allows), observe the training behavior. Does the model fail to train or converge poorly? Do you see NaNs or Infs appearing in the loss or gradients?

---

### 隼 **Exercise 3: Identifying Numerically Sensitive Operations**

**Goal:** Recognize model operations that might be numerically unstable in float16 and how AMP frameworks handle them.

**Instructions:**

1.  Review the documentation or guides for PyTorch AMP or TensorFlow Mixed Precision regarding how autocasting works.
2.  Frameworks typically maintain lists of operations that are safe to run in FP16 ("allow lists") and operations that should remain in FP32 for numerical stability ("block lists" or default FP32).
3.  Research or list common types of operations often kept in FP32:
    * Large reductions (e.g., summing across large dimensions).
    * Loss functions (often computed in FP32 for stability).
    * Certain activation functions or mathematical operations prone to precision issues.
4.  Explain how the autocast mechanism automatically selects the precision for each operation based on these internal lists.
5.  **Challenge:** Can you manually override the autocast behavior for specific layers or blocks within your model if needed (e.g., force a specific block to run in FP32 even if it's normally allowed in FP16)? Check your framework's documentation for how to achieve this.

---

### 隼 **Exercise 4: Debugging Mixed Precision Issues**

**Goal:** Learn basic strategies for diagnosing problems (like NaN losses or poor convergence) that can arise when using mixed-precision training.

**Instructions:**

1.  Suppose your model training fails with AMP enabled (e.g., loss becomes NaN). List common potential causes:
    * Numerical instability in a specific operation when run in FP16.
    * Incorrect loss scaling or gradient unscaling.
    * Underflow/Overflow issues not caught by the dynamic loss scaler.
    * Potential bugs in custom layers interacting with autocasting.
2.  Describe debugging steps you would take:
    * **Check for NaNs/Infs:** Add checks after the forward pass, loss calculation, and before the optimizer step to detect where NaNs first appear.
    * **Disable AMP Components:** Temporarily disable autocasting or loss scaling to see if the issue persists in FP32.
    * **Reduce Learning Rate:** Sometimes instability is exacerbated by high learning rates.
    * **Identify Problematic Layer:** Try running parts of the model or specific layers in FP32 (see Exercise 3 Challenge) to isolate the source of instability.
    * **Check Gradient Norms:** Monitor gradient norms before and after clipping/unscaling.
3.  **Challenge:** If you suspect a specific custom layer in your network is causing NaN issues with AMP, how would you modify the layer's `forward` method to potentially make it more robust or force it to run in FP32 using autocast control?

---