## Subtopic 1.4: System Design Fundamentals & Building Blocks

**Goal:** To understand and articulate core system design principles (scalability, availability, reliability, latency) and the purpose and basic function of essential building block components (Load Balancers, Caching, Databases, Message Queues).

**Resources:**

  * System Design Primer: [GitHub - donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) (Sections on System Design Topics, Basics)
  * Scalability Explained: [Scalability Article (e.g., Educative.io or similar)](https://www.google.com/search?q=https://www.educative.io/blog/scalability-system-design) (Search for a good primer article)
  * Load Balancers Explained: [AWS Elastic Load Balancing Concepts](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html) (Conceptual understanding)
  * Caching Overview: [DigitalOcean - Caching Explained](https://www.digitalocean.com/community/tutorials/web-caching-basics-terminology-http-headers-and-caching-strategies)
  * SQL vs NoSQL: [MongoDB - SQL vs NoSQL Differences](https://www.google.com/search?q=https://www.mongodb.com/sql-vs-nosql)
  * Message Queues Explained: [CloudAMQP - Message Queuing Explained](https://www.cloudamqp.com/blog/what-is-message-queuing.html)

-----

### Exercise 1: Define Core System Design Principles

**Goal:** Articulate the meaning of key system design non-functional requirements.
**Instructions:**

1.  Define **Scalability** in the context of system design. Explain the difference between **Vertical Scaling** (Scaling Up) and **Horizontal Scaling** (Scaling Out).
2.  Define **Availability**. Explain how it's typically measured (e.g., percentage uptime, "nines").
3.  Define **Reliability**. How does it relate to, yet differ from, Availability?
4.  Define **Latency**. Explain the difference between latency and bandwidth/throughput.
5.  Describe a scenario where you might need to prioritize one of these principles over another (e.g., high availability vs. strong consistency).

### Exercise 2: Role of Load Balancers

**Goal:** Explain the purpose and basic strategies of load balancers.
**Instructions:**

1.  Describe the primary function of a Load Balancer in a distributed system architecture.
2.  Explain at least two common load balancing algorithms (e.g., Round Robin, Least Connections). Briefly describe how they work.
3.  Besides distributing traffic, name one other function a load balancer might perform (e.g., health checks, SSL termination).
4.  Draw a simple diagram showing web servers behind a load balancer receiving user requests.

### Exercise 3: Understanding Caching Layers

**Goal:** Explain the purpose of caching and different caching strategies.
**Instructions:**

1.  Describe the primary benefit of using caching in a system.
2.  Explain where caching can be implemented (e.g., client-side, CDN, server-side application cache, database cache).
3.  Describe at least two common cache eviction policies (e.g., LRU - Least Recently Used, LFU - Least Frequently Used, FIFO - First-In, First-Out). Explain briefly how they decide what to remove from the cache.
4.  Define **Cache Invalidation**. Why is it a challenging problem? Briefly describe one cache invalidation strategy (e.g., write-through, write-back, time-to-live/TTL).

### Exercise 4: SQL vs NoSQL Database Tradeoffs

**Goal:** Compare and contrast relational (SQL) and non-relational (NoSQL) databases based on common characteristics.
**Instructions:**

1.  Describe the typical data model used by SQL databases (e.g., tables, rows, columns, relations).
2.  Describe at least two different data models used by NoSQL databases (e.g., Key-Value, Document, Column-family, Graph).
3.  Compare SQL and NoSQL databases regarding:
      * Schema (Fixed vs. Dynamic/Flexible)
      * Scalability (Typically Vertical vs. Often Horizontal)
      * Consistency (ACID properties vs. BASE properties/Eventual Consistency - briefly explain ACID).
4.  Provide an example use case where a SQL database might be a better fit, and another where a NoSQL database might be preferred.

### Exercise 5: Role of Message Queues

**Goal:** Explain the purpose of message queues and common use cases.
**Instructions:**

1.  Describe the primary function of a Message Queue (MQ) in decoupling system components.
2.  Explain the basic concepts of a **Producer**, a **Consumer**, and a **Queue** in an MQ system.
3.  Describe at least two common use cases for message queues (e.g., background job processing, asynchronous communication between microservices, buffering requests).
4.  Draw a simple diagram illustrating two services communicating asynchronously via a message queue.
