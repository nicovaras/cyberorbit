## 🛡️ Subtopic 4.2: Linux Filesystem Permissions & ACLs

**Goal:** Understand and manage standard Linux permissions (user, group, other), special permissions (SUID, SGID, Sticky Bit), default permissions (`umask`), and POSIX Access Control Lists (ACLs).

**Resources:**

* **Linux Commands:** `ls -l`, `chmod`, `chown`, `chgrp`, `umask`, `id`, `find`, `getfacl`, `setfacl` (use `man <command>` for details)
* **Tutorials:** Search for "Linux permissions tutorial", "Linux ACL tutorial"
* **Test Environment:** A Linux VM or sandbox environment where you have root/sudo access to create users/groups and modify permissions.

---

### 🔹 **Exercise 1: Decoding `ls -l` and Basic `chmod`**

**Goal:** Interpret the standard permission string and modify basic permissions using `chmod` in symbolic and octal notation.

**Instructions:**

1.  Create a test file (`touch testfile.txt`) and a test directory (`mkdir testdir`).
2.  Examine their permissions using `ls -l`. Decode the permission string (e.g., `-rwxr-xr--`) - identify the file type, user permissions, group permissions, and other permissions.
3.  Use `chmod` with **symbolic notation** to make the following changes to `testfile.txt`:
    * Add write permission for the group (`g+w`). Verify with `ls -l`.
    * Remove read permission for others (`o-r`). Verify.
    * Set user permissions to read/write only, group to read only, others no permissions (`u=rw,g=r,o=`). Verify.
4.  Use `chmod` with **octal notation** to set the following permissions:
    * `testfile.txt` to `rw-r-----` (octal `640`). Verify.
    * `testdir` to `rwxr-x---` (octal `750`). Verify.
5.  **Challenge:** What happens if you remove execute permission (`x`) from a directory for a user? Can they still `cd` into it? Can they list its contents (`ls`)? Test this behavior.

---

### 🔹 **Exercise 2: Understanding Special Permissions (SUID, SGID, Sticky)**

**Goal:** Identify and understand the function and security implications of SUID, SGID, and Sticky bits.

**Instructions:**

1.  Use `find` to locate files with the SUID bit set in `/usr/bin`: `sudo find /usr/bin -type f -perm -4000 -ls`. Examine common examples like `passwd`, `su`, `sudo`. Explain *why* `passwd` needs SUID root permissions to function correctly.
2.  Use `find` to locate files/directories with the SGID bit set, e.g., `sudo find / -type d -perm -2000 2>/dev/null`. Find a directory like `/var/log` or `/var/mail` (may vary by distro). Explain how the SGID bit on a directory affects the group ownership of new files created within it. Create a test directory, set the SGID bit (`chmod g+s testdir_sgid`), change its group ownership (`chgrp <yourgroup> testdir_sgid`), create a file inside it, and check the file's group owner.
3.  Explain the purpose of the Sticky Bit (`t`) on directories like `/tmp` (`ls -ld /tmp`). Create a test directory, set the sticky bit (`chmod +t testdir_sticky`), create two files inside it owned by different users (User A, User B - requires test users or using root). Log in or use `sudo -u` to act as User A. Can User A delete User B's file inside `testdir_sticky`?
4.  **Challenge:** Why is having SUID root on a custom script or a shell generally considered a major security risk? How could it be abused?

---

### 🔹 **Exercise 3: Controlling Default Permissions with `umask`**

**Goal:** Understand how the `umask` setting influences the default permissions assigned to newly created files and directories.

**Instructions:**

1.  Check your current `umask` value by simply typing `umask` in the shell.
2.  Temporarily set a specific `umask` value: `umask 027`.
3.  Create a new file (`touch file_027`) and a new directory (`mkdir dir_027`).
4.  Use `ls -l file_027` and `ls -ld dir_027` to observe the permissions assigned. Calculate why these permissions resulted from the base permissions (`666` for files, `777` for directories) and the `umask` of `027`.
5.  Repeat steps 2-4 with a different `umask`, e.g., `umask 002`. Compare the resulting permissions.
6.  Reset your umask to the default (usually done by logging out/in or setting it back explicitly if you know the default, often `022` or `002`). Explain which umask (`027` or `002`) provides more secure default permissions and why.
7.  **Challenge:** How can you make `umask` settings persistent for a user's login session? (Hint: Look at shell startup files like `.bashrc` or `.profile`).

---

### 🔹 **Exercise 4: Implementing Fine-Grained Access with ACLs**

**Goal:** Use POSIX Access Control Lists (ACLs) to grant permissions beyond the standard user/group/other model.

**Instructions:**

1.  **Setup:** Ensure your filesystem supports ACLs (most modern Linux filesystems do, might need mount option `acl` on some older setups). Create a directory `/opt/project_share` owned by root, group `root`. Create two test users (`user1`, `user2`) and a test group (`devteam`). Add `user1` to `devteam`.
2.  **Scenario:** Grant the following permissions on `/opt/project_share`:
    * `user1` needs read, write, and execute permissions.
    * Members of the `devteam` group need read and execute permissions.
    * `user2` needs read and execute permissions *only*.
    * Other users should have no permissions.
    * Default ACLs should ensure new files/dirs inside inherit permissions allowing `devteam` read/execute.
3.  **Implementation:** Use `setfacl -m` to add ACL entries for `user:user1`, `group:devteam`, and `user:user2`. Use `setfacl -d` to set default ACLs for the directory.
4.  **Verification:** Use `getfacl /opt/project_share` to view the assigned ACLs. Use `ls -l /opt/project_share` – what does the `+` sign at the end of the permission string indicate?
5.  **Testing:** Use `sudo -u user1`, `sudo -u user2`, or log in as the test users. Try to create files, read files (created by others if applicable), and list the directory contents inside `/opt/project_share` to verify the permissions work as intended.
6.  **Challenge:** Remove the ACL entry specifically for `user2` using `setfacl -x`. Verify `user2`'s access is now denied (assuming standard 'other' permissions are `---`).

---

### 💡 **Project: Secure File Area Setup**

**Goal:** Create a script or document a repeatable process to set up a secure directory structure with specific, non-trivial permission requirements using standard permissions, special bits, and ACLs.

**Instructions:**

1.  Define a scenario (e.g., a shared directory for submitting reports, a web application's upload area, a multi-team project space).
2.  Specify clear access requirements for different users and groups (e.g., web service user needs write but not execute, managers need read-only, specific users need write, prevent accidental deletion by others).
3.  Create a Bash script or Python script that:
    * Creates the necessary directories.
    * Sets appropriate base ownership (`chown`, `chgrp`).
    * Sets appropriate standard permissions (`chmod`).
    * Sets any necessary special bits (SGID for group inheritance, Sticky Bit for controlled deletion).
    * Applies required ACLs (`setfacl`) for fine-grained access.
    * Includes comments explaining the purpose of each command.
4.  Alternatively, write a detailed Markdown document outlining the manual steps (commands) to achieve the same setup, with explanations.
5.  **Portfolio Guidance:** Host your script or documentation on GitHub. The README should clearly state the scenario, the access requirements, and explain how the script/steps implement those requirements using specific Linux permission features (standard, special, ACLs). This demonstrates practical application of complex permission schemes.

---