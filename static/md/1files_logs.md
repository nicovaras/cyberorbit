## 📄 PDF: Topic 1 – Files, Logs, and Strings

**📚 Resource:**  
*“Python Crash Course” – Chapters 10 & 11*  
[https://ehmatthes.github.io/pcc_3e/](https://ehmatthes.github.io/pcc_3e/)

---

### 🔹 Exercise: Read, Write, and Clean Log Files  
**Goal:** Work with messy log data.  
**Instructions:**  
- Find and open `auth.log`.  
- Remove empty lines and lines starting with `#`.  
- Save cleaned lines into a new file `auth_cleaned.log`.

---

### 🔹 Exercise: Extract Fields from Messy Strings using `re`  
**Goal:** Pull useful information from unstructured text.  
**Instructions:**  
- Use regex to extract all usernames from failed login lines using `re`.  
- Print each match.

---

### 🔹 Exercise: Summarize Logs using `collections.Counter`  
**Goal:** Identify patterns in logs quickly.  
**Instructions:**  
- Count how many times each IP appears in failed login entries.  
- Use `Counter` to get the top 5.  
- Print them sorted in this format: `IP – count`

---

### 🔹 Exercise: Parse Timestamps and Sort Events  
**Goal:** Build a timeline of events.  
**Instructions:**  
- Extract timestamps from the log like `Jan 10 14:32:01`  
- Convert them to `datetime` objects using `strptime()`  
- Pair each log line with its parsed timestamp.  
- Sort and print the top 5 earliest and latest entries.

---

### 🔖 Project: Security Log Analyzer  
**Goal:** Build a script that ties it all together.  
**Instructions:**  
- Accept a file path as input  
- Clean the logs, extract IPs, count them  
- Output a simple report: total entries, top 5 IPs, time range  
- Save to `log_summary.txt`  
- Bonus: add colors to terminal output using `colorama`

