## 倹 Subtopic 4.8.3: Parameter-Efficient Fine-Tuning (PEFT) Techniques

**Goal:** Understand the motivation for PEFT methods and explore key techniques like LoRA, Adapters, and Prefix Tuning that allow fine-tuning large language models with significantly fewer trainable parameters.

**Resources:**

* **IBM Article on PEFT:** [What is parameter-efficient fine-tuning (PEFT)?](https://www.ibm.com/think/topics/parameter-efficient-fine-tuning)
* **GeeksforGeeks Article on PEFT:** [What is Parameter-Efficient Fine-Tuning (PEFT)?](https://www.geeksforgeeks.org/what-is-parameter-efficient-fine-tuning-peft/)
* **LoRA Paper:** [Hu et al., 2021 - LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
* **Hugging Face PEFT Library:** [Documentation](https://huggingface.co/docs/peft/index) (Provides implementations for LoRA, Adapters, Prefix Tuning, etc.)

---

### 隼 **Exercise 1: Motivation for PEFT**

**Goal:** Explain why PEFT methods are crucial for working with modern Large Language Models (LLMs).

**Instructions:**

1.  Describe the challenges associated with full fine-tuning of very large pre-trained language models (e.g., models with billions of parameters like GPT-3). Consider:
    * **Computational Cost:** GPU memory and time required for training.
    * **Storage Cost:** Storing a separate copy of the full model for each downstream task.
    * **Deployment:** Managing many large, task-specific models.
2.  How do Parameter-Efficient Fine-Tuning (PEFT) methods aim to address these challenges? What is the core idea behind most PEFT techniques (Hint: freezing most pre-trained weights and adding/modifying a small number of parameters)?
3.  List the key benefits of using PEFT methods mentioned in the resources. (e.g., reduced computational cost, smaller storage, less catastrophic forgetting, better multi-task learning).
4.  **Challenge:** If PEFT methods only tune a small fraction of parameters, how can they still achieve performance comparable to full fine-tuning on many tasks?

---

### 隼 **Exercise 2: LoRA (Low-Rank Adaptation) - Concept & Implementation**

**Goal:** Understand the LoRA technique and apply it to a pre-trained Transformer model using the Hugging Face PEFT library.

**Instructions:**

1.  Explain the core idea of LoRA:
    * Instead of updating the full weight matrix `W` of a layer, LoRA introduces two smaller, low-rank matrices `A` and `B`.
    * The update to the weights is represented by their product: `delta_W = B * A`.
    * During fine-tuning, only `A` and `B` are trained, while the original `W` is frozen.
    * The modified forward pass becomes `h = Wx + BAx`.
2.  Why is decomposing the weight update into low-rank matrices parameter-efficient? If `W` is `d x k`, `A` is `d x r`, and `B` is `r x k` (where rank `r << d, k`), compare the number of parameters in `BA` versus `W`.
3.  Using the Hugging Face `peft` library:
    * Load a pre-trained Transformer model (e.g., for sequence classification).
    * Define a `LoraConfig`, specifying:
        * `r` (rank of the update matrices).
        * `lora_alpha` (scaling factor).
        * `target_modules` (which layers to apply LoRA to, e.g., query/value matrices in attention).
        * `task_type`.
    * Use `get_peft_model` to apply the LoRA configuration to your base model.
    * Print the number of trainable parameters in the PEFT model versus the original model.
4.  Fine-tune this LoRA-enabled model on a downstream task (e.g., text classification from Subtopic 4.8.2). Compare its performance and training time/memory usage to full fine-tuning.
5.  How are the LoRA adapters typically saved and loaded for inference? (Hint: Only the small A and B matrices).
6.  **Challenge:** Experiment with different ranks `r` and different `target_modules` in the `LoraConfig`. How do these choices affect the number of trainable parameters and the final performance?

---

### 隼 **Exercise 3: Adapter Modules - Concept**

**Goal:** Understand the concept of Adapter modules as another PEFT technique.

**Instructions:**

1.  Explain the core idea of Adapter modules:
    * Small, task-specific neural network modules are inserted *between* the existing layers of a pre-trained Transformer.
    * The original Transformer weights are kept frozen.
    * Only the parameters of these newly added adapter modules are trained for each downstream task.
2.  Describe a typical adapter module architecture (often a bottleneck structure: down-project -> non-linearity -> up-project).
3.  How does this approach allow a single pre-trained model to be adapted for multiple tasks without storing full copies of the model?
4.  Compare Adapters to LoRA conceptually:
    * Where are the new parameters added (LoRA modifies existing weight updates, Adapters add new small layers)?
    * How might they differ in terms of inference latency (LoRA can be merged, Adapters add sequential computation)?
5.  **Challenge:** Find and review the `AdapterHub` project. How does it facilitate sharing and using pre-trained adapter modules?

---

### 隼 **Exercise 4: Prefix Tuning - Concept**

**Goal:** Understand the concept of Prefix Tuning, where learnable prefix vectors are added to the input of Transformer layers.

**Instructions:**

1.  Explain the core idea of Prefix Tuning:
    * A small sequence of continuous, task-specific vectors (the "prefix") is prepended to the input sequences (or to the keys and values in attention layers).
    * The original Transformer model parameters are kept frozen.
    * Only the parameters of this prefix vector are learned during fine-tuning.
2.  How does the model use these learned prefix vectors to adapt its behavior for a specific downstream task? (Hint: The prefix vectors act as task-specific instructions or context that guides the attention mechanisms).
3.  Where are prefixes typically inserted in the Transformer architecture (e.g., at each layer, affecting keys and values in attention)?
4.  Compare Prefix Tuning to LoRA and Adapters. How does it differ in terms of where and what parameters are tuned?
5.  Prefix Tuning was initially highlighted for Natural Language Generation (NLG) tasks. Why might it be effective for controlling generation style or content?
6.  **Challenge:** How does Prompt Tuning (P-Tuning) relate to Prefix Tuning? Are they similar concepts? (Hint: P-Tuning often involves learnable continuous *input embeddings* rather than prefixes at every layer).

---

### 隼 **Exercise 5: QLoRA - Quantization and LoRA**

**Goal:** Understand how QLoRA combines quantization with LoRA to further reduce memory requirements for fine-tuning very large models.

**Instructions:**

1.  What is **model quantization** in general? How does it reduce model size and potentially speed up inference by representing weights and/or activations with fewer bits (e.g., 8-bit or 4-bit integers instead of 32-bit floats)?
2.  Explain the core idea of **QLoRA**:
    * The large pre-trained model weights are quantized to a very low precision (e.g., 4-bit NormalFloat).
    * LoRA adapters (still in higher precision, e.g., 16-bit BrainFloat16) are added and fine-tuned.
    * How does this combination allow even very large models (e.g., 65B parameters) to be fine-tuned on a single GPU with significantly less memory?
3.  What are some of the special techniques used in QLoRA to maintain performance despite the aggressive quantization (e.g., 4-bit NormalFloat (NF4) data type, double quantization)?
4.  Why is it important that the LoRA adapter weights themselves are kept in a higher precision during training, even if the base model is quantized?
5.  **Challenge:** Using the Hugging Face `bitsandbytes` library (often used for QLoRA) and `peft`, try to load a pre-trained model in 4-bit or 8-bit precision and then apply LoRA for fine-tuning. Observe the memory footprint compared to loading the full precision model. (This may require specific hardware/setup).

---