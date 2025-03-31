## 📄 PDF: Topic 4 – Process Monitoring & Anomalies

**📚 Resource:**  
*The Linux Command Line – Chapter 32: Processes and Jobs*  
[https://linuxcommand.org/tlcl.php](https://linuxcommand.org/tlcl.php)

---

### 🔹 Exercise: Detect Strange Processes (`nc`, `python`, `curl`)  
**Goal:** Spot tools attackers use.  
**Instructions:**  
- Use Python and `psutil` to list running processes.  
- Alert if any contain `nc`, `nmap`, `curl`, or `bash`.  
- Think about case sensitivity and stealthy renaming—how can you catch those too?

---

### 🔹 Exercise: Correlate Processes with Usernames  
**Goal:** Find out who’s doing what.  
**Instructions:**  
- For each running process, log the user who owns it.  
- Group processes by user.  
- Extra: flag users running unusual tools (like a user running `nmap`)

---

### 🔹 Exercise: Alert on Rare Processes (via Frequency Thresholding)  
**Goal:** Define “normal” and catch what’s not.  
**Instructions:**  
- Run a process scanner every hour and save a count of seen process names.  
- After 5 runs, flag anything seen fewer than 2 times.  
- Bonus: detect processes that **never appeared before**.

---

### 🔹 Exercise: Log High CPU Usage Processes  
**Goal:** Catch resource hogs (potential cryptominers, etc).  
**Instructions:**  
- Use `psutil` to log all processes using >10% CPU  
- Save PID, command, CPU usage, and time.  
- Keep logs for comparison. See if any patterns emerge.

---

### 🕹️ TryHackMe Room: [Linux Monitoring](https://tryhackme.com/room/linuxmonitoring)  
- Complete challenges 1–4  
- Save your answers and any useful commands/scripts you reused  
