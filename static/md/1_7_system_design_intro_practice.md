## Subtopic 1.7: Practice: System Design Interview Scenarios (Intro)

**Goal:** To practice applying fundamental system design concepts (from 1.4, 1.5) and develop a structured approach for tackling introductory system design interview questions.

**Resources:**

  * Frameworks/Guides:
      * [System Design Primer: Framework Section](https://www.google.com/search?q=https://github.com/donnemartin/system-design-primer%23system-design-interview-tips)
      * [Educative.io: Grokking the System Design Interview (Course Preview or Full)](https://www.educative.io/courses/grokking-the-system-design-interview)
      * HiredInTech System Design Overview: [Part 1](http://www.hiredintech.com/system-design/the-system-design-process/), [Part 2](https://www.google.com/search?q=http://www.hiredintech.com/system-design/basics/)
  * Example Walkthroughs:
      * YouTube Channels (e.g., Gaurav Sen, Success in Tech, Exponent) covering basic designs like URL Shortener, Twitter Feed.
      * Books: "System Design Interview – An Insider's Guide" by Alex Xu (Volume 1 covers many classics).

-----

### Exercise 1: Develop a System Design Approach Framework

**Goal:** Outline a personal step-by-step framework for approaching system design interview questions.
**Instructions:**

1.  Based on the resources (like System Design Primer framework), define a sequence of steps you would take when presented with a system design question. Example steps might include:
      * Clarify Requirements (Functional & Non-Functional - Scale, Availability, Latency etc.)
      * Make High-Level Estimates (QPS, Storage, Bandwidth)
      * Define Data Model
      * High-Level Design (Core components and connections)
      * Deep Dive into Specific Components (APIs, DB choice, Caching strategy etc.)
      * Identify Bottlenecks & Scale Further
      * Discuss Trade-offs & Future Considerations
2.  Write down this framework clearly. Keep it concise (maybe 5-8 key steps).
3.  For each step, list 1-2 key questions you should ask the interviewer or consider yourself.

### Exercise 2: Requirements Gathering & Estimation Practice (URL Shortener)

**Goal:** Practice the initial steps (requirements, estimation) for a classic system design problem.
**Instructions:**

1.  Consider the "Design a URL Shortener" problem (like TinyURL).
2.  **Functional Requirements:** List the core functions the service must provide (e.g., shorten URL, redirect short URL to original URL). List any optional functions (e.g., custom aliases, analytics).
3.  **Non-Functional Requirements:** Assume scale (e.g., 100 million new URLs per month, 1 billion reads per month). Estimate required QPS (Queries Per Second) for writes and reads. Estimate storage needed for URLs over 5 years. State assumptions about availability and latency.
4.  **Data Model:** Propose a simple data model. What information needs to be stored for each short URL? What database type (SQL/NoSQL Key-Value) seems appropriate initially and why?

### Exercise 3: High-Level Design Practice (URL Shortener)

**Goal:** Practice drawing a high-level component diagram and identifying core APIs.
**Instructions:**

1.  Continuing with the URL Shortener:
2.  Draw a high-level block diagram showing the main components involved (e.g., User Client, Web Server/API Service, Database, potentially a Caching layer, Load Balancer). Show the basic flow for writing (shortening) and reading (redirecting).
3.  Define the basic API endpoints needed. For example:
      * `POST /api/v1/shorten` (Request body: `{"original_url": "..."}`, Response body: `{"short_url": "..."}`)
      * `GET /{short_code}` (Response: HTTP 301/302 Redirect to original URL)
4.  Briefly explain the role of each component in your diagram.

### Exercise 4: Component Deep Dive & Trade-offs (URL Shortener - Hashing)

**Goal:** Practice discussing implementation details and trade-offs for a specific component.
**Instructions:**

1.  Focus on the mechanism for generating the `short_code` in the URL Shortener.
2.  Describe at least two different approaches to generating a unique short code (e.g., hashing the original URL + collision handling, using a base-62 conversion of a distributed counter/sequence generator).
3.  Discuss the pros and cons of each approach regarding:
      * Uniqueness guarantee
      * Length of the short code
      * Potential for collisions / performance implications
      * Complexity of implementation in a distributed environment.
4.  Which approach seems more suitable given the scale estimated earlier? Justify your choice.

### Exercise 5: Walkthrough Practice (Basic Twitter Feed)

**Goal:** Apply the developed framework (from Exercise 1) to outline a design for another common problem.
**Instructions:**

1.  Consider the "Design a simplified Twitter-like feed" problem. Focus on posting tweets and viewing a user's home timeline (tweets from people they follow).
2.  Apply your framework from Exercise 1 step-by-step:
      * Briefly outline functional/non-functional requirements (assume reasonable scale).
      * Make basic estimates (e.g., tweets per second, reads per second for timelines).
      * Propose a basic data model (e.g., User table, Follows table, Tweets table).
      * Sketch a high-level design (API service, DBs).
      * Discuss the core challenge: Generating the home timeline efficiently (e.g., fan-out on write vs. fan-out on read). Briefly explain the trade-offs.
      * Mention potential optimizations (e.g., caching timelines).
3.  Keep the discussion high-level, focusing on applying the framework and identifying key challenges/components.
