## 倹 Subtopic 5.5: A2A Discovery & Communication Flow

**Goal:** Understand how agents discover each other's capabilities using Agent Cards and trace the communication flow for synchronous and asynchronous (streaming) A2A tasks.

**Resources:**

* **A2A GitHub README:** [google/A2A README.md](https://github.com/google/A2A/blob/main/README.md)(Agent Card, Task flow, SSE)
* **Google Blog Posts on A2A:** [Developers Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), [Cloud Blog](https://cloud.google.com/blog/topics/partners/best-agentic-ecosystem-helping-partners-build-ai-agents-next25)

---

### 隼 **Exercise 1: Agent Card for Discovery**

**Goal:** Understand the structure and purpose of the A2A Agent Card for capability discovery.

**Instructions:**

1.  According to the A2A READMEand Developers Blog, what is an **Agent Card**?
2.  What is the typical format (JSON) and standard location (`/.well-known/agent.json`) mentioned for an Agent Card?
3.  What key pieces of information does the Agent Card contain about the remote agent? List the examples mentioned (capabilities, skills, endpoint URL, authentication requirements).
4.  How does a client agent use the Agent Card to determine if a remote agent can perform a desired task and how to communicate with it?
5.  **Challenge:** Sketch a hypothetical JSON structure for a simple Agent Card, including fields for agent name, description, A2A endpoint URL, supported authentication methods (e.g., OAuth), and a list of simple capabilities/skills (e.g., "summarize_text", "translate_language").

---

### 隼 **Exercise 2: Synchronous Task Flow (`tasks/send`)**

**Goal:** Outline the communication sequence for a simple, synchronous A2A task execution.

**Instructions:**

1.  Assume a client agent wants a remote agent to perform a quick task (e.g., translate a short sentence) that can be completed immediately. The client uses the non-streaming `tasks/send` method.
2.  Describe the sequence of events:
    * **Client Request:** What information does the client send in the initial `tasks/send` request? (Hint: Task ID, initial message/prompt with Parts).
    * **Server Processing:** The remote agent (server) receives the request and processes the task synchronously.
    * **Server Response:** What does the server include in its HTTP response back to the client? (Hint: The final Task object, including status 'completed' and any resulting Artifacts).
3.  Draw a simple sequence diagram showing this client -> server -> client interaction.
4.  In what scenarios is this synchronous approach suitable? When might it be unsuitable?
5.  **Challenge:** What happens if the remote agent fails to complete the task synchronously? How would this likely be communicated back in the response according to the Task states mentioned?

---

### 隼 **Exercise 3: Asynchronous/Streaming Task Flow (`tasks/sendSubscribe` & SSE)**

**Goal:** Outline the communication sequence for a long-running A2A task using streaming updates via Server-Sent Events (SSE).

**Instructions:**

1.  Assume a client agent asks a remote agent to perform a long-running task (e.g., generate a detailed research report). The client uses `tasks/sendSubscribe` and the server supports streaming.
2.  Describe the sequence of events:
    * **Client Request:** What does the client send in the initial `tasks/sendSubscribe` request? Is it similar to `tasks/send`?
    * **Server Initial Response:** What does the server typically send back immediately in the HTTP response? (Hint: Usually confirms task submission, perhaps with initial status).
    * **Server-Sent Events (SSE):** The server keeps the connection open (or the client maintains an SSE connection). What kind of events does the server push to the client over time via SSE? Give examples based on the README (TaskStatusUpdateEvent, TaskArtifactUpdateEvent).
    * **Task Completion:** How is the final completion (or failure) of the task communicated via SSE?
3.  Draw a sequence diagram illustrating this flow, highlighting the ongoing SSE stream from server to client.
4.  Why is this asynchronous, streaming approach necessary for tasks that take significant time or involve intermediate updates/artifacts?
5.  **Challenge:** How might a client application update its user interface in real-time based on the `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` messages received via SSE?

---

### 隼 **Exercise 4: Handling `input-required` State**

**Goal:** Understand how agents handle situations where more information is needed from the client/user during task execution.

**Instructions:**

1.  The A2A task lifecycle includes an `input-required` state. In what kind of scenarios might a remote agent enter this state? (e.g., needing clarification, asking for a choice, requesting missing information).
2.  If a task enters the `input-required` state (communicated via synchronous response or SSE update):
    * What does the client agent need to do? (Hint: Likely prompt the end-user or decide programmatically).
    * How does the client agent send the required input back to the remote agent? Which A2A methods (`tasks/send` or `tasks/sendSubscribe`) can be used, and what key information must be included? (Hint: The same Task ID).
3.  How does this enable interactive, multi-turn conversations or workflows between agents (or between an agent and a user via a client)?
4.  **Challenge:** Design a hypothetical multi-turn interaction using A2A. For example, Agent A asks Agent B to book a flight. Agent B responds with `input-required` asking for preferred airline. Agent A sends back the preference. Agent B confirms booking or asks for payment details (`input-required` again).

---

### 隼 **Exercise 5: Multi-Modality Support**

**Goal:** Understand how A2A is designed to handle communication beyond just text.

**Instructions:**

1.  The A2A design principles mention being "Modality agnostic" and supporting audio/video streaming. The core concepts include `FilePart` and `DataPart` alongside `TextPart`.
2.  Explain how the use of different `Part` types within `Message` and `Artifact` objects allows A2A to handle multi-modal data.
3.  Provide examples of how these parts might be used:
    * `TextPart`: Standard text messages/prompts.
    * `FilePart`: Uploading a document for analysis, receiving a generated image or audio file. How might `uri` vs inline `bytes` be used?
    * `DataPart`: Sending structured JSON data for forms, receiving structured results from an API call made by the remote agent.
4.  How does supporting various modalities enable more sophisticated agent collaborations and user experiences (e.g., agents working with images, code, structured data, potentially voice interactions)?
5.  **Challenge:** Consider an interaction involving audio streaming (mentioned as a supported modality). How might A2A messages or parts need to be structured or streamed differently to handle real-time audio compared to static text or files? (Conceptual).

---