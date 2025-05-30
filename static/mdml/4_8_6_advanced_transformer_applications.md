## 倹 Subtopic 4.8.6: Advanced Transformer Applications

**Goal:** Explore the application of Transformer architectures beyond standard NLP tasks, including multilingual modeling, cross-lingual transfer, and an introduction to their use in multimodal contexts like vision.

**Resources:**

* **Multilingual Models:**
    * **mBERT:** [Original BERT paper Appendix](https://arxiv.org/abs/1810.04805), Hugging Face model docs.
    * **XLM-R Paper:** [Conneau et al., 2019 - Unsupervised Cross-lingual Representation Learning at Scale](https://arxiv.org/abs/1911.02116)
    * ACL Anthology on Multilingual Propaganda Detection (mentions mBERT, XLM-R):
    * arXiv on Distilling MMTs:
* **Multimodal Transformers:**
    * **ViT (Vision Transformer):** [Dosovitskiy et al., 2020 - An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)
    * **CLIP Paper:** [Radford et al., 2021 - Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
    * Scaler article mentioning ViT:
    * Netguru article mentioning ViT:

---

### 隼 **Exercise 1: Multilingual BERT (mBERT) - Architecture & Pre-training**

**Goal:** Understand how mBERT is pre-trained on multiple languages and its implications for cross-lingual understanding.

**Instructions:**

1.  Describe the core idea behind Multilingual BERT (mBERT). How does its architecture compare to the monolingual BERT model? Is it a single model for many languages?
2.  On what kind of data is mBERT pre-trained? (Hint: Wikipedia dumps from many languages, typically concatenated).
3.  What pre-training objectives does mBERT use? (Usually the same as BERT: Masked Language Modeling and Next Sentence Prediction).
4.  How does mBERT learn to align representations across different languages despite not having explicit cross-lingual signals (like parallel sentences) during pre-training? (Hint: Shared subword vocabulary, code-switching in data, shared model capacity).
5.  What are the benefits of using a single mBERT model for tasks in multiple languages compared to training separate monolingual models for each?
6.  **Challenge:** Using Hugging Face, load the `bert-base-multilingual-cased` model and tokenizer. Tokenize the same short phrase (e.g., "hello world") in several different languages that use different scripts (e.g., English, Hindi, Japanese). Observe the resulting token IDs. Are there any shared tokens?

---

### 隼 **Exercise 2: XLM-RoBERTa (XLM-R) - Improvements over mBERT**

**Goal:** Understand the key improvements of XLM-RoBERTa over mBERT for cross-lingual representation learning.

**Instructions:**

1.  XLM-R builds upon RoBERTa and previous XLM models. What were some of the limitations of mBERT that XLM-R aimed to address? (Hint: Vocabulary size per language, pre-training data size and balance).
2.  On what kind of data and scale is XLM-R pre-trained compared to mBERT? (Hint: CommonCrawl, significantly more languages and data).
3.  Does XLM-R use a shared vocabulary across all its languages? How is its vocabulary constructed (e.g., SentencePiece)?
4.  What pre-training objective does XLM-R primarily use? (Hint: Only Masked Language Modeling, like RoBERTa).
5.  Why does training on a larger number of languages and more data generally lead to better cross-lingual transfer performance, especially for low-resource languages?
6.  **Challenge:** Find examples of downstream tasks where XLM-R has shown superior performance over mBERT, particularly in zero-shot or few-shot cross-lingual settings.

---

### 隼 **Exercise 3: Cross-Lingual Transfer & Zero-Shot Learning**

**Goal:** Demonstrate and evaluate zero-shot cross-lingual transfer by fine-tuning a multilingual model on one language and testing on another.

**Instructions:**

1.  Choose a multilingual Transformer model (e.g., `xlm-roberta-base`) and a downstream task like text classification (e.g., sentiment analysis or topic classification).
2.  Find a dataset for this task that is available in at least two languages, one of which is relatively high-resource (e.g., English) and another lower-resource. (Alternatively, use a multilingual dataset like XNLI).
3.  **Fine-tune:** Fine-tune the chosen multilingual model *only* on the training data of the high-resource language (e.g., English).
4.  **Zero-Shot Evaluation:** Evaluate the performance of this fine-tuned model *directly* on the test data of the **other (lower-resource) language(s)** without any further fine-tuning on that language.
5.  As a baseline, evaluate the performance of the *untuned* pre-trained multilingual model on the lower-resource language test set (if applicable for the task head).
6.  Compare the zero-shot performance to the baseline and potentially to a model fine-tuned directly on the lower-resource language (if data were available). How effective is the cross-lingual transfer?
7.  **Challenge:** What factors influence the effectiveness of zero-shot cross-lingual transfer (e.g., language similarity, model capacity, quality of pre-training)?

---

### 隼 **Exercise 4: Vision Transformer (ViT) - Core Concept for Images**

**Goal:** Understand how the Transformer architecture is adapted for image classification tasks in the Vision Transformer (ViT).

**Instructions:**

1.  Explain the core idea of ViT: How does it treat an image as a sequence to make it suitable input for a Transformer encoder? (Hint: Splitting the image into fixed-size, non-overlapping patches).
2.  What happens to these image patches before they are fed into the Transformer encoder? (Hint: Flattened, linearly projected to create patch embeddings).
3.  How is positional information for the patches incorporated, given that Transformers are permutation-invariant? (Hint: Learnable or fixed positional embeddings are added to patch embeddings).
4.  Describe the role of the special `[CLS]` token (class token) in ViT for image classification. How is its corresponding output representation from the Transformer encoder used to make a classification decision?
5.  What modifications (if any) are needed for the standard Transformer encoder architecture to be used in ViT? (It's largely the standard encoder).
6.  **Challenge:** Compare the inductive biases of CNNs (e.g., locality, translation equivariance) with those of ViTs (which initially have fewer image-specific biases but can learn them from large data). Why might ViTs require more data or more extensive pre-training than CNNs to perform well?

---

### 隼 **Exercise 5: CLIP (Contrastive Language-Image Pre-training) - Concept**

**Goal:** Understand the core idea behind CLIP: learning joint embeddings for images and text using a contrastive pre-training objective.

**Instructions:**

1.  Describe the main goal of CLIP. What kind of task is it pre-trained on? (Hint: Matching images with their corresponding text descriptions from a large dataset of (image, text) pairs).
2.  What are the two main components (encoders) in the CLIP architecture? (An image encoder, e.g., ViT or ResNet, and a text encoder, e.g., Transformer).
3.  How are these encoders trained? Explain the **contrastive loss** function:
    * For a batch of (image, text) pairs, image embeddings and text embeddings are computed.
    * How are positive pairs (correctly matched image-text) and negative pairs (incorrectly matched) formed within a batch?
    * The model is trained to maximize the similarity (e.g., cosine similarity) between embeddings of positive pairs and minimize similarity for negative pairs.
4.  How can a pre-trained CLIP model be used for **zero-shot image classification**? (Hint: Create text prompts for class names like "a photo of a {class_name}", embed these prompts, embed the query image, and find the text prompt with the highest cosine similarity to the image embedding).
5.  **Challenge:** Beyond zero-shot classification, what other downstream tasks can benefit from the rich joint image-text representations learned by CLIP (e.g., image retrieval based on text queries, text retrieval based on image queries)?

---