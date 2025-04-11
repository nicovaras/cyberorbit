## 倹 Subtopic 3.5: ResNet Variants & Successors

**Goal:** Explore and implement key ideas from popular ResNet variants like Wide ResNets (WRN), ResNeXt (Aggregated Residual Transformations), and DenseNets (Dense Connectivity).

**Resources:**

* **Wide ResNet Paper:** [Zagoruyko & Komodakis - Wide Residual Networks](https://arxiv.org/abs/1605.07146)
* **ResNeXt Paper:** [Xie et al. - Aggregated Residual Transformations for Deep Neural Networks](https://arxiv.org/abs/1611.05431)
* **DenseNet Paper:** [Huang et al. - Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993)
* **PyTorch/TensorFlow/Timm:** Pre-trained models and reference implementations often available.

---

### 隼 **Exercise 1: Implementing Wide ResNet Blocks**

**Goal:** Modify standard ResNet blocks to create Wide ResNet blocks by increasing the number of channels (width factor `k`) while potentially decreasing depth.

**Instructions:**

1.  Start with your ResNet Basic Block or Bottleneck Block implementation (Subtopic 3.4).
2.  Introduce a `width_factor` (k) parameter. Modify the number of channels in the convolutional layers *within* the block by multiplying the standard channel counts by `k`.
    * For Basic Block: Increase channels in both 3x3 layers.
    * For Bottleneck Block: Increase channels primarily in the 3x3 layer (or proportionally across all). The paper focuses on widening the 3x3 part of bottleneck blocks.
3.  Implement a Wide ResNet block (e.g., WRN-B(k) structure from the paper, often involving modifying the bottleneck block).
4.  Build a Wide ResNet model (e.g., WRN-28-10) using these wider blocks. Compared to a standard ResNet (e.g., ResNet-34), the WRN might have fewer layers (`depth=28`) but significantly more channels per layer (`width=10`).
5.  Compare the parameter count of your WRN model to a standard deeper ResNet (e.g., ResNet-50 or ResNet-101).
6.  Train the WRN on a dataset (e.g., CIFAR-10/100) and compare its performance and training efficiency (time per epoch) to a deeper, thinner baseline ResNet with a similar parameter count (if possible).
7.  Discuss the findings of the WRN paper: Why might wider but shallower ResNets sometimes train faster and achieve better performance than extremely deep, thin ones?
8.  **Challenge:** The WRN paper also suggests using Dropout within the residual blocks. Add Dropout to your Wide ResNet blocks and evaluate its effect.

---

### 隼 **Exercise 2: Implementing a ResNeXt Block (Grouped Convolutions)**

**Goal:** Implement a ResNeXt block using grouped convolutions within the bottleneck structure to approximate aggregated parallel transformations.

**Instructions:**

1.  Start with your ResNet Bottleneck Block implementation (Subtopic 3.4).
2.  Review the ResNeXt architecture idea: Replace the single 3x3 convolution in the bottleneck with multiple parallel paths (the "cardinality" dimension), implemented efficiently using **grouped convolutions**.
3.  Modify the Bottleneck Block:
    * Keep the initial 1x1 convolution (reducing channels).
    * Replace the standard 3x3 `Conv2d(planes, planes, ...)` with a `Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, groups=cardinality, bias=False)`. The `cardinality` parameter controls the number of groups (e.g., 32). Ensure `planes` is divisible by `cardinality`.
    * Keep the final 1x1 convolution (restoring/increasing channels).
    * Keep the shortcut connection logic (identity or projection).
4.  Implement this ResNeXt block module.
5.  Instantiate the block, pass a dummy input, and verify the output shape.
6.  Compare the parameter count and FLOPs of a ResNeXt block to a standard ResNet Bottleneck block with roughly the same output channel dimension. How does increasing cardinality (while potentially adjusting width) affect complexity? (ResNeXt aims to improve accuracy with similar complexity by increasing cardinality).
7.  **Challenge:** Build and train a small network using ResNeXt blocks (e.g., ResNeXt-50 32x4d). Compare its performance to a ResNet-50 baseline.

---

### 隼 **Exercise 3: Understanding DenseNet Connectivity**

**Goal:** Understand the dense connectivity pattern in DenseNets where each layer receives feature maps from all preceding layers within a block.

**Instructions:**

1.  Review the DenseNet architecture concept: Within a "Dense Block", the input to layer `L` is the concatenation of the feature maps produced by all preceding layers `0, 1, ..., L-1`.
2.  Draw a diagram illustrating the connections within a small Dense Block with 3-4 layers. Contrast this with the skip connection pattern in ResNets.
3.  Explain the concept of the **"growth rate" (k)** in DenseNets. If each layer within a block produces `k` feature maps, and the input to the block has `C_in` channels, what is the number of input channels to layer `L` within the block? (Hint: `C_in + (L-1)*k`).
4.  Discuss the potential advantages of dense connectivity:
    * Feature Reuse: How does it encourage reusing features learned by earlier layers?
    * Gradient Flow: How might it alleviate vanishing gradient issues even more effectively than ResNets?
    * Parameter Efficiency: Why might DenseNets achieve good performance with potentially fewer parameters than ResNets (though memory usage can be high)?
5.  Explain the role of **Transition Layers** between Dense Blocks in DenseNets. What operations do they typically perform (e.g., 1x1 convolution, pooling)? Why are they needed?
6.  **Challenge:** If each layer in a Dense Block produces `k` feature maps, and the block has `L` layers, how many total feature maps are concatenated as input to the Transition Layer following the block (assuming input `C_in`)? How can this lead to high memory consumption during training?

---

### 隼 **Exercise 4: Implementing a DenseNet Basic Layer & Block**

**Goal:** Implement the basic components of a DenseNet: a single layer (BN-ReLU-Conv) and a Dense Block that concatenates outputs.

**Instructions:**

1.  Implement a "Dense Layer" module. This typically consists of:
    * `BatchNorm2d`
    * `ReLU`
    * `Conv2d(in_channels, growth_rate, kernel_size=1, stride=1, bias=False)` (Optional: Bottleneck layer - reduce channels before 3x3)
    * `BatchNorm2d`
    * `ReLU`
    * `Conv2d(growth_rate_intermediate, growth_rate, kernel_size=3, stride=1, padding=1, bias=False)`
    (Note: `in_channels` will vary depending on where the layer is in the block).
2.  Implement a "Dense Block" module. It takes the number of layers `L`, initial `in_channels`, and `growth_rate` `k` as input.
    * Inside its `forward` method, maintain a list of feature maps.
    * Loop `L` times:
        * Concatenate the input feature maps collected so far along the channel dimension.
        * Pass the concatenated features through a Dense Layer instance (calculating the correct `in_channels` for the layer based on the concatenation).
        * Add the *output* of the Dense Layer (with `growth_rate` channels) to the list of feature maps to be concatenated in the next iteration.
    * The final output of the Dense Block is typically the concatenation of all feature maps generated within the block (or just the input plus all generated feature maps).
3.  Instantiate a Dense Block, pass a dummy input tensor, and verify the output shape and the increasing number of channels being fed into subsequent layers within the block.
4.  **Challenge:** Implement the Transition Layer module (1x1 Conv to reduce channels, followed by Average Pooling). Combine Dense Blocks and Transition Layers to build a small DenseNet architecture.

---

### 隼 **Exercise 5: Comparing ResNet, ResNeXt, DenseNet**

**Goal:** Conceptually compare the core ideas and trade-offs of ResNet, ResNeXt, and DenseNet architectures.

**Instructions:**

1.  Create a table summarizing the key architectural innovations of each:
    * **ResNet:** Core idea? (Residual learning via skip connections). Block type? (Basic/Bottleneck).
    * **ResNeXt:** Core idea? (Aggregated transformations via grouped conv/cardinality). How does it modify the ResNet block?
    * **DenseNet:** Core idea? (Dense connectivity via feature concatenation). How does information flow differ from ResNet?
2.  Compare the potential advantages and disadvantages of each regarding:
    * **Parameter Efficiency:** Which might achieve good accuracy with fewer parameters?
    * **Computational Cost (FLOPs):** How might they compare for similar performance levels?
    * **Memory Usage during Training:** Which architecture tends to require more memory due to feature map concatenation/storage?
    * **Gradient Flow:** Which architectures are particularly effective at mitigating vanishing gradients?
    * **Feature Reuse:** Which explicitly encourages feature reuse?
3.  Which architecture (or variant) might you choose for a task requiring maximum accuracy on a large dataset with sufficient computational resources? Which might be better suited for mobile deployment?
4.  **Challenge:** Research recent successors or combinations of these ideas (e.g., SENets applied to ResNeXt, DenseNet variations). How do newer architectures continue to build upon these foundational concepts?

---