## 🛡️ Subtopic 4.7: Linux Auditing Configuration (auditd)

**Goal:** Configure and utilize the Linux Audit Daemon (`auditd`) and its associated tools (`auditctl`, `ausearch`, `aureport`) to monitor and log specific system events for security and compliance purposes.

**Resources:**

* **Commands:** `auditd`, `auditctl`, `ausearch`, `aureport`, `systemctl`
* **Config Files:** `/etc/audit/auditd.conf`, `/etc/audit/rules.d/` directory, `/etc/audit/audit.rules` (often generated)
* **Log File:** `/var/log/audit/audit.log` (or location specified in `auditd.conf`)
* **Manual Pages:** `man auditd`, `man auditd.conf`, `man auditctl`, `man ausearch`, `man aureport`, `man audit.rules`
* **Test Environment:** Linux VM with root/sudo privileges.

---

### 🔹 **Exercise 1: `auditd` Service and Configuration**

**Goal:** Ensure the audit service is running and understand its basic configuration parameters.

**Instructions:**

1.  Verify `auditd` package is installed (`dpkg -s auditd` or `rpm -q audit`). Install if necessary (`apt install auditd` or `yum install audit`).
2.  Check the status of the `auditd` service: `systemctl status auditd`. Ensure it is active and running. Start/enable if needed.
3.  Examine the main configuration file: `cat /etc/audit/auditd.conf`.
4.  Identify and explain the purpose of the following parameters:
    * `log_file`
    * `log_format`
    * `max_log_file`
    * `num_logs`
    * `max_log_file_action`
    * `space_left_action`
    * `admin_space_left_action`
5.  Modify `max_log_file_action` to `ROTATE` if it isn't already set. Change `num_logs` to a small number (e.g., 4) for testing rotation later (optional).
6.  Restart the `auditd` service to apply changes: `sudo systemctl restart auditd`.
7.  **Challenge:** What is the difference between the `RAW` and `ENRICHED` log formats? Which is generally more useful for direct analysis vs. feeding into a SIEM?

---

### 🔹 **Exercise 2: Watching Files and Directories (`auditctl -w`)**

**Goal:** Configure `auditd` rules to monitor specific files or directories for access or modification events.

**Instructions:**

1.  View the currently loaded audit rules: `sudo auditctl -l`. (May be empty initially).
2.  Add audit watches using `auditctl`. Use the `-k <keyname>` option to easily search for related events later:
    * Watch `/etc/shadow` for write access (`w`) or attribute changes (`a`):
      `sudo auditctl -w /etc/shadow -p wa -k shadow_changes`
    * Watch `/etc/ssh/sshd_config` for write or attribute changes:
      `sudo auditctl -w /etc/ssh/sshd_config -p wa -k sshd_config_changes`
    * Watch the entire `/sbin` directory for execute (`x`) permissions:
      `sudo auditctl -w /sbin/ -p x -k sbin_execution`
3.  Verify the rules are loaded: `sudo auditctl -l`.
4.  Trigger the rules:
    * Try opening `/etc/shadow` in an editor as root (don't save changes unless you have a backup!).
    * Run a command from `/sbin` (e.g., `sudo /sbin/iptables -L`).
5.  Search for the generated events using the keys: `sudo ausearch -k shadow_changes -i`, `sudo ausearch -k sbin_execution -i`. (`-i` interprets numerical IDs).
6.  **Challenge:** Rules added via `auditctl` are temporary (lost on reboot). Add the same rules permanently by creating a file like `/etc/audit/rules.d/99-custom.rules` with the rules written in the persistent format (remove `auditctl` command itself). Reload rules: `sudo augenrules --load`. Verify with `auditctl -l`.

---

### 🔹 **Exercise 3: Effective Audit Log Searching (`ausearch`)**

**Goal:** Practice using `ausearch` with various options to efficiently find specific events within potentially large audit logs.

**Instructions:**

1.  Generate various audit events (log in/out via SSH, use `sudo`, access/modify watched files from Ex2, trigger failed logins if possible).
2.  Use `ausearch` to find events based on different criteria:
    * **By Event Type:** Find all user login events: `sudo ausearch -m USER_LOGIN -i`
    * **By User ID:** Find all events related to a specific user ID (find UID with `id <username>`): `sudo ausearch -ui <UID> -i`
    * **By Success/Failure:** Find all failed login attempts: `sudo ausearch -m USER_LOGIN -sv no -i`
    * **By Time Range:** Find events from the last 10 minutes: `sudo ausearch -ts recent -i` or `sudo ausearch -ts today -te now -i`
    * **By Key:** (Using keys from Ex2) `sudo ausearch -k sshd_config_changes -i`
    * **Combining Filters:** Find failed login attempts for a specific user today: `sudo ausearch -m USER_LOGIN -sv no -ui <UID> -ts today -i`
3.  Analyze the structure of a typical audit event message (type, msg, pid, uid, auid, ses, comm, exe, key, etc.).
4.  **Challenge:** An event occurred, but you only remember the executable involved (`exe=/usr/bin/passwd`) and roughly when it happened. Construct an `ausearch` command to find it efficiently.

---

### 🔹 **Exercise 4: Auditing System Calls (`auditctl -S`)**

**Goal:** Configure audit rules to monitor specific system calls, potentially filtering by architecture, user, or arguments, for fine-grained monitoring.

**Instructions:**

1.  Plan rules to monitor potentially risky syscalls. Add these rules via `auditctl` or persistently in `/etc/audit/rules.d/`:
    * Monitor attempts to load kernel modules:
      `-a always,exit -F arch=b64 -S init_module -S finit_module -S delete_module -k kernel_module_changes` (Adjust arch if needed)
    * Monitor `setuid`/`setgid` syscalls (often involved in privilege escalation):
      `-a always,exit -F arch=b64 -S setuid -S setgid -k setuid_setgid_usage`
    * Monitor the `chmod`/`chown` family of syscalls specifically when applied to `/etc/`:
      `-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -S chown -S fchown -S fchownat -F dir=/etc -k etc_perm_changes`
2.  Verify rules are loaded: `sudo auditctl -l`.
3.  Attempt actions that trigger these syscalls:
    * Try (and likely fail unless you have a module) `sudo insmod dummy.ko`.
    * Use `chmod` or `chown` on a file within `/etc/`.
4.  Use `ausearch -k <keyname> -i` to find the corresponding audit events. Examine the syscall number, arguments (if logged), and other context provided.
5.  **Challenge:** Configure a rule to audit the `execve` syscall but *only* when executed by a *non-root* user (`-F auid!=0 -F auid!=4294967295`) for a specific command path (e.g., `-F path=/usr/bin/ncat`). Test this rule.

---

### 🔹 **Exercise 5: Generating Summary Reports (`aureport`)**

**Goal:** Use `aureport` to create summarized views of audit log data for quick analysis and reporting.

**Instructions:**

1.  Ensure you have generated a variety of audit events over time.
2.  Run `aureport` with different options to generate reports:
    * **Authentication Report:** `sudo aureport -au -i` (Shows successes and failures)
    * **Login Report:** `sudo aureport -l -i` (Shows user logins/logouts)
    * **Summary by Event Type:** `sudo aureport --summary -i`
    * **Summary by Key:** `sudo aureport -k --summary -i` (Uses keys defined in your rules)
    * **Executable Report:** `sudo aureport -x --summary -i` (Shows which executables generated events)
    * **Report for specific time:** `sudo aureport -ts yesterday -te today -i --summary`
3.  Analyze the output of each report type. How could these summaries help an administrator quickly spot anomalies or trends (e.g., a spike in failed logins, unexpected command executions)?
4.  **Challenge:** Combine `aureport` with standard command-line tools. For example, generate the authentication report (`aureport -au`) and pipe it to `grep` to find only failed authentications for a specific user.

---