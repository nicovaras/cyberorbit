
## 📄 PDF: Topic 3 – Subtopic: HTTP Mechanics  
**📚 Resource:**  
- *“Web Security for Developers” – Chapters 2 & 3*  
- [MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

---

### 🔹 **Exercise: Write a Script to Mimic a Browser (but Not Quite)**  
**Goal:** Send HTTP requests manually and spot what’s missing.  

**Instructions:**  
- Build a Python script using `http.client` or `socket`.  
- Send a request to a live HTTP endpoint (not HTTPS).  
- Save and inspect the raw response (headers + body).  
- Compare with what a browser sends—what’s different?

---

### 🔹 **Exercise: Build a CLI Login Tool Using `requests`**  
**Goal:** Simulate a form login and extract session cookies.  

**Instructions:**  
- Choose a site with a basic login form (like `reqres.in` or `testphp.vulnweb.com`).  
- Manually inspect the request in Burp.  
- Reproduce the POST request in Python.  
- Store and print the session cookie after login.  
- Bonus: use the cookie to access a protected page.

---

### 🔹 **Exercise: Poison the Headers**  
**Goal:** Trick the server using altered headers.  

**Instructions:**  
- Use `curl` or `requests` to send requests with weird headers:  
  - Empty `User-Agent`, fake `Referer`, multiple `Host` headers, long `X-Forwarded-For` chains  
- Send to your local Flask or Node.js test server.  
- Log what the server receives — which headers win?  
- Bonus: build a script to test a list of header anomalies in one go.

---

### 🔹 **Exercise: Intercept and Replay Login Requests with Burp Suite**  
**Goal:** Capture and replay a login flow, then automate it.  

**Instructions:**  
- Use Burp Suite to intercept a login form submission.  
- Modify one field (username or password) and resend — what changes?  
- Export the raw request and automate it using Python + `requests`.  
- Save a flag or response snippet to file after successful login.

---

### 🕹️ **Lab: PortSwigger – HTTP Request Smuggling & Parsing**  
**Goal:** Test how servers handle malformed or weirdly structured HTTP requests.  

**Instructions:**  
- Go to [PortSwigger HTTP Labs](https://portswigger.net/web-security/http)  
- Complete two labs:  
  - HTTP Request Smuggling  
  - HTTP Request Parsing  
- Record your payloads and write a short markdown note on how the server got confused.