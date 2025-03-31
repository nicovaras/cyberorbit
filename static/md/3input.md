## 📄 PDF: Topic 3 – Input Vulnerabilities

**📚 Resource:**  
*OWASP Testing Guide – Input Validation & Injection Sections*  
[https://owasp.org/www-project-web-security-testing-guide/](https://owasp.org/www-project-web-security-testing-guide/)

---

### 🔹 Exercise: Reflected XSS in a Search Parameter  
**Goal:** Discover if input is reflected back and can trigger code execution.  
**Instructions:**  
- Open the provided lab in PortSwigger’s Web Security Academy.  
- Use the search field to inject unexpected input.  
- Try to get the browser to behave strangely or display unexpected text.  
- If successful, craft input that causes JavaScript to execute.

**Lab:** [Reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-easy-reflected-xss)

---

### 🔹 Exercise: Stored XSS in a Comment System  
**Goal:** Insert persistent, harmful input into a web app.  
**Instructions:**  
- Launch the TryHackMe XSS room.  
- Look for a comment form or input that is displayed back to users.  
- Submit test inputs and reload the page to observe behavior.  
- Identify input that behaves differently on reload.

**Room:** [TryHackMe XSS](https://tryhackme.com/room/xss)

---

### 🔹 Exercise: Bypass a Login Using SQL Injection  
**Goal:** Trick the backend into bypassing authentication controls.  
**Instructions:**  
- In TryHackMe's SQL Injection room, find a login form.  
- Submit test inputs in the username and password fields.  
- Observe error messages and patterns in server response.  
- Construct inputs that modify the SQL query’s logic.

**Room:** [TryHackMe SQLi](https://tryhackme.com/room/sqlinjectionlm)

---

### 🔹 Exercise: Build Regex to Validate Safe Usernames  
**Goal:** Design a pattern that only allows clean, expected input.  
**Instructions:**  
- Write a regular expression that only allows:
  - lowercase letters  
  - numbers  
  - length between 3 and 15 characters  
- Test your pattern against:
  - Valid: `admin`, `guest123`  
  - Invalid: empty, symbols, HTML tags, long strings

---

### 🕹️ CTF: OWASP XSS & SQLi Practice  
**Goal:** Solve real-world injection vulnerabilities in a gamified environment.  
**Instructions:**  
- Complete the **XSS** and **SQL Injection** challenges in the OWASP Top 10 TryHackMe room.  
- Capture flags where required.  
- Write a personal log of what techniques worked and what didn’t.

**Room:** [TryHackMe – OWASP Top 10](https://tryhackme.com/room/owasptop10)
