## Subtopic 3.7: Evaluating Generative Models and NLP Tasks

**Goal:** To understand and apply common automatic evaluation metrics (BLEU, ROUGE, Perplexity) for generative NLP tasks, recognize their limitations, and appreciate the importance of human evaluation.

**Resources:**

  * Hugging Face `evaluate` Library: [Evaluate Documentation](https://www.google.com/search?q=https://huggingface.co/docs/evaluate), [Available Metrics](https://huggingface.co/evaluate-metric) (See BLEU, ROUGE, Perplexity)
  * BLEU Score Explained: [Wikipedia - BLEU](https://en.wikipedia.org/wiki/BLEU)
  * ROUGE Score Explained: [Wikipedia - ROUGE (metric)](https://en.wikipedia.org/wiki/ROUGE_\(metric\))
  * Perplexity Explained: [Blog Post: Perplexity in Language Models](https://www.google.com/search?q=https://towardsdatascience.com/perplexity-in-language-models-87a196019a94)
  * Human Evaluation: [Article/Guide on Human Evaluation Best Practices for NLP](https://www.google.com/search?q=https://ai.googleblog.com/2019/08/beyond-accuracy-behavioral-testing-of.html) (Look for similar articles focusing on LLM evaluation)
  * `nltk` library (for BLEU): [NLTK Book - Ch 5. Categorizing and Tagging Words (includes BLEU example)](https://www.nltk.org/book/ch05.html)

-----

### Exercise 1: Calculating BLEU Score for Translation

**Goal:** Calculate the BLEU score, a metric commonly used for machine translation evaluation, using the `evaluate` library.
**Instructions:**

1.  Install `evaluate` and potentially `sacrebleu`: `pip install evaluate sacrebleu`.
2.  Define a list of candidate machine translations (predictions) and a list of corresponding reference translations (ground truth). Use simple example sentences. Make sure references are provided as a list *within* a list for each candidate, as BLEU supports multiple references.
    ```python
    predictions = ["the cat sat on the mat", "the quick brown fox jumps over the lazy dog"]
    references = [["the cat was on the mat", "there is a cat on the mat"], ["the fast brown fox jumps over the lazy canine"]]
    ```
3.  Load the BLEU metric using `evaluate.load("bleu")`.
4.  Compute the BLEU score using `results = bleu.compute(predictions=predictions, references=references)`.
5.  Print the results dictionary. Interpret the main `bleu` score and understand what higher scores generally indicate.
6.  Experiment with slightly modifying the predictions (e.g., changing one word, reordering words) and observe the impact on the BLEU score.

### Exercise 2: Calculating ROUGE Score for Summarization

**Goal:** Calculate ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L), commonly used for evaluating automatic summarization.
**Instructions:**

1.  Install necessary packages: `pip install evaluate rouge_score`. (You might also need `nltk` for tokenization: `pip install nltk`, then run `python -m nltk.downloader punkt`).
2.  Define a list of generated summaries (predictions) and a list of reference summaries (ground truth).
    ```python
    predictions = ["Minister says cat deaths investigated.", "General election vote talks continue."]
    references = ["Authorities are looking into the deaths of cats, the minister confirmed.", "Negotiations over the timing of the general election vote are ongoing."]
    ```
3.  Load the ROUGE metric using `evaluate.load("rouge")`.
4.  Compute the ROUGE scores using `results = rouge.compute(predictions=predictions, references=references)`.
5.  Print the results dictionary. Explain briefly what ROUGE-1, ROUGE-2, and ROUGE-L measure (overlap of unigrams, bigrams, and longest common subsequence, respectively).

### Exercise 3: Understanding Perplexity

**Goal:** Understand the concept of perplexity as a measure of how well a language model predicts a sample of text.
**Instructions:**

1.  Define perplexity conceptually. How does it relate to the probability assigned by the language model to the observed sequence of text? What does a lower perplexity score indicate about the model's fit to the text?
2.  Explain the mathematical relationship between perplexity and cross-entropy loss (Perplexity = exp(Cross-Entropy Loss)).
3.  Assume you have a simple language model and a short test sentence "the cat sat". If the model assigns probabilities P("the"), P("cat"|"the"), P("sat"|"the cat"), explain how you would calculate the perplexity for this sentence (conceptually, no complex calculation needed).
4.  Why is perplexity often used during the *pre-training* or *validation* phase of language model development, rather than being the sole metric for evaluating downstream task performance?
    **Challenge:** Use a pre-trained Causal LM (like GPT-2) from Hugging Face `transformers` and the `evaluate` library (`evaluate.load("perplexity", module_type="metric")`) to calculate the perplexity of a short piece of text. Refer to the `evaluate` documentation for usage.

### Exercise 4: Limitations of Automatic Metrics (BLEU/ROUGE)

**Goal:** Critically evaluate the limitations of n-gram based metrics like BLEU and ROUGE.
**Instructions:**

1.  Provide an example of two candidate sentences where one is clearly a better translation/summary than the other, but they might receive similar BLEU or ROUGE scores (e.g., one is fluent but misses key info, the other includes info but is grammatically poor). Explain why the scores might be similar.
2.  Explain why these metrics struggle with semantic equivalence (synonyms, paraphrasing). If a prediction uses different words but conveys the same meaning as the reference, how will BLEU/ROUGE typically score it?
3.  Why might these metrics penalize creativity or stylistic variations in generative tasks like story writing?
4.  How well do these metrics capture factual accuracy or detect hallucination in generated text?

### Exercise 5: Designing a Human Evaluation Protocol

**Goal:** Outline a simple protocol for evaluating the quality of LLM-generated text using human judgment.
**Instructions:**

1.  Choose a specific generative task (e.g., chatbot responses, email drafts, article summaries).
2.  Define 2-3 key quality dimensions for human evaluators to assess (e.g., Fluency/Grammaticality, Coherence, Relevance to prompt, Factual Accuracy, Tone, Helpfulness). Define a simple rating scale for each dimension (e.g., 1-5 Likert scale, Yes/No).
3.  Describe the information you would provide to the human evaluators (e.g., the input prompt, the generated text, potentially reference text or guidelines).
4.  How would you ensure consistency between different human evaluators (inter-annotator agreement)? Mention one technique (e.g., providing clear guidelines, calibration exercises, calculating agreement scores like Cohen's Kappa).
5.  Why is human evaluation often considered the "gold standard" despite being more expensive and time-consuming than automatic metrics?

### Project: Comparative Evaluation of Summaries

**Goal:** Generate summaries using different methods and evaluate them using both automatic metrics and a qualitative assessment.
**Instructions:**

1.  Choose a short article (e.g., 500-1000 words).
2.  Generate 2-3 different summaries for this article:
      * **Method 1:** Use a pre-trained abstractive summarization model (e.g., from Hugging Face Hub, like `bart-large-cnn`).
      * **Method 2:** Use an LLM (via API or local) with a simple zero-shot prompt like "Summarize the following article: [Article Text]".
      * **Method 3 (Reference):** Write a concise reference summary yourself (or find an existing one if available).
3.  Calculate ROUGE scores comparing Method 1 and Method 2 against your reference summary (Method 3).
4.  Perform a qualitative human assessment: Read the three summaries (Methods 1, 2, and 3). Subjectively evaluate Methods 1 and 2 based on criteria like coherence, conciseness, coverage of main points, and fluency, using your reference summary as a benchmark.
    **Portfolio Guidance:**



  * Create a report (e.g., in a Jupyter Notebook or `README.md`).
  * Include the original article (or a link).
  * Show the generated summaries (Method 1, Method 2) and your reference summary (Method 3).
  * Present the calculated ROUGE scores in a table.
  * Provide your qualitative assessment, comparing the strengths and weaknesses of the two automatic methods based on your reading.
  * Discuss whether the automatic ROUGE scores align with your qualitative judgment and reflect on the limitations observed.
  * Upload the report/notebook and any relevant code to a GitHub repository.