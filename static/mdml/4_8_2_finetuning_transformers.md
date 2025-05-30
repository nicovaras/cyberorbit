## 倹 Subtopic 4.8.2: Fine-tuning Transformers for Downstream NLP Tasks

**Goal:** Learn how to adapt pre-trained Transformer models (like BERT, GPT, T5) for various downstream NLP tasks by adding task-specific heads, preparing data appropriately, and applying effective fine-tuning strategies.

**Resources:**

* **Hugging Face Transformers Tutorials:** [Fine-tuning a pretrained model](https://huggingface.co/docs/transformers/training), Task-specific examples (e.g., text classification, token classification, QA).
* **Blog Post on Fine-tuning GPT:** [30 Days Coding](https://30dayscoding.com/blog/fine-tuning-gpt-models-for-downstream-nlp-tasks)
* **Transfer Learning in NLP:** Articles discussing the benefits and challenges.
* **GLUE Benchmark:** [Homepage](https://gluebenchmark.com/) (Examples of diverse NLP tasks).

---

### 隼 **Exercise 1: Text Classification with Transformers**

**Goal:** Fine-tune a pre-trained Transformer (e.g., BERT or DistilBERT) for a text classification task (e.g., sentiment analysis).

**Instructions:**

1.  Choose a text classification dataset (e.g., IMDB sentiment, SST-2, or a GLUE task like CoLA/MNLI).
2.  Load a pre-trained Transformer model and its tokenizer from Hugging Face (e.g., `bert-base-uncased`).
3.  **Data Preparation:**
    * Tokenize the input texts. Ensure you handle padding and truncation correctly to match the model's expected input length. Include attention masks.
    * Convert labels to numerical format if necessary.
4.  **Model Modification:** Add a classification head on top of the pre-trained model's pooled output (e.g., the `[CLS]` token's representation from BERT, or sequence pooler output). This head is typically a linear layer followed by a softmax (or handled by the loss function). Hugging Face `AutoModelForSequenceClassification` does this automatically.
5.  Set up a training loop:
    * Define an optimizer (e.g., AdamW) and a learning rate scheduler (e.g., linear warmup with decay).
    * Define the loss function (e.g., CrossEntropyLoss).
    * Iterate through epochs and batches, perform forward pass, calculate loss, backward pass, and optimizer step.
    * Include an evaluation loop on a validation set to monitor performance (e.g., accuracy, F1-score).
6.  Fine-tune the model. Report its performance on the test set.
7.  **Challenge:** Compare the performance of fine-tuning the entire pre-trained model versus fine-tuning only the classification head (freezing the pre-trained layers). Which performs better and why might that be?

---

### 隼 **Exercise 2: Token Classification (Named Entity Recognition - NER) with Transformers**

**Goal:** Fine-tune a pre-trained Transformer for a token classification task like Named Entity Recognition (NER).

**Instructions:**

1.  Choose an NER dataset (e.g., CoNLL-2003, OntoNotes). NER labels are applied to each token (e.g., B-PER, I-PER, B-ORG, I-ORG, O).
2.  Load a pre-trained Transformer model and tokenizer suitable for token classification (e.g., `bert-base-cased`).
3.  **Data Preparation:**
    * Tokenize input sentences. Crucially, align the NER labels with the subword tokens produced by the tokenizer. (Hugging Face's `tokenizer` can often handle this with `is_split_into_words=True` and careful label mapping). Pay attention to special tokens and how labels are assigned to them (often ignored in loss calculation).
    * Handle padding and attention masks.
4.  **Model Modification:** Add a token classification head on top of the pre-trained model's sequence output (the hidden states for each token). This is typically a linear layer mapping hidden states to the number of NER tags, followed by softmax (or handled by loss). Hugging Face `AutoModelForTokenClassification` does this.
5.  Set up the training and evaluation loop, using appropriate metrics for NER (e.g., token-level F1-score, precision, recall, often using libraries like `seqeval`).
6.  Fine-tune the model and report its performance.
7.  **Challenge:** How do you handle words that are split into multiple subword tokens by the tokenizer when assigning labels and calculating metrics? Discuss strategies like labeling only the first subword token.

---

### 隼 **Exercise 3: Extractive Question Answering (QA) with Transformers**

**Goal:** Fine-tune a pre-trained Transformer for extractive QA, where the answer is a span of text within a given context.

**Instructions:**

1.  Choose an extractive QA dataset (e.g., SQuAD - Stanford Question Answering Dataset). Each sample consists of a context, a question, and the start/end token positions of the answer within the context.
2.  Load a pre-trained Transformer model and tokenizer suitable for QA (e.g., `bert-large-uncased-whole-word-masking-finetuned-squad`).
3.  **Data Preparation:**
    * For each context-question pair, tokenize them together, often as `[CLS] question [SEP] context [SEP]`.
    * Map the character-based start/end answer positions from the dataset to token-based start/end positions in the tokenized input. Handle cases where answers span multiple subword tokens or are not fully contained.
4.  **Model Modification:** Add a QA head on top of the pre-trained model's sequence output. This head typically consists of two linear layers that predict the probability of each token being the *start* of the answer span and the *end* of the answer span. Hugging Face `AutoModelForQuestionAnswering` does this.
5.  **Loss Function:** The loss is typically the sum of cross-entropy losses for the start token prediction and the end token prediction.
6.  Fine-tune the model. During inference, how do you combine the start and end logits to find the most likely answer span?
7.  Evaluate using SQuAD metrics (Exact Match - EM, F1-score).
8.  **Challenge:** How would you handle questions where the answer is not present in the context, or contexts that are longer than the model's maximum input length?

---

### 隼 **Exercise 4: Abstractive Summarization with Sequence-to-Sequence Transformers**

**Goal:** Fine-tune a pre-trained sequence-to-sequence Transformer (e.g., T5, BART) for abstractive text summarization.

**Instructions:**

1.  Choose a summarization dataset (e.g., CNN/DailyMail, XSum). Each sample has a long article and a shorter summary.
2.  Load a pre-trained sequence-to-sequence model and tokenizer (e.g., `t5-small`, `bart-large-cnn`).
3.  **Data Preparation:**
    * Tokenize the input articles (source sequences) and target summaries (target sequences). For T5, you might add a prefix like "summarize: " to the input article.
    * Ensure appropriate padding, truncation, and attention masks for both encoder inputs (articles) and decoder inputs/labels (summaries).
4.  Use the appropriate sequence-to-sequence model from Hugging Face (e.g., `AutoModelForSeq2SeqLM`). The model already has the necessary generation head.
5.  Set up the training loop. The loss is typically cross-entropy on the predicted tokens of the summary.
6.  Fine-tune the model. During inference/evaluation, use the model's `generate()` method to produce summaries.
7.  Evaluate using ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L).
8.  **Challenge:** Experiment with different decoding strategies during generation (e.g., beam search, top-k sampling, top-p sampling). How do these affect the quality and diversity of the generated summaries?

---

### 隼 **Exercise 5: Fine-tuning Strategies & Challenges**

**Goal:** Discuss and experiment with different learning rates, batch sizes, and methods to handle overfitting or catastrophic forgetting during fine-tuning.

**Instructions:**

1.  Referencing the challenges mentioned in the "Fine-Tuning GPT Models" blog post (Overfitting, Catastrophic Forgetting, Hyperparameter Tuning).
2.  **Learning Rates:** Why are smaller learning rates (e.g., 2e-5 to 5e-5) typically recommended for fine-tuning large pre-trained Transformers compared to training from scratch?
3.  **Batch Size:** How can batch size affect fine-tuning performance and stability?
4.  **Number of Epochs:** Fine-tuning often requires only a few epochs (e.g., 2-4). Why is this usually the case? What are the risks of fine-tuning for too many epochs?
5.  **Overfitting:** Besides early stopping (based on validation performance), what other regularization techniques can be applied during fine-tuning (e.g., weight decay, dropout in the classification head)?
6.  **Catastrophic Forgetting:** Explain what catastrophic forgetting is in the context of fine-tuning. How might techniques like using different learning rates for different layers (lower for pre-trained, higher for task-specific head) or PEFT methods (next subtopic) help mitigate this?
7.  **Experiment (Optional):** Take one of the previous fine-tuning exercises (e.g., text classification). Systematically vary the learning rate and number of epochs and observe the impact on validation performance and signs of overfitting.
8.  **Challenge:** Research "differential learning rates" for fine-tuning. How are different learning rates applied to different layers of the Transformer, and why?

---