## 📄 PDF: Topic 3 – Subtopic: Client-Side Security  
**Resource:** [OWASP – Client-Side Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

---

### 🔹 **Exercise: Exploit Vulnerable Client-Side JavaScript Validation**  
**Goal:** Trick a form by modifying JavaScript-enforced validation logic.  

**Instructions:**  
- Clone or create a simple HTML form that checks for input length or email format in JavaScript.  
- Open it in your browser, then disable or modify the validation logic via DevTools console.  
- Submit invalid inputs and see if the server accepts them.  
- Try sending the same payload via curl or Burp — any difference?

---

### 🔹 **Exercise: Bypass Client-Side Rate Limiting**  
**Goal:** Perform rapid form submissions despite frontend-imposed limits.  

**Instructions:**  
- Use a local form that prevents repeated submissions using JavaScript (`setTimeout`, button disabling, etc).  
- Submit once, then bypass the cooldown using DevTools or direct HTTP requests.  
- Try automating requests with a script or Postman runner.  
- How many successful submissions can you make in a short time?

---

### 🔹 **Exercise: Harden a Site Against Common Client-Side Bypasses**  
**Goal:** Implement real protections that don’t rely on the client.  

**Instructions:**  
- Take one of the previous forms and move the validation logic to the backend.  
- Ensure the server returns proper error codes for bad inputs.  
- Use DevTools to submit invalid data again — is it rejected now?  
- Bonus: add server-side rate limiting or CAPTCHA.

---

### 🕹️ **CTF: TryHackMe – JavaScript Exploitation Room**  
**Instructions:**  
- Go to [JavaScript Exploitation Room](https://tryhackme.com/room/javascriptmasquerade).  
- Complete the tasks involving DOM manipulation, token extraction, and bypassing logic.  
- Try solving one of the challenges *without* looking at the source code first.
