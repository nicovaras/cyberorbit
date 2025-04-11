## Subtopic 3.2: The Transformer Architecture Deep Dive

**Goal:** To understand the key components and mechanisms of the Transformer architecture, focusing on Self-Attention, Multi-Head Attention, and Positional Encoding.

**Resources:**

  * Foundational Paper: [Vaswani et al., 2017 - Attention Is All You Need (arXiv)](https://arxiv.org/abs/1706.03762) (Focus on architecture diagrams and attention sections)
  * Visual Explanation: [The Illustrated Transformer by Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
  * Code Examples/Tutorials (Conceptual Understanding):
      * [PyTorch Official Tutorial: Sequence-to-Sequence Modeling with nn.Transformer and TorchText](https://pytorch.org/tutorials/beginner/transformer_tutorial.html) (Focus on the architecture description)
      * [TensorFlow Official Tutorial: Transformer model for language understanding](https://www.tensorflow.org/text/tutorials/transformer) (Focus on architecture description)
  * Positional Encoding Explained: [Blog Post/Article explaining Positional Encoding in Transformers](https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/)

-----

### Exercise 1: Scaled Dot-Product Attention Calculation

**Goal:** Understand and manually calculate the steps involved in the Scaled Dot-Product Attention mechanism.
**Instructions:**

1.  Define the inputs to the Scaled Dot-Product Attention mechanism: Queries (Q), Keys (K), and Values (V). What do these typically represent in the context of self-attention within an encoder layer?
2.  Write down the formula for Scaled Dot-Product Attention: `Attention(Q, K, V) = softmax( (QK^T) / sqrt(d_k) ) * V`.
3.  Assume very small example matrices for Q, K, and V (e.g., 2x2 or 3x2 matrices) and a small dimension `d_k` (e.g., 2).
4.  Manually calculate the intermediate steps:
      * Matrix multiplication: `QK^T`
      * Scaling: Divide by `sqrt(d_k)`
      * Softmax (applied row-wise): Calculate the attention weights/scores. Explain what these scores represent.
      * Matrix multiplication: Multiply the softmax output by V to get the final output.
5.  Why is the scaling factor `sqrt(d_k)` used? What problem does it help mitigate?

### Exercise 2: Explaining Self-Attention

**Goal:** Articulate the concept of self-attention and how it allows the model to weigh the importance of different words in the *same* sequence.
**Instructions:**

1.  How are the Query (Q), Key (K), and Value (V) matrices typically derived from the *input* word embeddings in a self-attention layer? (Hint: Linear projections/Weight matrices Wq, Wk, Wv).
2.  Explain the intuition behind self-attention: When calculating the output representation for a specific word (e.g., "it" in "The animal didn't cross the street because it was too tired"), how does self-attention help the model determine which other words in the sentence ("animal", "street") are most relevant to understanding the current word ("it")?
3.  Compare self-attention to the attention mechanism discussed in Subtopic 3.1 (e.g., Bahdanau attention). What is the key difference in terms of what attends to what?
4.  What is the main advantage of self-attention over RNNs/LSTMs in terms of handling long-range dependencies and parallelization?

### Exercise 3: Understanding Multi-Head Attention

**Goal:** Explain the motivation and mechanism of Multi-Head Attention.
**Instructions:**

1.  Why use multiple "attention heads" instead of just one single self-attention mechanism? What benefit does this provide? (Hint: Attending to different types of relationships or "representation subspaces").
2.  Describe the process of Multi-Head Attention:
      * How are the Q, K, V inputs projected differently for each head?
      * How is Scaled Dot-Product Attention applied independently within each head?
      * How are the outputs from the multiple heads combined to produce the final output of the Multi-Head Attention layer? (Hint: Concatenation and a final linear projection).
3.  If a model has `h` attention heads and the total model dimension is `d_model`, what is typically the dimension (`d_k`, `d_v`) used for the Q, K, V projections within each *individual* head? Why?

### Exercise 4: The Need for Positional Encoding

**Goal:** Explain why Positional Encoding is necessary in the Transformer architecture and how it works conceptually.
**Instructions:**

1.  Explain why the core Transformer architecture (Self-Attention and Feed-Forward layers) is inherently **permutation-invariant**. What information about the input sequence is lost if only word embeddings are fed into the self-attention layers?
2.  What is the purpose of **Positional Encoding**? Where is it typically added in the Transformer model?
3.  Describe the sinusoidal positional encoding scheme proposed in the original Transformer paper (no need to write the exact formulas unless desired). What are the key properties of these sinusoidal encodings that make them suitable (e.g., unique for each position, relative position information)?
4.  Are sinusoidal encodings the only way to provide positional information? Mention one alternative approach (e.g., learned positional embeddings).

### Exercise 5: Role of Other Transformer Components

**Goal:** Briefly explain the purpose of the other key components within a standard Transformer Encoder/Decoder layer.
**Instructions:**

1.  Describe the purpose of the **Add & Norm** (Residual Connection and Layer Normalization) steps that follow the Multi-Head Attention and Feed-Forward layers. What problems do they help address during training?
2.  What is the structure and purpose of the **Position-wise Feed-Forward Network** within each Transformer layer? (Hint: Applied independently to each position).
3.  In a full Encoder-Decoder Transformer (like the original paper), describe the different types of attention layers used:
      * Self-Attention in the Encoder.
      * Self-Attention in the Decoder (masked). Why is masking needed here?
      * Encoder-Decoder Attention (Cross-Attention). What are the Q, K, V inputs for this layer?
