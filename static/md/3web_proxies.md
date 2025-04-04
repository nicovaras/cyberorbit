## 🕸️ Subtopic 3.3: Introduction to Web Proxies (Burp Suite / OWASP ZAP)

**Goal:** Set up and utilize an intercepting proxy (like Burp Suite Community Edition or OWASP ZAP) to inspect, intercept, and manipulate HTTP/S traffic for web application security testing.

**Resources:**

* **Burp Suite Community:** [Download](https://portswigger.net/burp/communitydownload) & [Documentation](https://portswigger.net/burp/documentation)
* **OWASP ZAP:** [Download](https://www.zaproxy.org/download/) & [Documentation](https://www.zaproxy.org/documentation/)
* **Browser Proxy Configuration:** Tools like [FoxyProxy Standard](https://getfoxyproxy.org/) (browser extension) simplify switching.
* **Installing Proxy CA Certificate:** Search docs for "Installing Burp CA Certificate" or "Installing ZAP Root CA Certificate" for your browser/OS.
* **Test Target:** OWASP Juice Shop (run locally), `http://testphp.vulnweb.com/`, `http://zero.webappsecurity.com/` or PortSwigger Academy labs.

---

### 🔹 **Exercise 1: Setup and Traffic Inspection**

**Goal:** Configure your browser and system to route traffic through Burp Suite or ZAP and observe the captured HTTP/S requests and responses.

**Instructions:**

1.  Install Burp Suite Community Edition or OWASP ZAP.
2.  Launch the proxy tool. Find its listening address and port (usually `127.0.0.1:8080`).
3.  Configure your browser to use this address/port as its HTTP and HTTPS proxy. Using an extension like FoxyProxy is recommended for easy switching.
4.  Install the proxy's Root CA certificate into your browser's or OS's certificate trust store (follow proxy documentation). This is crucial for intercepting HTTPS traffic without constant browser warnings. Verify installation by Browse to an HTTPS site – you should *not* get certificate errors if done correctly.
5.  Turn *off* interception in the proxy for now (Proxy > Intercept / Breakpoint icon).
6.  Browse several websites (HTTP and HTTPS).
7.  Go to the proxy's "HTTP History" (Burp) or "History" (ZAP) tab. Observe the log of requests and responses. Select individual entries to view the raw request/response details.
8.  **Challenge:** Use the History filter options (filter by host, status code, search term) to find specific types of requests you made (e.g., find all requests to a specific domain, find all POST requests).

---

### 🔹 **Exercise 2: Intercepting and Modifying Live Traffic**

**Goal:** Practice intercepting specific HTTP requests before they reach the server, modifying them, and observing the impact on the response.

**Instructions:**

1.  Ensure your proxy and browser are configured correctly.
2.  Enable interception in the proxy (Proxy > Intercept is ON / Set Breakpoint).
3.  In your browser, navigate to a page with a simple form (e.g., a search function on `http://testphp.vulnweb.com/search.php`, a login form).
4.  Enter some data into the form and click Submit.
5.  The request should be caught in the proxy's Intercept tab. Examine the raw request.
6.  Modify a parameter value in the intercepted request (e.g., change the search query, change a quantity, modify a hidden field value if present).
7.  Forward the modified request to the server (click "Forward").
8.  Forward any subsequent requests until the page loads in the browser. Observe the response received from the server in the browser or the proxy's History. Did your modification change the outcome (e.g., different search results, an error message)?
9.  Turn interception off.
10. **Challenge:** Configure the proxy's interception options (Intercept Client Requests / Breakpoint settings) to only intercept requests matching specific criteria (e.g., only intercept requests to a specific host, only intercept requests with parameters).

---

### 🔹 **Exercise 3: Replaying and Tampering with Repeater**

**Goal:** Use the Repeater (Burp) or Manual Request Editor (ZAP) tool to efficiently modify and resend individual requests multiple times to probe for vulnerabilities.

**Instructions:**

1.  Proxy traffic while Browse a target application (e.g., OWASP Juice Shop, testphp.vulnweb.com).
2.  Find an interesting request in the HTTP History (e.g., a request retrieving user data, submitting a form, or containing an ID parameter like `product.php?id=1`).
3.  Right-click the request and choose "Send to Repeater" (Burp) or "Open/Resend with Request Editor" (ZAP).
4.  Go to the Repeater/Request Editor tab. Click "Send" ("Go" in Burp) to issue the original request and view the response.
5.  Modify different parts of the request in the editor pane:
    * Change a parameter value in the URL (e.g., `id=1` to `id=2`, `id='`).
    * Add/modify/delete HTTP headers.
    * Change the request method (e.g., GET to POST).
    * Modify data in the request body (if present).
6.  Resend the request after each modification and carefully observe the corresponding response (status code, headers, body content, rendering). Look for errors, unexpected data exposure, or changes in application behavior.
7.  **Challenge:** Use Repeater to test for a basic reflected XSS. Find a request where a parameter value is reflected in the response (e.g., a search query). In Repeater, change the parameter value to `<b>test</b>`, send, check the raw response HTML. If bold tag appears, try `<script>alert(1)</script>`, send, check response. Does the script tag appear correctly?

---

### 🔹 **Exercise 4: Mapping the Application Structure**

**Goal:** Utilize the proxy's passive site mapping capabilities to understand the structure, endpoints, and technologies of a target web application.

**Instructions:**

1.  Ensure your proxy is running and configured in the browser (interception can be off).
2.  Choose a target application (e.g., OWASP Juice Shop, `http://zero.webappsecurity.com/`).
3.  Systematically browse through all the different sections and functionalities of the application. Click links, submit forms, interact with features.
4.  Go to the "Target" > "Site map" tab (Burp) or the "Sites" tab (ZAP).
5.  Observe the tree structure representing the application's directories, files, API endpoints, and parameters discovered passively through your Browse traffic.
6.  Expand different branches of the tree. Select specific endpoints. Examine the associated requests and responses logged in the lower panels.
7.  Look for comments, interesting filenames, or inferred technologies based on file extensions or server headers.
8.  **Challenge:** In Burp Target Scope or ZAP Context settings, define your target application's domain(s) as "in scope". How does this help filter the Site map and History to focus only on relevant traffic? Explore options for active scanning or spidering (use with caution on test targets only).

---

### 🔹 **(Optional) Exercise 5: Basic Fuzzing with Intruder/Fuzzer**

**Goal:** Get introduced to automated request modification using Burp Intruder or ZAP Fuzzer to test parameters for unexpected behavior or vulnerabilities.

**Instructions:**

1.  Find a request in your History that includes a numerical or string parameter you want to test (e.g., `product.php?id=1`, `search.php?query=test`).
2.  Send this request to Intruder (Burp) or Fuzzer (ZAP).
3.  **Configure Positions:** In the Intruder/Fuzzer tab, go to the "Positions" (Burp) or highlight the parameter value in the request editor (ZAP will often auto-detect). Ensure only the value of the parameter you want to fuzz is marked as a payload position/fuzz location. Clear any other automatic selections if necessary.
4.  **Configure Payloads:** Go to the "Payloads" tab.
    * **Burp:** Select Payload type "Numbers" and configure a simple sequential range (e.g., from 1 to 50, step 1).
    * **ZAP:** Click "Add..." for Payloads, choose Type "Numberzz" or "File Fuzz" (if using a simple wordlist file), and configure the range or file.
5.  **Start Attack:** Launch the Intruder attack / Start Fuzzer.
6.  Observe the results table as requests are sent. Pay attention to columns like Status Code, Response Length, and any error indicators. Look for responses that are different from the baseline or indicate errors (e.g., 500 errors, unusually large/small responses).
7.  **Challenge:** Try a different payload type, such as a simple list of common test strings (e.g., `'`, `"`, `<script>`, `../`, `OR 1=1`) using the "Simple list" (Burp) or "String" / "File Fuzz" (ZAP) payload type. Analyze the results for signs of injection vulnerabilities (errors, changes in content).

---