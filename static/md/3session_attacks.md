## 📄 PDF: Topic 3 – Subtopic: Session Attacks & Cookies  
**Resource:** [Flask Security – Sessions & Cookies](https://flask.palletsprojects.com/en/2.2.x/security/)

---

### 🔹 **Exercise: Capture and Reuse Cookies for Session Hijacking**  
**Goal:** Gain access to another user’s session using stolen cookies.  

**Instructions:**  
- Run a local vulnerable Flask app with login functionality.  
- Log in with User A, then capture their session cookie using Burp Suite.  
- Log out and log in as User B.  
- Replace B’s session cookie in the browser with A’s.  
- Reload — are you now logged in as A again?

---

### 🔹 **Exercise: Forge Cookies to Escalate Privileges**  
**Goal:** Alter client-side cookie values to gain unauthorized access.  

**Instructions:**  
- Use a Flask app that stores session data client-side (e.g., `username=guest; role=user`).  
- Capture the cookie and try changing `role=user` to `role=admin`.  
- Reload the page and check for access changes.  
- What protections would block this?

---

### 🔹 **Exercise: Implement Secure Session Cookies in Flask**  
**Goal:** Harden session cookies using Flask’s built-in options.  

**Instructions:**  
- In your Flask app, enable `SESSION_COOKIE_HTTPONLY`, `SECURE`, and `SAMESITE`.  
- Verify these flags are active using browser dev tools or Burp.  
- Try to access the cookie from JavaScript — is it blocked?

---

### ✨ **Bonus: Build a Python Tool to Detect Weak Session Management**  
**Goal:** Scan a live site (or local app) for insecure cookie practices.  

**Instructions:**  
- Use `requests` or `selenium` to fetch pages and read cookies.  
- Check for missing flags: `HttpOnly`, `Secure`, `SameSite`.  
- Alert if values are too permissive or cookies are modifiable.  
- Test against your own app and tighten it based on the report.

