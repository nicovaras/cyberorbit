
## 📄 PDF: Topic 5 – Subtopic: Memory & Swap Analysis  
**Resource:** [Volatility 3 Framework Quick Start](https://volatility3.readthedocs.io/en/latest/)

---

### 🔹 **Exercise: Analyze Active Processes via /proc Filesystem**  
**Goal:** Investigate what’s currently running and how it behaves.  

**Instructions:**  
- Navigate through `/proc` and explore subdirectories like `/proc/[PID]/cmdline`, `cwd`, `environ`, and `exe`.  
- Pick one process and list its command line, working directory, and binary path.  
- Look for anything strange: hidden paths, weird environment variables, etc.  
- Try comparing what `ps` shows vs what `/proc` reveals.

---

### 🔹 **Exercise: Search for Sensitive Data (Passwords) in Memory Snapshots**  
**Goal:** Find plaintext secrets in process memory.  

**Instructions:**  
- Create a memory dump of a process (e.g., using `gcore` or `cat /proc/[PID]/mem` if permitted).  
- Run `strings` or Volatility’s `strings` plugin on the dump.  
- Search for terms like `password=`, `Authorization:`, or known test credentials.  
- Identify what kinds of data are exposed in memory and how easily.

---

### 🔹 **Exercise: Detect Anomalies in Swap Files Using Volatility**  
**Goal:** Identify unexpected or malicious artifacts stored in swap.  

**Instructions:**  
- Use Volatility 3 and a Linux memory image with swap.  
- List active processes, then check for artifacts that belong to no running process.  
- Investigate memory regions that contain code or shell history.  
- Document anything that seems detached from active execution but present in memory.
