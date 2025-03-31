## 📄 PDF: Topic 3 – Fix & Defend

**📚 Resource:**  
*“Secure Python Web Development” – Chapters 2 & 4*  
or  
[Flask Security Docs](https://flask.palletsprojects.com/en/latest/security/)

---

### 🔹 Exercise: Use Flask’s `request.args` Safely  
**Goal:** Avoid code that trusts user input blindly.  
**Instructions:**  
- Create a small Flask app with a `/search?q=` route  
- Access `request.args.get("q")`, but ensure it’s filtered/sanitized  
- Return: “Searching for: {sanitized input}”

---

### 🔹 Exercise: Add Content Security Policy Headers  
**Goal:** Block unsafe content execution.  
**Instructions:**  
- Use Flask-Talisman to add a strict CSP header:  
  ```python
  Talisman(app, content_security_policy={
      'default-src': "'self'"
  })
  ```  
- Try loading a script from another domain and confirm it's blocked

---

### 🔹 Exercise: Block Dangerous Input with Whitelist Filtering  
**Goal:** Only allow what’s explicitly permitted.  
**Instructions:**  
- Write a function `is_valid_username()` that checks:
  - length between 3–15  
  - only letters and numbers  
- Test with payloads like `<img src=x onerror=alert(1)>`

---

### 🔖 Project: Break & Fix Flask App  
**Goal:** Exploit and fix a real vulnerable app.  
**Instructions:**  
- Clone: [https://github.com/shiftsecure/vuln-flask-app](https://github.com/shiftsecure/vuln-flask-app)  
- Find at least 2 bugs (XSS, missing headers, bad validation)  
- Patch them and write what you changed in a `FIXES.md`  
- Optional: document reproduction steps for each bug

---

### ✨ Bonus: Deploy a Secure Flask App on AWS Lightsail  
**Goal:** Put it online and configure real-world protections.  
**Instructions:**  
- Launch a Lightsail instance (Ubuntu)  
- Install Flask, gunicorn, nginx  
- Deploy your fixed app and add a firewall rule to block all ports except 22, 80, 443  
- Optional: set up HTTPS with Let’s Encrypt
