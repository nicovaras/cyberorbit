## 🌐 Subtopic 2.5: Active Reconnaissance Techniques

**Goal:** Learn to use tools, primarily Nmap, to actively probe target systems for open ports, running services, and potential operating system identification, while understanding ethical considerations.

**Resources:**

* **Nmap:** [Official Website & Download](https://nmap.org/), [Official Documentation (Reference Guide)](https://nmap.org/book/man.html)
* **Ethical Hacking/Testing Target:** `scanme.nmap.org` (Explicitly provided by Nmap creators for testing scans)
* **Privilege Requirements:** Many Nmap scan types (`-sS`, `-O`) require root/administrator privileges.

---

### 🔹 **Exercise 1: First Scans with Nmap**

**Goal:** Perform fundamental Nmap scans to identify potentially open TCP and UDP ports.

**Instructions:**

1.  Open your terminal/command prompt.
2.  Execute the following Nmap scans against `scanme.nmap.org`:
    * **SYN Scan (Default & Recommended):** `sudo nmap -sS scanme.nmap.org` (Run with `sudo` or as Admin). Analyze the output - what ports are listed as open? What state are other ports in (closed, filtered)?
    * **TCP Connect Scan:** `nmap -sT scanme.nmap.org` (Does not require special privileges). Compare the results and scan time to the SYN scan. When might you use `-sT` instead of `-sS`?
    * **UDP Scan (Top Ports):** `sudo nmap -sU --top-ports 20 scanme.nmap.org` (UDP scans are slower). What challenges exist with UDP scanning (e.g., open|filtered state)?
3.  **Challenge:** Explain the difference in how `-sS` and `-sT` scans establish or attempt connections at the TCP level. Why is `-sS` often called a "stealth" scan (though modern firewalls often detect it)?

---

### 🔹 **Exercise 2: Refining Scan Scope & Detecting Services**

**Goal:** Control Nmap's target ports and use its capabilities to identify the services and versions running on open ports.

**Instructions:**

1.  Perform the following Nmap scans against `scanme.nmap.org`:
    * **Specific Ports:** `nmap -p 22,80,135,445 scanme.nmap.org`
    * **Port Range:** `nmap -p 1-100 scanme.nmap.org`
    * **All Ports:** `sudo nmap -sS -p- scanme.nmap.org -T4` (This will take longer! `-T4` speeds it up. Be patient.)
    * **Service/Version Detection:** `sudo nmap -sS -sV -p 22,80,9929 scanme.nmap.org` (Port 9929 is open on scanme). Analyze the output: What service names and versions does Nmap identify? How does `-sV` work conceptually?
2.  **Challenge:** Use the `--reason` flag with a scan (e.g., `sudo nmap -sS --reason scanme.nmap.org`). How does the output change? What does the "Reason" column tell you about *why* Nmap determined a port's state?

---

### 🔹 **Exercise 3: OS Detection and Scan Timing**

**Goal:** Attempt operating system detection with Nmap and understand how timing templates affect scan speed and behavior.

**Instructions:**

1.  Perform the following Nmap scans against `scanme.nmap.org`:
    * **OS Detection:** `sudo nmap -O scanme.nmap.org` (Requires open *and* closed TCP ports to be found, may need `-p-` or a wider range if default scan doesn't find both). Analyze the OS detection results. How confident is Nmap? What information does it use to guess?
    * **Timing Templates:** Run a basic scan (e.g., `sudo nmap -sS scanme.nmap.org`) with different timing templates. **Do not use -T0 or -T1 on targets you don't own.** Compare the scan times reported by Nmap:
        * `sudo nmap -sS -T2 scanme.nmap.org`
        * `sudo nmap -sS -T4 scanme.nmap.org` (Aggressive - generally acceptable for scanme)
        * `(Optional/Caution) sudo nmap -sS -T5 scanme.nmap.org` (Insane - may be disruptive)
2.  Discuss the trade-offs between scan speed, accuracy, and potential intrusiveness/detection risk associated with different timing templates. Which template is generally recommended (`-T4`)?
3.  **Challenge:** Combine OS detection with version scanning (`sudo nmap -sV -O scanme.nmap.org`). Does having version information potentially improve OS detection accuracy?

---

### 🔹 **Exercise 4: Managing Nmap Output**

**Goal:** Learn to save Nmap scan results in various formats for later analysis or processing by other tools.

**Instructions:**

1.  Choose a comprehensive Nmap scan command (e.g., `sudo nmap -sS -sV -T4 scanme.nmap.org`).
2.  Run the scan and save the output simultaneously in three different formats using the `-oA <basename>` flag:
    * `sudo nmap -sS -sV -T4 scanme.nmap.org -oA scanme_results`
3.  This will create three files: `scanme_results.nmap` (Normal format), `scanme_results.gnmap` (Grepable format), and `scanme_results.xml` (XML format).
4.  Open and examine each file:
    * `.nmap`: Human-readable, good for quick review.
    * `.gnmap`: Compact, designed for processing with command-line tools like `grep`, `awk`. Identify the structure.
    * `.xml`: Structured, ideal for parsing with scripts (as seen in Sprint 1) or importing into other tools.
5.  **Challenge:** Use command-line tools (`grep`, `cut`) on the `.gnmap` file to extract just the IP addresses of hosts that have port 80 open.

---

### 🧪 **(Optional) Lab: Nmap Practice**

**Goal:** Apply Nmap scanning techniques in a practical lab environment.

**Instructions:**
* Sign up or log in to [TryHackMe](https://tryhackme.com/).
* Complete the **[Further Nmap](https://tryhackme.com/room/furthernmap)** room. This room covers various scan types, NSE scripts, and practical application.
* Alternatively, start with simpler Nmap rooms if available and build up.

---