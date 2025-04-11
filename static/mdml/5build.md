## 倹 Subtopic 5.3: Building & Consuming MCP Services

**Goal:** Understand the practical steps involved in creating MCP servers to expose tools/data and building client applications that interact with these servers, leveraging available SDKs.

**Resources:**

* **.NET Blog - Build MCP Server in C#:** [Blog Post](https://devblogs.microsoft.com/dotnet/build-a-model-context-protocol-mcp-server-in-csharp/)(Primary resource for practical steps)
* **MCP C# SDK Packages:** (Mentioned in the blog post, e.g., `ModelContextProtocol`, `Microsoft.Extensions.Hosting`, `Microsoft.Extensions.AI`)
* **Other SDKs/Implementations:** (Mentioned conceptually, e.g., Zapier MCP, implementations by Block, Apollo, Zed etc.)

---

### 隼 **Exercise 1: Setting up an MCP Server Project (.NET Example)**

**Goal:** Outline the initial project setup and dependency installation for building an MCP server using the .NET C# SDK based on the provided blog post.

**Instructions:**

1.  Following the .NET blog post, list the `dotnet` CLI commands needed to:
    * Create a new console application project.
    * Add the necessary NuGet packages (`ModelContextProtocol`, `Microsoft.Extensions.Hosting`, potentially `Microsoft.Extensions.AI`).
2.  What is the role of `Microsoft.Extensions.Hosting` in this context?
3.  What core functionalities does the `ModelContextProtocol` NuGet package provide according to the blog post?
4.  Examine the basic C# code structure presented in the blog post for initializing the host and configuring the MCP server within `Program.cs` (or equivalent startup code). What key methods are called (e.g., `AddModelContextProtocol`, `WithToolsFromAssembly`)?
5.  **Challenge:** Find the NuGet gallery pages for the mentioned packages. What are their current versions and dependencies?

---

### 隼 **Exercise 2: Defining MCP Tools (.NET Example)**

**Goal:** Understand how to define functions that can be exposed as callable tools by an MCP server using the .NET C# SDK attributes.

**Instructions:**

1.  Based on the C# code snippets in the .NET blog post, explain the purpose of the following attributes:
    * `[McpServerToolType]`: Where is this attribute applied? What does it signify?
    * `[McpServerTool]`: Where is this attribute applied? What does it signify?
    * `[Description("...")]`: What is the purpose of adding a description to an `McpServerTool`? How might a client use this information?
2.  Write a simple C# static class with a static method (similar to the `EchoTool` example) that takes two numbers as input and returns their sum. Annotate the class and method correctly with the MCP attributes, including a clear description.
3.  How does the MCP server discover these tools when using `WithToolsFromAssembly` during startup, according to the blog post?
4.  **Challenge:** Can MCP tools have asynchronous implementations (e.g., returning `Task<string>` instead of `string`)? How might this be useful? (Look for hints or patterns in the SDK documentation or advanced examples if available).

---

### 隼 **Exercise 3: Server Configuration and Execution Flow**

**Goal:** Understand how an MCP server is configured, run, and how it handles incoming tool execution requests.

**Instructions:**

1.  Describe how the MCP server is typically started and hosted based on the .NET example(e.g., using `IHost`).
2.  When an MCP client (like the one potentially integrated into GitHub Copilot or another AI assistant) wants to execute a tool:
    * How does the client likely discover the available tools and their descriptions? (Conceptual - likely via a protocol method).
    * How is the tool call likely represented (referencing Exercise 2 in Subtopic 5.2 - JSON-RPC)?
    * According to the blog post, what prompt or interaction might the *client/host* show to the user before executing the tool call on the server?Why is this user consent step important?
3.  How does the MCP server receive the request and route it to the correct C# method annotated with `[McpServerTool]`? (Conceptual - based on method name matching the JSON-RPC request).
4.  How is the result from the C# method sent back to the client? (Conceptual - via JSON-RPC response).
5.  **Challenge:** The blog mentions configuring servers to take access tokens or parameters on startup for calling other services. How might dependency injection provided by `Microsoft.Extensions.Hosting` be used to provide necessary configuration or authenticated clients (like an `HttpClient`) to your tool methods?

---

### 隼 **Exercise 4: Integrating MCP Server with External Data/APIs**

**Goal:** Understand the process of making MCP tools more useful by connecting them to external data sources or APIs.

**Instructions:**

1.  Explain why MCP servers become truly powerful when they integrate with existing APIs, services, or data.
2.  Modify the simple C# tool code from Exercise 2 (the adder tool). Instead of just adding two numbers, imagine it needs to:
    * Accept a `productId` as input.
    * Call an external (hypothetical) REST API `https://api.inventory.com/stock/{productId}` to get the current stock level. (Use `HttpClient` conceptually).
    * Return a string indicating the stock level (e.g., `"Product {productId} has {stockLevel} items in stock."`).
3.  Outline the code changes needed within the tool method to achieve this using `HttpClient`. Include conceptual error handling (e.g., product not found, API unavailable).
4.  How would you securely provide necessary API keys or base URLs needed by `HttpClient` to your MCP server/tool? (Refer back to configuration/dependency injection ideas from Exercise 3).
5.  **Challenge:** Consider the `Filesystem` tool example mentioned in the blog post. What kind of security considerations would be paramount when building an MCP tool that allows an AI assistant to interact with the server's local filesystem?

---

### 隼 **Exercise 5: Consuming MCP Services (Client Perspective)**

**Goal:** Understand the steps a client application would take to interact with an MCP server.

**Instructions:**

1.  Although the blog post focuses on building servers, it mentions the `ModelContextProtocol` package also provides APIs for creating clients.
2.  Outline the likely steps an MCP client application would need to perform:
    * **Discovery:** How would the client find available MCP servers? (Conceptual - maybe manual configuration, or a future discovery mechanism).
    * **Connection:** Establish a connection to the server's endpoint using the appropriate protocol (based on JSON-RPC).
    * **Capability Negotiation:** How would the client learn which tools the server provides and what parameters they expect? (Conceptual - likely involves calling specific MCP methods defined by the protocol standard, perhaps using the tool descriptions).
    * **Tool Invocation:** Construct and send a JSON-RPC request to call a specific tool method with the required parameters.
    * **Handling Response:** Receive and parse the JSON-RPC response (either success with a result or an error).
3.  How might a client handle user consent before invoking a potentially sensitive tool on the server?
4.  What kind of libraries or abstractions would make building an MCP client easier (similar to how `HttpClient` simplifies HTTP requests)? [cite: 1.1 suggests the SDK provides this].
5.  **Challenge:** Explore the examples or documentation for client usage if available in the MCP C# SDK samples mentioned, or consider how you might use a generic JSON-RPC client library to interact with a hypothetical MCP server endpoint.

---