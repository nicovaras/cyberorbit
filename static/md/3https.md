## 🕸️ Subtopic 3.1: HTTP/S Protocol Deep Dive

**Goal:** Understand the foundational protocol of the web, HTTP, including its request/response structure, methods, headers, status codes, cookies for state management, and the role of HTTPS in securing communication.

**Resources:**

* **MDN HTTP Documentation:** [HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview), [HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers), [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
* **Cookies:** [MDN HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
* **HTTPS Explained:** [Cloudflare Learning Center](https://www.cloudflare.com/learning/ssl/what-is-https/)
* **Tools:** `curl` (command line), `telnet` / `nc` (netcat), Wireshark, Browser Developer Tools (Network Tab)

---

### 🔹 **Exercise 1: Crafting Raw HTTP**

**Goal:** Gain a fundamental understanding of the HTTP request format by sending one manually.

**Instructions:**

1.  Open a terminal or command prompt.
2.  Use `telnet` or `nc` to connect to a simple, known HTTP server on port 80. Example: `telnet info.cern.ch 80` or `nc info.cern.ch 80`.
3.  Once connected, carefully type the following lines exactly, pressing Enter after each line, including the final blank line:
    ```
    GET /hypertext/WWW/TheProject.html HTTP/1.0
    Host: info.cern.ch

    ```
4.  Observe the raw HTTP response sent back by the server, including the status line, headers, and the HTML body.
5.  **Challenge:** Close the connection. Connect again and try sending a `HEAD` request instead of `GET`. What is the difference in the server's response? Why is `HEAD` useful?

---

### 🔹 **Exercise 2: Header Investigation**

**Goal:** Analyze common HTTP request and response headers captured from live traffic to understand their purpose.

**Instructions:**

1.  Open your browser's Developer Tools (usually F12) and go to the "Network" tab. Enable "Persist Logs" if available.
2.  Browse to a few different websites (e.g., a news site, a simple blog, `google.com`).
3.  Select one of the main HTML document requests (usually the first request listed for the page).
4.  Examine the "Headers" section in DevTools. Identify and research the purpose of these common headers:
    * **Request Headers:** `Host`, `User-Agent`, `Accept`, `Accept-Language`, `Cookie` (if present).
    * **Response Headers:** `Content-Type`, `Content-Length`, `Server`, `Date`, `Set-Cookie` (if present), `Location` (if it was a redirect).
5.  Write down a brief explanation for each header identified.
6.  **Challenge:** Find a request that uses a method other than `GET` (e.g., a `POST` request when submitting a form or logging in). What different request headers might be present (like `Content-Type` describing the request body)?

---

### 🔹 **Exercise 3: Decoding Status Codes**

**Goal:** Learn to interpret HTTP status codes to understand the outcome of a request.

**Instructions:**

1.  Use the `curl` command-line tool with the `-I` flag (which sends a HEAD request and shows only response headers) or use the Browser DevTools Network tab.
2.  Get the response headers/status code for the following types of URLs:
    * A valid page on a website (e.g., `curl -I https://github.com`). Expected: 2xx code.
    * A page that redirects (e.g., `curl -I http://google.com` - often redirects to `https://www.google.com`). Expected: 3xx code. Identify the `Location` header.
    * A page that does not exist on a valid domain (e.g., `curl -I https://github.com/thispagedoesnotexist`). Expected: 404 code.
    * An endpoint requiring authentication (if you know one, or conceptual). Expected: 401 or 403 code.
3.  List the status codes received for each case and briefly explain what each code signifies about the request's success or failure.
4.  **Challenge:** Research the difference between a `301 Moved Permanently` and a `302 Found` redirect. When might each be used?

---

### 🔹 **Exercise 4: Cookie Security Attributes**

**Goal:** Inspect browser cookies and understand the security implications of attributes like `HttpOnly`, `Secure`, and `SameSite`.

**Instructions:**

1.  Log in to a website that uses session cookies (e.g., `https://tryhackme.com`, your webmail, etc.).
2.  Open Browser DevTools and navigate to the Application (Chrome) or Storage (Firefox) tab. Find the Cookies section for the site you logged into.
3.  Locate the session cookie(s) (often named `sessionid`, `JSESSIONID`, `PHPSESSID`, etc.).
4.  Examine the attributes set for the session cookie:
    * Is the `HttpOnly` flag checked/set? What does this prevent?
    * Is the `Secure` flag checked/set? What does this enforce?
    * What is the `SameSite` attribute set to (`Strict`, `Lax`, `None`)? What cross-site request behavior does this control?
    * Look at the `Expires/Max-Age` attribute. Is it a session cookie (expires when browser closes) or persistent?
5.  Discuss the security benefits provided by enabling `HttpOnly`, `Secure`, and setting an appropriate `SameSite` policy (`Lax` or `Strict` recommended).
6.  **Challenge:** Can you find any cookies on the site *without* the `HttpOnly` flag set? If so, try accessing `document.cookie` in the DevTools Console tab. Can you see the cookie value? Now try accessing the session cookie value (if it *did* have `HttpOnly` set). What happens?

---

### 🔹 **(Optional) Exercise 5: Observing the HTTPS Handshake**

**Goal:** Use Wireshark to visualize the high-level steps involved in establishing a secure TLS/SSL connection.

**Instructions:**

1.  Start a Wireshark capture on your main network interface.
2.  In the capture filter bar, type `tls.handshake` and press Enter. This will only show TLS handshake messages.
3.  Open your web browser and navigate to any `https://` website (e.g., `https://google.com`).
4.  Observe the packets captured in Wireshark. You should see a sequence like:
    * `Client Hello`
    * `Server Hello`
    * `Certificate`, `Server Key Exchange` (optional), `Server Hello Done` (often in one packet)
    * `Client Key Exchange`, `Change Cipher Spec`, `Encrypted Handshake Message`
    * `Change Cipher Spec`, `Encrypted Handshake Message` (from server)
5.  Select the `Certificate` packet from the server. Expand the TLS record details in the packet details pane. Can you find information about the website's certificate (e.g., Common Name, Issuer)?
6.  **Challenge:** Without delving deep into the cryptographic details, explain the *purpose* of the Client Hello and Server Hello messages in negotiating the TLS session parameters (like cipher suites).

---