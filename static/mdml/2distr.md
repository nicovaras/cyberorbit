## 倹 Subtopic 2.8: Introduction to Distributed Training Paradigms

**Goal:** Understand the fundamental concepts, motivations, and basic strategies behind distributed training, primarily focusing on Data Parallelism.

**Resources:**

* **Data Parallelism Overview:** [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist_overview.html), [TensorFlow Distributed Training Guide](https://www.tensorflow.org/guide/distributed_training)
* **Model Parallelism Overview:** [Concepts explained](https://huggingface.co/docs/transformers/v4.18.0/en/parallelism#model-parallelism)
* **Frameworks:**
    * **PyTorch:** `torch.nn.parallel.DistributedDataParallel` (DDP), `torch.distributed` package.
    * **TensorFlow:** `tf.distribute.Strategy` (e.g., `MirroredStrategy`, `MultiWorkerMirroredStrategy`).
    * **Horovod:** [Documentation](https://horovod.readthedocs.io/en/stable/) (Framework-agnostic library).

---

### 隼 **Exercise 1: Motivation for Distributed Training**

**Goal:** Articulate the primary reasons for using distributed training for large models and datasets.

**Instructions:**

1.  Describe the two main bottlenecks encountered when training very large deep learning models on a single GPU:
    * **Memory Limitation:** Explain why model size (parameters, activations) or large batch sizes can exceed the memory capacity of a single GPU.
    * **Compute Limitation:** Explain why training time can become prohibitively long even if the model fits in memory.
2.  Explain how **Data Parallelism** addresses the *compute limitation*. How does it speed up training?
3.  Explain how **Model Parallelism** addresses the *memory limitation*. How does it allow training models that don't fit on a single device?
4.  Discuss the trade-offs: What are the communication overhead challenges associated with each paradigm?
5.  **Challenge:** Research **Pipeline Parallelism** as a specific type of model parallelism. How does it attempt to mitigate the sequential dependency issue in naive model parallelism?

---

### 隼 **Exercise 2: Data Parallelism Workflow**

**Goal:** Outline the steps involved in a typical synchronous Data Parallel training iteration.

**Instructions:**

1.  Assume you have multiple workers (GPUs), each with a copy of the model. Describe the workflow for one training step using synchronous Data Parallelism:
    * **Data Distribution:** How is the mini-batch of data divided among the workers?
    * **Forward Pass:** What does each worker compute independently?
    * **Loss Calculation:** What does each worker compute independently?
    * **Backward Pass:** What does each worker compute independently? (Resulting in local gradients).
    * **Gradient Synchronization:** What needs to happen with the gradients computed on each worker? What collective communication operation is typically used (e.g., All-Reduce)?
    * **Optimizer Step:** How are the model weights updated on each worker? Ensure they remain consistent.
2.  Draw a simple diagram illustrating this flow across multiple workers (e.g., 2 or 4 GPUs).
3.  **Challenge:** What is **asynchronous** Data Parallelism? What are its potential benefits and drawbacks compared to the synchronous approach described above? (Hint: Stale gradients).

---

### 隼 **Exercise 3: Using Framework Data Parallel Utilities (Conceptual/Code Structure)**

**Goal:** Understand the high-level code structure required to implement Data Parallelism using standard frameworks like PyTorch DDP or TensorFlow MirroredStrategy. **(Running this may require multiple GPUs or specific environment setup).**

**Instructions:**

1.  **Initialization:** Research how the distributed environment is typically initialized. What information needs to be shared between processes (e.g., rank, world size)? (e.g., `torch.distributed.init_process_group`, environment variables `MASTER_ADDR`, `MASTER_PORT`, `RANK`, `WORLD_SIZE`).
2.  **Model Wrapping:** How is the model typically modified or wrapped to enable data parallel training? (e.g., `torch.nn.parallel.DistributedDataParallel(model)`, `tf.distribute.MirroredStrategy` scope).
3.  **Data Loading:** How does the data loader need to be adapted to ensure each process gets a unique shard of the data? (e.g., `torch.utils.data.distributed.DistributedSampler`, `tf.data.Dataset.shard`).
4.  **Training Loop:** Are significant changes needed within the main training loop (forward pass, loss, backward, optimizer step) compared to single-GPU training once the setup (model wrapping, data loading) is done? Discuss the role of the wrapper (like DDP) in handling gradient synchronization automatically.
5.  **Saving/Loading Checkpoints:** What special considerations are needed when saving and loading model checkpoints in a distributed setting (e.g., saving only on rank 0)?
6.  **Challenge:** Compare PyTorch's `DistributedDataParallel` (multi-process) with the older `DataParallel` (multi-thread). Why is DDP generally recommended for performance?

---

### 隼 **Exercise 4: Model Parallelism Concepts**

**Goal:** Understand the core idea behind Model Parallelism by assigning different parts of a model to different devices.

**Instructions:**

1.  Consider a simple sequential model (e.g., MLP with multiple large linear layers: `Input -> Layer1 -> Layer2 -> Layer3 -> Output`).
2.  Assume `Layer1` fits on GPU 0, `Layer2` fits on GPU 1, and `Layer3` fits on GPU 0.
3.  Describe the flow of data during the **forward pass**:
    * Where does the input data start?
    * Where is the computation for `Layer1` performed?
    * What data needs to be transferred between which devices after `Layer1`?
    * Where is `Layer2` computed? What transfer happens next?
    * Where is `Layer3` computed?
4.  Describe the flow during the **backward pass**:
    * Where does the initial gradient calculation start?
    * How are gradients propagated back through the layers and across devices? What data needs to be transferred?
5.  Explain the "pipeline bubble" or device under-utilization problem that can occur in naive model parallelism.
6.  **Challenge:** How might you apply model parallelism to a large Transformer model? Where are natural splitting points within the architecture? (e.g., splitting attention heads, splitting feed-forward layers).

---

### 隼 **(Optional) Exercise 5: Exploring Horovod**

**Goal:** Learn about Horovod as a framework-agnostic library for distributed training.

**Instructions:**

1.  Visit the Horovod documentation (linked in Resources).
2.  Understand Horovod's core concept: How does it integrate with existing frameworks like TensorFlow, Keras, and PyTorch? (Hint: Wraps optimizer, broadcasts initial state, averages gradients).
3.  What communication backend does Horovod typically rely on (e.g., MPI, NCCL)? How does NCCL optimize collective communication operations like All-Reduce on NVIDIA GPUs?
4.  Compare the typical code modifications required to use Horovod with those needed for native framework utilities (PyTorch DDP, TF MirroredStrategy). Is it generally more or less intrusive?
5.  **Challenge:** Find examples in the Horovod documentation for running a simple PyTorch or TensorFlow script using Horovod across multiple processes (even if simulated on a single machine using `horovodrun -np 2 ...`).

---