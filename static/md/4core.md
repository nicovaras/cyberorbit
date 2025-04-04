## 🛡️ Subtopic 4.1: Core OS Security Principles & Attack Surface

**Goal:** Understand and apply fundamental security concepts like Least Privilege, Defense in Depth, and Attack Surface Reduction in practical operating system contexts.

**Resources:**

* **CIS Benchmarks:** [Center for Internet Security Benchmarks](https://www.cisecurity.org/cis-benchmarks/) (Overview and concept)
* **Least Privilege:** [Wikipedia Article](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
* **Attack Surface:** [OWASP Attack Surface Analysis Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)
* **Tools:** `ss`, `netstat`, `ps` (Linux), Task Manager, Resource Monitor (Windows)

---

### 🔹 **Exercise 1: Least Privilege Scenario Analysis**

**Goal:** Determine the minimum necessary permissions for specific system roles.

**Instructions:**

1.  Consider a scenario: A dedicated user account (`webapp`) runs a web application server (like Nginx or Apache) on a Linux system. The application needs to read web content from `/var/www/html`, write logs to `/var/log/webapp/`, and bind to network port 80 (or 443). It does *not* need shell access or access to other users' data.
2.  Research and list the specific Linux permissions (filesystem ownership/permissions, possibly capabilities like `cap_net_bind_service`) the `webapp` user would need to fulfill its function, adhering strictly to the principle of least privilege.
3.  Explain *why* granting broader permissions (e.g., running as root, making `/var/www/html` world-writable) would violate least privilege and increase risk.
4.  **Challenge:** Repeat the analysis for a Windows scenario: A service account (`SQLSvc`) running a database service needs to read/write database files in `D:\SQLData` and listen on TCP port 1433. What specific NTFS permissions and User Rights Assignments are minimally required?

---

### 🔹 **Exercise 2: Mapping the Attack Surface**

**Goal:** Identify potential points of entry or interaction on a default OS installation.

**Instructions:**

1.  Use a fresh default installation of a common Linux server distribution (e.g., Ubuntu Server, CentOS Stream in a VM) or analyze your current Linux system.
2.  Use command-line tools to identify:
    * All running processes (`ps aux` or `top`).
    * All listening network ports (TCP and UDP) and the processes associated with them (`ss -tulnp` or `sudo netstat -tulnp`).
    * Key installed software packages/services (e.g., using `dpkg -l` or `rpm -qa`).
3.  List the top 5-10 services/ports that represent the most significant network-facing attack surface.
4.  For a hypothetical role (e.g., "This server will only host static web pages via Nginx"), identify which of the running services/open ports could potentially be disabled or restricted to reduce the attack surface without breaking the required functionality.
5.  **Challenge:** How would you identify services configured to start automatically on boot (`systemctl list-unit-files --state=enabled`)? Why is disabling unnecessary auto-starting services important for attack surface reduction?

---

### 🔹 **Exercise 3: Designing Defense in Depth**

**Goal:** Conceptualize a multi-layered security approach for a common scenario.

**Instructions:**

1.  Scenario: You need to protect highly sensitive research data stored in text files within a specific directory (`/srv/research_data` on Linux or `C:\ResearchData` on Windows) on a file server within an internal network. Only authorized researchers (`research_group`) should have read/write access.
2.  Describe at least one specific security control you would implement at each of the following conceptual layers to protect this data, illustrating "Defense in Depth":
    * **Network Layer:** (e.g., Firewall rules)
    * **Operating System Layer:** (e.g., OS hardening, authentication)
    * **Filesystem Layer:** (e.g., Permissions)
    * **Auditing/Monitoring Layer:** (e.g., Logging access)
    * **Data Layer (Optional):** (e.g., Encryption)
3.  Explain how the failure of one layer's control might still be mitigated by controls at other layers in your design.
4.  **Challenge:** Add "Human Layer" controls to your design (e.g., training, access reviews). How do they contribute to the overall defense?

---

### 🔹 **(Optional) Exercise 4: CVE Analysis**

**Goal:** Connect theoretical principles to real-world vulnerabilities.

**Instructions:**

1.  Find a recently published CVE (Common Vulnerabilities and Exposures) entry for a major operating system (Linux kernel, Windows). Use resources like [Mitre CVE](https://cve.mitre.org/) or [NIST NVD](https://nvd.nist.gov/).
2.  Read the CVE description and any linked analysis (e.g., vendor advisories, security researcher blogs).
3.  Briefly summarize the vulnerability.
4.  Explain which core security principle(s) (e.g., least privilege, input validation, secure defaults, attack surface management) were violated or bypassed by this vulnerability.
5.  What was the recommended mitigation or patch provided by the vendor?

---