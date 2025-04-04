## 🛡️ Subtopic 4.5: Linux Privilege Management (sudo)

**Goal:** Configure the `sudo` utility securely to grant specific administrative privileges based on user roles and the principle of least privilege, while ensuring proper logging and avoiding common pitfalls.

**Resources:**

* **Commands:** `sudo`, `visudo` (essential for editing `sudoers`), `su`
* **Manual Pages:** `man sudo`, `man sudoers`
* **Test Environment:** Linux VM with root/sudo privileges and at least one standard test user account and one test group.

---

### 🔹 **Exercise 1: Basic `sudoers` Grant via `visudo`**

**Goal:** Learn the safe way to edit the `sudoers` file and grant a user permission to run a specific command as root.

**Instructions:**

1.  As root or using `sudo`, run `visudo` to safely edit the `/etc/sudoers` configuration. **Never edit this file directly with a text editor.**
2.  Add a line to grant your standard test user (e.g., `testuser`) the ability to run the command `/usr/bin/systemctl status sshd` *as root*. The line format is typically: `username ALL=(ALL) /path/to/command`.
3.  Save and exit `visudo`.
4.  Log in or use `su` or `sudo -u testuser -s /bin/bash` to become `testuser`.
5.  Try running `sudo /usr/bin/systemctl status sshd`. It should succeed (possibly after asking for `testuser`'s password, depending on defaults).
6.  Try running `sudo /usr/bin/whoami`. This should fail, demonstrating the restriction.
7.  **Challenge:** Modify the `sudoers` entry to allow `testuser` to run the command *without* being prompted for their password using the `NOPASSWD:` tag. Test again. Discuss the security implications.

---

### 🔹 **Exercise 2: Leveraging Aliases (User, Host, Command)**

**Goal:** Use aliases in the `sudoers` file to manage permissions more efficiently for groups of users, commands, or hosts.

**Instructions:**

1.  Using `visudo`, define the following aliases near the top of the file:
    * `User_Alias WEBMASTERS = user1, user2` (replace with your test usernames)
    * `Cmnd_Alias WEBSERVER_CTRL = /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx, /usr/bin/journalctl -u nginx` (adjust service name if needed)
    * `Host_Alias LOCAL = localhost, 127.0.0.1` (Example)
2.  Add a rule that grants users in the `WEBMASTERS` alias the ability to run commands listed in the `WEBSERVER_CTRL` alias when logged into hosts defined in the `LOCAL` alias: `WEBMASTERS LOCAL = (ALL) WEBSERVER_CTRL`.
3.  Save and exit `visudo`.
4.  Test the permissions: As `user1` (or `user2`), try running `sudo /usr/bin/systemctl restart nginx`. Try running `sudo /usr/bin/journalctl -u nginx`. Try running `sudo /usr/bin/whoami` (which should fail).
5.  **Challenge:** Explain how using aliases simplifies managing sudo permissions when you have multiple users needing similar access or when commands/hosts change.

---

### 🔹 **Exercise 3: Restricting Commands & Preventing Shell Escapes**

**Goal:** Configure `sudo` to allow execution of specific commands while preventing users from escaping to a full root shell via those commands.

**Instructions:**

1.  Identify a command that might allow shell escapes (e.g., editors like `vi`, pagers like `less`, or tools with `!` commands like `find -exec`). Let's use `less` as an example.
2.  Using `visudo`, grant a test user the ability to run `/usr/bin/less /var/log/syslog` as root: `testuser ALL = (ALL) /usr/bin/less /var/log/syslog`.
3.  As `testuser`, run `sudo /usr/bin/less /var/log/syslog`. While inside `less`, type `!sh` and press Enter. What happens? (You likely get a root shell). Exit the sub-shell and `less`.
4.  Research `sudoers` options to prevent command execution from within the allowed command (e.g., the `NOEXEC` tag, although its availability/effectiveness varies). Modify the `sudoers` rule: `testuser ALL = (ALL) NOEXEC: /usr/bin/less /var/log/syslog` (if `NOEXEC` is supported).
5.  Retest step 3. Does `!sh` still work? If `NOEXEC` isn't available or doesn't work, discuss alternative approaches (e.g., using more restrictive commands, custom wrapper scripts).
6.  **Challenge:** Configure sudo to allow a user to run `find` but prevent them from using the `-exec` or `-execdir` options to run arbitrary commands. This often requires careful command path specification or sometimes isn't fully possible directly in sudoers.

---

### 🔹 **Exercise 4: Logging, Timeouts, and `NOPASSWD` Risks**

**Goal:** Configure `sudo` logging options, understand password timeouts, and evaluate the risks of using `NOPASSWD`.

**Instructions:**

1.  Using `visudo`, examine the `Defaults` entries.
2.  Add or modify `Defaults` lines to:
    * Log all sudo commands and I/O to a specific file: `Defaults log_output`, `Defaults logfile=/var/log/sudo.log`. (Ensure directory exists and has correct permissions).
    * Set a short password timeout: `Defaults timestamp_timeout=1` (timeout in minutes).
3.  Grant a *different*, specific, highly restricted command to a user with `NOPASSWD`: `scriptuser ALL=(ALL) NOPASSWD: /usr/local/bin/run_report.sh` (assume `run_report.sh` is a safe, non-interactive script).
4.  Test the changes:
    * Run a few allowed `sudo` commands (some requiring a password, some not). Verify logs appear in `/var/log/sudo.log` (or your specified file).
    * Run a password-requiring `sudo` command, wait longer than the timeout (1 minute), run it again. Are you prompted for the password again?
    * Run the `NOPASSWD` command as `scriptuser`. Verify it runs without a password prompt.
5.  Discuss the security risks of using `NOPASSWD`. Why should it be used sparingly and only for extremely restricted commands, especially in scripts?
6.  **Challenge:** How does I/O logging (`log_output`) differ from standard command logging? When would it be particularly useful for forensic analysis?

---

### 🔹 **(Optional) Exercise 5: Sudoedit for Secure File Editing**

**Goal:** Understand and configure `sudoedit` as a safer alternative to granting direct editor access via `sudo`.

**Instructions:**

1.  Using `visudo`, grant your test user permission to edit a specific configuration file (e.g., `/etc/hosts`) using `sudoedit`: `testuser ALL = (ALL) sudoedit /etc/hosts`.
2.  As `testuser`, run `sudoedit /etc/hosts`.
3.  Observe the behavior: `sudoedit` creates a temporary copy of the file, launches the user's default editor (or one specified by `SUDO_EDITOR` environment variable) running *as the user*, allows editing, and then replaces the original file *atomically* only if changes were made.
4.  Now, using `visudo`, grant the user direct editor access instead: `testuser ALL = (ALL) /usr/bin/vim /etc/hosts` (replace with `nano` or your editor).
5.  As `testuser`, run `sudo /usr/bin/vim /etc/hosts`. While inside the editor, try to execute a shell command (e.g., `:!whoami` in vim). What user does the command run as?
6.  Explain why `sudoedit` is considered safer than allowing direct `sudo <editor> <file>`. (Hint: The editor runs as the user, not root; reduced risk of shell escapes with root privileges).

---