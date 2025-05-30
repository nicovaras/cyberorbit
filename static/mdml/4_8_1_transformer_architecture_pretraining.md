## 倹 Subtopic 4.8.1: Transformer Architecture In-Depth & Pre-training Objectives

**Goal:** Gain a detailed understanding of the full Transformer encoder-decoder architecture, the nuances of its components like layer normalization and positional encodings, and the core self-supervised pre-training objectives (MLM, NSP, Autoregressive LM, Text-to-Text) that enable their powerful language understanding capabilities.

**Resources:**

* **Original Transformer Paper:** [Vaswani et al., 2017 - Attention Is All You Need](https://arxiv.org/abs/1706.03762)
* **BERT Paper:** [Devlin et al., 2018 - BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
* **GPT Paper Series:** (e.g., Radford et al. - original GPT papers)
* **T5 Paper:** [Raffel et al., 2019 - Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)
* **Hugging Face Documentation:** [Transformer Models](https://huggingface.co/docs/transformers/index), [LLM Course Ch1](https://huggingface.co/learn/llm-course/chapter1/4)
* **Blog Posts:** [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/), [Netguru on Transformer Models](https://www.netguru.com/blog/transformer-models-in-nlp)

---

### 隼 **Exercise 1: Encoder vs. Decoder Block Analysis**

**Goal:** Compare and contrast the components and roles of a single Transformer Encoder block versus a single Transformer Decoder block.

**Instructions:**

1.  Referencing the original Transformer paper or illustrative guides, draw (or describe in detail) the internal components of:
    * One Encoder block (Self-Attention, Add & Norm, Feed-Forward Network, Add & Norm).
    * One Decoder block (Masked Self-Attention, Add & Norm, Encoder-Decoder Cross-Attention, Add & Norm, Feed-Forward Network, Add & Norm).
2.  Explain the purpose of each sub-layer within both blocks.
3.  What is the key difference between the self-attention mechanism in the encoder and the *masked* self-attention mechanism in the decoder? Why is masking necessary in the decoder during training an autoregressive model?
4.  What are the inputs and outputs for the Encoder-Decoder Cross-Attention layer in the decoder? What information does it allow the decoder to leverage?
5.  **Challenge:** Implement a simplified Encoder block and a Decoder block (just the layer structure, not necessarily full training) using PyTorch or TensorFlow, ensuring correct input/output flow for dummy tensors.

---

### 隼 **Exercise 2: Pre-LN vs. Post-LN Layer Normalization**

**Goal:** Understand the difference between Pre-Layer Normalization (Pre-LN) and Post-Layer Normalization (Post-LN) in Transformer blocks and their implications.

**Instructions:**

1.  In the original Transformer paper, Layer Normalization was applied *after* the residual connection (Post-LN): `output = LayerNorm(sublayer_output + x)`.
2.  Many modern Transformer implementations use Pre-LN: `output = LayerNorm(x) + sublayer_output` or `output = x + sublayer_output(LayerNorm(x))`.
3.  Explain the motivation for using Pre-LN. How can it help with training stability, especially for very deep Transformers? (Hint: Gradient flow, preventing activations from growing too large).
4.  Implement two simple "sub-layer" modules (e.g., a dummy self-attention followed by a dummy feed-forward).
    * One using Post-LN after each residual addition.
    * One using Pre-LN before each sub-layer operation and then the residual addition.
5.  Conceptually, trace how the activations and gradients might flow differently in these two setups.
6.  **Challenge:** Research and summarize findings from papers that compare Pre-LN vs. Post-LN empirically. Which is generally favored now and why?

---

### 隼 **Exercise 3: Masked Language Modeling (MLM) - BERT**

**Goal:** Understand and implement the Masked Language Modeling (MLM) pre-training objective used by BERT.

**Instructions:**

1.  Explain the MLM objective:
    * How are input tokens randomly masked (e.g., replaced with `[MASK]`, a random token, or kept original)? What are typical masking probabilities?
    * What is the model trained to predict for these masked positions? (Hint: The original token ID).
    * How does this objective encourage the model to learn bidirectional context and deep language understanding?
2.  Take a sample sentence. Manually apply the MLM masking strategy (e.g., mask 15% of tokens, with 80% of those being `[MASK]`, 10% random, 10% original).
3.  Conceptually, how would a BERT-like model use the unmasked tokens to predict the original tokens at the `[MASK]` positions? What kind of output layer would be needed on top of the Transformer encoder outputs for this? (Hint: A linear layer followed by softmax over the vocabulary).
4.  What is the loss function typically used for MLM? (Hint: Cross-entropy).
5.  **Challenge:** Using Hugging Face Transformers, load a pre-trained BERT model and tokenizer. Take a sentence, mask a word, and use the model to predict the top-k most probable words for the masked position.

---

### 隼 **Exercise 4: Next Sentence Prediction (NSP) - BERT**

**Goal:** Understand the Next Sentence Prediction (NSP) pre-training objective used by BERT alongside MLM.

**Instructions:**

1.  Explain the NSP objective:
    * How are sentence pairs `(A, B)` created for training? (50% actual next sentences, 50% random sentences).
    * What is the model trained to predict for these pairs? (Hint: A binary classification - `IsNext` or `NotNext`).
    * How is the special `[CLS]` token's final hidden representation typically used for this prediction?
2.  What was the original motivation for including the NSP task? (Hint: To help with downstream tasks requiring understanding of sentence relationships, like QA or NLI).
3.  Later models like RoBERTa and ALBERT found that NSP might not be as crucial as initially thought, or could even be detrimental if implemented poorly. Briefly research and summarize these findings.
4.  **Challenge:** Create a small dataset of sentence pairs, half of which are consecutive and half are random. How would you format this input for a BERT model to perform NSP (including special tokens like `[CLS]`, `[SEP]`, and segment embeddings)?

---

### 隼 **Exercise 5: Autoregressive Language Modeling - GPT**

**Goal:** Understand the autoregressive (left-to-right) language modeling objective used by GPT-style models.

**Instructions:**

1.  Explain autoregressive language modeling:
    * How does the model predict the next token in a sequence given all preceding tokens?
    * Why is this inherently a unidirectional (causal) modeling approach?
2.  How is the training objective formulated? (Hint: Predict each token `t_i` given tokens `t_1, ..., t_{i-1}`). What loss function is used?
3.  How is the "masked self-attention" (causal attention) in GPT's decoder crucial for this objective during training? (Ensures that predicting token `i` only uses information from tokens before `i`).
4.  Compare and contrast this objective with BERT's MLM. Which is better suited for text generation tasks, and why? Which might be better for tasks requiring deep bidirectional understanding of existing text?
5.  **Challenge:** Using Hugging Face Transformers, load a pre-trained GPT-2 model and tokenizer. Provide it with a prompt (a few words) and use its `generate()` method to produce a continuation of the text. How does this generation process reflect the autoregressive nature of the model?

---

### 隼 **Exercise 6: Text-to-Text Transfer Transformer (T5)**

**Goal:** Understand the unified "text-to-text" framework proposed by T5, where all NLP tasks are cast as sequence generation problems.

**Instructions:**

1.  Explain the core idea of the T5 model: how does it frame diverse NLP tasks (e.g., translation, summarization, classification, QA) as a single "text-to-text" problem? (Hint: Using task-specific prefixes in the input string).
2.  What kind of Transformer architecture does T5 typically use (Encoder-only, Decoder-only, or Encoder-Decoder)? Why is this choice suitable for its text-to-text approach?
3.  Provide examples of how different NLP tasks would be formatted as input and expected output strings for a T5 model:
    * Translation (English to German): e.g., Input: "translate English to German: That is good." Output: "Das ist gut."
    * Summarization: e.g., Input: "summarize: [long article text]" Output: "[short summary]"
    * Sentiment Classification: e.g., Input: "sentiment: This movie was fantastic!" Output: "positive"
4.  What pre-training objective is primarily used for T5, considering its text-to-text nature? (Hint: A variation of MLM, often involving masking spans of text and predicting the missing spans).
5.  **Challenge:** How does T5's approach simplify handling multiple tasks with a single model compared to having separate fine-tuned models for each task? What are the potential benefits and drawbacks of this unified framework?

---