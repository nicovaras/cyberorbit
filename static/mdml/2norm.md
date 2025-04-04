## 倹 Subtopic 2.5: Normalization Layers as Implicit Regularizers

**Goal:** Analyze how normalization layers (Batch Normalization, Layer Normalization, etc.) stabilize training, speed up convergence, and can provide an implicit regularization effect.

**Resources:**

* **Batch Normalization Paper:** [Ioffe & Szegedy, 2015](https://arxiv.org/abs/1502.03167)
* **Layer Normalization Paper:** [Ba et al., 2016](https://arxiv.org/abs/1607.06450)
* **Instance Normalization Paper:** [Ulyanov et al., 2016](https://arxiv.org/abs/1607.08022)
* **Group Normalization Paper:** [Wu & He, 2018](https://arxiv.org/abs/1803.08494)
* **PyTorch Norm Layers:** [BatchNorm](https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html), [LayerNorm](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html), [InstanceNorm](https://pytorch.org/docs/stable/generated/torch.nn.InstanceNorm1d.html), [GroupNorm](https://pytorch.org/docs/stable/generated/torch.nn.GroupNorm.html)
* **TensorFlow Norm Layers:** [BatchNormalization](https://www.tensorflow.org/api_docs/python/tf/keras/layers/BatchNormalization), [LayerNormalization](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LayerNormalization), [InstanceNormalization (in TFA)](https://www.tensorflow.org/addons/api_docs/python/tfa/layers/InstanceNormalization), [GroupNormalization (in TFA)](https://www.tensorflow.org/addons/api_docs/python/tfa/layers/GroupNormalization)

---

### 隼 **Exercise 1: Implementing Batch Normalization**

**Goal:** Add Batch Normalization layers to a deep neural network and observe its effect on training speed and stability.

**Instructions:**

1.  Build a relatively deep MLP or CNN (e.g., >5 layers) for a standard classification task (e.g., CIFAR-10). Use standard activation functions like ReLU.
2.  Train this network **without** Batch Normalization. Carefully tune the learning rate. Plot training loss and validation accuracy. Note the number of epochs required to reach a certain performance level and observe training stability.
3.  Modify the network architecture by adding Batch Normalization layers **after** the linear/convolutional layers and **before** the activation functions.
4.  Train the modified network **with** Batch Normalization. You might be able to use a significantly higher learning rate now. Retune the learning rate if necessary. Plot the training loss and validation accuracy.
5.  Compare the training curves (speed of convergence, stability) and potentially the final performance with and without Batch Normalization.
6.  **Important:** Remember that BatchNorm behaves differently during training (using batch statistics) and evaluation (using running averages). Ensure your framework handles this correctly (via `model.train()` / `model.eval()`).
7.  **Challenge:** Visualize the distribution of activations for a specific layer before the activation function, both with and without Batch Normalization, during training. How does BatchNorm affect the distribution (mean and variance)?

---

### 隼 **Exercise 2: Batch Norm's Regularization Effect**

**Goal:** Investigate the implicit regularization effect often attributed to Batch Normalization.

**Instructions:**

1.  Use the network architectures with and without Batch Normalization from Exercise 1. Choose a setup prone to overfitting (e.g., small dataset, deep network).
2.  Train both networks (with and without BN) for enough epochs to observe overfitting in the non-BN version. Plot training vs. validation accuracy/loss for both.
3.  Compare the gap between training and validation performance for the two networks. Does the network with Batch Normalization exhibit less overfitting (a smaller gap)?
4.  Discuss the hypothesized reasons for BatchNorm's regularization effect (e.g., noise introduced by mini-batch statistics).
5.  **Challenge:** Train the Batch Normalization network *also* with additional explicit regularization like Dropout. Does adding Dropout provide further significant gains in generalization when BatchNorm is already present, or does BatchNorm handle much of the regularization?

---

### 隼 **Exercise 3: Batch Norm and Batch Size Sensitivity**

**Goal:** Analyze how the effectiveness of Batch Normalization can depend on the mini-batch size used during training.

**Instructions:**

1.  Use the network architecture *with* Batch Normalization from Exercise 1.
2.  Train the network using a **large batch size** (e.g., 128, 256, or as large as memory allows). Record the final validation performance.
3.  Train the *same* network again, but this time use a **very small batch size** (e.g., 2, 4, or 8). You may need to adjust the learning rate. Record the final validation performance.
4.  Compare the performance achieved with large vs. small batch sizes when using Batch Normalization.
5.  Explain why Batch Normalization's performance might degrade with very small batch sizes. (Hint: How reliable are the mean/variance estimates from small batches?).
6.  **Challenge:** Research alternatives like Group Normalization or Layer Normalization. Why are they considered less sensitive to batch size?

---

### 隼 **Exercise 4: Layer Normalization Implementation**

**Goal:** Implement Layer Normalization, typically used in Recurrent Neural Networks and Transformers, and compare its behavior to Batch Normalization.

**Instructions:**

1.  Build a simple MLP or potentially a sequence model (RNN/Transformer if familiar).
2.  Implement Layer Normalization (using framework layers). Unlike BatchNorm, Layer Normalization normalizes across the features/channel dimension for *each individual data sample* in the batch. Add LN layers (often *before* the activation function or attention/feed-forward blocks).
3.  Train the model with Layer Normalization. Plot training curves.
4.  Compare its performance and training dynamics to a similar model using Batch Normalization (if applicable) or no normalization.
5.  Discuss the key difference in the normalization axis between Batch Norm and Layer Norm. Why is Layer Norm often preferred in sequence models where sequence lengths can vary within a batch?
6.  **Challenge:** Repeat the batch size sensitivity experiment from Exercise 3, but using Layer Normalization instead of Batch Normalization. Is Layer Normalization's performance significantly affected by small batch sizes?

---

### 隼 **Exercise 5: Group Norm & Instance Norm (Conceptual & Use Cases)**

**Goal:** Understand the concepts behind Group Normalization and Instance Normalization and their typical application domains.

**Instructions:**

1.  Research Group Normalization (GN). How does it calculate the mean and variance? (Hint: It divides channels into groups). How does the `num_groups` parameter control its behavior?
2.  Research Instance Normalization (IN). How does it calculate the mean and variance? (Hint: Per channel, per instance). Note that IN is equivalent to GN with `num_groups` equal to the number of channels, and also equivalent to LayerNorm if applied over spatial dimensions as well.
3.  Discuss the typical use cases:
    * Why is Instance Normalization often used in style transfer tasks? (Hint: Contrast normalization).
    * Why was Group Normalization proposed as an alternative to Batch Normalization, particularly regarding batch size independence?
4.  Compare GN and IN to BN and LN based on the features/dimensions they normalize over.
5.  **Challenge:** If using a framework with support (like PyTorch or TFA), add Group Normalization to a CNN and compare its performance to Batch Normalization, especially when trained with small batch sizes.

---