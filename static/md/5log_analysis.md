
## 📄 PDF: Topic 5 – Subtopic: Log Analysis CLI

**📚 Resource:**  
*“The Linux Command Line” – Chapters 12–14 (Text processing)*  
[https://linuxcommand.org/tlcl.php](https://linuxcommand.org/tlcl.php)

---

### 🔹 Exercise: `grep`, `awk`, `cut`, `uniq`, `sort` on `auth.log`  
**Goal:** Slice and dice logs like a forensics ninja.  
**Instructions:**  
- Use a single-line shell pipeline to print all usernames who logged in  
- Print only the usernames — no timestamps, no junk  
- Sort and count them  
- Bonus: find out who logs in the most

---

### 🔹 Exercise: Identify Brute-Force Attempts via Repeated IPs  
**Goal:** Hunt down that persistent attacker.  
**Instructions:**  
- Print all IPs from failed SSH logins  
- Find any IP that appears more than 10 times  
- Print those IPs with their attempt count  
- Think: is there a pattern in timing or method?

---

### 🔹 Exercise: Find `sudo` or `su` Usage per User  
**Goal:** Trace privilege escalation attempts.  
**Instructions:**  
- Use `auth.log` to extract all `sudo` and `su` command attempts  
- Group by user  
- Figure out who tried the most  
- Look out for failed `sudo` attempts — who’s getting rejected?

---

### 🔹 Exercise: Check Login Times and Correlate to `.bash_history`  
**Goal:** Match real login sessions to what was typed.  
**Instructions:**  
- Grab login timestamps from `auth.log`  
- Then check `.bash_history`  
- Can you match command patterns to specific sessions?  
- Find something weird? Document it.
