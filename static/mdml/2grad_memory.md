## 倹 Subtopic 2.6: Gradient Manipulation & Memory Efficiency

**Goal:** Implement techniques like gradient clipping to stabilize training and gradient accumulation to train with larger effective batch sizes than fit in memory.

**Resources:**

* **Gradient Clipping:** [Explanation and discussion](https://towardsdatascience.com/what-is-gradient-clipping-b8e815cdfb48), Framework functions (e.g., `torch.nn.utils.clip_grad_norm_`, `tf.clip_by_value`, `tf.clip_by_norm`)
* **Gradient Accumulation:** [Explanation and pseudo-code](https://kozodoi.me/blog/20210219/gradient-accumulation), [Example Implementation (PyTorch)](https://pytorch.org/docs/stable/notes/amp_examples.html#gradient-accumulation)

---

### 隼 **Exercise 1: Implementing Gradient Norm Clipping**

**Goal:** Apply gradient clipping by norm to prevent exploding gradients during training, particularly in RNNs or deep networks.

**Instructions:**

1.  Choose a task/model potentially prone to exploding gradients (e.g., training an RNN on a sequence task, or a very deep CNN with high learning rates).
2.  Train the model **without** gradient clipping. Monitor the norm of the gradients during training (if possible within your framework, or just monitor the loss curve for sudden spikes). Try to provoke instability with a higher learning rate.
3.  Implement **gradient clipping by norm**. After the backward pass (`loss.backward()`) but *before* the optimizer step (`optimizer.step()`):
    * Use framework functions (e.g., `torch.nn.utils.clip_grad_norm_`) to clip the gradients of the model parameters based on their total L2 norm. Choose a `max_norm` value (e.g., 1.0, 5.0).
4.  Train the model again **with** gradient norm clipping enabled, using the same potentially high learning rate.
5.  Compare the training stability (loss curve behavior) with and without clipping. Did clipping prevent loss spikes or allow training with a higher learning rate?
6.  **Challenge:** Experiment with different `max_norm` values. How does this threshold affect training stability and potentially the final model performance?

---

### 隼 **Exercise 2: Gradient Clipping by Value**

**Goal:** Apply gradient clipping by value and understand its difference from clipping by norm.

**Instructions:**

1.  Use the same setup as Exercise 1.
2.  Implement **gradient clipping by value**. After the backward pass and before the optimizer step:
    * Use framework functions (e.g., `torch.nn.utils.clip_grad_value_` or `tf.clip_by_value`) to clamp each individual gradient value within a specified range (`[-clip_value, +clip_value]`). Choose a `clip_value` (e.g., 0.5, 1.0).
3.  Train the model with gradient value clipping enabled.
4.  Compare its effect on stability to clipping by norm (Exercise 1) and no clipping.
5.  Discuss the difference: Clipping by norm rescales the entire gradient vector if its norm exceeds a threshold, preserving direction. Clipping by value clips each element independently, potentially changing the gradient's direction. In what scenarios might one be preferred over the other?
6.  **Challenge:** Create a simple 2D gradient vector. Visualize how its direction and magnitude change when applying norm clipping versus value clipping.

---

### 隼 **Exercise 3: Implementing Gradient Accumulation**

**Goal:** Simulate training with a larger batch size than fits into GPU memory by accumulating gradients over multiple smaller batches.

**Instructions:**

1.  Choose a dataset/model setup where a large batch size is desirable but might exceed GPU memory (e.g., large images, complex models). Determine your target *effective* batch size (e.g., 256) and the maximum *physical* batch size your GPU can handle (e.g., 64).
2.  Calculate the number of accumulation steps needed: `accumulation_steps = effective_batch_size / physical_batch_size` (e.g., 256 / 64 = 4).
3.  Modify your training loop:
    * Initialize `optimizer.zero_grad()` *outside* the accumulation loop.
    * Loop `accumulation_steps` times:
        * Fetch a *physical* batch of data.
        * Perform the forward pass (`outputs = model(inputs)`).
        * Calculate the loss (`loss = criterion(outputs, labels)`).
        * **Scale the loss** by dividing by `accumulation_steps` (`loss = loss / accumulation_steps`). This ensures the average gradient magnitude is correct.
        * Perform the backward pass (`loss.backward()`). **Gradients will accumulate** because `zero_grad()` wasn't called.
    * *After* the accumulation loop finishes, perform the optimizer step: `optimizer.step()`.
    * *Then* zero the gradients: `optimizer.zero_grad()`.
4.  Train the model using gradient accumulation. Compare its performance and convergence to training with the smaller *physical* batch size without accumulation (if possible to train stably). Does it seem to converge more similarly to how training with the large *effective* batch size would?
5.  **Challenge:** Why is scaling the loss before the backward pass important when using gradient accumulation? What would happen if you didn't scale it?

---

### 隼 **Exercise 4: Combining Gradient Accumulation and Clipping**

**Goal:** Integrate gradient accumulation and gradient clipping within the same training loop.

**Instructions:**

1.  Start with the gradient accumulation training loop from Exercise 3.
2.  Decide where to apply gradient clipping (norm or value). The standard approach is to clip the *accumulated* gradients just before the optimizer step.
3.  Modify the loop:
    * Perform the forward pass, loss calculation, loss scaling, and backward pass inside the accumulation loop as before.
    * *After* the accumulation loop finishes (all gradients for the effective batch are accumulated) but *before* `optimizer.step()`:
        * Apply gradient clipping (e.g., `torch.nn.utils.clip_grad_norm_`) to the model's parameters.
    * Then perform `optimizer.step()` and `optimizer.zero_grad()`.
4.  Train the model with both techniques enabled.
5.  Discuss if any adjustments to the clipping threshold (`max_norm` or `clip_value`) might be necessary when using accumulation compared to standard training.
6.  **Challenge:** Could you apply clipping *inside* the accumulation loop (i.e., after each `loss.backward()`)? What would be the potential drawbacks of that approach compared to clipping the final accumulated gradient? (Hint: Consider the effective `max_norm` over the whole accumulated batch).

---