## 倹 Subtopic 4.8.7: Evaluation & Interpretability for Transformer Models

**Goal:** Learn to evaluate Transformer-based models using standard NLP metrics and benchmarks, understand the challenges in evaluating LLMs, and explore basic techniques for interpreting their behavior and predictions.

**Resources:**

* **NLP Metrics:**
    * **BLEU/ROUGE:** [MoldStud Blog](https://moldstud.com/articles/p-the-importance-of-evaluation-metrics-in-building-strong-nlp-applications), [Lamatic.ai Blog](https://blog.lamatic.ai/guides/llm-evaluation-metrics/)
    * **GLUE/SuperGLUE:** [GLUE Benchmark](https://gluebenchmark.com/), [SuperGLUE Benchmark](https://super.gluebenchmark.com/)
* **LLM Evaluation Challenges:** [Lamatic.ai Blog](https://blog.lamatic.ai/guides/llm-evaluation-metrics/)
* **Interpretability:**
    * **Attention Visualization:** [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
    * **LIME/SHAP for Transformers:** [Restack.io Article](https://www.restack.io/p/explainable-ai-answer-transformer-interpretability-cat-ai)
    * **Transformer-specific Interpretability:** [ACL Anthology Tutorial Slides](https://aclanthology.org/2024.eacl-tutorials.4.pdf)

---

### 隼 **Exercise 1: Metrics for Generative Tasks (BLEU & ROUGE)**

**Goal:** Understand and calculate BLEU and ROUGE scores for evaluating text generation tasks like machine translation and summarization.

**Instructions:**

1.  Explain **BLEU (Bilingual Evaluation Understudy)** score:
    * What task is it primarily used for?
    * How does it work conceptually (n-gram precision, brevity penalty)?
    * Is a higher or lower BLEU score better?
2.  Explain **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)** score:
    * What task is it primarily used for?
    * What are the common variants (ROUGE-N for n-gram recall, ROUGE-L for longest common subsequence)?
    * Is a higher or lower ROUGE score better?
3.  Given a machine-generated translation/summary and one or more human reference translations/summaries:
    * Manually calculate a simplified BLEU-1 score (unigram precision with brevity penalty).
    * Manually calculate a simplified ROUGE-1 score (unigram recall).
4.  Use a library (e.g., `nltk.translate.bleu_score`, `rouge-score` pip package) to calculate BLEU and ROUGE scores for a few example generated vs. reference texts.
5.  Discuss the limitations of BLEU and ROUGE. Do they capture semantic similarity or fluency well?
6.  **Challenge:** Why are multiple reference translations/summaries beneficial when calculating BLEU/ROUGE?

---

### 隼 **Exercise 2: Metrics for NLU Tasks (GLUE/SuperGLUE)**

**Goal:** Understand the purpose of benchmark suites like GLUE and SuperGLUE and the types of NLU tasks and metrics they include.

**Instructions:**

1.  What are **GLUE (General Language Understanding Evaluation)** and **SuperGLUE** benchmarks? What is their primary purpose in NLP research?
2.  List at least 3-4 different types of NLU tasks included in GLUE/SuperGLUE (e.g., sentiment analysis, natural language inference, question answering, paraphrase detection).
3.  For each task you listed, identify a common evaluation metric used (e.g., Accuracy, F1-score, Matthews Correlation Coefficient, Exact Match).
4.  How are overall scores on GLUE/SuperGLUE typically calculated (e.g., macro-average of individual task scores)?
5.  Why were these benchmarks created, and what impact have they had on the development of pre-trained language models?
6.  **Challenge:** SuperGLUE was designed to be more challenging than GLUE. Research one task that is present in SuperGLUE but not GLUE (or is significantly harder in SuperGLUE) and explain why it's more difficult.

---

### 隼 **Exercise 3: Challenges in Evaluating Large Language Models (LLMs)**

**Goal:** Discuss the specific difficulties and limitations in reliably evaluating the performance of modern, very large language models.

**Instructions:**

1.  Beyond standard task-specific metrics, what are some of the broader capabilities or qualities of LLMs that are hard to evaluate quantitatively? (e.g., coherence, creativity, factual accuracy/hallucinations, safety/bias, reasoning ability).
2.  Explain the concept of **"hallucinations"** in LLM outputs. Why is this a significant evaluation challenge?
3.  Discuss the limitations of relying solely on automated metrics for LLM evaluation. Why is human evaluation still critical? What are the drawbacks of human evaluation?
4.  Research and briefly describe emerging benchmarks or approaches designed to evaluate more nuanced aspects of LLMs, such as:
    * Truthfulness/Factual Accuracy (e.g., TruthfulQA).
    * Robustness to adversarial inputs.
    * Ethical considerations and bias detection.
5.  **Challenge:** If an LLM is fine-tuned for a very specific domain or task not covered by standard benchmarks, how might you design an effective evaluation strategy for it?

---

### 隼 **Exercise 4: Attention Visualization**

**Goal:** Use attention visualization techniques to gain insights into what parts of the input sequence a Transformer model focuses on when making predictions.

**Instructions:**

1.  Use a library like `transformers` from Hugging Face and a pre-trained model that outputs attention weights (e.g., BERT, GPT-2). Ensure `output_attentions=True` is set when calling the model.
2.  Choose a task and an input sample:
    * For classification: An input sentence.
    * For translation (if using an encoder-decoder model): A source sentence.
3.  Extract the attention weights from the model's output. Attention weights typically have a shape like `(batch_size, num_heads, seq_len_query, seq_len_key)`.
4.  Select a specific layer and attention head to visualize.
5.  Use a tool (e.g., `bertviz` library, or plot manually with Matplotlib/Seaborn) to visualize the attention matrix for your chosen layer/head and input sample. This often involves showing which input tokens (keys) are attended to by each output token (queries).
6.  Interpret the visualization:
    * For self-attention in an encoder: Do certain tokens attend strongly to other related tokens in the sentence?
    * For encoder-decoder cross-attention in translation: When generating a target word, which source words does the decoder attend to?
7.  **Challenge:** Average the attention weights across all heads in a specific layer. Does this averaged attention provide a clearer or different interpretation compared to a single head? Why might different heads learn to focus on different aspects of the input?

---

### 隼 **Exercise 5: Introduction to Model-Agnostic Interpretability (LIME/SHAP on Transformers)**

**Goal:** Understand how model-agnostic interpretability techniques like LIME and SHAP can be conceptually applied to Transformer models to explain individual predictions.

**Instructions:**

1.  Explain the core idea of **LIME (Local Interpretable Model-agnostic Explanations)**. How does it approximate the behavior of a complex model (like a Transformer) locally around a specific prediction using a simpler, interpretable model?
2.  Explain the core idea of **SHAP (SHapley Additive exPlanations)**. How does it use concepts from game theory (Shapley values) to assign an importance value (contribution) to each input feature for a specific prediction?
3.  Discuss how LIME or SHAP could be applied to a Transformer-based text classifier:
    * What would constitute an "input feature" (e.g., individual words/tokens, presence/absence of words)?
    * How would LIME generate "neighboring" samples by perturbing the input text?
    * What would the SHAP values for each token in an input sentence represent regarding the model's classification decision?
4.  What are some of the challenges in applying LIME/SHAP to text data and Transformer models (e.g., defining meaningful perturbations, computational cost for SHAP)?
5.  **Challenge:** Compare attention visualization with LIME/SHAP for explaining Transformer predictions. What different types of insights might each method provide? Are they complementary?

---

### 隼 **(Optional) Exercise 6: Transformer-Specific Interpretability Methods**

**Goal:** Become aware of interpretability techniques developed specifically for the Transformer architecture.

**Instructions:**

1.  The ACL tutorial slides mention that model-agnostic methods might have limitations for Transformers and that Transformer-specific methods are emerging.
2.  Research one or two Transformer-specific interpretability techniques beyond simple attention visualization. Examples mentioned or related include:
    * **Layer-wise Relevance Propagation (LRP)** adapted for Transformers.
    * **Contextual Decomposition.**
    * **Analyzing specific head functions or neuron activations.**
    * **Logit Lens:** Examining predictions at intermediate layers.
3.  For the chosen technique(s), briefly explain its core idea and what kind of insights it aims to provide about the Transformer's internal workings or decision-making process.
4.  Why might methods designed specifically for the Transformer architecture (leveraging knowledge of self-attention, feed-forward layers, residual connections) potentially offer deeper or more accurate insights than purely model-agnostic approaches?
5.  **Challenge:** Can any of these Transformer-specific methods help in understanding phenomena like "polysemanticity" of neurons or identifying "circuits" within the model?

---