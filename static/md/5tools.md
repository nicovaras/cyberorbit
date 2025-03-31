## 📄 PDF: Topic 5 – Subtopic: Tools & Automation  
**📚 Resource:**  
Sample Logs Repository: [https://github.com/sansblue-team/Log_Analysis](https://github.com/sansblue-team/Log_Analysis)  
(This repo contains `.log` files from a simulated attack – perfect for every exercise here.)

---

### 🔹 **Exercise: Build a Timeline Tool in Python**  
**Goal:** Create a script that reads messy logs and builds a clean, chronological timeline.  

**Instructions:**  
- Download any `.log` files from the repo above (start with `syslog.log` and `auth.log`).  
- Extract timestamps and relevant messages from each line.  
- Combine them in one list and sort chronologically.  
- Output the result like:  
  `[2025-03-30 14:11:02] – auth.log – Failed password for user bob`  
- Extra: allow passing multiple filenames via `argparse`.

---

### 🔹 **Exercise: Generate Incident Report in Markdown**  
**Goal:** Tell the story of an attack through clean, structured reporting.  

**Instructions:**  
- Use the timeline from the previous exercise.  
- Create a Markdown file with the following structure:  
  - **Summary:** What happened, in one paragraph.  
  - **Impact:** Which systems, users, or data were affected?  
  - **Indicators of Compromise:** Suspicious IPs, commands, hashes, or users.  
  - **Mitigation Steps:** What should be done next?  
- Use proper formatting (bold, headers, code blocks).  
- Save as `incident_report.md`.

---

### 🔖 **Project: Timeline of Attack from Sample Logs**  
**Goal:** Reconstruct a full compromise from scattered logs and deliver a polished forensic report.  

**Instructions:**  
- Go to [https://github.com/sansblue-team/Log_Analysis](https://github.com/sansblue-team/Log_Analysis)  
- Download all logs from the `attack-day1` folder.  
- Identify:
  - First intrusion point (time, method)  
  - Lateral movement or privilege escalation  
  - Key commands or payloads used  
- Build a Python script to extract and merge the logs into a timeline.  
- Write a Markdown or PDF report summarizing the compromise.  
- Output: `timeline.md` and `incident_summary.md`

---

### ✨ **Bonus: Create Regex Patterns to Catch Obfuscated Behavior**  
**Goal:** Write simple detection rules for suspicious log entries.  

**Instructions:**  
- Create a file `rules.txt` containing regexes for:  
  - Base64-encoded strings (look for long base64-looking blobs with `=` padding)  
  - Suspicious commands like `eval`, `os.system`, `exec`, `subprocess`  
  - Download commands: `curl http`, `wget`, `Invoke-WebRequest`  
- Now download `auth.log` or `.bash_history` from the same repo above.  
- Write a Python script to scan lines using your regexes.  
- Output all matching lines with the rule that triggered.
