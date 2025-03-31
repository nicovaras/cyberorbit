## 📄 PDF: Topic 5 – Subtopic: Timeline Reconstruction  
**📚 Resource:**  
*“Linux Forensics” – Chapter 3: Timeline Analysis*  
[https://nostarch.com/linuxforensics](https://nostarch.com/linuxforensics)

**🧪 Practice Sources:**  
These offer downloadable logs or access to simulated forensic cases:  
- [https://blueteamlabs.online](https://blueteamlabs.online)  
- [https://cyberdefenders.org](https://cyberdefenders.org)  
- [https://www.malware-traffic-analysis.net](https://www.malware-traffic-analysis.net)  
- [https://dfirmadness.com](https://dfirmadness.com)

---

### 🔹 **Exercise: Untangle a Timeline from Multiple Logs**  
**Goal:** Create a single story from scattered sources.  

**Instructions:**  
- Use any three logs: `auth.log`, `syslog`, and `.bash_history` (use real or sample files).  
- Extract timestamped entries related to user logins, command executions, and system alerts.  
- Shuffle them together into one master timeline.  
- Something looks out of place—can you find what doesn't belong chronologically?

---

### 🔹 **Exercise: Follow a Single Intruder’s Session**  
**Goal:** Reconstruct one attacker’s session, step by step.  

**Instructions:**  
- Choose a suspicious login event from your logs.  
- Find every log entry that could be part of that session—commands, errors, downloads, escalations.  
- Draw a timeline that starts with the login and ends with logout—or something worse.  
- What’s the most surprising thing they did?

---

### 🔹 **Exercise: Trace a Silent Privilege Escalation**  
**Goal:** Spot someone becoming root without making noise.  

**Instructions:**  
- Look for subtle signs that a user gained elevated privileges.  
- Not all `sudo` is loud—some escalation happens through environment manipulation or sudo misconfigurations.  
- Can you find the point where a regular user became root without running `su`?  
- Who knew what, and when?

---

### 🔹 **Exercise: Spot Encoded Payloads in Bash History**  
**Goal:** Catch someone hiding in plain sight.  

**Instructions:**  
- Open `.bash_history` and scan for weird or long commands that don’t look human-written.  
- Focus on lines using `base64`, `eval`, `python -c`, or `curl` with pipes.  
- Choose three lines you can't immediately understand.  
- Can you tell what they might have done just by looking?

---

### 🕹️ **CTF: TryHackMe – [Intro to Digital Forensics](https://tryhackme.com/room/introtodigitalforensics)**  
**Goal:** Analyze a real digital crime scene.  

**Instructions:**  
- Start the room and treat it like a real-world investigation.  
- Focus on how events connect, not just what tools to run.  
- At the end, write a 5-line incident summary using your reconstructed timeline.