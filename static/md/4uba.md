## 📄 PDF: Topic 4 – Subtopic: User Behavior Analytics (UBA)  
**Resource:** [Insider Threat Mitigation – NIST Guide](https://csrc.nist.gov/publications/detail/nistir/8228/final) *(Read section 3 on abnormal behavior patterns)*

---

### 🔹 **Exercise: Track Login/Logout Times per User; Detect Unusual Activity Hours**  
**Goal:** Collect login times and analyze user activity windows.  

**Instructions:**  
- Use `last` or `journalctl _COMM=sshd` to gather login sessions.  
- Parse and group login times per user.  
- Find sessions happening outside of typical hours (e.g., 1am–5am).  
- Highlight the users and dates that deviate from the norm.

---

### 🔹 **Exercise: Detect Abnormal Shell Command Patterns Using Frequency Analysis**  
**Goal:** Identify when users start running strange or rare commands.  

**Instructions:**  
- Get command history from `.bash_history` or audit logs.  
- Build a frequency table for common commands (`ls`, `cd`, `nano`, etc.).  
- Flag commands that appear only once or are rarely used (e.g., `nc`, `chmod 777`, `python`).  
- Bonus: visualize this as a bar chart of command frequency.

---

### 🔖 **Project: Create Automated Alerts for Abnormal User Activities**  
**Goal:** Build a script that watches logs in real-time and raises alerts on suspicious behavior.  

**Instructions:**  
- Monitor login times, command usage, or processes tied to specific users.  
- Define “abnormal” thresholds (e.g., `login between 2am–4am`, `use of curl`, or `unexpected sudo`).  
- Log these events to a separate alert file.  
- Optional: send an email or system notification when a new alert is triggered.

