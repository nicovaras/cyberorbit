## 倹 Subtopic 4.1: Fundamentals of Bayesian Inference

**Goal:** Understand and apply the core concepts of Bayesian inference, including Bayes' Theorem, the roles of prior and likelihood, posterior interpretation, and the use of conjugate priors for analytical solutions.

**Resources:**

* **Bayes' Theorem:** [Wikipedia Article](https://en.wikipedia.org/wiki/Bayes%27_theorem)
* **Conjugate Prior:** [Wikipedia Article](https://en.wikipedia.org/wiki/Conjugate_prior)
* **SciPy Stats Distributions:** [Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) (Beta, Binomial, Normal, etc.)
* **Matplotlib/Seaborn:** For plotting distributions.
* **Introductory Bayesian Text/Tutorial:** (e.g., "Bayesian Methods for Hackers" book/notebooks, "Statistical Rethinking" book/lectures)

---

### 隼 **Exercise 1: Applying Bayes' Theorem (Simple Example)**

**Goal:** Calculate posterior probabilities using Bayes' Theorem directly for a simple scenario with discrete events.

**Instructions:**

1.  Consider a medical test scenario:
    * Disease prevalence (Prior P(Disease)): 1%
    * Test Sensitivity (P(Positive Test | Disease)): 95% (True Positive Rate)
    * Test Specificity (P(Negative Test | No Disease)): 98% (True Negative Rate)
    * Calculate P(Negative Test | Disease) = 1 - Sensitivity.
    * Calculate P(Positive Test | No Disease) = 1 - Specificity (False Positive Rate).
    * Calculate Prior P(No Disease) = 1 - P(Disease).
2.  A patient tests positive. Use Bayes' Theorem to calculate the **posterior probability** P(Disease | Positive Test).
    * `P(D|Pos) = [ P(Pos|D) * P(D) ] / P(Pos)`
    * Calculate the denominator `P(Pos)` using the law of total probability: `P(Pos) = P(Pos|D)*P(D) + P(Pos|No D)*P(No D)`.
3.  Implement this calculation in Python. Print the prior probability of having the disease and the posterior probability after observing a positive test.
4.  Interpret the result. How did the positive test update the belief about the patient having the disease? Is the posterior probability high or low, and why?
5.  **Challenge:** Calculate the posterior probability P(No Disease | Negative Test).

---

### 隼 **Exercise 2: Beta-Binomial Conjugacy Simulation**

**Goal:** Simulate Bayesian updating for a binomial likelihood (e.g., coin flips) using its conjugate prior, the Beta distribution.

**Instructions:**

1.  Assume you want to estimate the bias `theta` (probability of heads) of a potentially unfair coin.
2.  **Prior:** Choose a Beta distribution as your prior belief about `theta`. Start with a relatively uninformative prior, like `Beta(alpha=1, beta=1)` (which is uniform). Plot this prior distribution using `scipy.stats.beta`.
3.  **Likelihood:** Assume the number of heads `h` in `n` flips follows a Binomial distribution `Binomial(n, theta)`.
4.  **Data:** Simulate flipping the coin `n=20` times with a true bias `true_theta=0.7`. Record the number of heads `h`.
5.  **Posterior Calculation:** Use the conjugate prior update rule: If the prior is `Beta(alpha, beta)` and you observe `h` heads in `n` trials, the posterior distribution is `Beta(alpha + h, beta + n - h)`. Calculate the parameters of the posterior Beta distribution based on your prior and simulated data.
6.  Plot the posterior distribution over `theta` alongside the prior distribution. How has observing the data updated your belief (distribution) about the coin's bias?
7.  Calculate the mean of the posterior distribution (`alpha_post / (alpha_post + beta_post)`). How close is it to the true bias `true_theta`?
8.  **Challenge:** Repeat steps 4-7, simulating more data (e.g., `n=100`). How does the posterior distribution change (become narrower/more peaked)? How does the posterior mean change?

---

### 隼 **Exercise 3: Normal-Normal Conjugacy Simulation**

**Goal:** Simulate Bayesian updating for the mean `mu` of a Normal distribution (with known variance) using its conjugate prior, also a Normal distribution.

**Instructions:**

1.  Assume you want to estimate the mean height `mu` of a population. Assume the standard deviation `sigma` is known (e.g., `sigma=10 cm`).
2.  **Prior:** Choose a Normal distribution as your prior belief about `mu`. Let the prior be `Normal(mu_0=170, sigma_0^2=15^2)`. Plot this prior.
3.  **Likelihood:** Assume observed heights `x_i` come from a Normal distribution `Normal(mu, sigma^2)` where `sigma` is known.
4.  **Data:** Simulate observing `n=5` height measurements drawn from a Normal distribution with true mean `true_mu=180` and known standard deviation `sigma=10`. Calculate the sample mean `x_bar` of your simulated data.
5.  **Posterior Calculation:** Use the conjugate prior update rule: If the prior is `Normal(mu_0, sigma_0^2)` and you observe `n` data points with sample mean `x_bar` from a likelihood `Normal(mu, sigma^2)` (known `sigma`), the posterior for `mu` is `Normal(mu_n, sigma_n^2)`, where:
    * `mu_n = (sigma_0^2 / (sigma_0^2 + sigma^2/n)) * x_bar + ( (sigma^2/n) / (sigma_0^2 + sigma^2/n) ) * mu_0`
    * `1 / sigma_n^2 = 1 / sigma_0^2 + n / sigma^2`
    Calculate the posterior mean `mu_n` and variance `sigma_n^2`.
6.  Plot the posterior distribution for `mu` alongside the prior distribution. How has the data shifted your belief about the mean height? Is the posterior narrower or wider than the prior?
7.  **Challenge:** Repeat steps 4-6 with more data (`n=50`). How does the posterior change? How much influence does the prior have when you have more data?

---

### 隼 **Exercise 4: Prior Sensitivity Analysis**

**Goal:** Investigate how the choice of prior distribution affects the resulting posterior distribution, especially with limited data.

**Instructions:**

1.  Use the Beta-Binomial setup from Exercise 2. Simulate a small amount of data (e.g., `n=10` flips, observe `h=7` heads).
2.  Calculate and plot the posterior distribution using three different priors:
    * **Uniform Prior:** `Beta(1, 1)`
    * **Informative Prior biased towards fair coin:** `Beta(10, 10)`
    * **Informative Prior biased towards biased coin:** `Beta(5, 2)`
3.  Plot the three priors and their corresponding posteriors on separate graphs (or overlaid clearly).
4.  Compare the resulting posterior distributions. How much does the posterior differ based on the chosen prior when the amount of data is small?
5.  Repeat the process but with a larger amount of data (e.g., `n=100`, observe `h=70` heads). Now compare the posteriors resulting from the three different priors.
6.  Discuss the results: How does the influence of the prior change as the amount of data increases?
7.  **Challenge:** What is an "improper" prior? Why might they sometimes be used, and what are the potential risks?

---

### 隼 **Exercise 5: Interpreting Posterior Distributions**

**Goal:** Practice extracting meaningful summaries and interpretations from a calculated posterior distribution.

**Instructions:**

1.  Use the final posterior distribution obtained from one of the previous exercises (e.g., the Beta posterior from Exercise 2 with `n=100` data points).
2.  **Point Estimates:** Calculate common point estimates from the posterior distribution:
    * Posterior Mean (Expected Value)
    * Posterior Median (50th percentile)
    * Posterior Mode (Maximum a Posteriori or MAP estimate - the peak of the distribution)
3.  **Credible Intervals:** Calculate a 95% credible interval (Bayesian confidence interval) for the parameter. This is typically done by finding the 2.5th and 97.5th percentiles of the posterior distribution (e.g., using `scipy.stats.beta.ppf`). Interpret the meaning of this interval.
4.  **Hypothesis Testing (Conceptual):** How would you use the posterior distribution to evaluate a hypothesis like "Is the coin biased towards heads (theta > 0.5)?" (Hint: Calculate the probability mass of the posterior distribution where theta > 0.5).
5.  Plot the posterior distribution and mark the mean, median, mode, and the 95% credible interval on the plot.
6.  **Challenge:** Compare the Bayesian credible interval to a frequentist confidence interval calculated for the same parameter (e.g., confidence interval for a binomial proportion). How does their interpretation differ fundamentally?

---