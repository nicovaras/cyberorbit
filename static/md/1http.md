## 🐍 Subtopic 1.4: HTTP Interactions with 'requests'

**Goal:** Leverage the `requests` library for more advanced HTTP interactions common in security testing and automation, such as handling sessions, authentication, and different request types. Builds upon the basic usage in Subtopic 1.1.

**Resources:**

* **Python `requests` library:** [Official Documentation](https://requests.readthedocs.io/en/latest/) (Explore Sessions, Authentication, Error Handling sections)
* **Test Target:** `httpbin.org` (Provides endpoints for various HTTP methods and authentication)
* **Optional Test Target:** [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) (Run locally via Docker - for session/login testing if desired, requires more setup) or [Web Security Academy](https://portswigger.net/web-security) (Some labs might be suitable)

---

### 🔹 **Exercise 1: Exploring HTTP Methods**

**Goal:** Use `requests` to send different types of HTTP requests and understand their purpose by observing the responses.

**Instructions:**

1.  Ensure you have `requests` installed in your virtual environment.
2.  Write a script that uses `requests` to:
    * Send a `GET` request to `https://httpbin.org/get` and print the response JSON.
    * Send a `POST` request to `https://httpbin.org/post` with some simple `data={'key': 'value'}` and print the response JSON (notice your data reflected).
    * Send a `PUT` request to `https://httpbin.org/put` with data and print the response.
    * Send a `DELETE` request to `https://httpbin.org/delete` and print the response.
3.  Inspect the `args`, `form`, `data`, and `json` fields in the responses from `httpbin.org` to see how your data was received.
4.  **Challenge:** Add custom headers (e.g., `User-Agent`, `X-Custom-Header`) to your requests and verify they are reflected in the `headers` section of the `httpbin.org` response.

---

### 🔹 **Exercise 2: Handling Sessions with Cookies**

**Goal:** Use a `requests.Session` object to maintain context (like cookies) across multiple HTTP requests, simulating a logged-in user.

**Instructions:**

1.  Write a script that uses a `requests.Session()` object.
2.  First, send a `GET` request using the session to `https://httpbin.org/cookies/set?mycookie=secretvalue`. This endpoint will set a cookie.
3.  Next, using the *same* session object, send another `GET` request to `https://httpbin.org/cookies`.
4.  Print the JSON response from the second request. Verify that `mycookie` sent by the server in the first request was automatically sent back by your session object in the second request.
5.  **Challenge (Requires external setup or vulnerable VM):** If you have OWASP Juice Shop or similar running, adapt this script to:
    * POST login credentials to the login endpoint using the session.
    * Verify successful login (e.g., check response, look for session cookies).
    * Use the same session to access a page/API endpoint that requires authentication.

---

### 🔹 **Exercise 3: Basic Authentication**

**Goal:** Use `requests` to authenticate to a resource protected by HTTP Basic Authentication.

**Instructions:**

1.  Write a script using `requests`.
2.  `httpbin.org` provides a basic auth endpoint: `https://httpbin.org/basic-auth/{user}/{password}`. Choose a simple user/password (e.g., `testuser`/`testpass`).
3.  Attempt to send a `GET` request to this URL *without* providing credentials. Print the status code (should be 401 Unauthorized).
4.  Now, send the `GET` request again, but this time provide the correct credentials using the `auth` parameter in `requests.get()` (e.g., `auth=('testuser', 'testpass')`).
5.  Print the status code (should now be 200) and the response JSON (which indicates authenticated status).
6.  **Challenge:** Inspect the `Authorization` header sent by `requests` when using the `auth` parameter. Manually construct this header (Base64 encoded `user:password`) and send the request using the `headers` parameter instead of `auth`.

---

### 🔹 **Exercise 4: Robust Error Handling**

**Goal:** Write `requests` code that anticipates and gracefully handles common network and HTTP errors.

**Instructions:**

1.  Write a script that attempts to make `GET` requests to the following types of URLs:
    * A non-existent domain (e.g., `http://thisshouldnotexist12345.com`)
    * A valid domain but a resource that returns a 404 Not Found error (e.g., `https://httpbin.org/status/404`)
    * A URL that might time out (e.g., `https://httpbin.org/delay/10` - delays 10 seconds).
2.  Use `try...except` blocks to catch specific `requests.exceptions` like `ConnectionError`, `Timeout`, `HTTPError`.
3.  For timeouts, use the `timeout` parameter in your `requests.get()` call (e.g., `timeout=3`).
4.  For HTTP errors (like 404), check the `response.status_code` or use `response.raise_for_status()` within a try-except block.
5.  Print informative messages indicating the type of error encountered for each case.
6.  **Challenge:** Create a reusable function `make_request(url)` that encapsulates the request logic and robust error handling, returning the response object on success or `None` on failure, printing appropriate error messages internally.

---

### 💡 **Project: Simple Website Link Crawler**

**Goal:** Build a basic web crawler that starts at a given URL and finds all unique links belonging to the same domain, using `requests` for fetching pages and a basic HTML parser.

**Instructions:**

1.  **Setup:** Install the `BeautifulSoup4` library (`pip install beautifulsoup4`) for HTML parsing, alongside `requests`.
2.  Write a script that takes a starting URL (e.g., `http://quotes.toscrape.com/` - designed for scraping) as input.
3.  Use `requests` to fetch the HTML content of the starting URL. Handle potential errors.
4.  Use `BeautifulSoup` to parse the HTML content.
5.  Find all anchor tags (`<a>`) within the parsed HTML.
6.  Extract the `href` attribute (the link) from each anchor tag.
7.  Filter these links: keep only those that start with `/` (relative links) or that start with the same domain base as the starting URL (e.g., `http://quotes.toscrape.com/...`). Convert relative links to absolute links.
8.  Store all unique, valid links found in a set to avoid duplicates.
9.  Print the set of unique internal links found on the starting page.
10. **Challenge / Extension (Optional):** Turn this into a recursive crawler. Maintain a set of visited URLs. Use a queue or list for URLs to visit. Start with the initial URL. While the queue is not empty, dequeue a URL, fetch it (if not already visited), parse it, add new valid internal links back to the queue and the master set, and mark the current URL as visited. Limit the crawl depth or number of pages to prevent infinite loops or excessive requests.
11. **Portfolio Guidance:** Document your crawler on GitHub. Explain its function, how to install dependencies (`requirements.txt`), and how to run it. Discuss limitations (e.g., doesn't handle JavaScript-rendered links, doesn't respect `robots.txt` properly yet).