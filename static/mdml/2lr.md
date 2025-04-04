## 倹 Subtopic 2.2: Learning Rate Scheduling Strategies

**Goal:** Implement and compare various learning rate scheduling techniques to improve model convergence speed, stability, and final performance.

**Resources:**

* **PyTorch Schedulers:** [torch.optim.lr_scheduler Documentation](https://pytorch.org/docs/stable/optim.lr_scheduler.html)
* **TensorFlow Schedulers:** [tf.keras.optimizers.schedules Documentation](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/schedules)
* **Blog Post on LR Schedules:** [Illustrations and explanations of common schedules](https://www.jeremyjordan.me/learning-rate-schedulers/)
* **Warmup Explanation:** [Rationale for learning rate warmup](https://towardsdatascience.com/learning-rate-warm-up-for-maintaining-forward-momentum-8995670f493)

---

### 隼 **Exercise 1: Step Decay Implementation & Tuning**

**Goal:** Implement a step decay learning rate schedule and observe its effect on training convergence.

**Instructions:**

1.  Choose a dataset and model (e.g., CIFAR-10 with a simple CNN). Select a base optimizer (e.g., SGD with momentum).
2.  Train the model using a **constant learning rate** (appropriately tuned) for a fixed number of epochs. Plot the training loss and validation accuracy curves.
3.  Implement a **step decay** schedule: Reduce the learning rate by a factor (e.g., 0.1 or 0.2) at specific pre-defined epochs (e.g., at epochs 30, 60, 80).
4.  Train the model again using SGD with momentum and your step decay schedule. Use the same initial learning rate as in step 2. Plot the new training loss and validation accuracy curves. Record the learning rate at each epoch.
5.  Compare the convergence speed and final performance of the constant LR vs. step decay schedule. Plot the learning rate over epochs for the step decay run.
6.  **Challenge:** Experiment with different step decay schedules (different drop factors, different epoch milestones). How sensitive is the final performance to the exact schedule?

---

### 隼 **Exercise 2: Cosine Annealing Schedule**

**Goal:** Implement and evaluate the cosine annealing learning rate schedule.

**Instructions:**

1.  Use the same dataset, model, and base optimizer (SGD w/ momentum) as in Exercise 1.
2.  Implement a **cosine annealing** schedule using your framework's scheduler (e.g., `CosineAnnealingLR` in PyTorch, `CosineDecay` in TensorFlow). Set the minimum learning rate (`eta_min` or `alpha`) to a small value (e.g., 0 or 1e-6) and the period (`T_max` or `decay_steps`) typically to the total number of training epochs (or iterations).
3.  Train the model using SGD with momentum and the cosine annealing schedule. Choose a suitable initial learning rate (often slightly higher than for constant LR). Plot the training loss and validation accuracy curves. Record and plot the learning rate over epochs.
4.  Compare the performance (convergence, final accuracy) of cosine annealing to the constant LR and step decay schedules from Exercise 1.
5.  Discuss the theoretical benefit of the smooth, cyclical decay provided by cosine annealing compared to sharp drops in step decay.
6.  **Challenge:** Implement **cosine annealing with restarts** (`CosineAnnealingWarmRestarts` in PyTorch). Set a restart period (`T_0`). How does periodically resetting the learning rate to its initial value affect the training dynamics and final performance?

---

### 隼 **Exercise 3: Linear and Polynomial Decay**

**Goal:** Implement and compare linear and polynomial learning rate decay schedules.

**Instructions:**

1.  Use the same dataset, model, and base optimizer setup.
2.  Implement a **linear decay** schedule where the learning rate decreases linearly from the initial value to a final value (e.g., 0) over the course of training. Use framework functions if available (e.g., `PolynomialDecay` in TF with `power=1`) or implement manually.
3.  Implement a **polynomial decay** schedule (e.g., with `power=2` for quadratic decay).
4.  Train the model using SGD with momentum, once with linear decay and once with polynomial decay (power=2). Plot loss/accuracy curves and the LR curve for each.
5.  Compare the performance of linear and polynomial decay against each other and potentially against step decay or cosine annealing.
6.  **Challenge:** How does the choice of `power` in polynomial decay affect the shape of the decay curve and potentially the training outcome? Try `power=0.5` (square root decay).

---

### 隼 **Exercise 4: Learning Rate Warmup**

**Goal:** Implement a learning rate warmup phase at the beginning of training and analyze its impact, especially when using large initial learning rates or certain optimizers like Adam.

**Instructions:**

1.  Choose a dataset/model setup, potentially with a slightly larger initial learning rate than usual or using an optimizer like Adam.
2.  Train the model *without* warmup. Record the initial training loss behavior (first few epochs) and final performance.
3.  Implement a **warmup** phase: For the first `k` epochs (or iterations), linearly increase the learning rate from a very small value (e.g., 0 or 1e-6) up to the target initial learning rate. After the warmup phase, switch to another schedule (e.g., constant LR, step decay, or cosine annealing). Many framework schedulers have warmup built-in or can be combined (e.g., `LinearWarmup` followed by `CosineAnnealing`).
4.  Train the model *with* the warmup phase included. Record initial training loss and final performance.
5.  Compare the training stability (especially in the first few epochs) and final performance with and without warmup. Plot the learning rate schedule including the warmup phase.
6.  Explain the rationale behind using warmup: Why might starting immediately with a large learning rate be detrimental, especially in deep learning?
7.  **Challenge:** Combine warmup with a cosine annealing schedule. Does this combination generally perform well?

---