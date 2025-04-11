## Subtopic 1.5: API Design & Core Scalability Patterns

**Goal:** To understand principles of good API design (focusing on REST), common patterns for scaling systems like CDNs and database scaling strategies, and the implications of the CAP theorem.

**Resources:**

  * REST API Design Principles: [Microsoft API Design Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design), [Google Cloud API Design Guide](https://cloud.google.com/apis/design/) (Focus on core principles)
  * Rate Limiting Explained: [Cloudflare Learning - Rate Limiting](https://www.google.com/search?q=https://www.cloudflare.com/learning/ddos/glossary/rate-limiting/)
  * Content Delivery Networks (CDNs): [Cloudflare Learning - What is a CDN?](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)
  * Database Scaling Patterns: [DigitalOcean - Database Replication Explained](https://www.google.com/search?q=https://www.digitalocean.com/community/tutorials/understanding-database-replication-synchronous-asynchronous), [MongoDB - Sharding Introduction](https://www.google.com/search?q=https://www.mongodb.com/sharding) (Conceptual)
  * CAP Theorem Explained: [IBM - What is CAP Theorem?](https://www.ibm.com/topics/cap-theorem), [Visual Guide to CAP Theorem](https://mwhittaker.github.io/blog/an_illustrated_proof_of_the_cap_theorem/)

-----

### Exercise 1: Principles of RESTful API Design

**Goal:** Identify and explain key principles of designing RESTful APIs.
**Instructions:**

1.  Define **Resource** in the context of REST. How are resources typically identified? (Hint: URIs)
2.  Explain the use of standard **HTTP Methods** (GET, POST, PUT, DELETE, PATCH) in RESTful APIs. Provide an example use case for each.
3.  Explain the concept of **Statelessness** in REST. Why is it important for scalability?
4.  Describe the purpose of using standard **HTTP Status Codes** (e.g., 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error).
5.  Discuss the importance of **Versioning** in API design. Describe one common versioning strategy (e.g., URI path, header, query parameter).

### Exercise 2: Understanding Rate Limiting

**Goal:** Explain the purpose of rate limiting and common implementation algorithms.
**Instructions:**

1.  Describe the primary reasons for implementing rate limiting on an API.
2.  Explain at least two common rate limiting algorithms (e.g., Token Bucket, Leaky Bucket, Fixed Window Counter, Sliding Window Log). Briefly describe how they work.
3.  Where can rate limiting be implemented in a typical web architecture? (e.g., API Gateway, Load Balancer, Application Code)
4.  What HTTP status code is typically returned when a user exceeds their rate limit?

### Exercise 3: Role of Content Delivery Networks (CDNs)

**Goal:** Explain how CDNs work and their benefits for web performance and availability.
**Instructions:**

1.  Describe the primary function of a Content Delivery Network (CDN).
2.  Explain how a CDN typically improves website **latency** for users geographically distributed from the origin server.
3.  Explain how a CDN can improve website **availability** and reduce load on the origin server.
4.  What types of content are most suitable for delivery via a CDN? (e.g., static assets like images, CSS, JavaScript vs. dynamic content)

### Exercise 4: Database Scaling Patterns (Replication & Sharding)

**Goal:** Understand and compare common strategies for scaling databases.
**Instructions:**

1.  Explain **Database Replication**. What is the difference between a Primary (Master/Leader) replica and Secondary (Slave/Follower) replicas?
2.  Describe how replication typically helps with **read scalability**. How might it help with availability?
3.  Explain **Database Sharding** (Partitioning). How does it differ from replication?
4.  Describe how sharding typically helps with **write scalability** and managing very large datasets.
5.  What are some common challenges associated with implementing sharding? (e.g., shard key selection, cross-shard queries, rebalancing).

### Exercise 5: Applying the CAP Theorem

**Goal:** Explain the CAP theorem and its implications for distributed system design.
**Instructions:**

1.  Define the three properties of the CAP theorem: **Consistency**, **Availability**, and **Partition Tolerance**.
2.  Explain what the CAP theorem states about these three properties in a distributed system experiencing a network partition.
3.  Why is **Partition Tolerance** generally considered non-negotiable for most distributed systems?
4.  Given that P must usually be chosen, describe the trade-off a system designer typically faces between **Consistency (C)** and **Availability (A)** during a network partition.
5.  Provide an example of a system that might prioritize CP (Consistency over Availability during partition) and another that might prioritize AP (Availability over Consistency during partition). Justify your choices.
