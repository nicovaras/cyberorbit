## Subtopic 3.1: Foundations of Modern NLP

**Goal:** To understand foundational concepts preceding the Transformer era, including word embedding techniques (Word2Vec/GloVe), the basic mechanics and limitations of sequence models (RNNs/LSTMs), and the core intuition behind attention mechanisms.

**Resources:**

  * Word Embeddings:
      * `gensim` library documentation: [gensim documentation](https://radimrehurek.com/gensim/)
      * GloVe Project: [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)
      * Word2Vec Explained: [The Illustrated Word2vec by Jay Alammar](https://jalammar.github.io/illustrated-word2vec/)
  * Sequence Models (Recap):
      * Understanding LSTMs: [Colah's Blog: Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
      * RNN Effectiveness: [Blog Post: The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
  * Attention Mechanisms (Intro):
      * Attention Concept: [Blog Post: Attention and Augmented Recurrent Neural Networks](https://distill.pub/2016/augmented-rnns/) (Focus on the attention concept section)
      * Neural Machine Translation with Attention: [Bahdanau et al., 2014 paper (arXiv)](https://arxiv.org/abs/1409.0473) (Read abstract and introduction)

-----

### Exercise 1: Exploring Pre-trained Word Embeddings

**Goal:** Load and interact with pre-trained Word2Vec or GloVe embeddings to understand their semantic properties.
**Instructions:**

1.  Install the `gensim` library (`pip install gensim`).
2.  Download pre-trained GloVe vectors (e.g., `glove-wiki-gigaword-100`) or use `gensim`'s downloader to fetch a Word2Vec model (e.g., `word2vec-google-news-300`). Refer to `gensim` documentation for loading.
3.  Load the pre-trained model using `gensim`.
4.  Perform the following operations using the loaded model:
      * Find the vector representation for common words like "king", "queen", "man", "woman".
      * Find the most similar words to "computer" using `model.most_similar()`.
      * Perform vector arithmetic analogies: Find the word closest to `vector('king') - vector('man') + vector('woman')`. Does it approximate "queen"?
      * Calculate the cosine similarity between pairs of words (e.g., "cat" and "dog", "cat" and "car") using `model.similarity()`.
5.  Discuss what these operations demonstrate about the semantic information captured by word embeddings.

### Exercise 2: Recapping RNNs and LSTMs (Conceptual)

**Goal:** Explain the basic mechanism of Recurrent Neural Networks (RNNs) and the improvements offered by LSTMs/GRUs for handling sequential data.
**Instructions:**

1.  Describe the core idea of an RNN: how does it process sequential input (e.g., words in a sentence) and maintain a "memory" or hidden state? Draw a simple diagram of an unrolled RNN cell.
2.  Explain the **vanishing gradient problem** in the context of training simple RNNs on long sequences. How does this limit their ability to capture long-range dependencies?
3.  Describe the purpose of the key components introduced in an LSTM cell (Input Gate, Forget Gate, Output Gate, Cell State) at a high level. How do these gates help mitigate the vanishing gradient problem and control information flow?
4.  What are GRUs (Gated Recurrent Units), and how do they relate to LSTMs (conceptually, e.g., simpler architecture)?

### Exercise 3: Basic Attention Mechanism Intuition

**Goal:** Explain the core concept of attention mechanisms as originally applied in sequence-to-sequence models (e.g., machine translation).
**Instructions:**

1.  Consider a sequence-to-sequence task like translating an English sentence to French using an encoder-decoder architecture (e.g., based on LSTMs).
2.  Explain the limitation of using only the final hidden state of the encoder LSTM as the context vector for the entire decoding process, especially for long input sentences.
3.  Describe the core idea of the **Bahdanau attention mechanism** (or similar additive attention). How does the decoder selectively focus on different parts of the *encoder's hidden states* when generating each output word?
4.  What are "attention weights" or "alignment scores" in this context? What do they represent?
5.  How does this attention mechanism help improve performance on tasks like machine translation compared to using only the fixed final encoder state?

### Exercise 4: Word Embedding Limitations

**Goal:** Identify key limitations of traditional static word embeddings like Word2Vec and GloVe.
**Instructions:**

1.  Using your loaded Word2Vec/GloVe model from Exercise 1, find the vector for a word with multiple meanings (e.g., "bank"). Does the model provide different vectors for "river bank" vs. "financial bank"? Explain this limitation (handling polysemy).
2.  Consider the phrases "good service" and "not good service". How well would static embeddings capture the negated meaning in the second phrase when representing the word "good"? Explain this limitation regarding context sensitivity.
3.  How are Out-Of-Vocabulary (OOV) words typically handled (or not handled) by models trained with a fixed vocabulary like Word2Vec/GloVe?
