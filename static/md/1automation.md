## 📄 PDF: Topic 1 – Subtopic: Automation & CLI Integration  
**📚 Resource:**  
📘 *“Automate the Boring Stuff” – Chapters 17 & 18*  
[https://automatetheboringstuff.com/2e/chapter17/](https://automatetheboringstuff.com/2e/chapter17/)  

---

### 🔹 **Exercise: Script a CLI Recon Routine**  
**Goal:** Automate basic recon tasks to prepare for an investigation.  

**Instructions:**  
- Write a script that runs several CLI commands (e.g., system info, open ports, users).  
- Collect their output and store it in a timestamped file.  
- How could you run this daily and organize outputs over time?

---

### 🔹 **Exercise: Clone `uptime`, `top`, and `who` in One Script**  
**Goal:** Emulate sysadmin classics with Python.  

**Instructions:**  
- Display current user, system uptime, and system load.  
- Show top processes by CPU and memory.  
- Format the output like a compact terminal dashboard.  
- Can you run this in a loop like `top`?

---

### 🔹 **Exercise: Chain Python and Bash for Custom CLI Commands**  
**Goal:** Combine the power of shell and Python to make hybrid tools.  

**Instructions:**  
- Build a script that uses Python to generate input for a shell command (e.g., directory list, search pattern).  
- Feed that into a Bash pipeline using `subprocess`.  
- Try chaining `find`, `grep`, and custom parsing logic—can you detect recently modified `.log` files in `/var`?

---

### ✨ **Bonus: Trigger a Live Alert on Suspicious Behavior**  
**Goal:** Build a watchdog that reacts immediately when something odd happens.  

**Instructions:**  
- Monitor active processes in a loop.  
- If a process like `nc`, `msfconsole`, or `python -c` appears, trigger an alert.  
- You choose: email, write to log, or flash it in red on screen.  
- Can your script stay quiet until something truly weird happens?
