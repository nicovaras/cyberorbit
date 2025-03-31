
## 📄 PDF: Topic 4 – Subtopic: Audit and Alerts  
**📚 Resource:**  
*DigitalOcean Guide – [How to Use Auditd to Monitor File Access](https://www.digitalocean.com/community/tutorials/how-to-use-auditd-to-monitor-file-access-on-ubuntu-20-04)*

---

### 🔹 **Exercise: Something Touched the Shadows**  
**Goal:** Detect unusual reads or changes to critical system files.  

**Instructions:**  
- Use `auditctl` to monitor access to `/etc/shadow`.  
- Perform a normal operation that touches this file (e.g., change a user password).  
- Look in `/var/log/audit/audit.log` and figure out what happened.  
- Who did it? What process was responsible?  
- Write one sentence describing the event.

---

### 🔹 **Exercise: Trap the Rogue Admin**  
**Goal:** Set up a tripwire that tells you when someone adds a new user.  

**Instructions:**  
- Configure audit rules to monitor changes to `/etc/passwd` and `/etc/group`.  
- Simulate an attack by adding a user manually.  
- Review the logs and trace the action from command → system file → audit entry.  
- Can you identify the exact user and tool used?

---

### 🔹 **Exercise: Who Just Logged In From… Where?**  
**Goal:** Track SSH login sources and raise an alert when something new appears.  

**Instructions:**  
- Write a Python or Bash script that watches `auth.log` for successful logins.  
- Maintain a local file with “known” IPs.  
- If a new one appears, log it and display an alert on screen.  
- Run the script, log in from another machine (or use a second terminal to simulate).  
- Did it trigger?

---

### 🔹 **Exercise: Monitor for Unexpected Changes in System Binaries**  
**Goal:** Watch a system directory for tampering or replacement of binaries.  

**Instructions:**  
- Use `auditctl` to monitor a file like `/bin/ls` or `/usr/bin/sudo`.  
- Trigger an event by copying or modifying the file (safely, in a VM).  
- Review what shows up in `audit.log`.  
- Who or what caused the change, and how fast did you catch it?

---

### 🔖 **Project: The Alert Engine**  
**Goal:** Build a simple alerting engine that correlates multiple events.  

**Instructions:**  
- Write a script that checks:  
  - Login attempts from new IPs  
  - Creation of new users  
  - File access to `/etc/shadow` or `/etc/passwd`  
- Each alert should include: timestamp, source, and action  
- Store alerts in a log file and print a daily summary  
- Bonus: include severity levels or categories
