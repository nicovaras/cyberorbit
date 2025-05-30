## 倹 Subtopic 4.7.2: Deep Convolutional GANs (DCGAN)

**Goal:** Understand and implement the architectural guidelines from the DCGAN paper that led to stable training of GANs with convolutional networks for image generation.

**Resources:**

* **DCGAN Paper:** [Radford et al., 2015 - Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks](https://arxiv.org/abs/1511.06434)
* **PyTorch DCGAN Tutorial:** [DCGAN Faces Tutorial](https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html)
* **TensorFlow DCGAN Tutorial:** [DCGAN Tutorial](https://www.tensorflow.org/tutorials/generative/dcgan)
* **Activation Functions:** ReLU, LeakyReLU, Tanh, Sigmoid.
* **Normalization Layers:** Batch Normalization (`BatchNorm2d`).

---

### 隼 **Exercise 1: DCGAN Architectural Guidelines**

**Goal:** Summarize and explain the key architectural modifications proposed in the DCGAN paper for stable training.

**Instructions:**

1.  Read the DCGAN paper, focusing on the "Approach and Model Architectures" section.
2.  List the main architectural guidelines proposed for both the Generator (G) and Discriminator (D). These include:
    * Replacing pooling layers with strided convolutions (Discriminator) and fractional-strided convolutions / transposed convolutions (Generator).
    * Using Batch Normalization in both G and D (with exceptions).
    * Removing fully connected hidden layers for deeper architectures.
    * Using ReLU activation in G for all layers except the output (which uses Tanh).
    * Using LeakyReLU activation in D for all layers.
3.  For each guideline, briefly explain its motivation or the problem it aimed to solve (e.g., why use strided convolutions instead of pooling? Why use LeakyReLU in D?).
4.  Which specific layers did the paper suggest *not* applying Batch Normalization to in G and D, and why?
5.  **Challenge:** The paper also mentions hyperparameter settings (optimizer, learning rate, batch size). How might these contribute to training stability alongside the architectural choices?

---

### 隼 **Exercise 2: Implementing a DCGAN Generator**

**Goal:** Implement a DCGAN Generator network using transposed convolutions, batch normalization, and appropriate activations, capable of generating small images (e.g., 64x64).

**Instructions:**

1.  Define the input: A latent vector `z` (e.g., of size 100).
2.  The Generator will use a series of `ConvTranspose2d` layers to upsample the latent vector to the desired image size (e.g., 64x64 with 3 color channels).
3.  Structure the Generator following DCGAN guidelines:
    * Start with a fully connected layer to project `z` to a suitable shape for the first transposed convolution (e.g., `latent_dim` -> `initial_channels * 4 * 4`). Reshape to `(batch_size, initial_channels, 4, 4)`.
    * Stack multiple `ConvTranspose2d` layers. Each layer should typically:
        * Upsample spatially (e.g., `stride=2`, `padding=1`, `kernel_size=4`).
        * Reduce the number of channels (e.g., `ngf*8` -> `ngf*4` -> `ngf*2` -> `ngf` -> `output_channels`).
        * Be followed by `BatchNorm2d` (except for the output layer's conv).
        * Use `ReLU` activation (except for the output layer).
    * The final `ConvTranspose2d` layer should output the target number of channels (e.g., 3 for RGB) and use a `Tanh` activation function to scale outputs to [-1, 1].
4.  Implement this Generator in PyTorch or TensorFlow. Initialize it and pass a dummy latent vector to verify output shape and layer connectivity.
5.  **Challenge:** Calculate the parameter count of your Generator. How does the choice of `ngf` (number of generator filters in the last conv layer before output) affect the model size?

---

### 隼 **Exercise 3: Implementing a DCGAN Discriminator**

**Goal:** Implement a DCGAN Discriminator network using strided convolutions, batch normalization, and LeakyReLU activations.

**Instructions:**

1.  Define the input: An image (e.g., 64x64 with 3 color channels, matching G's output).
2.  The Discriminator will use a series of `Conv2d` layers to downsample the image into a single probability score.
3.  Structure the Discriminator following DCGAN guidelines:
    * Stack multiple `Conv2d` layers. Each layer (except the first and last) should typically:
        * Downsample spatially (e.g., `stride=2`, `padding=1`, `kernel_size=4`).
        * Increase the number of channels (e.g., `input_channels` -> `ndf` -> `ndf*2` -> `ndf*4` -> `ndf*8`).
        * Be followed by `BatchNorm2d` (except for the input layer's conv and the output layer).
        * Use `LeakyReLU` activation (e.g., `slope=0.2`).
    * The final `Conv2d` layer should output a single channel (e.g., `kernel_size=4, stride=1, padding=0` if the feature map is 4x4 at this point, to get a 1x1 output).
    * Apply a `Sigmoid` activation function to the final output to get a probability.
4.  Implement this Discriminator in PyTorch or TensorFlow. Instantiate it and pass a dummy image tensor to verify output shape and layer connectivity.
5.  **Challenge:** Explain the purpose of not using Batch Norm in the first layer of the Discriminator, as is common practice.

---

### 隼 **Exercise 4: Training a DCGAN on Images**

**Goal:** Train the implemented DCGAN Generator and Discriminator on a real image dataset (e.g., MNIST, Fashion-MNIST, CIFAR-10, or a subset of CelebA).

**Instructions:**

1.  Prepare your chosen dataset:
    * Load images.
    * Resize to the target size for your G/D (e.g., 32x32 or 64x64).
    * Normalize pixel values to the range [-1, 1] (to match G's Tanh output).
    * Create a DataLoader.
2.  Instantiate your G and D models, and initialize their weights (the DCGAN paper suggests specific initialization from a Normal distribution with mean 0, std 0.02).
3.  Set up two optimizers (e.g., Adam, as recommended in the paper) with the specified learning rate and beta1. One for G's parameters, one for D's parameters.
4.  Implement the training loop from Subtopic 4.7.1 Exercise 3, using your DCGAN G and D, and the minimax loss functions.
5.  During training:
    * Periodically save generated image samples from a fixed latent vector `z_fixed` to visually monitor G's progress.
    * Plot G and D loss curves.
6.  Train for a sufficient number of epochs. Observe the quality of generated images.
7.  **Challenge:** Implement the "non-saturating" generator loss (`maximize log D(G(z))`) and compare its training stability and generated image quality to the original minimax generator loss (`minimize log(1 - D(G(z)))`).

---

### 隼 **Exercise 5: Analyzing DCGAN Latent Space**

**Goal:** Perform simple interpolations in the latent space of a trained DCGAN to observe how the generator maps latent vectors to image features.

**Instructions:**

1.  Use your trained DCGAN Generator from Exercise 4.
2.  Select two random latent vectors, `z1` and `z2`, from the noise distribution (e.g., `N(0,1)`).
3.  Perform **linear interpolation** between `z1` and `z2` in the latent space:
    * `z_interp(alpha) = (1 - alpha) * z1 + alpha * z2`, where `alpha` goes from 0 to 1 (e.g., in 10 steps).
4.  For each interpolated latent vector `z_interp(alpha)`, generate an image using `G(z_interp(alpha))`.
5.  Display the sequence of generated images. Do you observe smooth transitions between the images corresponding to `z1` and `z2`? What does this suggest about the learned latent space?
6.  **Challenge:** Try performing arithmetic in the latent space. For example, if your GAN is trained on faces: take an average latent vector for "man with glasses", subtract average "man without glasses", add average "woman without glasses". Does the resulting generated image look like a "woman with glasses"? (This requires a well-trained GAN and potentially specific latent vectors identified through other means, but the concept can be explored).
