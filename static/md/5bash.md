
## 📄 PDF: Topic 5 – Subtopic: Advanced Bash History Forensics  
**📚 Resource:**  
- **Sample `.bash_history` with tampering, timestamps, and obfuscation:**  
  [Download from GitHub (custom dataset)](https://raw.githubusercontent.com/DFIRMadness/bashtest-data/main/bash_history_sample.txt)  
- **Reference reading:**  
  [“Linux Command Line Forensics” – SANS Whitepaper](https://www.sans.org/white-papers/389/)  

---

### 🔹 **Exercise: Interrogate a Dirty Bash History File**  
**Goal:** Dig into a `.bash_history` file and find signs of manipulation.  

**Instructions:**  
- Download this [bash_history_sample.txt](https://raw.githubusercontent.com/DFIRMadness/bashtest-data/main/bash_history_sample.txt) and rename it `.bash_history`.  
- Inspect line structure: any gaps, duplicates, or missing commands?  
- Find at least two lines that suggest tampering or clearing attempts.  
- Which command looks like it was never meant to be logged?

---

### 🔹 **Exercise: Track Suspicious Time Gaps in Command Execution**  
**Goal:** Reconstruct what a user did—and when—using timestamped history.  

**Instructions:**  
- Add `export HISTTIMEFORMAT="%F %T "` to a `.bashrc`, then source it.  
- Run 5–10 test commands with intentional gaps or weird timing.  
- Open `.bash_history` and study the timestamp flow.  
- Where are the gaps? Could a hidden command have run during that time?  
- Optional: convert timestamps to a visual timeline.

---

### 🔹 **Exercise: Recover a Missing Session Using System Logs**  
**Goal:** Rebuild a deleted or wiped session using `syslog` and `auth.log`.  

**Instructions:**  
- Use these sample logs from CyberDefenders:  
  [https://github.com/cyberdefenders/linux-forensics-challenge](https://github.com/cyberdefenders/linux-forensics-challenge)  
- Look for a login event with no corresponding `.bash_history` content.  
- Trace what commands or programs the user may have run (via audit logs or system calls).  
- What was their goal? What evidence did they try to erase?

---

### ✨ **Bonus: Build a Suspicious Command Extractor**  
**Goal:** Write a tool that highlights dangerous patterns in a `.bash_history` file.  

**Instructions:**  
- Download the bash sample again or use your own history.  
- Search for keywords like: `base64`, `nc`, `eval`, `curl`, `python3 -c`, `wget`, `chmod 777`.  
- Output each line with its timestamp (if present).  
- Highlight commands typed at odd hours (e.g., between 2am–5am).  
- Extra: score the file’s overall “suspiciousness” from 0–10.
