## 倹 Subtopic 3.3: Network Design Principles

**Goal:** Understand fundamental principles guiding the design of effective CNN architectures, including the trade-offs between network width and depth, the motivation behind Inception modules, and the use of factorized convolutions.

**Resources:**

* **GoogLeNet / Inception Paper:** [Szegedy et al. - Going Deeper with Convolutions](https://arxiv.org/abs/1409.4842)
* **Deep Learning Book:** [Chapter on Convolutional Networks](https://www.deeplearningbook.org/contents/convnets.html)
* **Factorized Convolutions:** [Example in Inception V3 paper](https://arxiv.org/abs/1512.00567)
* **Width vs Depth Studies:** (Often found in papers analyzing specific architectures like ResNets or EfficientNets)

---

### 隼 **Exercise 1: Width vs. Depth Trade-off**

**Goal:** Empirically investigate the impact of increasing network depth versus increasing network width on performance and parameter count.

**Instructions:**

1.  Design a simple baseline CNN architecture (e.g., a few stacked Conv-ReLU-Pool layers).
2.  Create two variations:
    * **Deeper Network:** Keep the number of channels (width) in each layer the same as the baseline, but significantly increase the number of convolutional layers (depth).
    * **Wider Network:** Keep the number of layers (depth) the same as the baseline, but significantly increase the number of channels (width) in each convolutional layer.
3.  Try to roughly match the parameter count or computational cost (FLOPs) between the Deeper and Wider networks, if possible, by adjusting the specific depth/width increases. (This might be difficult, focus on the trend).
4.  Train all three networks (Baseline, Deeper, Wider) on a standard dataset (e.g., CIFAR-10).
5.  Compare the final validation accuracy achieved by the three networks.
6.  Compare the parameter counts and potentially training times.
7.  Discuss the findings: Did increasing depth or width provide a better performance improvement for this baseline architecture and dataset? What are the potential downsides of making networks excessively deep (vanishing/exploding gradients, training time) or excessively wide (memory usage, parameter count)?
8.  **Challenge:** How do techniques like skip connections (ResNets) change the conventional wisdom regarding the limits of network depth?

---

### 隼 **Exercise 2: Implementing an Inception Module**

**Goal:** Implement a basic Inception module (as in GoogLeNet) combining convolutions with different kernel sizes and pooling within a single block.

**Instructions:**

1.  Review the structure of an early Inception module (e.g., "Inception v1"). It typically consists of parallel branches:
    * 1x1 Convolution branch.
    * 1x1 Convolution followed by 3x3 Convolution branch.
    * 1x1 Convolution followed by 5x5 Convolution branch.
    * MaxPool layer followed by 1x1 Convolution branch.
2.  Pay close attention to the use of **1x1 convolutions before the 3x3 and 5x5 convolutions**. What is their purpose here? (Hint: Dimensionality reduction/bottleneck).
3.  Implement this Inception module as a custom layer/module in PyTorch or TensorFlow. The module should take the number of input channels as an argument and define the number of output channels for each internal 1x1, 3x3, and 5x5 convolution (refer to the paper for typical values or choose reasonable ones).
4.  The outputs of all parallel branches are **concatenated** along the channel dimension at the end of the module. Ensure the spatial dimensions (H, W) are preserved throughout the branches using appropriate padding.
5.  Create a dummy input tensor and pass it through your implemented Inception module. Verify the output shape (channels should be the sum of output channels from each branch).
6.  **Challenge:** Build a small network by stacking a few instances of your Inception module. Train it on a simple dataset.

---

### 隼 **Exercise 3: Understanding Factorized Convolutions**

**Goal:** Understand how larger convolutions can be factorized into smaller, sequential convolutions to reduce parameters and computation, as used in later Inception versions.

**Instructions:**

1.  Consider replacing a standard 5x5 convolution. The InceptionV3 paper proposes factorizing it into **two stacked 3x3 convolutions**.
2.  Assume an input feature map with `C` channels and an output feature map with `C` channels.
    * Calculate the approximate parameter count for a standard 5x5 convolution: `C * C * 5 * 5`.
    * Calculate the approximate parameter count for two stacked 3x3 convolutions (the first mapping `C` to `C` channels, the second mapping `C` to `C` channels): `(C * C * 3 * 3) + (C * C * 3 * 3)`.
3.  Compare the parameter counts. By what factor is the computation reduced?
4.  Explain the hypothesis behind this factorization: Does stacking two 3x3 convolutions capture a similar effective receptive field as one 5x5 convolution? Does it potentially introduce more non-linearity (if activations are used between them)?
5.  Research another factorization mentioned in Inception papers: Factorizing an `NxN` convolution into a `1xN` followed by an `Nx1` convolution (or vice-versa). Calculate the parameter savings for this factorization (e.g., for N=3 or N=7).
6.  **Challenge:** Implement both a standard 5x5 conv layer and a block consisting of two stacked 3x3 conv layers (with an activation in between). Compare their parameter counts using framework tools (`model.summary()` or similar).

---

### 隼 **Exercise 4: Network-in-Network (NiN) Concept**

**Goal:** Understand the core ideas of the Network-in-Network paper, particularly the use of MLP-like structures (using 1x1 convolutions) within convolutional blocks and Global Average Pooling.

**Instructions:**

1.  Read the abstract or introduction of the "Network in Network" paper (linked in resources).
2.  Explain the concept of the "MLPConv" layer proposed in the paper. How is a micro multi-layer perceptron (MLP) implemented using convolutional layers? (Hint: Stacked 1x1 convolutions with activation functions).
3.  What is the motivation for replacing standard linear convolutional filters with these MLPConv layers? (Hint: Learning more complex and abstract features within the receptive field).
4.  Explain the concept of **Global Average Pooling (GAP)** as introduced in the NiN paper as a replacement for traditional fully connected layers at the end of a CNN.
    * How does GAP work? (Average each feature map spatially down to a single value).
    * If the layer before GAP has `C` feature maps, what is the size of the output vector after GAP?
    * What are the advantages of GAP over Flatten + Fully Connected layers (e.g., parameter reduction, built-in spatial invariance, better correspondence between feature maps and categories)?
5.  **Challenge:** Modify a simple CNN architecture to replace the final Flatten and Dense layers with a Global Average Pooling layer followed by a single Dense layer for classification. Train both versions and compare parameter counts and performance.

---