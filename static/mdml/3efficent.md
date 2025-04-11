## 倹 Subtopic 3.2: Efficient CNN Architectures

**Goal:** Understand and implement techniques used in efficient CNN architectures designed for mobile devices or resource-constrained environments, focusing on depthwise separable convolutions, squeeze-and-excitation blocks, and related concepts.

**Resources:**

* **MobileNet Paper:** [Howard et al. - MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/abs/1704.04861) (Depthwise Separable Convolutions)
* **Squeeze-and-Excitation (SE) Paper:** [Hu et al. - Squeeze-and-Excitation Networks](https://arxiv.org/abs/1709.01507)
* **ShuffleNet Paper:** [Zhang et al. - ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices](https://arxiv.org/abs/1707.01083) (Channel Shuffle)
* **PyTorch/TensorFlow Layers:** Framework implementations of DepthwiseConv2D, SeparableConv2D, and standard layers needed to build SE blocks.

---

### 隼 **Exercise 1: Depthwise Separable Convolutions**

**Goal:** Understand and implement depthwise separable convolutions as used in MobileNets, comparing their parameter count and computational cost to standard convolutions.

**Instructions:**

1.  Describe the two stages of a depthwise separable convolution:
    * **Depthwise Convolution:** Applies a *single* filter per input channel. What is the shape of the output feature map? How many filters are used in total?
    * **Pointwise Convolution (1x1 Convolution):** Applies 1x1 convolutions to combine the outputs of the depthwise convolution. What is its purpose?
2.  Consider a standard `Conv2d` layer with `in_channels=C_in`, `out_channels=C_out`, `kernel_size=K`. Calculate its approximate parameter count and computational cost (e.g., FLOPs, proportional to `C_in * C_out * K*K`).
3.  Now consider implementing the same transformation using a depthwise separable convolution:
    * Depthwise Conv: `kernel_size=K`, applied to `C_in` channels (parameter count? FLOPs?).
    * Pointwise Conv (1x1): `in_channels=C_in`, `out_channels=C_out` (parameter count? FLOPs?).
    * Calculate the total parameter count and FLOPs for the depthwise separable convolution.
4.  Compare the parameter count and FLOPs of the standard convolution vs. the depthwise separable convolution for typical values (e.g., K=3, C_in=128, C_out=256). By roughly what factor are parameters and computation reduced?
5.  Implement a depthwise separable block using your framework's layers (e.g., `Conv2d` with `groups=in_channels` for depthwise, followed by `Conv2d` with `kernel_size=1` for pointwise, OR use built-in `SeparableConv2D` if available). Verify input/output shapes.
6.  **Challenge:** Build a small CNN using standard convolutions and another using depthwise separable convolutions for most layers. Compare their total parameter counts. Train both on a simple dataset and compare performance vs. parameter trade-offs.

---

### 隼 **Exercise 2: Squeeze-and-Excitation (SE) Block Implementation**

**Goal:** Implement an SE block and integrate it into a CNN architecture to perform channel-wise feature recalibration.

**Instructions:**

1.  Describe the two main operations within an SE block applied to a feature map `X` with shape `(N, C, H, W)`:
    * **Squeeze:** Global Average Pooling across spatial dimensions (H, W). What is the shape of the output? What does it represent?
    * **Excitation:** Two Fully Connected (FC) layers with a non-linearity in between. The first FC layer reduces the number of channels (`C`) to `C/r` (where `r` is a reduction ratio), and the second FC layer expands it back to `C`. A Sigmoid activation is typically applied at the end. What is the shape of the final output of the Excitation step? What do these values represent?
2.  How is the output of the Excitation step used to recalibrate the original input feature map `X`? (Hint: Channel-wise multiplication/scaling).
3.  Implement an SE block as a custom module/layer in PyTorch or TensorFlow. It should take the number of input channels `C` and a reduction ratio `r` as parameters.
4.  Integrate your SE block into a standard CNN architecture (e.g., add it after some convolutional blocks in a simple ResNet-like structure).
5.  Train the network with SE blocks and compare its performance (e.g., accuracy on CIFAR-10) to the baseline network without SE blocks. Did the SE blocks provide an improvement?
6.  **Challenge:** Visualize the channel attention weights (the output of the Sigmoid in the Excitation step) for a few sample images. Do different channels receive significantly different attention weights?

---

### 隼 **Exercise 3: ShuffleNet Concepts (Channel Shuffle)**

**Goal:** Understand the motivation and mechanism behind the channel shuffle operation used in ShuffleNet, designed to work efficiently with pointwise group convolutions.

**Instructions:**

1.  Consider using **Pointwise Group Convolutions** (1x1 convolutions applied separately to groups of input channels) as an efficiency measure. What is the potential downside of stacking multiple pointwise group convolutions without mixing information *between* the groups? (Hint: Information flow is restricted within groups).
2.  Explain the **Channel Shuffle** operation: Given an input feature map with `G * N` channels (organized into `G` groups of `N` channels each), how does channel shuffle rearrange the channels to ensure that the next group convolution receives input from different groups from the previous layer? Draw a simple diagram illustrating the reshape, transpose, and flatten steps for a small example (e.g., G=2, N=3, total 6 channels).
3.  Why is channel shuffle particularly important for architectures like ShuffleNet that rely heavily on pointwise group convolutions?
4.  Implement the channel shuffle operation as a function or layer in PyTorch/TensorFlow using basic tensor manipulation (reshape, permute/transpose, contiguous/reshape). Verify that it correctly rearranges channels for a sample input tensor.
5.  **Challenge:** Build a simplified ShuffleNet unit incorporating pointwise group convolution, channel shuffle, and potentially a depthwise convolution, following the architecture described in the ShuffleNet paper.

---

### 隼 **Exercise 4: Comparing Efficiency Metrics**

**Goal:** Evaluate and compare different efficient CNN architectures (e.g., MobileNetV1/V2, ShuffleNetV1/V2, EfficientNet-B0) based on standard metrics like parameter count, FLOPs, and accuracy on a benchmark dataset.

**Instructions:**

1.  Choose a standard image classification benchmark dataset (e.g., CIFAR-10, or use reported results on ImageNet).
2.  Select implementations of several efficient CNN architectures (available in libraries like `torchvision.models`, `tf.keras.applications`, or `timm`).
3.  For each selected architecture:
    * Find its reported (or calculate using a tool like `ptflops` or `tf.profiler`) **FLOPs** (Floating Point Operations per second - measure of computational cost).
    * Find its **parameter count**.
    * Find its reported top-1 **accuracy** on the benchmark dataset (e.g., ImageNet). If training yourself on CIFAR-10, train each model and record accuracy.
4.  Create a table comparing these architectures based on Accuracy, Parameters, and FLOPs.
5.  Plot Accuracy vs. FLOPs and Accuracy vs. Parameters for the different architectures.
6.  Analyze the plots and table. Which architectures achieve the best trade-off between accuracy and efficiency (FLOPs/parameters)? Discuss how different techniques (depthwise separable conv, SE blocks, channel shuffle, compound scaling in EfficientNet) contribute to these trade-offs.
7.  **Challenge:** Choose one specific efficient architecture (e.g., MobileNetV2). Research its specific block structure (e.g., the inverted residual block). How does it differ from MobileNetV1 or standard residual blocks?

---