## 🕸️ Subtopic 3.4: Injection Vulnerabilities (SQLi, Command Inj.)

**Goal:** Understand, identify, and perform basic exploitation of critical injection flaws, specifically SQL Injection (SQLi) and OS Command Injection, where user-supplied input is improperly executed by the backend system. *(Cert relevance: CompTIA Sec+, eJPT, OSCP)*

**Resources:**

* **OWASP Top 10:** [A03:2021-Injection](https://owasp.org/Top10/A03_2021-Injection/)
* **PortSwigger Academy:** [SQL Injection Labs](https://portswigger.net/web-security/sql-injection), [Command Injection Labs](https://portswigger.net/web-security/os-command-injection)
* **Cheat Sheets:** [PayloadAllTheThings SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection), [PayloadAllTheThings Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)
* **Tools:** Burp Suite / OWASP ZAP, Browser DevTools.
* **Test Environment:** OWASP Juice Shop, DVWA (Damn Vulnerable Web Application), or PortSwigger Academy Labs. **Do not test on live sites without permission.**

---

### 🔹 **Exercise 1: Detecting Error-Based SQLi**

**Goal:** Learn to provoke database errors by injecting SQL metacharacters into input parameters, indicating potential SQL injection vulnerability.

**Instructions:**

1.  Identify an application feature that likely interacts with a database using user input (e.g., product search, category filter with an ID in the URL like `?category=1`, user profile lookup). Use a suitable test environment.
2.  Using your browser or Burp/ZAP Repeater, systematically inject single SQL metacharacters or simple sequences into the vulnerable parameter value:
    * Append a single quote (`'`). Observe the response.
    * Append a double quote (`"`). Observe the response.
    * Append SQL comment sequences (`-- ` or `#` - note the space after `--`). Observe the response.
    * Append simple logical probes (`' OR 1=1 -- `).
3.  Carefully analyze the server's response after each injection attempt. Look for:
    * Explicit database error messages (e.g., "Syntax error near...", "Unterminated string literal...").
    * Generic error pages (e.g., HTTP 500) that appear *only* when injecting SQL characters.
    * Significant changes in page content or structure compared to valid input.
4.  Document which characters/sequences provoked errors or noticeable changes.
5.  **Challenge:** Explain *why* injecting a single quote often causes a SQL error if the application is vulnerable. Consider how the input might be inserted into a SQL query string.

---

### 🔹 **Exercise 2: Basic Union-Based SQLi Exploitation**

**Goal:** Exploit a SQL injection vulnerability to extract data from other database tables using the `UNION SELECT` technique.

**Instructions:**

1.  Identify a parameter confirmed to be vulnerable to SQLi (from Exercise 1 or a lab) where the query's results are visibly displayed on the page.
2.  **Determine Column Count:** Use the `ORDER BY` clause to find the number of columns being selected by the original query. Inject payloads like `' ORDER BY 1-- `, `' ORDER BY 2-- `, etc., increasing the number until you cause an error (which means you exceeded the column count). The last number that *didn't* error is the correct column count.
3.  **Find Data Types (Optional but helpful):** Determine which columns accept string data by injecting `' UNION SELECT 'a',NULL,NULL-- ` (adjust `NULL` count to match column count). See if the 'a' is displayed. Move 'a' to different positions (`NULL,'a',NULL`...) to find a suitable string column.
4.  **Extract Data:** Construct a `UNION SELECT` payload to retrieve data from the database. Replace one of the `NULL`s (ideally one corresponding to a string column found in step 3) with the data you want to extract.
    * Find the database version: `' UNION SELECT NULL, @@version, NULL-- `
    * Find the database user: `' UNION SELECT NULL, user(), NULL-- `
    * (If database/table/column names are known or guessed) Find data from another table: `' UNION SELECT username, password FROM users LIMIT 1-- ` (adjust columns/NULLs).
5.  Analyze the application's response to see the extracted data displayed on the page.
6.  **Challenge:** Research "information_schema". How can you use `UNION SELECT` queries against `information_schema.tables` and `information_schema.columns` to discover table and column names within the database when they are not known beforehand?

---

### 🔹 **Exercise 3: Detecting OS Command Injection**

**Goal:** Learn to identify potential OS command injection vulnerabilities by injecting command separators and simple OS commands into user input.

**Instructions:**

1.  Identify application features where user input might be passed as an argument to a system command (e.g., tools that ping a host, lookup DNS records, resize images, check file status). Use a test environment.
2.  Inject command separators followed by a benign OS command into the relevant input field or parameter. Try common separators for both Linux and Windows:
    * `; whoami`
    * `| whoami`
    * `&& whoami` (or `&& dir` on Windows)
    * `|| whoami`
    * `` `whoami` `` (backticks)
    * `$(whoami)`
3.  Submit the modified input.
4.  Carefully examine the application's output (both visible content and HTTP response body). Look for:
    * The direct output of your injected command (e.g., your username, directory listing).
    * Error messages indicating a command failed to execute.
    * Noticeable time delays if injecting a command like `sleep 5`.
5.  Document which separators and commands resulted in evidence of execution.
6.  **Challenge:** Try injecting commands into less obvious places, like HTTP headers (`User-Agent`, custom headers) if you suspect they might be processed insecurely by backend scripts. Use Burp/ZAP Repeater for this.

---

### 🔹 **Exercise 4: Blind Command Injection Exploitation (Time-Based)**

**Goal:** Confirm and exploit command injection when the command's output is *not* directly visible in the response, using time delays.

**Instructions:**

1.  Identify a parameter suspected to be vulnerable to command injection, but where you don't see command output (from Exercise 3).
2.  Inject payloads designed to cause a verifiable time delay on the server:
    * Linux: `; sleep 10` or `| sleep 10`
    * Windows: `& ping -n 11 127.0.0.1 > nul` (pings localhost 11 times, approx 10 sec delay) or `& timeout /t 10 /nobreak > nul`
3.  Submit the request using Burp/ZAP Repeater or `curl` and accurately measure the server's response time.
4.  Compare the response time with the time taken for a normal request. If the response takes approximately 10 seconds longer when injecting the sleep/ping command, it confirms blind command injection.
5.  **Challenge:** How could you exfiltrate data (e.g., the output of `whoami` or contents of a file) using only time-based blind command injection? (Hint: Think about conditional execution based on characters in the data and varying sleep times. This is advanced!). Research "time-based blind command injection data exfiltration".

---

### 🧪 **Lab: PortSwigger Academy Injection Labs**

**Goal:** Apply SQLi and Command Injection techniques in pre-built, vulnerable lab environments.

**Instructions:**

* Navigate to the [PortSwigger Web Security Academy](https://portswigger.net/web-security). Create a free account if needed.
* Complete the following labs (or similar ones if these exact ones change):
    * **SQL Injection:**
        * "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data"
        * "SQL injection UNION attack, finding a column containing text"
        * "SQL injection UNION attack, retrieving data from other tables"
    * **Command Injection:**
        * "OS command injection, simple case"
        * "Blind OS command injection with time delays"
* Follow the lab instructions carefully and try to solve them manually using techniques learned in the exercises.

---