## 🛡️ Subtopic 4.4: OS Hardening Baselines & Automation

**Goal:** Learn to apply security configurations based on established hardening guides (like CIS Benchmarks) and utilize tools for assessing compliance and automating checks.

**Resources:**

* **CIS Benchmarks:** [Center for Internet Security Benchmarks](https://www.cisecurity.org/cis-benchmarks/) (Download requires free registration)
* **Lynis (Linux):** [Website](https://cisofy.com/lynis/), [GitHub](https://github.com/CISOfy/lynis)
* **OpenSCAP (Linux):** [Website](https://www.open-scap.org/), package `openscap-scanner` on many distros. SCAP Security Guide (SSG) policies often included or downloadable.
* **Microsoft Security Baselines:** [Official Blog/Downloads](https://techcommunity.microsoft.com/t5/microsoft-security-baselines/bg-p/MicrosoftSecurityBaselines) (Often part of Security Compliance Toolkit)
* **Scripting:** Bash, PowerShell, Python (`os`, `subprocess` modules)
* **Test Environment:** Linux VM, Windows VM (ideally non-domain joined for local policy application).

---

### 🔹 **Exercise 1: Manual Hardening - Windows Services & Registry**

**Goal:** Manually implement specific hardening recommendations from a security baseline for Windows.

**Instructions:**

1.  Obtain the CIS Benchmark PDF for your Windows test OS version (or use Microsoft Security Baselines documentation).
2.  **Services:** Identify 2-3 services recommended for disabling in the benchmark (e.g., "TCP/IP NetBIOS Helper", "Remote Registry" if not needed). Use `services.msc` to locate these services, stop them, and set their Startup Type to "Disabled". Document the services and CIS recommendation number.
3.  **Registry/Policy:** Identify 1-2 specific security settings recommended in the benchmark that are configured via Local Security Policy (`secpol.msc`), Local Group Policy (`gpedit.msc`), or directly in the Registry (`regedit`). Examples: "Accounts: Rename administrator account", "Network access: Do not allow anonymous enumeration of SAM accounts". Implement these settings manually. Document the setting, its recommended value, and how you configured it. **Be careful when editing the registry.**
4.  **Challenge:** Find a CIS recommendation that involves configuring Windows Firewall and implement it using `wf.msc`.

---

### 🔹 **Exercise 2: Linux Assessment with Lynis**

**Goal:** Use the Lynis tool to perform a security audit of a Linux system and interpret its findings.

**Instructions:**

1.  On your Linux test VM, download or install Lynis (often available via package manager or clone from GitHub).
2.  Run a system audit: `sudo lynis audit system`.
3.  Let the scan complete. Carefully review the output, paying attention to:
    * Warnings (highlighted in yellow).
    * Suggestions (highlighted in white/green).
    * Hardening Index score (provides a general idea of posture).
4.  Choose **two** specific Warnings or Suggestions provided by Lynis.
5.  For each chosen item:
    * Research the underlying security issue or best practice it relates to.
    * Describe the recommended action suggested by Lynis or found during research.
    * Explain *how* you would manually implement the fix (e.g., command to run, file to edit, package to install/remove).
6.  **Challenge:** Explore Lynis command-line options. How can you run the audit non-interactively (`-Q`) or focus on specific test categories (`--tests-category <name>`)?

---

### 🔹 **Exercise 3: Linux Assessment with OpenSCAP**

**Goal:** Use OpenSCAP and a security profile (like SCAP Security Guide - SSG) to perform automated compliance checking against a baseline.

**Instructions:**

1.  On your Linux test VM, install the `openscap-scanner` package and potentially the `ssg-tools` and `ssg-` profiles relevant to your distribution (e.g., `ssg-centos7`, `ssg-ubuntu2004`).
2.  Identify the location of SCAP XML definition files (often under `/usr/share/xml/scap/ssg/content/`). Find an XCCDF profile file (e.g., `ssg-ubuntu2004-xccdf.xml`).
3.  List available profiles within the file: `oscap info --profiles ssg-ubuntu2004-xccdf.xml`. Choose a relevant profile ID (e.g., `xccdf_org.ssgproject.content_profile_cis_level1_server`).
4.  Run an evaluation scan against the chosen profile:
    `sudo oscap xccdf eval --profile <Profile_ID> --report report.html --results results.xml ssg-ubuntu2004-xccdf.xml`
    (Replace profile ID and definition file name as needed).
5.  Open the generated `report.html` file in a web browser.
6.  Analyze the report: Examine the overall compliance score, rules that passed, and rules that failed. Click on a failing rule to see its description, rationale, and often remediation steps/scripts.
7.  **Challenge:** Find the `results.xml` file. Briefly examine its structure. How could this XML output be used for automated reporting or integration with other tools?

---

### 🔹 **Exercise 4: Scripting a Hardening Check (Linux Example)**

**Goal:** Write a simple script to automate the verification of a specific hardening configuration item.

**Instructions:**

1.  Choose a specific hardening check for Linux, e.g., verifying that `PermitRootLogin` is set to `no` in `/etc/ssh/sshd_config`.
2.  Write a Bash script (`check_ssh_root_login.sh`) that:
    * Reads the `/etc/ssh/sshd_config` file.
    * Uses `grep` or similar tools to find the `PermitRootLogin` line (ignoring commented lines).
    * Checks if the value is exactly `no`.
    * Prints "Compliant: PermitRootLogin is set to no" or "NON-COMPLIANT: PermitRootLogin is NOT set to no (or is missing/commented)".
    * Exits with status 0 for compliant, 1 for non-compliant.
3.  Make the script executable (`chmod +x`) and test it on systems with compliant and non-compliant configurations (modify `sshd_config` temporarily for testing, then revert).
4.  **Challenge:** Enhance the script to handle cases where the setting might be commented out or missing entirely, reporting those as non-compliant. Use more robust parsing if possible (e.g., `awk` or parameter expansion instead of simple `grep`).

---

### 💡 **Project: Automated Hardening Checks**

**Goal:** Develop a script that automates the checking of multiple security configuration settings against a baseline subset.

**Instructions:**

1.  Choose either Linux (Bash/Python) or Windows (PowerShell).
2.  Select 5-10 specific, checkable hardening recommendations from a relevant CIS Benchmark (Level 1 recommendations are often good candidates). Examples:
    * **Linux:** Check SSH config (Root login, protocol), check umask default, check for world-writable files, check specific sysctl network settings, check if a service is disabled.
    * **Windows:** Check password complexity requirement, check Guest account status, check SMBv1 status, check specific audit policy settings, check UAC level.
3.  Write a script that performs each of these checks.
4.  For each check, the script should determine if the system is compliant or non-compliant based on the benchmark recommendation.
5.  The script should output a clear summary report indicating the status of each check performed (e.g., "[PASS] SSH PermitRootLogin = no", "[FAIL] SMBv1 is Enabled").
6.  Structure the script with functions for each check for better organization. Include comments explaining each check.
7.  **Portfolio Guidance:** Host your script on GitHub. Create a `README.md` that:
    * Lists the specific checks performed and the baseline they relate to (e.g., "Checks items from CIS Ubuntu 20.04 LTS Benchmark v1.1.0 Level 1").
    * Explains how to run the script and interpret its output.
    * Discusses any limitations (e.g., doesn't fix issues, requires appropriate privileges to run).

---