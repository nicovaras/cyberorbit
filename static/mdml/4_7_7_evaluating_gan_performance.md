## 倹 Subtopic 4.7.7: Evaluating GAN Performance

**Goal:** Understand the challenges in evaluating GANs, learn to calculate and interpret common quantitative metrics like Inception Score (IS) and Fréchet Inception Distance (FID), and appreciate the role of qualitative assessment.

**Resources:**

* **Challenges in GAN Evaluation:** [Survey/Review Articles on GAN Evaluation]
* **Inception Score (IS):** [Original Paper (Improved Techniques for Training GANs)](https://arxiv.org/abs/1606.03498), [Wikipedia explanation](https://en.wikipedia.org/wiki/Inception_score), [PyPI package `gans-eval`](https://pypi.org/project/gans-eval/)
* **Fréchet Inception Distance (FID):** [Original Paper (GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium)](https://arxiv.org/abs/1706.08500), [PyTorch FID implementations (e.g., `pytorch-frechet-inception-distance` on GitHub)](https://github.com/hukkelas/pytorch-frechet-inception-distance), [MachineLearningMastery explanation](https://machinelearningmastery.com/how-to-implement-the-frechet-inception-distance-fid-from-scratch/)
* **Qualitative vs. Quantitative Evaluation:** [Sharif.ir Slides](https://sharif.ir/~beigy/courses/14022/40959/Lect-24.pdf)

---

### 隼 **Exercise 1: Challenges in GAN Evaluation**

**Goal:** Articulate why evaluating the performance of generative models, particularly GANs, is inherently difficult.

**Instructions:**

1.  Unlike supervised learning models which have clear ground truth labels for calculating metrics like accuracy or MSE, what makes evaluating GANs more challenging?
2.  Discuss the two main aspects of GAN performance that evaluation metrics aim to capture:
    * **Sample Quality/Fidelity:** How realistic or "good" are the individual generated samples?
    * **Sample Diversity:** Does the generator produce a wide variety of samples that capture the full diversity of the true data distribution, or does it suffer from mode collapse?
3.  Why is it often insufficient to just look at the generator or discriminator loss curves to assess GAN performance?
4.  What is the role of human evaluation (qualitative assessment) in judging GAN outputs, and what are its limitations (e.g., subjectivity, cost, scalability)?
5.  **Challenge:** Can a GAN have a low (good) discriminator loss but still produce poor quality or non-diverse samples? Explain why.

---

### 隼 **Exercise 2: Understanding Inception Score (IS)**

**Goal:** Explain the intuition and calculation steps behind the Inception Score (IS).

**Instructions:**

1.  The Inception Score uses a pre-trained Inception v3 model (trained on ImageNet) for evaluation. What two properties of the generated images does IS try to measure based on the Inception v3 model's predictions?
    * Property 1 (Related to individual image quality/clarity): Conditional label distribution `p(y|x_generated)` should have low entropy (i.e., Inception model is confident about what object is in the image).
    * Property 2 (Related to diversity): Marginal label distribution `p(y)` (averaged over all generated images) should have high entropy (i.e., generator produces diverse images spanning many classes).
2.  Outline the steps to calculate IS:
    * Generate a large number of samples from your GAN.
    * For each generated sample `x`, get the conditional probability distribution `p(y|x)` over ImageNet classes from the Inception v3 model.
    * Calculate the marginal distribution `p(y) = mean_x[p(y|x)]`.
    * Calculate the KL divergence `D_KL(p(y|x) || p(y))` for each sample `x`.
    * Average these KL divergences over all samples and take the exponential: `IS = exp(E_x[D_KL(p(y|x) || p(y))])`.
3.  Is a higher or lower IS better? What are its typical ranges?
4.  What are some known limitations or criticisms of the Inception Score? (e.g., sensitivity to ImageNet classes, doesn't compare to real data distribution directly, can be fooled).
5.  **Challenge:** If a GAN only generates perfect images of a single class (e.g., only one specific dog breed perfectly), would it get a high or low IS? Explain why, considering both properties IS tries to measure.

---

### 隼 **Exercise 3: Understanding Fréchet Inception Distance (FID)**

**Goal:** Explain the intuition and calculation steps behind the Fréchet Inception Distance (FID), and how it improves upon IS.

**Instructions:**

1.  Like IS, FID also uses features extracted from a pre-trained Inception v3 model. Which layer's activations are typically used? (Hint: Often the activations from the last average pooling layer).
2.  FID compares the distribution of these Inception activations for a set of **real images** to the distribution of activations for a set of **generated images**.
3.  Outline the steps to calculate FID:
    * Extract Inception activations for a large set of real images from your target domain.
    * Extract Inception activations for a large set of generated images from your GAN.
    * Model the activations from the real images as a multivariate Gaussian distribution with mean `mu_real` and covariance matrix `Sigma_real`. Calculate these.
    * Model the activations from the generated images as a multivariate Gaussian with mean `mu_fake` and `Sigma_fake`. Calculate these.
    * The FID score is the Fréchet distance between these two Gaussian distributions:
      `FID = ||mu_real - mu_fake||^2 + Trace(Sigma_real + Sigma_fake - 2 * (Sigma_real * Sigma_fake)^(1/2))`
4.  Is a higher or lower FID score better? Why?
5.  How does FID address some of the limitations of IS? (Hint: Compares to real data, more robust to noise, less sensitive to mode dropping if the modes are far apart).
6.  **Challenge:** Implement the FID calculation (the formula part) using NumPy/SciPy, assuming you are given the means (`mu_real`, `mu_fake`) and covariance matrices (`Sigma_real`, `Sigma_fake`) of the activations. You'll need `scipy.linalg.sqrtm` for the matrix square root of the covariance product.

---

### 隼 **Exercise 4: Using Libraries for IS and FID Calculation**

**Goal:** Use existing libraries to calculate IS and FID for generated image samples.

**Instructions:**

1.  Train a simple GAN (e.g., DCGAN on MNIST or CIFAR-10) or use pre-generated samples from a trained GAN.
2.  Find a Python library that provides implementations for IS and FID (e.g., `gans-eval` on PyPI, `pytorch-fid` on GitHub, or built-in/community implementations in TensorFlow/PyTorch ecosystems). Install it.
3.  Prepare your generated images in the format required by the library (e.g., NumPy arrays, a directory of image files). Ensure pixel values are in the expected range (e.g., 0-255 or 0-1).
4.  If calculating FID, you will also need a set of real images from the same domain.
5.  Use the library functions to calculate:
    * Inception Score for your generated samples.
    * Fréchet Inception Distance between your generated samples and the real samples.
6.  Report the scores. Try to find reported IS/FID scores for well-known models on the dataset you used to get a sense of scale.
7.  **Challenge:** How does the number of samples used to calculate IS and FID affect the stability and reliability of the scores? Run the calculations with different numbers of generated/real samples and observe the variation.

---

### 隼 **Exercise 5: Qualitative Evaluation and Limitations of Metrics**

**Goal:** Appreciate the importance of visual inspection and understand the limitations of relying solely on quantitative metrics for GAN evaluation.

**Instructions:**

1.  Generate a diverse set of images from a GAN you've trained or from a pre-trained model.
2.  **Qualitative Assessment:**
    * Visually inspect the images for **fidelity**: Are they sharp? Do they have artifacts (e.g., checkerboard patterns, distorted shapes)? Do they look realistic for the domain?
    * Visually inspect for **diversity**: Are the samples varied, or do many look similar (indicating potential mode collapse)?
3.  Consider a GAN that achieves a very good (low) FID score but generates images that, while statistically similar to real image features, have subtle but consistent unrealistic artifacts that a human would notice. Why might FID miss this?
4.  Consider a GAN that has mode-collapsed to produce only one type of very high-quality image from the target distribution. How might IS and FID behave in this scenario? (IS might be high for quality but low for diversity aspect, FID might still be good if that one mode is very realistic and close to a mode in real data).
5.  Discuss why a combination of quantitative metrics and careful qualitative human evaluation is crucial for a holistic assessment of GAN performance.
6.  **Challenge:** Research "Precision and Recall for Distributions" as proposed by Kynkäänniemi et al. or Sajjadi et al. How do these metrics attempt to separately quantify fidelity (precision) and diversity (recall) of GANs, potentially offering more insight than single scalar values like IS/FID?

---