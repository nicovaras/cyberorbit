## Subtopic 3.6: Introduction to Retrieval-Augmented Generation (RAG)

**Goal:** To understand the concept of RAG and gain basic hands-on experience implementing a simple RAG pipeline involving document embedding, vector storage/retrieval, and combining retrieved context with a query for an LLM prompt.

**Resources:**

  * RAG Overview:
      * [Pinecone Blog: What is Retrieval Augmented Generation?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
      * [LangChain Docs: Question Answering over Docs](https://www.google.com/search?q=https://python.langchain.com/docs/use_cases/Youtubeing/) (Illustrates the concept)
  * Vector Databases (Examples):
      * [ChromaDB Documentation](https://docs.trychroma.com/) (Good for local experimentation)
      * [FAISS GitHub](https://github.com/facebookresearch/faiss) (Library for efficient similarity search)
  * Embedding Models (Sentence Transformers):
      * [Sentence Transformers Library Documentation](https://www.sbert.net/)
      * [Hugging Face Hub: Sentence Transformer Models](https://huggingface.co/models?library=sentence-transformers) (e.g., `all-MiniLM-L6-v2`)
  * Access to an LLM (API or Local): (Same as Subtopic 3.4)

-----

### Exercise 1: Conceptual RAG Pipeline Design

**Goal:** Outline the core steps involved in a typical Retrieval-Augmented Generation system.
**Instructions:**

1.  Describe the main problem that RAG aims to solve compared to using a standard LLM alone (e.g., hallucination, lack of access to specific/recent information).
2.  Outline the major stages of a RAG pipeline for answering questions based on a document set:
      * **Indexing/Ingestion:** What happens during this phase (e.g., loading documents, chunking, embedding, storing in vector DB)?
      * **Retrieval:** What happens when a user query comes in (e.g., embedding the query, searching the vector DB)?
      * **Generation:** How is the retrieved information used along with the original query to generate the final answer using an LLM?
3.  Draw a simple block diagram illustrating these stages and the flow of data.

### Exercise 2: Document Loading and Chunking

**Goal:** Load text documents and split them into manageable chunks suitable for embedding.
**Instructions:**

1.  Select a small set of text documents (e.g., 2-3 short articles, sections from a Wikipedia page saved as `.txt` files).
2.  Use Python to read the content of these files.
3.  Implement a simple chunking strategy:
      * **Option 1 (Fixed Size):** Split the text into chunks of a fixed number of characters or words (e.g., 500 characters) with some overlap (e.g., 50 characters).
      * **Option 2 (Sentence Splitting):** Use a library like `nltk` (`sent_tokenize`) to split the text into sentences, then group sentences into chunks up to a certain size.
4.  Store the resulting text chunks in a list. Print the first few chunks to verify.
5.  Discuss why chunking is necessary before embedding. What are the trade-offs between different chunking strategies/sizes?

### Exercise 3: Generating Text Embeddings

**Goal:** Use a pre-trained Sentence Transformer model to convert text chunks into dense vector embeddings.
**Instructions:**

1.  Install the `sentence-transformers` library (`pip install sentence-transformers`).
2.  Load a pre-trained Sentence Transformer model (e.g., `model = SentenceTransformer('all-MiniLM-L6-v2')`).
3.  Use the loaded model's `.encode()` method to generate vector embeddings for each text chunk created in Exercise 2. Store these embeddings (e.g., in a NumPy array or list).
4.  Check the dimensionality of the resulting embeddings.
5.  What properties should these embeddings ideally have (e.g., semantically similar chunks should have vectors close to each other in the embedding space)?

### Exercise 4: Setting Up a Basic Vector Database & Indexing

**Goal:** Store text chunks and their corresponding embeddings in a simple vector database (like ChromaDB or FAISS).
**Instructions:**

  * **Option 1 (ChromaDB - Recommended for simplicity):**
    1.  Install ChromaDB (`pip install chromadb`).
    2.  Import `chromadb` and create a persistent or in-memory client.
    3.  Create a Chroma collection (`client.create_collection(...)`).
    4.  Use the collection's `.add()` method to store the embeddings generated in Exercise 3. Also include the original text chunks as `documents` and unique IDs for each chunk.
  * **Option 2 (FAISS - More low-level):**
    1.  Install FAISS (`pip install faiss-cpu` or `faiss-gpu`).
    2.  Convert your list/array of embeddings (from Exercise 3) into a NumPy array of type `float32`.
    3.  Create a FAISS index (e.g., `faiss.IndexFlatL2(dimension)` where `dimension` is your embedding dimension).
    4.  Add the embeddings to the index using `.add()`. Keep a separate mapping from the index position back to your original text chunk.



5.  Verify that the data has been added (e.g., using Chroma's `.count()` or checking the FAISS index's `ntotal`).

### Exercise 5: Performing Similarity Search (Retrieval)

**Goal:** Embed a user query and retrieve the most relevant text chunks from the vector database.
**Instructions:**

1.  Define a sample user query relevant to the content of your documents (e.g., "What is the main topic of document X?").
2.  Use the same Sentence Transformer model (from Exercise 3) to generate an embedding for the user query.
3.  Perform a similarity search using your vector database:
      * **ChromaDB:** Use the collection's `.query()` method, passing the query embedding and specifying the number of results (`n_results`, e.g., 3).
      * **FAISS:** Use the index's `.search()` method, passing the query embedding (as a NumPy array) and the number of results (`k`). This returns distances and indices. Use the indices to look up the original text chunks from your mapping.
4.  Examine the retrieved text chunks. Are they relevant to the user query?

### Exercise 6: Generating an Answer with LLM and Context

**Goal:** Combine the user query and retrieved context into a prompt for an LLM to generate a final answer.
**Instructions:**

1.  Take the user query (from Exercise 5) and the top `k` relevant text chunks retrieved from the vector database.
2.  Construct a prompt for your chosen LLM (API or local). The prompt should clearly instruct the LLM to answer the user's query *based only on the provided context*. Example structure:
    ```
    Context information is below.
    ---------------------
    [Retrieved Chunk 1 Text]
    ---------------------
    [Retrieved Chunk 2 Text]
    ---------------------
    [Retrieved Chunk 3 Text]
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: [User Query]
    Answer:
    ```
3.  Send this combined prompt to the LLM.
4.  Analyze the generated answer. Does it accurately reflect the information in the retrieved context? Does it avoid hallucinating information not present in the context? Compare this to asking the LLM the original query *without* the retrieved context.

### Project: Simple Document Q\&A System

**Goal:** Build and package a basic RAG pipeline that can answer questions about a specific document.
**Instructions:**

1.  Choose a single document (e.g., a relevant paper abstract, a short blog post, product documentation).
2.  Create a Python script that encapsulates the RAG pipeline:
      * Function to load and chunk the document.
      * Function to initialize the embedding model.
      * Function to create/load a vector database (ChromaDB recommended for simplicity) and index the chunks.
      * Function that takes a user query, embeds it, retrieves relevant chunks from the DB, constructs the LLM prompt with context, calls the LLM (via API or local model interface), and returns the final answer.
3.  Add basic command-line interaction (e.g., using `input()`) to allow a user to ask questions.
    **Portfolio Guidance:**



  * Structure your code clearly (e.g., separate functions for indexing, retrieval, generation).
  * Include a `requirements.txt` file.
  * Create a `README.md` explaining:
      * The purpose of the RAG system.
      * The document(s) it uses.
      * The embedding model, vector DB, and LLM used.
      * How to set up (install requirements, potentially download models/API keys).
      * How to run the script and ask questions.
      * Limitations of the simple system.
  * Upload the code, README, and potentially the source document(s) to a GitHub repository.
