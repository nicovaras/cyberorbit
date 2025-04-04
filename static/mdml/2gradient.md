
## 倹 Subtopic 2.1: Advanced Gradient Descent Variants & Dynamics

**Goal:** Understand the mechanics, implementation nuances, and practical performance differences between advanced first-order optimization algorithms beyond standard SGD, focusing on Momentum, Nesterov Accelerated Gradient (NAG), RMSprop, Adam, and AdamW.

**Resources:**

* **Overview of Gradient Descent Algorithms:** [Sebastian Ruder's Blog Post](https://ruder.io/optimizing-gradient-descent/) (Excellent overview)
* **Adam / AdamW Paper:** [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980), [Decoupled Weight Decay Regularization (AdamW)](https://arxiv.org/abs/1711.05101)
* **PyTorch Optimizers:** [torch.optim Documentation](https://pytorch.org/docs/stable/optim.html) (See SGD, Adam, AdamW, RMSprop)
* **TensorFlow Optimizers:** [tf.keras.optimizers Documentation](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers) (See SGD, Adam, AdamW, RMSprop)
* **Visualizations:** [Loss Landscape Visualization Tools/Papers](https://losslandscape.com/) (For conceptual understanding)

---

### 隼 **Exercise 1: Momentum vs NAG Visualization**

**Goal:** Implement and visualize the optimization paths of SGD, SGD with Momentum, and Nesterov Accelerated Gradient (NAG) on a simple 2D loss surface to intuitively grasp their differences in trajectory.

**Instructions:**

1.  Choose a simple 2D test function with a known minimum (e.g., Rosenbrock function, Beale function).
2.  Implement the update rules for standard SGD, SGD with Momentum, and NAG from scratch using NumPy or using framework primitives (like PyTorch/TensorFlow by manually applying gradients and optimizer steps).
3.  Initialize all optimizers at the same starting point, far from the minimum.
4.  Run each optimizer for a fixed number of iterations, recording the (x, y) coordinates at each step. Use the *same* learning rate initially for all.
5.  Plot the 2D loss surface using a contour plot.
6.  Overlay the optimization paths (sequences of recorded coordinates) for SGD, Momentum, and NAG on the contour plot using different colors/markers.
7.  Analyze the plots: Compare how quickly each optimizer approaches the minimum, how much they overshoot or oscillate, and how NAG's "lookahead" behavior appears compared to standard Momentum.
8.  **Challenge:** Experiment with different learning rates and momentum coefficients (e.g., 0.9, 0.99). How do these changes affect the trajectories and convergence speed?

---

### 隼 **Exercise 2: Adam/AdamW Deep Dive & Weight Decay**

**Goal:** Implement Adam/AdamW (or use framework versions) and empirically compare their performance, particularly focusing on the effect of L2 regularization (weight decay).

**Instructions:**

1.  Choose a standard image classification dataset (e.g., CIFAR-10) and a moderately complex model (e.g., a simple CNN like LeNet-5 or a small ResNet).
2.  Set up a training loop using PyTorch or TensorFlow.
3.  Train the model using the **Adam** optimizer. Add L2 regularization by setting the `weight_decay` parameter in the optimizer constructor (e.g., `weight_decay=1e-4`). Train for a fixed number of epochs and record the final validation accuracy and loss.
4.  Reset the model weights.
5.  Train the model again using the **AdamW** optimizer, using the *same* learning rate and `weight_decay` value as in step 3. Train for the same number of epochs and record the final validation accuracy and loss.
6.  Compare the final performance metrics (accuracy, loss) achieved with Adam vs AdamW when using the same `weight_decay` value.
7.  Read the AdamW paper (linked in Resources) and explain *why* AdamW often performs better than Adam when weight decay is used. Relate it to how weight decay is applied in each algorithm.
8.  **Challenge:** Repeat the experiment with different `weight_decay` strengths (e.g., 1e-5, 1e-3). Does the performance gap between Adam and AdamW change?

---

### 隼 **Exercise 3: RMSprop Implementation & Comparison**

**Goal:** Understand and implement the RMSprop optimization algorithm and compare its convergence characteristics to SGD and Momentum.

**Instructions:**

1.  Implement the RMSprop update rule from scratch (using NumPy or framework primitives) or use the framework's built-in version. Pay attention to the moving average of squared gradients and the epsilon term for stability.
2.  Choose a suitable test function (2D like in Exercise 1 or a simple ML model training task).
3.  Train the model or optimize the function using RMSprop. Tune its hyperparameters (learning rate, decay factor/alpha, epsilon).
4.  Compare its convergence speed and stability (e.g., plot loss curves) against standard SGD and SGD with Momentum on the same task.
5.  Discuss the motivation behind RMSprop: How does adapting the learning rate based on the magnitude of recent gradients help?
6.  **Challenge:** How does RMSprop differ fundamentally from AdaGrad? What problem with AdaGrad does RMSprop attempt to solve?

---

### 隼 **Exercise 4: Optimizer Stability on Noisy Data**

**Goal:** Investigate the convergence stability and final performance of different optimizers (SGD, Momentum, Adam, RMSprop) when training on a dataset with potentially noisy labels or a complex loss landscape.

**Instructions:**

1.  Choose a dataset and task. To simulate noise, you could artificially flip a percentage of labels in a standard dataset like MNIST or CIFAR-10. Alternatively, use a dataset known to be somewhat challenging.
2.  Select a simple model architecture suitable for the task.
3.  Train the model separately using different optimizers: SGD, SGD with Momentum, Adam, RMSprop. Tune hyperparameters for each.
4.  Use the same number of training epochs for all runs.
5.  Plot the training loss curves for all optimizers on the same graph.
6.  Compare the curves: Which optimizer shows the smoothest convergence? Which converges fastest initially? Are there significant oscillations or spikes?
7.  Compare the final validation accuracy/performance achieved by each optimizer.
8.  Discuss which optimizer appeared most robust or stable under the potentially noisy conditions.
9.  **Challenge:** Introduce gradient clipping during training for all optimizers. Does this improve the stability of any of the optimizers, particularly SGD or Momentum, on this noisy task?

---

### 隼 **Exercise 5: Loss Landscape Visualization (Conceptual & Tool-Based)**

**Goal:** Gain intuition about how different optimizers navigate the loss landscape using visualization tools.

**Instructions:**

1.  Research methods and tools for visualizing high-dimensional loss landscapes (e.g., filter normalization methods projecting to 1D or 2D). Refer to resources like losslandscape.com.
2.  Find a pre-computed visualization or use a library (like `lucid` or others specifically for loss landscape plotting, if available and manageable) to visualize the landscape for a standard model/dataset (e.g., ResNet on CIFAR-10).
3.  Conceptually trace or overlay the expected paths of different optimizers (based on your understanding from previous exercises) onto the visualization:
    * How might SGD navigate sharp valleys or plateaus?
    * How would Momentum help cross small local minima or accelerate in flat regions?
    * How might Adam's adaptive learning rates behave in areas with varying gradient magnitudes?
4.  Discuss the relationship between the geometry of the loss landscape (e.g., presence of local minima, saddle points, flat regions, sharp valleys) and the performance/behavior of different optimizers.
5.  **Challenge:** If using a tool, try to generate visualizations at different stages of training (early vs. late). Does the landscape appear to change as the model trains?

---