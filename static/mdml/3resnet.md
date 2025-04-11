## 倹 Subtopic 3.4: Residual Networks (ResNets) & Skip Connections

**Goal:** Understand the motivation behind residual learning (ResNets), implement residual blocks with identity and projection shortcuts, and analyze their effectiveness in training very deep networks.

**Resources:**

* **ResNet Paper:** [He et al. - Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
* **Vanishing/Exploding Gradients:** [Explanation/Article](https://towardsdatascience.com/the-vanishing-gradient-problem-69bf08b15484)
* **PyTorch ResNet Implementation:** [torchvision.models.resnet](https://pytorch.org/vision/stable/_modules/torchvision/models/resnet.html) (Good reference for block structure)
* **TensorFlow ResNet Implementation:** [tf.keras.applications.ResNet50](https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet50) (Reference for block structure)

---

### 隼 **Exercise 1: The Vanishing Gradient Problem**

**Goal:** Empirically observe the difficulty in training very deep "plain" networks compared to shallower ones, illustrating the motivation for ResNets.

**Instructions:**

1.  Build two "plain" CNN architectures (stacked Conv-BN-ReLU layers, no skip connections) on a dataset like CIFAR-10:
    * **Plain-Shallow:** A network with a moderate depth (e.g., 8-10 layers).
    * **Plain-Deep:** A network with significantly more layers (e.g., 20-30 layers), keeping layer widths similar.
2.  Train both networks using the same optimizer and learning rate schedule. Plot the training loss and validation accuracy for both.
3.  Compare the results. Does the deeper plain network achieve better performance than the shallower one? Or does its performance degrade (or saturate sooner)? This degradation is the problem ResNets address.
4.  (Optional) Monitor the magnitude of gradients flowing back to the earlier layers during training for both networks. Do gradients appear smaller (vanish) in the deeper plain network?
5.  Discuss why simply stacking more layers in plain networks can lead to optimization difficulties (vanishing/exploding gradients, degradation problem).
6.  **Challenge:** Try initializing the deeper plain network using methods specifically designed to mitigate vanishing gradients (e.g., Kaiming He initialization). Does this solve the degradation problem entirely, or just delay it?

---

### 隼 **Exercise 2: Implementing a ResNet Basic Block (Identity Shortcut)**

**Goal:** Implement a standard ResNet "basic block" with two 3x3 convolutions and an identity skip connection.

**Instructions:**

1.  Define a module/layer for a ResNet Basic Block in PyTorch/TensorFlow. It should take `in_channels` and `out_channels` (or `planes`) and `stride` as input.
2.  The main path should consist of:
    * `Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)`
    * `BatchNorm2d(out_channels)`
    * `ReLU()`
    * `Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)`
    * `BatchNorm2d(out_channels)`
3.  Implement the **identity shortcut connection**:
    * If `stride == 1` and `in_channels == out_channels`, the shortcut is simply the input `x` itself.
    * (Handle the case where dimensions don't match in Exercise 3).
4.  In the `forward` method:
    * Calculate the output of the main path (`out`).
    * Add the shortcut connection to the output: `out += shortcut`.
    * Apply the final `ReLU()` activation *after* the addition.
5.  Instantiate the block with `stride=1` and `in_channels == out_channels`. Pass a dummy input tensor and verify the output shape.
6.  **Challenge:** What is "Pre-activation" ResNet? Modify the block structure to apply Batch Norm and ReLU *before* the convolutional layers, as suggested in the identity mappings paper by He et al.

---

### 隼 **Exercise 3: Implementing a ResNet Bottleneck Block (Projection Shortcut)**

**Goal:** Implement a ResNet "bottleneck block" using 1x1, 3x3, and 1x1 convolutions, including handling dimension changes with a projection shortcut.

**Instructions:**

1.  Define a module/layer for a ResNet Bottleneck Block. It typically takes `in_channels`, `planes` (bottleneck channels), `stride`, and an `expansion` factor (usually 4) as input. `out_channels` will be `planes * expansion`.
2.  The main path consists of:
    * `Conv2d(in_channels, planes, kernel_size=1, stride=1, bias=False)` + BN + ReLU
    * `Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)` + BN + ReLU
    * `Conv2d(planes, planes * expansion, kernel_size=1, stride=1, bias=False)` + BN
3.  Implement the **shortcut connection**:
    * Initialize `shortcut = x`.
    * If `stride != 1` OR `in_channels != planes * expansion` (i.e., dimensions need to change), apply a **projection shortcut**:
        * `shortcut = Conv2d(in_channels, planes * expansion, kernel_size=1, stride=stride, bias=False)` applied to the input `x`.
        * Follow this 1x1 convolution with a `BatchNorm2d(planes * expansion)`.
4.  In the `forward` method:
    * Calculate the output of the main path (`out`).
    * Calculate the shortcut output (identity or projection).
    * Add the shortcut: `out += shortcut`.
    * Apply the final `ReLU()`.
5.  Instantiate the block for a case requiring projection (e.g., `stride=2` or changing channel counts). Pass a dummy input and verify the output shape (`planes * expansion` channels).
6.  **Challenge:** Compare the parameter count and computational cost (FLOPs) of a Bottleneck block vs. two stacked Basic blocks that achieve a similar change in channels and spatial dimension reduction. Why are bottleneck blocks preferred for deeper ResNets (e.g., ResNet-50/101/152)?

---

### 隼 **Exercise 4: Building and Training a Small ResNet**

**Goal:** Construct a small ResNet model by stacking the implemented residual blocks and train it.

**Instructions:**

1.  Define a ResNet model architecture (e.g., ResNet-18 or ResNet-34 using Basic Blocks, or a smaller custom version). The structure usually involves:
    * An initial convolution and pooling layer.
    * Multiple "stages", where each stage consists of several residual blocks. The first block in a stage (except the first stage) typically handles downsampling using `stride=2` and potentially increases the number of channels.
    * A Global Average Pooling layer at the end.
    * A final fully connected layer for classification.
2.  Implement this architecture using your Basic Block (and potentially Bottleneck Block) modules from Exercises 2 & 3. Refer to standard ResNet structures (like PyTorch/TensorFlow implementations) for layer configurations (number of blocks, channels per stage).
3.  Train your ResNet model on a dataset like CIFAR-10.
4.  Compare its performance and training convergence (plot loss/accuracy curves) to the "Plain-Deep" network from Exercise 1. Does the ResNet train successfully and achieve better performance?
5.  **Challenge:** Implement a ResNet-50 architecture using your Bottleneck Blocks. Compare its parameter count and training behavior to ResNet-18/34.

---

### 隼 **Exercise 5: Ablation Study: The Skip Connection**

**Goal:** Empirically verify the importance of the skip connection by training a ResNet architecture with and without it.

**Instructions:**

1.  Take your working ResNet implementation from Exercise 4.
2.  Create a modified version of the network where the skip connection addition (`out += shortcut`) inside the residual blocks is **removed** (i.e., the output of the block is just the output of the main path followed by ReLU). This essentially turns it back into a "plain" network but with the ResNet block structure.
3.  Train both the original ResNet and the modified network (without skip connections) under identical conditions (optimizer, learning rate, epochs).
4.  Compare their training curves (loss, accuracy) and final performance.
5.  Discuss the results. How crucial is the skip connection for enabling the training of deep networks and achieving good performance? What does this ablation study demonstrate?
6.  **Challenge:** Try initializing both networks with very small weights. Does the plain version still struggle significantly more than the ResNet version even with careful initialization?

---