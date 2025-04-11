## Subtopic 2.4: Real-time Data Streaming: Kafka Concepts & Use Cases

**Goal:** To understand the fundamental concepts, architecture, and common use cases of Apache Kafka as a distributed streaming platform, including topics, partitions, producers, consumers, brokers, and basic delivery guarantees.

**Resources:**

  * Apache Kafka Official Documentation: [Introduction to Kafka](https://kafka.apache.org/intro)
  * Kafka Core Concepts: [Kafka Documentation - Concepts](https://www.google.com/search?q=https://kafka.apache.org/documentation/%23intro_concepts) (Topics, Partitions, Producers, Consumers, Brokers, Zookeeper/KRaft)
  * Delivery Semantics Explained: [Blog post or article explaining At-Least Once, At-Most Once, Exactly-Once Semantics](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/) (Conceptual understanding)
  * Use Cases: [Kafka Use Cases Overview](https://kafka.apache.org/uses)

-----

### Exercise 1: Define Core Kafka Components

**Goal:** Articulate the roles of the fundamental components in a Kafka cluster.
**Instructions:**

1.  Define **Broker**. What is its main responsibility in a Kafka cluster?
2.  Define **Topic**. How is data organized within Kafka?
3.  Define **Partition**. Why are topics divided into partitions? What benefit does partitioning provide (e.g., parallelism, scalability)?
4.  Define **Producer**. What is its role?
5.  Define **Consumer** and **Consumer Group**. How do consumer groups enable parallel consumption?
6.  Define **Offset**. What does it represent for a consumer within a partition?
7.  Explain the role of Zookeeper (in older versions) or KRaft (in newer versions) in managing the Kafka cluster.

### Exercise 2: Understand Topic Partitions and Offsets

**Goal:** Explain how data is written to and read from topic partitions and the significance of offsets.
**Instructions:**

1.  Explain how a producer decides which partition to write a message to if a key is provided versus if no key is provided.
2.  Describe the ordering guarantee Kafka provides *within* a single partition. Is there an ordering guarantee *across* different partitions of the same topic?
3.  Explain how Kafka uses offsets to track a consumer group's progress in reading from a partition.
4.  What happens if a consumer in a group crashes and restarts? How does it know where to resume reading from? Where is this offset information typically stored?

### Exercise 3: Compare Delivery Semantics (Conceptual)

**Goal:** Understand the different message delivery guarantees Kafka can be configured for.
**Instructions:**

1.  Describe **At-Most-Once** delivery semantics. In what scenarios might this be acceptable? What could cause message loss?
2.  Describe **At-Least-Once** delivery semantics. What does this guarantee? What is the potential side effect (Hint: duplicates)? How might producers/consumers typically achieve this?
3.  Describe **Exactly-Once** delivery semantics (EOS). Why is this the most challenging to achieve? Briefly mention the techniques Kafka uses to enable EOS (e.g., idempotent producers, transactions).

### Exercise 4: Identify Kafka Use Cases

**Goal:** Recognize common patterns and applications where Kafka is frequently used.
**Instructions:**

1.  Describe how Kafka can be used for **Real-time Website Activity Tracking** (e.g., page views, clicks). What kind of data would producers send? What might consumers do with this data?
2.  Explain how Kafka acts as a **Messaging System** for decoupling microservices. Provide a simple example scenario.
3.  Describe how Kafka can be used for **Log Aggregation**. How does it compare to traditional log file handling?
4.  Explain how Kafka fits into **Stream Processing** architectures. What role does it play alongside stream processing frameworks like Spark Streaming, Flink, or Kafka Streams?
5.  How could Kafka be used in an **MLOps context** (e.g., streaming features for real-time inference, logging prediction results, triggering model retraining)?

### Exercise 5: Producer/Consumer Logic Outline (Pseudo-code)

**Goal:** Outline the basic logic involved in writing simple Kafka producer and consumer applications.
**Instructions:**

1.  Write pseudo-code (or Python comments) outlining the essential steps for a **Kafka Producer** application:
      * Import necessary Kafka library.
      * Configure producer properties (e.g., bootstrap servers).
      * Create a producer instance.
      * Define the topic to write to.
      * Create a message (ProducerRecord) potentially with a key and value.
      * Send the message (asynchronously, potentially with a callback).
      * Flush/close the producer.
2.  Write pseudo-code (or Python comments) outlining the essential steps for a **Kafka Consumer** application belonging to a consumer group:
      * Import necessary Kafka library.
      * Configure consumer properties (e.g., bootstrap servers, group ID, auto-offset-reset policy).
      * Create a consumer instance.
      * Subscribe the consumer to one or more topics.
      * Start a polling loop (`consumer.poll()`).
      * Process the received records within the loop.
      * Handle consumer closing/shutdown gracefully.
