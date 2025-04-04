## 倹 Subtopic 2.3: Advanced & Adaptive LR Schedulers

**Goal:** Explore more sophisticated learning rate schedules like Cyclical Learning Rates (CLR), the One-Cycle Policy, and adaptive methods like ReduceLROnPlateau.

**Resources:**

* **Cyclical Learning Rates Paper:** [Leslie N. Smith - Cyclical Learning Rates for Training Neural Networks](https://arxiv.org/abs/1506.01186)
* **One-Cycle Policy Blog Post:** [Fast.ai - The 1cycle policy](https://docs.fast.ai/callback.schedule.html#The-1cycle-policy)
* **PyTorch Schedulers:** [CyclicLR](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CyclicLR.html), [OneCycleLR](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html), [ReduceLROnPlateau](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html)
* **TensorFlow Addons:** May contain implementations like [CyclicalLearningRate](https://www.tensorflow.org/addons/api_docs/python/tfa/optimizers/CyclicalLearningRate), check [tf.keras.callbacks.ReduceLROnPlateau](https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/ReduceLROnPlateau)

---

### 隼 **Exercise 1: Cyclical Learning Rates (CLR)**

**Goal:** Implement the Cyclical Learning Rates (CLR) schedule and understand its effect on navigating the loss landscape.

**Instructions:**

1.  Use a standard dataset/model setup (e.g., CIFAR-10/CNN).
2.  Implement CLR using a framework scheduler (e.g., `CyclicLR` in PyTorch) or manually implement the triangular or triangular2 policy described in the paper. Key parameters include `base_lr`, `max_lr`, and `step_size_up`/`step_size_down`.
3.  Determine a reasonable range for `base_lr` and `max_lr` (the LR Range Test, often associated with CLR/One-Cycle, can help find these, but start with reasonable guesses like 1e-4 and 1e-2). Set `step_size_up` to typically 2-10 epochs worth of iterations.
4.  Train the model using an appropriate optimizer (like SGD or Adam) with the CLR schedule. Plot the training loss, validation accuracy, and the learning rate over epochs.
5.  Analyze the results: How does the periodic increase and decrease of the learning rate affect the loss curve? Did it help escape local minima or achieve better final performance compared to previous schedules?
6.  **Challenge:** Implement the "triangular2" policy for CLR (where the maximum learning rate decreases with each cycle). Compare its performance to the standard triangular policy.

---

### 隼 **Exercise 2: The One-Cycle Policy**

**Goal:** Implement the One-Cycle learning rate policy and compare its rapid convergence potential to other schedules.

**Instructions:**

1.  Use the same dataset/model setup.
2.  Implement the One-Cycle policy using a framework scheduler (e.g., `OneCycleLR` in PyTorch). This policy typically involves:
    * A warmup phase increasing LR from a low value (`div_factor`) to `max_lr`.
    * A longer annealing phase decreasing LR from `max_lr` down to the low value again (often using cosine annealing).
    * An optional short "annihilation" phase decreasing LR further.
    * Often combined with cyclical momentum (decreasing momentum as LR increases).
3.  Choose `max_lr` (potentially higher than usual, e.g., found via an LR Range Test) and the total number of epochs/steps. Set `div_factor` (e.g., 10 or 25) to determine the starting LR.
4.  Train the model using an appropriate optimizer (often SGD w/ momentum or AdamW) with the One-Cycle policy. Plot loss, accuracy, and learning rate curves.
5.  Compare the convergence speed (especially early epochs) and final performance to other schedules like standard cosine annealing or step decay, potentially using fewer total epochs for the One-Cycle run.
6.  **Challenge:** Experiment with the momentum cycle component of the One-Cycle policy (if supported by your framework scheduler, e.g., `cycle_momentum=True` in PyTorch `OneCycleLR`). How does varying momentum inversely with learning rate potentially help?

---

### 隼 **Exercise 3: ReduceLROnPlateau**

**Goal:** Implement an adaptive learning rate schedule that reduces the LR when a monitored metric stops improving.

**Instructions:**

1.  Use a standard dataset/model setup. Choose a metric to monitor (e.g., validation loss or validation accuracy).
2.  Implement the `ReduceLROnPlateau` schedule using your framework's scheduler or callback. Key parameters include:
    * `monitor`: The metric to track.
    * `factor`: Factor by which LR is reduced (e.g., 0.1, 0.2).
    * `patience`: Number of epochs with no improvement after which LR is reduced (e.g., 5, 10).
    * `mode`: 'min' (for loss) or 'max' (for accuracy).
    * `min_lr`: Lower bound on the learning rate.
3.  Train the model using an optimizer (e.g., Adam) and the `ReduceLROnPlateau` schedule. Plot loss, accuracy, and learning rate curves.
4.  Observe how the learning rate changes during training. Does it drop when the monitored metric plateaus?
5.  Compare its performance and behavior to fixed schedules (like step decay). In what scenarios might `ReduceLROnPlateau` be particularly useful?
6.  **Challenge:** How does the choice of `patience` and `factor` affect the schedule's responsiveness and the risk of reducing the LR too early or too late? Experiment with different values.

---

### 隼 **Exercise 4: Adaptive Optimizers and Scheduling**

**Goal:** Investigate the interaction between adaptive optimizers (like Adam) and learning rate schedules.

**Instructions:**

1.  Choose a dataset/model setup.
2.  Train the model using **Adam** with a **constant learning rate**. Plot convergence curves.
3.  Train the model using **Adam** combined with a **cosine annealing schedule**. Plot convergence curves.
4.  Train the model using **Adam** combined with **ReduceLROnPlateau**. Plot convergence curves.
5.  Compare the results. Does adding an explicit schedule significantly improve performance when using Adam compared to using Adam with a constant LR?
6.  Discuss the theoretical viewpoint: Since Adam already adapts learning rates per parameter, is adding a global schedule always necessary or as impactful as it is for SGD? Why might schedules still be beneficial with Adam (e.g., for large-scale convergence)?
7.  **Challenge:** Repeat the comparison using **SGD with momentum** instead of Adam (i.e., SGD+ConstantLR vs SGD+CosineAnnealing vs SGD+ReduceLROnPlateau). Is the impact of scheduling more pronounced for SGD compared to Adam?

---