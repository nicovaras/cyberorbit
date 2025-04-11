## 倹 Subtopic 3.6: Attention Mechanisms: The Foundation

**Goal:** Understand the motivation for attention mechanisms, implement scaled dot-product attention and multi-head attention, and differentiate between self-attention and cross-attention.

**Resources:**

* **Attention Is All You Need Paper:** [Vaswani et al., 2017](https://arxiv.org/abs/1706.03762) (Introduced Transformers)
* **Attention Mechanism Explanations:** [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/), [Distill.pub Article on Attention](https://distill.pub/2016/augmented-rnns/)
* **PyTorch Attention Layers:** [MultiheadAttention](https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
* **TensorFlow Attention Layers:** [MultiHeadAttention](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention)

---

### 隼 **Exercise 1: Motivation - Overcoming Sequence Limitations**

**Goal:** Understand why attention mechanisms became crucial for improving sequence modeling beyond standard RNNs/LSTMs.

**Instructions:**

1.  Describe the basic workflow of a standard Recurrent Neural Network (RNN) or LSTM for sequence-to-sequence tasks (e.g., machine translation). How is information from the input sequence typically compressed into a fixed-size context vector?
2.  What is the **bottleneck problem** associated with this fixed-size context vector, especially when dealing with long input sequences? How might information from early parts of a long sequence be lost?
3.  Explain the core idea of **attention** in this context: Instead of relying solely on the final hidden state (context vector), the decoder is allowed to selectively look back at ("attend to") different parts of the *entire* input sequence's hidden states when generating each output step.
4.  How does this attention mechanism potentially solve the bottleneck problem and better handle long-range dependencies?
5.  **Challenge:** Consider machine translation. Why would allowing the decoder to focus on specific input words relevant to the current output word being generated be beneficial? Provide a hypothetical example.

---

### 隼 **Exercise 2: Scaled Dot-Product Attention Implementation**

**Goal:** Implement the scaled dot-product attention mechanism from scratch.

**Instructions:**

1.  Define the inputs to scaled dot-product attention: Queries (`Q`), Keys (`K`), and Values (`V`). Assume they are matrices/tensors. Let `d_k` be the dimension of the keys and queries.
2.  Implement the steps:
    * **Calculate Scores:** Compute the dot products of the Queries and Keys: `scores = matmul(Q, K.transpose(-1, -2))`.
    * **Scale Scores:** Divide the scores by the square root of the key dimension: `scaled_scores = scores / sqrt(d_k)`. Why is this scaling important? (Hint: Prevents softmax saturation with large `d_k`).
    * **Apply Mask (Optional):** If implementing masked attention (e.g., for decoders), apply a mask (e.g., setting certain elements to negative infinity) to `scaled_scores` before the softmax step.
    * **Softmax:** Apply the softmax function along the key dimension (last dimension of `scaled_scores`) to get attention weights/probabilities: `attention_weights = softmax(scaled_scores, dim=-1)`. Ensure weights sum to 1 across the keys for each query.
    * **Weighted Sum:** Compute the weighted sum of the Values using the attention weights: `output = matmul(attention_weights, V)`.
3.  Write a Python function `scaled_dot_product_attention(Q, K, V, mask=None)` using PyTorch/TensorFlow/NumPy that performs these steps.
4.  Create sample `Q`, `K`, `V` tensors and test your function. Verify the output shape and that `attention_weights` sum to 1 appropriately.
5.  **Challenge:** Implement the masking step correctly for a decoder self-attention scenario, where a position `i` can only attend to positions `j <= i`.

---

### 隼 **Exercise 3: Multi-Head Attention Implementation**

**Goal:** Implement multi-head attention by combining multiple scaled dot-product attention "heads" running in parallel.

**Instructions:**

1.  Understand the concept: Multi-head attention applies scaled dot-product attention multiple times (`num_heads`) in parallel to linearly projected versions of Q, K, and V.
2.  Define the inputs: `Q`, `K`, `V`, embedding dimension `d_model`, number of heads `num_heads`. Ensure `d_model` is divisible by `num_heads`. Calculate the dimension per head `d_k = d_v = d_model / num_heads`.
3.  Implement the Multi-Head Attention forward pass:
    * **Linear Projections:** Define linear layers (without bias) to project Q, K, V *for each head*. It's more efficient to define one large linear layer for all heads for Q, one for K, one for V, each outputting `d_model` dimensions.
    * Apply the projections: `Q_proj = W_q(Q)`, `K_proj = W_k(K)`, `V_proj = W_v(V)`.
    * **Reshape for Heads:** Reshape `Q_proj`, `K_proj`, `V_proj` to split the last dimension (`d_model`) into `num_heads` and `d_k`/`d_v`. Typical shape: `(Batch, num_heads, Seq_Len, d_k)`.
    * **Apply Scaled Dot-Product Attention:** Apply your function from Exercise 2 (or framework equivalent) to the reshaped projections *in parallel* for all heads. Result shape: `(Batch, num_heads, Seq_Len_Q, d_v)`.
    * **Concatenate Heads:** Reshape the output attention heads back into shape `(Batch, Seq_Len_Q, d_model)`.
    * **Final Linear Projection:** Apply a final linear layer `W_o` (outputting `d_model` dimensions) to the concatenated output.
4.  Implement this as a module/layer in PyTorch/TensorFlow (or use the built-in `MultiheadAttention` layer and compare).
5.  Test with sample inputs and verify output shapes.
6.  Discuss the motivation for multi-head attention: How does allowing the model to attend to information from different representation subspaces at different positions potentially help?
7.  **Challenge:** Compare the parameter count of a single MultiHeadAttention layer (including all projection matrices) versus a single Scaled Dot-Product Attention mechanism operating on the original `d_model` dimensions.

---

### 隼 **Exercise 4: Self-Attention vs. Cross-Attention**

**Goal:** Differentiate between self-attention (within a sequence) and cross-attention (between two different sequences).

**Instructions:**

1.  Define **Self-Attention**:
    * What are the sources for the Q, K, and V inputs? (Hint: They all come from the *same* input sequence).
    * What relationships is self-attention designed to capture? (Hint: Relationships between different elements *within* the same sequence).
    * Where is self-attention used in the original Transformer architecture (Encoder? Decoder?)?
2.  Define **Cross-Attention**:
    * What are the sources for the Q, K, and V inputs? (Hint: Q comes from one sequence, K and V come from *another* sequence).
    * What relationship is cross-attention designed to capture? (Hint: Relevance of elements in the second sequence to elements in the first sequence).
    * Where is cross-attention used in the original Transformer architecture? (Hint: Connecting the Decoder to the Encoder output).
3.  Provide a simple example scenario for each:
    * Self-Attention: e.g., Understanding pronoun references within a single sentence.
    * Cross-Attention: e.g., A decoder generating an English translation focusing on relevant French words from the encoder output.
4.  **Challenge:** Can the `MultiheadAttention` layer implementation (from Exercise 3 or frameworks) be used for both self-attention and cross-attention? How would you pass the inputs differently for each case?

---

### 隼 **Exercise 5: Introduction to Positional Encodings**

**Goal:** Understand why positional information is needed in attention-based models like Transformers and how sinusoidal positional encodings provide this.

**Instructions:**

1.  Explain why standard self-attention mechanisms are **permutation invariant**. If you shuffle the order of input tokens, would the self-attention output change fundamentally (assuming Q, K, V are derived solely from token embeddings)?
2.  Why is information about the *position* or *order* of tokens crucial for most language tasks?
3.  Describe the **Positional Encoding** technique used in the original Transformer paper:
    * Fixed sinusoidal functions of different frequencies are used.
    * A vector (with the same dimension as the token embedding, `d_model`) is generated for each position in the sequence.
    * This positional encoding vector is **added** to the corresponding token embedding before feeding into the attention layers.
4.  What are the advantages of using sinusoidal positional encodings compared to, say, learned positional embeddings? (Hint: Ability to potentially generalize to longer sequences, no extra parameters).
5.  Implement the sinusoidal positional encoding function as described in the "Attention Is All You Need" paper (using `sin` for even dimensions and `cos` for odd dimensions based on position and dimension index). Generate encodings for a sequence of a given length and dimension and visualize them.
6.  **Challenge:** Research other types of positional encoding methods (e.g., relative positional encodings, learned positional embeddings). How do they differ from the original sinusoidal approach?

---