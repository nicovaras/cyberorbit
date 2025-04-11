## 🔬 Subtopic 7.1: Logging Strategy & Key Data Sources

**Goal:** Identify critical log sources across different operating systems and applications, understand common log formats, and define basic logging requirements for security monitoring. *(While strategic, exercises focus on practical identification and configuration)*.

**Resources:**

* **Default Log Locations:** Research common paths (`/var/log/` on Linux, Event Viewer channels on Windows).
* **Log Format Examples:** Syslog (RFC 5424), Apache Combined Log Format, Nginx default format, JSON logs.
* **Compliance Frameworks (Examples):** PCI-DSS Requirement 10 (Logging), NIST SP 800-92 (Log Management Guide) - Use for requirement analysis.
* **Tools:** Text editors, log viewing tools (`less`, `tail`, Event Viewer), basic web server (Apache/Nginx).

**Test Environment / Tools Needed:**

* Access to both a Linux VM (e.g., Ubuntu Server, CentOS) and a Windows VM (e.g., Windows Server eval, Windows 10/11 Pro/Enterprise).
* (Optional) A basic web server like Apache or Nginx installed on the Linux VM.
* Access to the internet for research.

---

### 🔹 **Exercise 1: Exploring Native OS Logs**

**Goal:** Locate and examine default operating system logs to identify key security-relevant events and understand native formats.

**Instructions:**

1.  **Linux:**
    * Navigate the `/var/log` directory. Identify key log files like `syslog` (or `journalctl` output), `auth.log` (or `secure`), `kern.log`, `messages`.
    * Use `tail`, `less`, or `journalctl` to view the contents of `auth.log`/`secure`. Find examples of successful logins, failed logins, and `sudo` command usage. Note the typical timestamp format and fields included.
    * Use `journalctl -u sshd` (or similar service name) to view logs specific to the SSH service.
2.  **Windows:**
    * Open Event Viewer (`eventvwr.msc`). Navigate to `Windows Logs` > `Security`.
    * Filter the Security log for Event ID `4624` (Successful Logon) and `4625` (Failed Logon). Examine the details pane for a few events. Note the Logon Type, Account Name, Source IP Address, etc.
    * Navigate to `Windows Logs` > `System`. Look for service start/stop events or error messages.
3.  Document the key log files/channels you examined and 2-3 examples of security-relevant event types found in each OS.
4.  **Challenge:** How does the structure/format of Linux syslog/journald logs typically differ from Windows Event Log entries (e.g., text lines vs. structured XML/binary)?

---

### 🔹 **Exercise 2: Configuring Application Logging (Web Server)**

**Goal:** Modify the logging configuration of a standard application (web server) to include additional useful fields or change the output format.

**Instructions:**

1.  **Setup:** If you don't have one, install Apache (`httpd`) or Nginx on your Linux VM. Ensure it's running and accessible (e.g., `curl localhost`).
2.  **Apache:**
    * Locate the Apache configuration file defining the access log format (e.g., within `/etc/apache2/apache2.conf` or related files, look for `LogFormat`).
    * Define a **new** custom `LogFormat` directive that includes additional fields beyond the "combined" format, such as the time taken to serve the request (`%D`) and the User-Agent (`%User-Agent`). Give your format a nickname (e.g., `detailed`).
    * Modify the `CustomLog` directive for your virtual host to use your new `detailed` format.
3.  **Nginx:**
    * Locate the Nginx configuration file (`nginx.conf`) and find the `log_format` directive.
    * Define a **new** `log_format` (e.g., named `detailed`) including additional variables like request processing time (`$request_time`) and user agent (`$http_user_agent`).
    * Modify the `access_log` directive in your server block to use the `detailed` format.
4.  Restart the web server service.
5.  Generate some web traffic by accessing the server from a browser or `curl`.
6.  Examine the web server's access log file. Verify that the new fields are present in the log entries.
7.  **Challenge:** Configure the web server to log in JSON format instead of the traditional space-delimited format. Why is JSON often preferred for log processing by downstream tools?

---

### 🔹 **Exercise 3: Mapping Compliance Requirements to Logs**

**Goal:** Analyze logging requirements from a compliance standard and identify corresponding log sources and event types on a system.

**Instructions:**

1.  Research the core logging requirements outlined in PCI-DSS Requirement 10 ("Track and monitor all access to network resources and cardholder data"). Focus on requirements like 10.2.x (e.g., logging user identification, actions, success/failure, changes to accounts).
2.  For each specific requirement identified (e.g., "10.2.2 - All actions taken by any individual with administrative privileges"):
    * Identify which **log source(s)** on Linux (e.g., `auth.log`, `auditd`, `sudo logs`) and Windows (e.g., Security Event Log, PowerShell logs) would likely contain this information.
    * Identify specific **event types or event IDs** within those logs that correspond to the requirement (e.g., `sudo` command execution logs, Windows Event ID 4720 'User Account Created', Event ID 4688 'Process Creation').
3.  Create a simple mapping table showing the PCI-DSS sub-requirement, the relevant OS log source(s), and example event types/IDs.
4.  **Challenge:** Consider requirement 10.2.7 ("Audit log history is retained for at least one year, with a minimum of three months immediately available for analysis"). How would you technically *implement* this retention requirement using standard Linux/Windows logging tools or log rotation configurations (`logrotate`, Event Log settings)?

---

### 🔹 **Exercise 4: Basic Logging Plan**

**Goal:** Develop a concise logging plan for a simple, hypothetical system.

**Instructions:**

1.  **Scenario:** You are setting up a single Linux server acting as a public-facing web server (Nginx/Apache) and also running an internal SSH service for administration.
2.  Create a brief logging plan document (e.g., in Markdown) covering:
    * **Key Log Sources:** List the essential sources to monitor (OS system logs, OS security/auth logs, SSH service logs, Web server access logs, Web server error logs, host firewall logs - if configured).
    * **Critical Event Types:** For each source, list 2-3 critical event types you'd want to ensure are captured (e.g., Auth: failed/successful logins, sudo use; Web: Errors (4xx/5xx), access from specific IPs; SSH: failed/successful logins).
    * **Log Format Preference:** Specify a preferred format for easier parsing (e.g., JSON for web logs, standard syslog).
    * **Retention Goal:** Define a basic retention period (e.g., 30 days local, 1 year archived).
    * **(Optional) Centralization Goal:** Mention the intent to forward logs to a central system (covered in next subtopics).
3.  Keep the plan concise and focused on actionable items for this simple scenario.
4.  **Challenge:** Add a section to your plan considering "What *not* to log" or how to handle excessive logging volume from a specific source (e.g., firewall allow rules).

---