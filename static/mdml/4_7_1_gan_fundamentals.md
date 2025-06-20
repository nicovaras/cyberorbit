## 倹 Subtopic 4.7.1: GAN Fundamentals & The Minimax Game

**Goal:** Understand the core components of a Generative Adversarial Network (Generator and Discriminator), the adversarial training process, the formulation of the minimax loss function, and common challenges like mode collapse.

**Resources:**

* **Original GAN Paper:** [Goodfellow et al., 2014 - Generative Adversarial Nets](https://arxiv.org/abs/1406.2661)
* **GAN Tutorial (TensorFlow):** [DCGAN Tutorial](https://www.tensorflow.org/tutorials/generative/dcgan) (Illustrates G/D architecture and training loop)
* **GAN Tutorial (PyTorch):** [DCGAN Tutorial](https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html)
* **Blog Post on GAN Loss Functions:** [Understanding GAN Loss Functions](https://developers.google.com/machine-learning/gan/loss)
* **Mode Collapse Explanation:** [Blog Post/Article explaining mode collapse](https://www.baeldung.com/cs/gan-mode-collapse)

---

### 隼 **Exercise 1: Designing a Simple Generator & Discriminator**

**Goal:** Implement the basic neural network architectures for a Generator (G) and a Discriminator (D) suitable for a simple dataset (e.g., generating 1D Gaussian data or very low-resolution images like 8x8 MNIST digits).

**Instructions:**

1.  Choose a simple data type to generate (e.g., 1D data points sampled from a Gaussian distribution, or flattened 8x8 pixel images).
2.  **Generator (G):**
    * Define an input: A latent vector `z` (e.g., 1D noise of size 10-100).
    * Design a simple MLP architecture (e.g., 2-3 fully connected layers with ReLU/LeakyReLU activations).
    * The output layer should produce data of the chosen type (e.g., a single scalar for 1D data, or 64 scalars for 8x8 flattened images, potentially with a Tanh activation to scale outputs to [-1, 1] if generating normalized images).
3.  **Discriminator (D):**
    * Define an input: A data sample (either real or generated by G), matching the output shape of G.
    * Design a simple MLP architecture (e.g., 2-3 fully connected layers with LeakyReLU/ReLU activations).
    * The output layer should produce a single scalar probability (the "realness" score), typically passed through a Sigmoid activation function.
4.  Implement these G and D architectures using PyTorch or TensorFlow. Instantiate them and verify their input/output shapes with dummy tensors.
5.  **Challenge:** What considerations would you have for the capacity (number of layers/neurons) of G versus D? Should one generally be more powerful than the other?

---

### 隼 **Exercise 2: Implementing the Minimax Loss Function**

**Goal:** Implement the original minimax loss function for training GANs from the Goodfellow et al. paper.

**Instructions:**

1.  Recall the GAN minimax objective function:
    `min_G max_D V(D, G) = E_{x~p_data(x)}[log D(x)] + E_{z~p_z(z)}[log(1 - D(G(z)))]`
2.  Separate this into two loss functions, one for the Discriminator (D) and one for the Generator (G):
    * **Discriminator Loss (`loss_D`):** D wants to maximize `log D(x_real) + log(1 - D(x_fake))`. This is equivalent to minimizing `- [log D(x_real) + log(1 - D(x_fake))]`.
    * **Generator Loss (`loss_G`):** G wants to minimize `log(1 - D(x_fake))` (original formulation) OR maximize `log D(x_fake)` (non-saturating heuristic, often preferred).
3.  Write Python functions using PyTorch/TensorFlow that calculate these losses, given:
    * `D_real_outputs`: Discriminator's output (logits or probabilities after sigmoid) for real data.
    * `D_fake_outputs`: Discriminator's output for fake data generated by G.
    * Use binary cross-entropy (`BCELoss` or `BinaryCrossentropy`) appropriately with target labels (1 for real, 0 for fake for D; 1 for fake for G if using the non-saturating version).
4.  Test your loss functions with dummy output tensors from a hypothetical D. Ensure the losses behave as expected (e.g., `loss_D` is low if D correctly classifies real as real and fake as fake).
5.  **Challenge:** Explain why the non-saturating Generator loss (`maximize log D(G(z))`) is often preferred over the original minimax version (`minimize log(1 - D(G(z)))`) in practice. (Hint: Gradient saturation for G when D is very confident).

---

### 隼 **Exercise 3: GAN Training Loop (Conceptual Outline)**

**Goal:** Outline the alternating training steps for the Generator and Discriminator in a GAN.

**Instructions:**

1.  Describe the typical GAN training loop, emphasizing the alternating updates:
    * **Discriminator Training Phase:**
        * Sample a mini-batch of real data `x_real`.
        * Sample a mini-batch of latent vectors `z` and generate fake data `x_fake = G(z)`.
        * Pass both `x_real` and `x_fake` through the Discriminator `D`.
        * Calculate `loss_D` using the outputs `D(x_real)` and `D(x_fake)`.
        * Compute gradients of `loss_D` with respect to D's parameters and update D.
    * **Generator Training Phase:**
        * Sample a new mini-batch of latent vectors `z`.
        * Generate fake data `x_fake = G(z)`.
        * Pass `x_fake` through the (now updated) Discriminator `D`.
        * Calculate `loss_G` using `D(x_fake)`.
        * Compute gradients of `loss_G` with respect to G's parameters (importantly, D's parameters are frozen/not updated here) and update G.
2.  Why is it generally recommended to train the Discriminator for `k` steps for every one step of the Generator (or vice-versa) in some cases, especially early in training?
3.  What are the roles of the two separate optimizers (one for D, one for G)?
4.  **Challenge:** When updating the Generator, why is it important to detach the fake samples from the Generator's computation graph if they are used for the Discriminator's loss, or alternatively, why must the Discriminator's weights be frozen during the Generator's update?

---

### 隼 **Exercise 4: Simulating the Minimax Game (Simple Scenario)**

**Goal:** Conceptually simulate a few steps of the GAN training process on a very simple problem to understand the adversarial dynamic.

**Instructions:**

1.  Consider a 1D GAN trying to learn a target Gaussian distribution `P_data = N(0, 1)`.
2.  Initialize a simple Generator G (e.g., a linear transformation of 1D noise `z ~ N(0,1)`) and Discriminator D (e.g., a simple logistic regressor on the input value).
3.  **Iteration 1:**
    * **Train D:** Sample from `P_data` (real samples). Generate fake samples from G (initially random). Train D to distinguish them. How might D's decision boundary look?
    * **Train G:** Generate fake samples. Get D's feedback. How would G adjust its parameters to make its samples look more "real" to the current D?
4.  **Iteration 2:**
    * **Train D:** D now sees improved fake samples from G and the real samples. How might D's decision boundary shift?
    * **Train G:** G sees the new D. How does G adapt further?
5.  Describe how this iterative process, in theory, leads G to produce samples closer to `P_data` and D to become better at distinguishing real from increasingly sophisticated fakes.
6.  When does this game reach an equilibrium according to the original GAN paper? (Hint: `D(x) = 0.5` everywhere, and G's distribution matches `P_data`).
7.  **Challenge:** What is "mode collapse"? In this 1D Gaussian example, how might mode collapse manifest (e.g., G always produces samples around a single value, even if `P_data` is broader)?

---