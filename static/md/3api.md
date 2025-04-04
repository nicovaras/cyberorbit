## 🕸️ Subtopic 3.7: API Security Fundamentals (OWASP API Top 10 Intro)

**Goal:** Introduce the concepts of web APIs (specifically RESTful APIs using JSON), understand how they differ from traditional web applications, and identify common vulnerabilities outlined in the OWASP API Security Top 10 project. *(Cert relevance: eJPT, OSCP)*

**Resources:**

* **OWASP API Security Project:** [Top 10 List (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), [Project Home](https://owasp.org/www-project-api-security/)
* **Introduction to REST APIs:** [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Glossary/REST)
* **PortSwigger Academy:** [API Security Labs](https://portswigger.net/web-security/api-testing)
* **Tools:** Browser DevTools (Network Tab, filtering XHR/Fetch), Burp Suite / OWASP ZAP, Postman / Insomnia (API Clients), `requests` (Python library)

---

### 🔹 **Exercise 1: Identifying API Calls**

**Goal:** Learn to distinguish between standard web page loads and background API calls made by modern web applications.

**Instructions:**

1.  Choose a modern web application known to use APIs extensively (e.g., Twitter/X web client, GitHub interface, Reddit, a Single Page Application demo).
2.  Open Browser DevTools and go to the "Network" tab. Check "Persist Logs" and potentially filter for "Fetch/XHR".
3.  Perform actions within the web application (e.g., load new content/tweets, star a repository, upvote a post, navigate between sections without full page reloads).
4.  Observe the requests appearing in the Network tab. Identify requests that fetch data (often using `GET`) or submit actions (often using `POST`, `PUT`, `DELETE`) without causing a full page navigation. These are likely API calls.
5.  Examine the details for a few identified API calls:
    * Request URL: Does it follow a pattern like `/api/v1/...`?
    * Request Method: What HTTP verb is used?
    * Headers: Look for `Content-Type: application/json` and `Authorization` headers (e.g., Bearer tokens).
    * Response Body: Is the data typically formatted as JSON?
6.  **Challenge:** Compare the structure and headers of an API call (e.g., fetching user data) with a standard request for an HTML page from the same domain. What are the key differences?

---

### 🔹 **Exercise 2: Basic API Interaction (Python `requests`)**

**Goal:** Practice sending requests directly to API endpoints and parsing JSON responses using Python.

**Instructions:**

1.  Choose a *public* API that doesn't require complex authentication for basic `GET` requests (e.g., `https://jsonplaceholder.typicode.com/`, `https://api.github.com/users/google`, `https://catfact.ninja/fact`).
2.  Write a Python script using the `requests` library (Sprint 1).
3.  Make a `GET` request to a specific endpoint provided by the public API (e.g., `https://jsonplaceholder.typicode.com/posts/1`).
4.  Check the response status code for success (e.g., 200).
5.  Parse the JSON response body using `response.json()`.
6.  Print specific data fields from the parsed JSON response (e.g., the `title` and `body` of the post).
7.  **Challenge:** Find a public API that allows `POST` requests (e.g., `jsonplaceholder` allows posting to `/posts`). Consult its documentation and modify your script to send a `POST` request with a valid JSON payload body to create a new resource. Print the response (often includes the created resource with an ID).

---

### 🔹 **Exercise 3: Testing for BOLA (API1:2023)**

**Goal:** Identify Broken Object Level Authorization vulnerabilities where a user can access resources belonging to another user by manipulating object IDs in API requests.

**Instructions:**

1.  Use a test application with API endpoints that reference object IDs in the URL path or parameters (e.g., `/api/v1/users/{userId}/orders/{orderId}`). OWASP Juice Shop or PortSwigger labs are good sources.
2.  **Setup:** You'll likely need two user accounts (User A and User B).
3.  Log in as User A. Use the application normally to access a resource belonging *only* to User A (e.g., view User A's profile via `/api/v1/users/userA_id/profile`). Capture this valid request using Burp/ZAP.
4.  Send the captured request to Repeater/Manual Editor.
5.  Identify the object ID(s) in the URL path or parameters that belong to User A (`userA_id`).
6.  Find out (or guess) the object ID belonging to User B (`userB_id`).
7.  Modify the request in Repeater by replacing `userA_id` with `userB_id`. Ensure you are still using User A's session token/authentication headers.
8.  Send the modified request.
9.  Analyze the response: Did you successfully retrieve/modify data belonging to User B, even though you were authenticated as User A? If yes, you've found a BOLA vulnerability.
10. **Challenge:** Try accessing administrative endpoints or functions by guessing IDs (e.g., trying `/api/v1/users/1/delete` if you are user 123).

---

### 🔹 **Exercise 4: Checking for Excessive Data Exposure (API3:2023)**

**Goal:** Analyze API responses to determine if they return more data than is necessary for the client application's functionality, potentially exposing sensitive information.

**Instructions:**

1.  Use your test application and proxy (Burp/ZAP) to capture API responses. Focus on endpoints that retrieve object details (e.g., user profile, product details, order information).
2.  For several different API `GET` requests, examine the full JSON response body in the proxy or DevTools Network tab.
3.  Compare the data fields present in the JSON response with the data actually displayed or used by the user interface in the browser for that specific feature.
4.  Look for fields in the JSON that are *not* used by the UI but contain potentially sensitive or internal information, such as:
    * Password hashes or security questions/answers.
    * Administrative flags or internal user roles.
    * Personal Identifiable Information (PII) not needed for the current view.
    * Internal IDs or implementation details.
5.  Document any instances where the API appears to be exposing excessive data.
6.  **Challenge:** Consider how an attacker might leverage excessive data exposure. Could combining data leaked from multiple endpoints allow unauthorized access or privilege escalation?

---

### 🧪 **Lab: PortSwigger Academy API Labs**

**Goal:** Practice identifying and exploiting common API vulnerabilities in dedicated lab environments.

**Instructions:**

* Navigate to the [PortSwigger Web Security Academy API Security section](https://portswigger.net/web-security/api-testing).
* Complete labs focusing on the OWASP API Top 10 vulnerabilities introduced in this subtopic:
    * Find and complete labs specifically demonstrating **"Broken Object Level Authorization" (BOLA)**.
    * Find and complete labs demonstrating **"Excessive data exposure"**.
    * (Optional) Explore labs related to **"Broken Authentication"** specifically within an API context (API5:2023 - Broken Function Level Authorization might also be relevant if available).
* Pay attention to how interacting with APIs differs from standard web applications (using tools like Repeater, different content types, authentication methods like Bearer tokens).

---