## 倹 Subtopic 4.7.4: Conditional GANs (cGANs)

**Goal:** Understand how to condition Generative Adversarial Networks on auxiliary information (like class labels or embeddings) to control the generation process, and implement a cGAN.

**Resources:**

* **cGAN Paper:** [Mirza and Osindero, 2014 - Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784)
* **Tutorials on cGANs:** GeeksforGeeks, MathWorks
* **Methods for Feeding Conditional Info:** Concatenation, Embedding layers
* **Applications of cGANs:** Image-to-image translation, image generation from text/attributes

---

### 隼 **Exercise 1: Understanding Conditional Generation**

**Goal:** Explain the motivation and basic mechanism for conditioning in GANs.

**Instructions:**

1.  What is the primary limitation of an unconditional GAN in terms of controlling its output?
2.  Define Conditional GAN (cGAN). How does it address the limitation of unconditional GANs?
3.  Describe the two main ways conditional information `y` (e.g., a class label) is typically fed into:
    * The Generator `G(z, y)`
    * The Discriminator `D(x, y)`
    (Hint: Concatenation with noise/image, using embedding layers for `y` then concatenating/projecting).
4.  How does the objective function of a cGAN differ (if at all) conceptually from the original GAN minimax objective, given that both G and D now also see `y`?
5.  **Challenge:** Besides class labels, what other forms of conditional information `y` could be used in a cGAN (e.g., text descriptions, bounding boxes, segmentation masks)?

---

### 隼 **Exercise 2: Modifying G and D for Conditioning (MNIST Example)**

**Goal:** Implement modifications to simple Generator and Discriminator architectures to incorporate class label conditioning for a dataset like MNIST.

**Instructions:**

1.  Choose MNIST (digits 0-9) as your dataset. The condition `y` will be the digit label.
2.  **Generator Modification:**
    * Start with a simple MLP or DCGAN-style generator architecture for MNIST.
    * For class labels, use an `Embedding` layer to convert the integer label `y` into a dense vector `y_emb`.
    * How would you combine `y_emb` with the input latent noise vector `z` before the first layer of G? (Common methods: concatenate `z` and `y_emb`, or project `y_emb` to match `z`'s dimension and add/multiply). Implement one such method.
3.  **Discriminator Modification:**
    * Start with a simple MLP or DCGAN-style discriminator.
    * Similar to G, convert the input label `y` into an embedding `y_emb`.
    * How would you combine `y_emb` with the input image `x` for the discriminator? (Common methods: concatenate `y_emb` (reshaped to be spatial if D is convolutional) with `x`'s feature maps, or project and add to an intermediate layer). Implement one such method.
4.  Implement these modified G and D architectures in PyTorch or TensorFlow. Verify input/output shapes.
5.  **Challenge:** Instead of simple concatenation for the discriminator, try projecting the label embedding `y_emb` to the same spatial dimensions as the image and concatenating it as an additional channel to the input image.

---

### 隼 **Exercise 3: Training a Conditional GAN (cGAN) on MNIST**

**Goal:** Train the implemented cGAN to generate specific digits from MNIST based on provided class labels.

**Instructions:**

1.  Use your modified G and D from Exercise 2. Prepare the MNIST dataset, ensuring you have access to both images and their corresponding labels.
2.  Set up the cGAN training loop:
    * **Discriminator Training:**
        * Get a batch of real images `x_real` and their labels `y_real`.
        * Generate fake images: Sample noise `z`, sample random labels `y_fake_cond`, generate `x_fake = G(z, y_fake_cond)`.
        * Calculate `loss_D` based on `D(x_real, y_real)` and `D(x_fake, y_fake_cond)`. Update D.
    * **Generator Training:**
        * Sample noise `z` and random labels `y_gen_cond`.
        * Generate `x_fake = G(z, y_gen_cond)`.
        * Calculate `loss_G` based on `D(x_fake, y_gen_cond)`. Update G.
3.  Train the cGAN. Periodically, generate images for *each* digit class (0 through 9) by feeding fixed noise vectors and the specific class label to G. Visualize these generated digits.
4.  Compare the generated digits to those from an unconditional GAN (if you trained one previously). Can you control the output of the cGAN?
5.  **Challenge:** What happens if the conditional information provided to G during its training phase is different from the conditional information provided to D when evaluating `D(G(z,y))` for G's loss? Why must they be consistent?

---

### 隼 **Exercise 4: Evaluating cGAN Output Quality per Class**

**Goal:** Assess if the cGAN is generating recognizable and diverse samples for each specified condition.

**Instructions:**

1.  Using your trained cGAN from Exercise 3:
2.  For each class label (e.g., digits 0 through 9 for MNIST):
    * Generate a batch of N images (e.g., N=100) by feeding the same fixed class label and N different random noise vectors `z` to the generator.
    * Visually inspect the generated images for that class. Are they recognizable as the target digit? Is there diversity among the N samples for that digit, or are they all very similar (minor mode collapse per class)?
3.  If you have a pre-trained MNIST classifier, classify the generated images for each class and report the accuracy. Does the classifier recognize the generated digits correctly according to their intended class label?
4.  Discuss any observed differences in generation quality or diversity across different classes. Are some digits harder for the cGAN to generate well?
5.  **Challenge:** Try interpolating the *conditional input embedding* `y_emb` between two classes (e.g., from digit '1' embedding to digit '7' embedding) while keeping the noise vector `z` fixed. Visualize the generated images. Does the cGAN produce a smooth transition?

---