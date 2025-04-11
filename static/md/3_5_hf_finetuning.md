## Subtopic 3.5: Fine-tuning Pre-trained Models for Specific Tasks

**Goal:** To gain hands-on experience fine-tuning pre-trained Transformer models (like BERT, DistilBERT, etc.) for common NLP tasks (Classification, Q\&A, Summarization) using the Hugging Face `transformers` and `datasets` libraries.

**Resources:**

  * Hugging Face `transformers` Library: [Main Documentation](https://huggingface.co/docs/transformers/index)
  * Hugging Face `datasets` Library: [Main Documentation](https://huggingface.co/docs/datasets/)
  * Hugging Face `evaluate` Library: [Main Documentation](https://www.google.com/search?q=https://huggingface.co/docs/evaluate)
  * Hugging Face Task Guides:
      * [Fine-tuning for Text Classification](https://www.google.com/search?q=https://huggingface.co/docs/transformers/tasks/text_classification)
      * [Fine-tuning for Question Answering](https://www.google.com/search?q=https://huggingface.co/docs/transformers/tasks/Youtubeing)
      * [Fine-tuning for Summarization](https://huggingface.co/docs/transformers/tasks/summarization)
  * Hugging Face Hub: [Model Hub](https://huggingface.co/models), [Dataset Hub](https://huggingface.co/datasets)
  * Google Colab / Kaggle Kernels: Useful for free GPU access for training.

-----

### Exercise 1: Setup and Data Loading for Text Classification

**Goal:** Set up the environment and load a standard text classification dataset using the `datasets` library.
**Instructions:**

1.  Install necessary libraries: `pip install transformers datasets evaluate accelerate torch` (or `tensorflow`).
2.  Choose a text classification dataset from the Hugging Face Hub (e.g., `imdb` for sentiment analysis, `ag_news` for topic classification).
3.  Use the `load_dataset` function from the `datasets` library to load the chosen dataset. Explore the dataset structure (`DatasetDict`, features, splits like 'train', 'test').
4.  Print a few examples from the training split to understand the text and label format.
5.  Choose a pre-trained model suitable for classification (e.g., `distilbert-base-uncased`) from the Hub. Use `AutoTokenizer.from_pretrained` to load its corresponding tokenizer.

### Exercise 2: Preprocessing Data with Tokenizer

**Goal:** Tokenize and prepare the text data for input into the chosen Transformer model.
**Instructions:**

1.  Define a preprocessing function that takes a batch of examples from the dataset.
2.  Inside the function, use the loaded tokenizer to tokenize the text field(s). Ensure you handle padding and truncation appropriately (`padding="max_length"`, `truncation=True`).
3.  Apply this preprocessing function to the entire dataset using the `.map()` method of the `DatasetDict` object (use `batched=True` for efficiency).
4.  Set the format of the dataset to 'torch' or 'tensorflow' to prepare for training.
5.  Verify the processed dataset contains the expected input fields for the model (e.g., `input_ids`, `attention_mask`, `labels`).

### Exercise 3: Fine-tuning for Text Classification

**Goal:** Fine-tune the pre-trained model on the prepared classification dataset using the Hugging Face `Trainer` API or a custom training loop.
**Instructions:**

1.  Load the pre-trained model using `AutoModelForSequenceClassification.from_pretrained`, specifying the number of labels for your dataset.
2.  Define training arguments using `TrainingArguments`. Set essential parameters like `output_dir`, `num_train_epochs`, `per_device_train_batch_size`, `per_device_eval_batch_size`, `evaluation_strategy` (e.g., "epoch"), `save_strategy` (e.g., "epoch"), `load_best_model_at_end=True`.
3.  (Optional) Define a `compute_metrics` function using the `evaluate` library to calculate relevant metrics (e.g., accuracy, F1-score) during evaluation. Load the metric using `evaluate.load()`.
4.  Instantiate the `Trainer` object, passing the model, training arguments, training dataset, evaluation dataset, tokenizer, and optionally the `compute_metrics` function.
5.  Start the fine-tuning process by calling `trainer.train()`. Monitor the training progress (loss, evaluation metrics if computed). (Use GPU if available via Colab/Kaggle/local setup).
6.  Once training is complete, save the fine-tuned model using `trainer.save_model()`.

### Exercise 4: Fine-tuning for Extractive Question Answering

**Goal:** Adapt the fine-tuning process for an extractive Question Answering task.
**Instructions:**

1.  Load a suitable dataset (e.g., `squad`). Note its structure (context, question, answers with start/end indices).
2.  Load a pre-trained model suitable for QA (e.g., `bert-large-uncased-whole-word-masking-finetuned-squad`, or fine-tune a base model like `distilbert-base-uncased`). Use `AutoModelForQuestionAnswering`.
3.  Adapt the preprocessing function for QA: Tokenize context and question together. Handle long contexts (e.g., using `return_overflowing_tokens=True`, `stride`). Map answer start/end character indices to token indices. This preprocessing is more complex than classification - refer carefully to Hugging Face QA task guide/notebooks.
4.  Define `TrainingArguments`.
5.  Instantiate and run the `Trainer`. Note that QA models output start and end logits, not class labels. Evaluation often involves post-processing to find the best answer span and metrics like Exact Match (EM) and F1-score over tokens. (Implementing full QA evaluation can be complex, focus on running the training).
6.  Save the fine-tuned QA model.

### Exercise 5: Fine-tuning for Summarization (Seq2Seq)

**Goal:** Adapt the fine-tuning process for a sequence-to-sequence summarization task.
**Instructions:**

1.  Load a summarization dataset (e.g., `cnn_dailymail`, `xsum`). Note the input text and target summary structure.
2.  Load a pre-trained sequence-to-sequence model (e.g., `t5-small`, `bart-large-cnn`). Use `AutoModelForSeq2SeqLM`. Load its corresponding tokenizer.
3.  Adapt the preprocessing function for Seq2Seq: Tokenize the input text (e.g., article) and the target text (e.g., summary) separately. The target token IDs are typically used as labels. Handle padding/truncation for both inputs and labels.
4.  Define `Seq2SeqTrainingArguments`.
5.  Instantiate the `Seq2SeqTrainer`.
6.  Define a `compute_metrics` function using `evaluate.load("rouge")` to calculate ROUGE scores during evaluation (requires `nltk` and `rouge_score` packages). Handle token decoding for metric calculation.
7.  Start the `Seq2SeqTrainer`.
8.  Save the fine-tuned summarization model.

### Project: Fine-tune and Share a Model

**Goal:** Fine-tune a model on a dataset of interest and share it on the Hugging Face Hub.
**Instructions:**

1.  Choose a specific task (classification, QA, summarization, etc.) and a dataset from the Hugging Face Hub that interests you.
2.  Select an appropriate pre-trained base model.
3.  Implement the full fine-tuning pipeline: data loading, preprocessing, training (using `Trainer` or a custom loop), and evaluation. Ensure you save the best performing model checkpoint.
4.  Log in to the Hugging Face Hub using `huggingface-cli login`.
5.  Use the `push_to_hub()` method of your trained model and tokenizer (or the `Trainer`'s `push_to_hub()` method) to upload your fine-tuned model to your Hugging Face Hub profile.
    **Portfolio Guidance:**



  * The Hugging Face Hub model card serves as documentation. Ensure it is well-filled: describe the base model, dataset used, preprocessing steps, training hyperparameters, evaluation results, and intended use/limitations.
  * Include code snippets or a link to a Colab/Kaggle notebook showing the fine-tuning process in the model card or a linked GitHub repo.
  * Add a clear license to your model on the Hub.
