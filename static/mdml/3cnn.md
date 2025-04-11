## 倹 Subtopic 3.1: Convolutional Neural Networks (CNNs) Deep Dive

**Goal:** Gain a deeper understanding of advanced convolutional operations beyond standard 2D convolutions, including filter visualization, transposed convolutions for upsampling, dilated convolutions for larger receptive fields, and the utility of 1x1 convolutions.

**Resources:**

* **CNN Explainer:** [Interactive Visualization Tool](https://poloclub.github.io/cnn-explainer/)
* **PyTorch Conv Layers:** [Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html), [ConvTranspose2d](https://pytorch.org/docs/stable/generated/torch.nn.ConvTranspose2d.html)
* **TensorFlow Conv Layers:** [Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D), [Conv2DTranspose](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2DTranspose)
* **Transposed Convolution Explanation:** [Blog Post/Tutorial](https://towardsdatascience.com/what-is-transposed-convolutional-layer-40e5e6e31c11)
* **Dilated/Atrous Convolution Explanation:** [Blog Post/Tutorial](https://towardsdatascience.com/review-dilated-convolution-semantic-segmentation-9d5a5bd768f5)
* **1x1 Convolutions:** [Paper/Blog explaining utility ("Network in Network")](https://arxiv.org/abs/1312.4400)

---

### 隼 **Exercise 1: Visualizing First Layer Filters**

**Goal:** Train a simple CNN and visualize the filters learned by the first convolutional layer to gain insight into the basic features detected.

**Instructions:**

1.  Build and train a simple CNN (e.g., 2-3 conv layers) on an image dataset like MNIST, Fashion-MNIST, or CIFAR-10.
2.  After training, access the weights of the *first* convolutional layer. The weights typically have a shape like `(out_channels, in_channels, kernel_height, kernel_width)`.
3.  For grayscale input (e.g., MNIST, `in_channels=1`), each filter `(kernel_height, kernel_width)` can be directly visualized as an image. For color input (e.g., CIFAR-10, `in_channels=3`), you might visualize each input channel separately or convert the `(3, H, W)` filter to a displayable format.
4.  Use Matplotlib or Seaborn to plot the learned filters (weights) as grayscale or color images. Arrange them in a grid.
5.  Analyze the visualizations. What kinds of patterns do the first layer filters seem to detect (e.g., edges, corners, specific colors, textures)?
6.  **Challenge:** Train the same network on two different datasets (e.g., MNIST vs. CIFAR-10). Compare the visualized first-layer filters. Are the learned features dataset-dependent?

---

### 隼 **Exercise 2: Understanding Transposed Convolutions**

**Goal:** Implement and analyze the output shape and behavior of a Transposed Convolution layer (`ConvTranspose2d`) used for upsampling feature maps.

**Instructions:**

1.  Create a small input tensor representing a feature map (e.g., `1xCxHxW` like `1x16x8x8` using PyTorch/TensorFlow).
2.  Define a `ConvTranspose2d` layer. Key parameters include `in_channels`, `out_channels`, `kernel_size`, `stride`, `padding`, `output_padding`.
3.  Experiment with different parameter combinations:
    * **Basic Upsampling:** Use `stride=2`, `padding=kernel_size // 2 - 1` (typical calculation, adjust as needed). Pass the input tensor through the layer and observe the output shape `(H_out, W_out)`. How does it relate to the input shape and stride?
    * **Effect of Kernel Size:** Keep stride=2, vary the kernel size. How does it affect the output?
    * **Effect of Padding:** How does padding influence the output size?
    * **Effect of `output_padding`:** What problem does `output_padding` solve when the output size might be ambiguous due to stride? Find a combination of input size, kernel size, stride, and padding where `output_padding` is needed to achieve a specific target output size.
4.  Explain why Transposed Convolution is sometimes called "Deconvolution" but why that term can be misleading. It performs a standard convolution but rearranges input/output relationships to achieve upsampling.
5.  **Challenge:** Build a minimal autoencoder-like structure with a Conv2d layer followed by a ConvTranspose2d layer. Try to make the output shape match the input shape. Pass data through and visualize input vs. output.

---

### 隼 **Exercise 3: Applying Dilated (Atrous) Convolutions**

**Goal:** Use dilated convolutions to increase the receptive field of a CNN layer without increasing the number of parameters or reducing spatial resolution.

**Instructions:**

1.  Create an input tensor (e.g., `1xCxHxW`).
2.  Define a standard `Conv2d` layer with `kernel_size=3`, `stride=1`, `padding=1`. Calculate its theoretical receptive field on the input.
3.  Define a `Conv2d` layer with the *same* parameters but add `dilation=2`. Pass the input tensor through it. Observe the output shape (it should be the same as the standard conv if padding is adjusted correctly, e.g., `padding=dilation * (kernel_size // 2)`).
4.  Define another `Conv2d` layer with `dilation=3`.
5.  Explain how dilation works: It introduces gaps between the kernel weights, allowing the kernel to cover a wider area of the input feature map.
6.  Discuss the benefit: How does dilation increase the effective receptive field compared to the standard convolution with the same kernel size and parameter count?
7.  In what applications is this particularly useful (e.g., semantic segmentation, dense prediction tasks)?
8.  **Challenge:** Stack multiple dilated convolution layers (e.g., with increasing dilation rates like 1, 2, 4). What potential issue can arise if dilation rates share common factors ("gridding effect")? How can this be mitigated (e.g., using Hybrid Dilated Convolutions - HDC)?

---

### 隼 **Exercise 4: The Role of 1x1 Convolutions**

**Goal:** Understand the different ways 1x1 convolutions are used in modern CNN architectures.

**Instructions:**

1.  Consider a feature map input with shape `(N, C_in, H, W)`.
2.  Define a `Conv2d` layer with `kernel_size=1`, `stride=1`, `padding=0`. Set `out_channels` to a value `C_out`.
3.  Pass the input tensor through this 1x1 convolution layer. What is the shape of the output tensor?
4.  Explain the primary functions achieved by a 1x1 convolution:
    * **Dimensionality Reduction/Increase:** How can it change the number of channels (`C_in` to `C_out`) while preserving the spatial dimensions (`H`, `W`)? When is reducing channels (creating a bottleneck) useful? When is increasing channels useful?
    * **Adding Non-linearity:** If followed by an activation function (like ReLU), how does the 1x1 convolution allow learning complex combinations across channels, acting like a small fully connected network applied at each spatial location?
5.  Find examples of architectures that heavily utilize 1x1 convolutions (e.g., GoogLeNet/Inception modules, ResNet bottleneck blocks). Explain the specific role the 1x1 convolution plays in those blocks (e.g., reducing computation before a 3x3 conv, increasing channels after).
6.  **Challenge:** Implement a simple "bottleneck" block using a sequence of 1x1 conv (reduce channels), 3x3 conv (process spatially), and 1x1 conv (restore/increase channels). Compare the parameter count and computational cost (e.g., FLOPs, conceptually) of this block to a single 3x3 convolution with the same input/output channel dimensions as the block's start/end.

---