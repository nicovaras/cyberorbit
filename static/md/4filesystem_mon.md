## 📄 PDF: Topic 4 – Filesystem Monitoring

**📚 Resource:**  
*Linux Hardening in Hostile Networks – Chapter 4: Monitoring Critical Files*  
[Preview: https://nostarch.com/linuxhardening]*

---

### 🔹 Exercise: Monitor File Access with `inotifywait`  
**Goal:** Catch access to sensitive files in real-time.  
**Instructions:**  
- Use `inotifywait` to watch `/etc/passwd`, `.bashrc`, or any target file.  
- Trigger the event by viewing or modifying the file.  
- Log the exact timestamp and the type of event (read, modify, delete).  
- Your task: figure out a way to catch **multiple events** in sequence—without missing any.

---

### 🔹 Exercise: Write a File Change Logger in Python  
**Goal:** Create a Python-based mini file-watcher.  
**Instructions:**  
- Use `watchdog` or `inotify` bindings in Python.  
- Monitor a directory like `~/monitored/` and log all events to a file.  
- Handle at least 3 types of events (created, modified, deleted).  
- Bonus: Detect when a file is renamed into the folder.

---

### 🔹 Exercise: Compare File Hashes to Detect Tampering  
**Goal:** Build a tamper-evidence system.  
**Instructions:**  
- Write a script that stores SHA256 hashes of key files.  
- Run it again later to compare current hashes with stored ones.  
- Flag any differences.  
- Don't store the hashes in plain sight—think about where and how to store them securely.

---

### 🔹 Exercise: Schedule Integrity Checks with Cron  
**Goal:** Automate checks to run while you're sleeping.  
**Instructions:**  
- Schedule your hash-checker or file-watcher to run every 6 hours using `cron`.  
- Make it log to a file with a timestamp in the filename.  
- Optional: create a simple shell wrapper that emails you the result.

---

### ✨ Bonus: Track USB Insertion Events (udevadm + Logging)  
**Goal:** Detect physical tampering.  
**Instructions:**  
- Use `udevadm monitor` or watch `/var/log/syslog` to catch USB insert/remove events.  
- Log the USB device’s vendor ID and product ID.  
- Extra challenge: Identify the device type and mount point automatically.