## Subtopic 3.3: Understanding Large Language Models (LLMs)

**Goal:** To grasp the core concepts behind Large Language Models (LLMs), including common pre-training objectives, fine-tuning strategies, the idea of scaling laws, and the key characteristics of prominent model families like BERT and GPT.

**Resources:**

  * Pre-training Objectives:
      * BERT Paper: [Devlin et al., 2018 - BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (arXiv)](https://arxiv.org/abs/1810.04805) (Focus on MLM and NSP)
      * GPT-3 Paper: [Brown et al., 2020 - Language Models are Few-Shot Learners (arXiv)](https://arxiv.org/abs/2005.14165) (Focus on autoregressive pre-training)
  * Fine-tuning: [Hugging Face Blog/Docs on Fine-tuning](https://huggingface.co/docs/transformers/training) (Conceptual Overview)
  * Scaling Laws:
      * Kaplan et al., 2020 - Scaling Laws for Neural Language Models (arXiv): [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) (Read abstract and conclusion)
      * Blog summaries (e.g., [AI Impacts overview](https://www.google.com/search?q=https://aiimpacts.org/scaling-laws-for-language-models/))
  * Model Overviews:
      * BERT Explained: [The Illustrated BERT by Jay Alammar](https://jalammar.github.io/illustrated-bert/)
      * GPT Explained: [The Illustrated GPT-2 by Jay Alammar](https://jalammar.github.io/illustrated-gpt2/)
      * Hugging Face Models: [Models Documentation](https://www.google.com/search?q=https://huggingface.co/docs/transformers/index%23supported-models) (Browse different model types)

-----

### Exercise 1: Explain Pre-training Objectives

**Goal:** Describe common objectives used to pre-train large language models on vast amounts of unlabeled text data.
**Instructions:**

1.  Describe the **Masked Language Model (MLM)** objective used by BERT. How does it work? What kind of understanding does it encourage the model to learn (e.g., bidirectional context)?
2.  Describe the **Next Sentence Prediction (NSP)** objective originally used by BERT (though later found less critical). What was its purpose?
3.  Describe the **Causal Language Model (CLM)** or **Autoregressive Language Model** objective used by GPT-style models. How does it work (predicting the next token)? What kind of tasks is this objective naturally suited for?
4.  Explain why these pre-training tasks are considered "self-supervised" learning.

### Exercise 2: Compare BERT vs. GPT Architectures & Goals

**Goal:** Differentiate between the architectural choices and primary intended use cases of BERT-style and GPT-style models.
**Instructions:**

1.  Compare the core Transformer architecture used in BERT (Encoder-only) versus GPT (Decoder-only). How does this difference relate to their pre-training objectives (MLM vs. CLM)?
2.  Explain the concept of **bidirectionality** in BERT. How does it achieve this during pre-training?
3.  Explain the concept of **unidirectionality** (autoregressive nature) in GPT.
4.  What types of downstream NLP tasks was BERT originally designed to excel at (requiring understanding of the full sentence context)?
5.  What types of downstream NLP tasks are GPT models inherently well-suited for (requiring generation)?

### Exercise 3: Understanding Fine-tuning Paradigms

**Goal:** Describe different ways pre-trained LLMs can be adapted (fine-tuned) for specific downstream tasks.
**Instructions:**

1.  Describe **Full Fine-tuning**. What parts of the pre-trained model are updated during this process? What typically needs to be added or modified for a specific task (e.g., a classification head)?
2.  Explain the concept of **Parameter-Efficient Fine-Tuning (PEFT)** at a high level (no deep implementation details needed). Why is PEFT becoming increasingly important for very large models? Mention one common PEFT technique conceptually (e.g., LoRA - Low-Rank Adaptation, Adapter Modules, Prompt Tuning).
3.  What is **Transfer Learning** in the context of LLMs? How do pre-training and fine-tuning fit into the transfer learning paradigm?

### Exercise 4: Scaling Laws in LLMs (Conceptual)

**Goal:** Understand the relationship between model size, dataset size, compute, and performance as described by scaling laws.
**Instructions:**

1.  Briefly summarize the key findings of research on scaling laws for language models (e.g., Kaplan et al., 2020). How does model performance (typically measured by loss) generally scale with increases in:
      * Model Size (Number of parameters)
      * Dataset Size
      * Training Compute
2.  What do these scaling laws suggest about the optimal allocation of resources when training very large models (e.g., is it better to train a larger model for less time or a smaller model for more time on a larger dataset, given a fixed compute budget)? (Refer to Chinchilla scaling laws for a more recent perspective if desired, conceptually).
3.  What are some potential limitations or caveats to these observed scaling laws?

### Exercise 5: Identify Different LLM Families/Variants

**Goal:** Recognize the names and general characteristics of several important LLM families beyond the original BERT and GPT.
**Instructions:**

1.  Briefly describe the key idea or contribution of **T5 (Text-to-Text Transfer Transformer)**. How does it frame different NLP tasks?

2.  Briefly describe the purpose of **ELECTRA**. How does its pre-training differ from BERT's MLM?

3.  Mention one example of a prominent **Open-Source LLM** family (e.g., Llama, Mistral, Falcon - as of your knowledge cutoff or current search). What is the significance of open-source models in the LLM landscape? (Use current date: April 11, 2025)

4.  What distinguishes **Multimodal LLMs** (like GPT-4V or Gemini) from text-only LLMs?
