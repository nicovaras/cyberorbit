## 倹 Subtopic 4.8.4: Prompt Engineering & In-Context Learning (ICL) with LLMs

**Goal:** Master the art and science of designing effective prompts to guide Large Language Models (LLMs) in performing various tasks using in-context learning (zero-shot, one-shot, few-shot), including advanced techniques like Chain-of-Thought prompting.

**Resources:**

* **Hopsworks on ICL:** [What is In Context Learning (ICL)?](https://www.hopsworks.ai/dictionary/in-context-learning-icl)
* **PromptLayer Blog on ICL:** [What is In-Context Learning? How LLMs Learn From ICL Examples](https://blog.promptlayer.com/what-is-in-context-learning/)
* **K2view on Prompt Engineering vs Fine-tuning:** [Prompt Engineering vs Fine-Tuning](https://www.k2view.com/blog/prompt-engineering-vs-fine-tuning/)
* **Ubiai on Instruction Fine-Tuning & CoT:** [Why Instruction Fine-Tuning is the Key to Smarter AI](https://ubiai.tools/what-is-instruction-fine-tuning-and-why-is-it-important-2/)
* **LLM APIs:** (e.g., OpenAI API, Hugging Face Inference API, or local LLM inference setups) for practical experimentation.

---

### 隼 **Exercise 1: Understanding In-Context Learning (ICL)**

**Goal:** Explain the concept of In-Context Learning and how it differs from traditional fine-tuning.

**Instructions:**

1.  Define In-Context Learning (ICL) as it applies to Large Language Models (LLMs). How does an LLM "learn" to perform a new task during ICL?
2.  What are the key characteristics of ICL? Specifically address:
    * **No Weight Updates:** Are the LLM's internal parameters (weights) modified during ICL?
    * **Role of the Prompt:** How are task demonstrations and instructions provided to the model?
    * **Temporary Learning:** Is the "learning" persistent across different inference requests if the prompt changes?
3.  Compare ICL with traditional fine-tuning. What are the main advantages and disadvantages of ICL in terms of flexibility, computational cost, data requirements, and potential performance?
4.  **Challenge:** Why do larger LLMs typically exhibit stronger ICL capabilities?

---

### 隼 **Exercise 2: Zero-Shot, One-Shot, and Few-Shot Prompting**

**Goal:** Design and test zero-shot, one-shot, and few-shot prompts for different NLP tasks.

**Instructions:**

1.  Choose a capable LLM (e.g., via an API like OpenAI's, or a local model using Hugging Face `pipeline`).
2.  Select three different simple NLP tasks (e.g., sentiment analysis, simple question answering, text generation in a specific style).
3.  For **each task**:
    * **Zero-Shot Prompt:** Craft a prompt that describes the task to the LLM without providing any examples. Test it.
    * **One-Shot Prompt:** Craft a prompt that includes one example of the task (input and desired output) in addition to the instruction. Test it.
    * **Few-Shot Prompt:** Craft a prompt that includes 2-5 examples of the task. Test it.
4.  Compare the quality and consistency of the LLM's responses for zero-shot, one-shot, and few-shot prompts for each task.
5.  Discuss how the number of examples (shots) in the prompt influences the LLM's performance and its understanding of the desired output format or task nuances.
6.  **Challenge:** For one task, systematically vary the quality and diversity of examples in your few-shot prompt. How sensitive is the LLM's performance to the examples provided?

---

### 隼 **Exercise 3: Designing Effective Prompts - Clarity, Context, Examples**

**Goal:** Practice crafting high-quality prompts by focusing on clarity, providing sufficient context, and using well-chosen examples.

**Instructions:**

1.  Choose a moderately complex task for an LLM, e.g., "Extract key entities (Person, Organization, Location) from a news paragraph" or "Generate a product description for a new type of eco-friendly water bottle, highlighting its unique features and target audience."
2.  **Initial Poor Prompt:** Write an initial, vague, or underspecified prompt for this task. Test it with an LLM and note the (likely poor) results.
3.  **Iterative Refinement:** Improve your prompt step-by-step, focusing on:
    * **Clarity of Instruction:** Is the task explicitly and unambiguously stated?
    * **Sufficient Context:** Does the prompt provide all necessary background information the LLM needs?
    * **Role-Playing:** Can you instruct the LLM to act as a specific persona (e.g., "You are a helpful marketing assistant...")?
    * **Output Format Specification:** Do you guide the LLM on how to structure its output (e.g., JSON, bullet points, specific tone)?
    * **Quality of Examples (for few-shot):** If using examples, are they diverse, accurate, and representative of the desired output? The Hopsworks article mentions adding relevant context at the beginning or end.
4.  Test each refined version of your prompt and document how the LLM's output improves.
5.  Present your final, effective prompt and explain the rationale behind your design choices.
6.  **Challenge:** Explore "negative prompting" – instructing the LLM what *not* to do or what topics/styles to avoid. Add a negative constraint to your refined prompt and see if the LLM adheres to it.

---

### 隼 **Exercise 4: Chain-of-Thought (CoT) Prompting**

**Goal:** Implement Chain-of-Thought (CoT) prompting to encourage LLMs to perform step-by-step reasoning for complex tasks.

**Instructions:**

1.  Explain the core idea behind Chain-of-Thought (CoT) prompting. How does it differ from standard few-shot prompting? (Hint: Examples show intermediate reasoning steps).
2.  Choose a task that requires multi-step reasoning (e.g., a simple math word problem, a logical puzzle, or a question that requires synthesizing information from a provided text).
3.  **Standard Few-Shot Prompt:** Create a few-shot prompt for this task *without* CoT (i.e., examples only show input and final answer). Test it with an LLM.
4.  **CoT Few-Shot Prompt:** Modify your prompt to include examples where the intermediate reasoning steps are explicitly shown before the final answer.
    * Example (Math Word Problem):
      `Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?`
      `A: Roger started with 5 balls. He bought 2 cans of 3 tennis balls each, which is 2 * 3 = 6 balls. So he has 5 + 6 = 11 balls. The final answer is 11.`
5.  Test the CoT prompt with the LLM on new instances of the task.
6.  Compare the performance (accuracy, correctness of reasoning) of the LLM with standard few-shot prompting versus CoT prompting.
7.  Discuss why CoT prompting can significantly improve performance on reasoning tasks.
8.  **Challenge:** Can you combine CoT with zero-shot prompting by explicitly asking the model to "think step-by-step" or "show its work" before giving the final answer? Test this "Zero-Shot-CoT".

---

### 隼 **Exercise 5: Introduction to Instruction Fine-Tuning (IFT)**

**Goal:** Understand the concept of Instruction Fine-Tuning (IFT) and how it relates to improving an LLM's ability to follow instructions and generalize to unseen tasks.

**Instructions:**

1.  Define Instruction Fine-Tuning (IFT). How does it differ from standard fine-tuning on a single downstream task? (Hint: IFT uses datasets of (instruction, response) pairs for many diverse tasks).
2.  What is the primary goal of IFT? (Hint: To make LLMs better at understanding and following natural language instructions, improving zero-shot performance on new tasks).
3.  How does IFT complement prompt engineering? Can a model that has undergone IFT still benefit from well-crafted prompts?
4.  Models like FLAN (Fine-tuned Language Net) are examples of instruction-tuned models. Research briefly how FLAN was trained.
5.  **Challenge:** If you have access to an instruction-tuned LLM (many modern chat models are), compare its ability to follow complex zero-shot instructions against a base LLM (if available) that has not undergone extensive instruction tuning. How does their performance differ?

---