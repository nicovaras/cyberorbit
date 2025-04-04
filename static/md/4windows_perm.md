## 🛡️ Subtopic 4.3: Windows File/Share Permissions & UAC

**Goal:** Understand and configure NTFS file/folder permissions (including inheritance), Windows Share permissions, and the behavior and security implications of User Account Control (UAC).

**Resources:**

* **Windows Tools:** File Explorer (Properties > Security Tab > Advanced), Computer Management (`compmgmt.msc` > Shared Folders > Shares), User Account Control Settings (`UserAccountControlSettings.exe`), `icacls.exe` (command line).
* **Documentation:** Microsoft Docs on NTFS Permissions, Share Permissions, UAC.
* **Test Environment:** A Windows machine (VM recommended) with Administrator privileges. Create at least one additional standard test user account.

---

### 🔹 **Exercise 1: NTFS vs. Share Permission Interaction**

**Goal:** Observe how NTFS and Share permissions combine to determine effective permissions for network access.

**Instructions:**

1.  Create a folder on your test machine (e.g., `C:\TestData`).
2.  Create a text file inside it (`C:\TestData\testfile.txt`).
3.  Share the `TestData` folder with a specific share name (e.g., `DataShare`). Use Computer Management or File Explorer sharing options.
4.  Configure **Share Permissions** for `DataShare`: Grant your standard test user "Full Control".
5.  Configure **NTFS Permissions** for the `C:\TestData` folder (Security tab): Explicitly *Deny* "Write" permission for your standard test user, but ensure they have "Read" permission.
6.  From another machine on the network (or conceptually, logged in as the test user), try to access `\\<TestMachineName>\DataShare\testfile.txt`. Can you read the file? Can you write to/delete the file?
7.  Explain the observed behavior based on the rule that the *most restrictive* combination of Share and NTFS permissions applies.

---

### 🔹 **Exercise 2: Managing NTFS Inheritance**

**Goal:** Understand how NTFS permissions inheritance works and how explicit permissions and inheritance blocking affect access.

**Instructions:**

1.  Create a folder structure: `C:\ProjectX` containing a subfolder `ProjectX\Secrets` which contains `ProjectX\Secrets\confidential.docx`.
2.  Set specific NTFS permissions on the top-level `C:\ProjectX` folder (e.g., grant your test user Modify access). Verify that `Secrets` and `confidential.docx` inherit these permissions by default.
3.  Now, go to the Advanced Security Settings for the `ProjectX\Secrets` subfolder.
4.  Click "Disable inheritance" and choose "Convert inherited permissions into explicit permissions on this object."
5.  Remove the inherited entry granting Modify access to your test user for the `Secrets` folder. Add an explicit entry granting the test user only "Read & execute" permissions on `Secrets`.
6.  Check the permissions on `confidential.docx` again. What are they now? Check the permissions on `ProjectX` again (they should be unchanged).
7.  Explain how disabling inheritance affects permissions on the object and its children. Use the "Effective Access" tab in Advanced Security Settings for the `Secrets` folder to verify the test user's resulting permissions.

---

### 🔹 **Exercise 3: Exploring UAC Behavior**

**Goal:** Observe the effects of different User Account Control (UAC) levels on system operations requiring elevation.

**Instructions:**

1.  On your Windows test machine, open User Account Control Settings (`UserAccountControlSettings.exe`).
2.  Note the current UAC level.
3.  Perform an action that requires administrator privileges (e.g., open `cmd` and type `net session > nul` - requires elevation, open `regedit`, try installing simple software). Observe the UAC prompt behavior (e.g., dimmed screen prompt for credentials/confirmation).
4.  Lower the UAC level by one step. Click OK (this may require confirmation).
5.  Repeat the action requiring elevation from step 3. Did the prompt behavior change?
6.  Continue lowering the UAC level one step at a time and repeating the test action, observing the prompt changes until UAC is effectively off (not recommended).
7.  Return the UAC setting to the default level. Discuss the security implications of the different levels, especially the risks of disabling UAC or using lower settings.

---

### 🔹 **Exercise 4: Command-Line Permissions with `icacls`**

**Goal:** Practice viewing and modifying NTFS permissions using the `icacls` command-line utility.

**Instructions:**

1.  Create a test file: `echo "Test data" > C:\icacls_test.txt`.
2.  Open `cmd` or `PowerShell` **as Administrator**.
3.  View the current permissions: `icacls C:\icacls_test.txt`. Note the permissions listed for different users/groups (e.g., `(R)`=Read, `(W)`=Write, `(F)`=Full).
4.  Grant your standard test user Read permission: `icacls C:\icacls_test.txt /grant <TestUserName>:(R)`. Replace `<TestUserName>` with the actual username. Verify the change with `icacls` again and via the GUI Security tab.
5.  Explicitly Deny your test user Write permission: `icacls C:\icacls_test.txt /deny <TestUserName>:(W)`. Verify the change. What takes precedence, Grant or Deny?
6.  Remove the specific Deny entry: `icacls C:\icacls_test.txt /remove:d <TestUserName>`. Verify.
7.  Reset permissions to defaults (inherit from parent): `icacls C:\icacls_test.txt /reset`. Verify.
8.  **Challenge:** Use `icacls` to save the current permissions of a folder to a file (`/save aclfile`) and then restore them (`/restore aclfile`). When might this be useful?

---

### 🔹 **(Optional) Exercise 5: Researching UAC Bypass Techniques**

**Goal:** Understand conceptually how attackers might try to circumvent UAC protections.

**Instructions:**

1.  Research common UAC bypass techniques. Look for explanations of methods like:
    * Abusing auto-elevated executables (those that don't prompt).
    * DLL hijacking in the context of elevated processes.
    * Using scheduled tasks running with high privileges.
    * Exploiting specific privileged file operations.
2.  Choose one specific technique.
3.  Write a brief explanation (1-2 paragraphs) describing how the technique works conceptually to achieve privilege escalation without triggering the standard UAC prompt seen by the user.
4.  **Note:** The goal is conceptual understanding, **do not attempt to download or execute UAC bypass tools or exploits.** Focus on the mechanism described in reputable security research blogs or articles.

---