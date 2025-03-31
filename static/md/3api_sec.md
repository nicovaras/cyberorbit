## 📄 PDF: Topic 3 – Subtopic: API Security  
**Resource:** [API Security Top 10 (OWASP)](https://owasp.org/API-Security/)

---

### 🔹 **Exercise: Find and Exploit a Basic API Authentication Flaw (JWT Manipulation)**  
**Goal:** Bypass API authentication by manipulating a weakly protected JSON Web Token.  

**Instructions:**  
- Use [JWT.io](https://jwt.io) to explore how JWTs work.  
- Generate a sample JWT using HS256 and a known key (`"secret"`).  
- Modify the payload (e.g., change `"role": "user"` to `"role": "admin"`) and re-sign it.  
- Use Postman or curl to send this tampered token to an API that validates it.  
- Test whether the server accepts your modified token.

---

### 🔹 **Exercise: Intercept and Replay API Calls with Postman and Burp**  
**Goal:** Capture API traffic and simulate repeated or modified requests.  

**Instructions:**  
- Use any public API (e.g., `https://reqres.in/`) or a small self-hosted Flask API.  
- Set Postman to capture the request history.  
- Configure Burp Suite as a proxy and route Postman through it.  
- Intercept a login or GET request.  
- Replay it with modified headers or parameters — what changes?

---

### 🔹 **Exercise: Enumerate Hidden API Endpoints with Burp Suite Intruder**  
**Goal:** Use fuzzing to find undocumented endpoints.  

**Instructions:**  
- Use a testable API (your own or a sandbox like `https://fakerapi.it/`).  
- Load the base URL (e.g., `/api/v1/`) into Burp Intruder.  
- Add a wordlist (e.g., common endpoint names like `admin`, `debug`, `logs`).  
- Scan for valid responses — are any unexpected endpoints accessible?  
- Log and analyze the status codes and response sizes.

---

### 🕹️ **Lab: PortSwigger – API Security Labs**  
**Instructions:**  
- Go to [PortSwigger’s API Labs](https://portswigger.net/web-security/api)  
- Complete the “Exploiting insecure JWT validation” and “Fuzzing for endpoints” challenges.  
- Note which protections fail and how you exploited them.

---