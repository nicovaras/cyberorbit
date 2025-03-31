## 📄 PDF: Topic 2 – Subtopic: Network Honeypots  
**Resource:** [Cowrie Honeypot Documentation](https://cowrie.readthedocs.io/en/latest/)  

---

### 🔹 **Exercise: Set Up a Basic SSH Honeypot (Cowrie)**  
**Goal:** Deploy a honeypot that looks and feels like a real SSH server.  

**Instructions:**  
- Use a fresh Ubuntu VM (local or cloud, not your main machine).  
- Follow the Cowrie install guide, enable SSH emulation only.  
- Change the port to 2222 or any unused one.  
- Start Cowrie and monitor connection attempts.  
- Do attackers reach it? What usernames and passwords do they try?

---

### 🔹 **Exercise: Analyze Attacker Interactions in Honeypot Logs**  
**Goal:** Explore what attackers do once they think they have shell access.  

**Instructions:**  
- Navigate to Cowrie’s log and session directories.  
- Find at least one complete session log.  
- Identify the commands used.  
- Did they try to download files, pivot, escalate privileges?  
- Write a 1-paragraph “attack summary” from a session.

---

### 🔖 **Project: Custom Python Honeypot – Fake FTP Service**  
**Goal:** Build your own lightweight honeypot that mimics an insecure FTP server.  

**Instructions:**  
- Use Python’s `socketserver` or `asyncio` to create a fake FTP listener on port 21.  
- Accept login attempts but always allow access.  
- Simulate simple FTP commands like `ls`, `cd`, `get`, and `put` — but don’t actually perform any actions.  
- Log each command and store the full session per IP.  
- Extra: add deliberate delay to feel real, and plant a fake “secret” file.
