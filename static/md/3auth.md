## 🕸️ Subtopic 3.6: Authentication & Session Management Flaws

**Goal:** Identify and understand common vulnerabilities related to user authentication (login mechanisms, password policies) and session management (how user sessions are tracked after login). *(Cert relevance: CompTIA Sec+, eJPT, OSCP)*

**Resources:**

* **OWASP Top 10:** [A07:2021-Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/), [A01:2021-Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) (Session issues can lead to access control bypass)
* **OWASP Cheat Sheets:** [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html), [Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
* **PortSwigger Academy:** [Authentication Labs](https://portswigger.net/web-security/authentication), [Session Management Labs](https://portswigger.net/web-security/sessions)
* **Tools:** Burp Suite / OWASP ZAP, Browser DevTools.
* **Test Environment:** OWASP Juice Shop, DVWA, PortSwigger Academy Labs, `http://zero.webappsecurity.com/`.

---

### 🔹 **Exercise 1: Analyzing Login Error Messages (Username Enumeration)**

**Goal:** Determine if a login function reveals whether a username is valid or invalid through differing error messages or response behavior.

**Instructions:**

1.  Target the login form of your test application.
2.  Using Burp/ZAP Repeater or just your browser:
    * Attempt to log in with a known **valid** username and an **incorrect** password. Record the exact error message displayed and/or observe the HTTP response details (status code, length, specific content).
    * Attempt to log in with a definitely **invalid** username (e.g., `thisusernamedoesnotexist123`) and any password. Record the exact error message and response details.
3.  Compare the responses from the two attempts.
    * Are the error messages identical ("Invalid username or password")? This is good practice.
    * Are the error messages different (e.g., "Password incorrect" vs. "User not found")? This confirms username enumeration vulnerability.
    * Are there subtle differences in response time or content length? This might indicate timing-based enumeration.
4.  Document your findings regarding whether username enumeration is possible.
5.  **Challenge:** If enumeration is possible, try using Burp Intruder/ZAP Fuzzer with a list of potential usernames against the login endpoint (keeping the password field constant and incorrect). Analyze response lengths or messages to quickly identify potentially valid usernames from the list.

---

### 🔹 **Exercise 2: Testing Password Policies**

**Goal:** Evaluate the strength requirements and lockout mechanisms of an application's password handling.

**Instructions:**

1.  Target the user registration form and/or the password reset/change form of your test application.
2.  **Policy Check:** Attempt to register or change a password using various weak passwords:
    * Very short passwords (e.g., "123", "abc").
    * Common passwords (e.g., "password", "123456").
    * Passwords without required complexity (e.g., all lowercase, no numbers/symbols if required).
    * Does the application enforce length, complexity, and possibly prevent common passwords? Document the policy enforced.
3.  **Lockout Check:** Target the login form. Attempt to log in repeatedly with a valid username but incorrect passwords.
    * Does the application lock the account after a certain number of failed attempts (e.g., 3, 5, 10)?
    * How long does the lockout last (temporary or permanent until admin reset)?
    * Is there any CAPTCHA mechanism to slow down attempts?
    * Document the account lockout behavior (or lack thereof).
4.  **Challenge:** Research password history policies. Does your test application prevent users from immediately reusing their previous passwords after a change/reset?

---

### 🔹 **Exercise 3: Session Cookie Analysis (Security Attributes)**

**Goal:** Revisit session cookies (from 3.1) and analyze their security attributes in the context of session management security.

**Instructions:**

1.  Log into your test web application.
2.  Use Browser DevTools (Application/Storage tab) or Burp/ZAP (inspecting Set-Cookie headers in responses) to find the session cookie(s).
3.  For the primary session cookie, verify the status of these security attributes and explain the protection each offers:
    * `HttpOnly`: Prevents access via client-side script (mitigates basic XSS cookie theft). Is it set?
    * `Secure`: Ensures the cookie is only sent over HTTPS connections (prevents eavesdropping over HTTP). Is it set? (Should always be set if the site uses HTTPS).
    * `SameSite` (`Strict`, `Lax`, or `None`): Protects against Cross-Site Request Forgery (CSRF). What is the policy set? Is it appropriate? (`Lax` or `Strict` generally preferred).
4.  **Challenge:** Consider a scenario where the `Secure` flag is *not* set on a session cookie for an HTTPS application. How could an attacker potentially capture this cookie even if the main site uses HTTPS? (Hint: Think about network sniffing and mixed content or insecure redirects).

---

### 🔹 **Exercise 4: Predicting Session Tokens**

**Goal:** Analyze session token values to determine if they are sufficiently random and unpredictable.

**Instructions:**

1.  Log into your test application multiple times (using different browser sessions or private Browse windows) or observe session tokens generated for different users if possible.
2.  Collect several session token values (from cookies or URL parameters).
3.  Examine the collected tokens:
    * Do they appear to be long, random strings (good)?
    * Or are they short, sequential, or based on predictable information like username or timestamp (bad)?
    * Try decoding them (e.g., if they look like Base64 or Hex) to see if they reveal underlying patterns.
4.  Use Burp Sequencer (if available) or statistical analysis tools/observation to assess the randomness/entropy of the tokens. (This is advanced, for basic analysis just look for obvious patterns).
5.  Discuss why predictable session tokens are a major security risk.
6.  **Challenge:** Research common sources of weak session IDs (e.g., using `rand()`, timestamp + username, sequential numbers). How would you test for these specific patterns?

---

### 🧪 **Lab: PortSwigger Academy Authentication/Session Labs**

**Goal:** Practice identifying and exploiting authentication and session management vulnerabilities.

**Instructions:**

* Navigate to the [PortSwigger Web Security Academy Authentication](https://portswigger.net/web-security/authentication) and [Session Management](https://portswigger.net/web-security/sessions) sections.
* Complete the following labs (or similar):
    * Authentication:
        * "Username enumeration via different responses"
        * "Password reset broken logic" (Explore logic flaws)
        * "2FA broken logic" (If available and relevant)
    * Session Management:
        * "Session tokens stored in cookies" (Analysis)
        * "Session token vulnerability" (Find labs focusing on predictable tokens or insecure handling)

---