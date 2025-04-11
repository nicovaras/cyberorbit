## Subtopic 3.4: Practical LLM Application: Prompt Engineering Techniques

**Goal:** To develop skills in designing effective prompts for Large Language Models (LLMs) to elicit desired behaviors using techniques like zero-shot prompting, few-shot prompting, Chain-of-Thought, and understanding the basics of instruction following.

**Resources:**

  * Prompt Engineering Guides:
      * [Prompt Engineering Guide (Community Resource)](https://www.promptingguide.ai/)
      * [OpenAI API Documentation - Prompt Design](https://platform.openai.com/docs/guides/prompt-engineering)
      * [Anthropic Prompting Resources](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
  * Chain-of-Thought Paper: [Wei et al., 2022 - Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (arXiv)](https://arxiv.org/abs/2201.11903)
  * Access to an LLM:
      * API Providers (OpenAI, Anthropic, Cohere, Google AI Studio/Vertex AI)
      * Local LLM Interfaces (Ollama, LM Studio, Hugging Face `transformers` pipeline)

-----

### Exercise 1: Zero-Shot Prompting for Classification

**Goal:** Elicit classification behavior from an LLM without providing any examples in the prompt.
**Instructions:**

1.  Choose an LLM accessible to you (e.g., via API or local setup).
2.  Select a simple classification task (e.g., sentiment analysis, topic classification).
3.  Craft a **zero-shot prompt** that clearly describes the task and instructs the model on the desired output format. Example for sentiment:
    ```
    Classify the sentiment of the following movie review as positive, negative, or neutral.

    Review: "This movie was absolutely fantastic, I loved every minute of it!"
    Sentiment:
    ```
4.  Test the prompt with several different input reviews (clearly positive, clearly negative, neutral/ambiguous).
5.  Analyze the LLM's responses. Does it consistently follow the instructions and output format? How does it handle ambiguity?

### Exercise 2: Few-Shot Prompting for Improved Performance

**Goal:** Improve task performance by providing a small number of examples (shots) within the prompt (In-Context Learning).
**Instructions:**

1.  Using the same classification task and LLM from Exercise 1:
2.  Craft a **few-shot prompt** by adding 2-4 examples (input and desired output pairs) before the final query. Example for sentiment:
    ```
    Classify the sentiment of the following movie review as positive, negative, or neutral.

    Review: "It was okay, not great but not terrible."
    Sentiment: neutral

    Review: "Worst film I've seen all year, a complete disaster."
    Sentiment: negative

    Review: "A masterpiece! Truly inspiring and beautifully made."
    Sentiment: positive

    Review: "This movie was absolutely fantastic, I loved every minute of it!"
    Sentiment:
    ```
3.  Test this few-shot prompt with the same input reviews you used in Exercise 1, plus some new ones.
4.  Compare the consistency and accuracy of the LLM's responses using the few-shot prompt versus the zero-shot prompt. Did providing examples improve performance or adherence to the output format?

### Exercise 3: Chain-of-Thought (CoT) Prompting for Reasoning

**Goal:** Encourage step-by-step reasoning from the LLM for problems requiring logic or calculation using Chain-of-Thought prompting.
**Instructions:**

1.  Choose a simple multi-step reasoning problem (e.g., a basic math word problem, a simple logic puzzle). Example: "Alice has 5 apples. She gives 2 apples to Bob. Bob already had 3 apples. How many apples does Bob have now?"
2.  First, try solving it with a standard prompt (zero-shot or few-shot) asking only for the final answer. Observe the result.
3.  Now, craft a **Chain-of-Thought prompt**. This typically involves providing a few-shot example where the reasoning steps *are explicitly shown* before the final answer. Example structure:
    ```
    Q: [Example Problem 1]
    A: [Step 1 reasoning]. [Step 2 reasoning]. Therefore, the final answer is [Answer 1].

    Q: Alice has 5 apples. She gives 2 apples to Bob. Bob already had 3 apples. How many apples does Bob have now?
    A:
    ```
4.  Send this CoT prompt to the LLM.
5.  Analyze the LLM's output. Does it show the intermediate reasoning steps? Is the final answer more likely to be correct compared to the standard prompt?
    **Challenge:** Try zero-shot CoT by simply adding "Let's think step by step." before the LLM is expected to generate the answer in a zero-shot prompt. Does this improve reasoning?

### Exercise 4: Instruction Following and Role Playing

**Goal:** Craft prompts that instruct the LLM to adopt a specific persona or follow complex instructions.
**Instructions:**

1.  Craft a prompt instructing the LLM to act as a specific **persona** (e.g., "You are a skeptical pirate reviewing a new smartphone. Write a short review in character."). Send it to the LLM and evaluate the output for persona consistency.
2.  Craft a prompt with **multiple constraints** or instructions. Example: "Write a short story (under 100 words) about a robot discovering a flower. The story must include the color 'blue' but not the word 'metal'. The tone should be melancholic." Send it to the LLM.
3.  Analyze the output. Did the LLM successfully adhere to all instructions (persona, length, word inclusion/exclusion, tone)?
4.  Experiment with rephrasing or structuring the instructions differently (e.g., using bullet points) to see if it improves the LLM's ability to follow them.

### Exercise 5: Exploring Prompt Iteration

**Goal:** Understand the iterative nature of prompt engineering by refining a prompt to improve results for a specific task.
**Instructions:**

1.  Choose a moderately complex task (e.g., summarizing a technical paragraph into a single sentence suitable for a non-expert, generating Python code for a specific small function, extracting specific entities from a block of text).
2.  Write an initial prompt (V1) for the task. Send it to the LLM and evaluate the output based on desired criteria (accuracy, format, completeness, tone etc.).
3.  Identify weaknesses in the output and hypothesize how the prompt (V1) could be improved.
4.  Write a revised prompt (V2) incorporating your improvements (e.g., adding more context, being more specific about the output format, providing clearer instructions, adding constraints, using few-shot examples if needed).
5.  Send prompt V2 to the LLM and evaluate the output again. Compare it to the output from V1.
6.  Document the changes made between V1 and V2 and the observed impact on the LLM's output. Repeat the refinement process if necessary (V3...).
