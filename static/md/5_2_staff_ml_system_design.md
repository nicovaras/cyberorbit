
## Subtopic 5.2: Staff-Level ML System Design Case Studies

**Goal:** To practice designing complex, large-scale, end-to-end machine learning systems, integrating various components (data pipelines, MLOps, models, infra), considering trade-offs, and addressing Staff-level concerns like scalability, reliability, maintainability, and business impact.

**Resources:**

  * System Design Interview Guides:
      * "System Design Interview – An Insider's Guide" (Vol 1 & 2) by Alex Xu
      * "Designing Data-Intensive Applications" by Martin Kleppmann (Deeper technical foundations)
      * Educative.io: "Grokking the Machine Learning Interview", "Grokking the System Design Interview"
  * Platform Engineering Blogs:
      * [Netflix Tech Blog](https://netflixtechblog.com/)
      * [Meta AI Blog](https://ai.meta.com/blog/)
      * [Google AI Blog](https://ai.googleblog.com/)
      * Uber / Airbnb / LinkedIn / Spotify Engineering Blogs
  * MLOps Resources: (From Module 2, e.g., MLOps monitoring, pipelines)
  * Model Architecture Resources: (From Module 3, understanding different model types)
  * Experimentation Resources: (From Module 4, how to embed experimentation)

-----

### Exercise 1: Design a Large-Scale Recommendation System (e.g., Netflix/YouTube)

**Goal:** Outline the end-to-end design for a personalized recommendation system serving millions of users.
**Instructions:**

1.  **Clarify Requirements:** Define functional requirements (e.g., show personalized recommendations on homepage, similar items on item page) and non-functional requirements (high availability, low latency recommendations, handle large item/user base, update recommendations frequently, allow experimentation).
2.  **High-Level Design:** Draw a component diagram. Include: Data ingestion (user interactions, item metadata), Feature Store, Candidate Generation (multiple sources like collaborative filtering, content-based, popularity), Ranking Model (ML model predicting relevance/watch time/click-through), A/B Testing Framework, Serving Layer (API, Caching), Monitoring.
3.  **Data & Features:** Discuss types of data needed. How would features be generated and stored (Feature Store)? Consider real-time vs. batch features.
4.  **Candidate Generation:** Describe 2-3 different methods for generating initial candidate recommendations (e.g., user/item embeddings from matrix factorization/deep learning, content-based filtering, business rules). Why use multiple sources?
5.  **Ranking:** Describe the purpose of the ranking model. What kind of model might be used (e.g., Gradient Boosted Trees, Deep Neural Network)? What features would it use? What would it optimize for (e.g., click probability, watch time)?
6.  **MLOps & Operations:** How would models be trained, evaluated, deployed? How would the system be monitored? How would you incorporate A/B testing for new algorithms or features? Discuss cold-start problem.
7.  **Scale & Availability:** Discuss key considerations for scaling (e.g., partitioning data, distributed training/serving, caching strategies, database choices).

### Exercise 2: Design a Search Ranking System (e.g., E-commerce/Web Search)

**Goal:** Outline the design for a system that takes a user query and returns a ranked list of relevant documents/products.
**Instructions:**

1.  **Clarify Requirements:** Functional (accept query, return ranked results, maybe filtering/faceting) and Non-functional (low latency, high relevance, handle large index, index updates, scalability, experimentation).
2.  **High-Level Design:** Diagram components: Query Parser/Preprocessor, Indexing Pipeline (Crawling/Ingestion, Document Processing, Indexing), Retrieval/Candidate Generation, Feature Engineering, Ranking Model (Learning-to-Rank), Serving Layer, A/B Testing, Monitoring.
3.  **Indexing:** Describe the process of creating an inverted index. What information is stored? How are updates handled?
4.  **Retrieval/Candidate Generation:** How does the system quickly retrieve a set of potentially relevant documents for a given query from the massive index? (e.g., using the inverted index, term matching).
5.  **Feature Engineering:** What kinds of features might be used by the ranking model? Categorize them (e.g., Query Features, Document Features, Query-Document Interaction Features like TF-IDF/BM25, User Features if personalized).
6.  **Ranking (Learning-to-Rank - LTR):** Explain the purpose of the LTR model. Describe one common LTR approach (Pointwise, Pairwise, or Listwise) conceptually. What metrics would you use to evaluate ranking quality offline (e.g., NDCG, MAP)?
7.  **MLOps & Experimentation:** How would the LTR model be trained (using click logs/human judgments)? How would new ranking models or features be A/B tested online? How would query performance and system health be monitored?

### Exercise 3: Design an Ad Targeting & Serving Platform

**Goal:** Outline the design for a system that selects and serves relevant ads to users based on their profile and context.
**Instructions:**

1.  **Clarify Requirements:** Functional (receive ad request with user/context info, select relevant ad, return ad creative, track impressions/clicks) and Non-functional (very low latency response, high throughput, accurate targeting, scalability, budget pacing for advertisers, experimentation).
2.  **High-Level Design:** Diagram components: Ad Request Handler, User Profile Store, Targeting Service (Candidate Ad Selection), Prediction Service (e.g., pCTR, pCVR models), Ranking & Auction Logic, Ad Creative Store, Budget Management/Pacing, Data Collection/Logging, Reporting, ML Model Training Pipeline, Monitoring & Alerting.
3.  **User Profiling:** How would user profiles (demographics, interests, behavior) be built and stored? Consider data sources and privacy.
4.  **Targeting & Candidate Selection:** How are potentially relevant ads selected based on the ad request context and advertiser campaign settings (e.g., keyword matching, audience segment matching)?
5.  **Prediction Models (pCTR/pCVR):** What do these models predict? What kind of ML models are commonly used? What features are important? How critical is prediction latency?
6.  **Auction & Ranking:** Explain a common ad auction mechanism (e.g., Generalized Second Price - GSP). How are bids and predicted quality scores (e.g., pCTR) often combined to rank ads (e.g., Ad Rank = Bid \* Quality Score)?
7.  **MLOps & Scale:** Discuss challenges in training/updating prediction models frequently. How would the system handle billions of requests per day (low latency, high availability)? How would new prediction models or targeting strategies be tested?

### Exercise 4: Design a System for Deploying a GenAI Application (e.g., RAG Chatbot)

**Goal:** Outline the design for deploying and managing a Generative AI application, specifically focusing on a Retrieval-Augmented Generation (RAG) system.
**Instructions:**

1.  **Clarify Requirements:** Functional (accept user query, retrieve relevant context, generate response based on query and context, potentially handle conversation history) and Non-functional (reasonable response latency, control over hallucination, ability to update knowledge base, scalability, monitorability, cost-effectiveness).
2.  **High-Level Design:** Diagram components: User Interface/API Gateway, Query Preprocessor, Embedding Service (for query), Vector Database (for knowledge base), Context Retriever, Prompt Construction Service, LLM Generation Service (API call or self-hosted), Response Postprocessor, Logging/Monitoring Service, Indexing Pipeline (for knowledge base updates).
3.  **Indexing Pipeline:** Describe the offline process for creating/updating the Vector DB: Document loading, chunking, embedding generation (using which model?), storing chunks/embeddings/metadata. How often does this need to run?
4.  **Retrieval Step:** Discuss choices for the embedding model (trade-offs: performance vs. size/latency). Discuss choices for the Vector DB (scalability, filtering capabilities). How many chunks (`k`) to retrieve? Strategies for relevance scoring?
5.  **Generation Step:** Discuss choices for the LLM (API vs. self-hosted; model size vs. cost/latency/quality). How is the prompt constructed using the query and retrieved context? Techniques to reduce hallucination (e.g., strong prompting instructions, grounding).
6.  **MLOps & Monitoring:** How would you evaluate the quality of the RAG system (retrieval metrics, generation metrics, human eval)? How would you monitor for issues like irrelevant context retrieval or poor LLM responses? How would you update the knowledge base or the LLM? Discuss latency bottlenecks.

### Portfolio/Practice Guidance: Documenting System Designs

**Goal:** Structure detailed system design walkthroughs for personal review and potential interview discussion.
**Instructions:**

1.  For each system design case study practiced:
      * Create a dedicated document (e.g., using Excalidraw/Miro for diagrams, Google Docs/Markdown for text).
      * Follow a structured approach (e.g., the framework from 1.7, expanded): Requirements -\> Estimation -\> Data Model -\> High-Level Design -\> API Design -\> Component Deep Dive -\> Scalability -\> MLOps/Maintenance -\> Trade-offs/Future.
      * Include clear diagrams for the high-level architecture and potentially key data flows.
      * Explicitly list functional and non-functional requirements considered.
      * Detail the core components, their responsibilities, and interactions.
      * Discuss key design choices and trade-offs made (e.g., database choice, caching strategy, model selection, build vs. buy).
      * Address scalability, reliability, and monitoring aspects specifically.
2.  Maintain these design documents in an organized manner (e.g., a folder in Google Drive, a private GitHub repository). Reviewing these detailed walkthroughs is crucial preparation.


