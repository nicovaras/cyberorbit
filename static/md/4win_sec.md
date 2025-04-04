## 🛡️ Subtopic 4.6: Windows Security Policy & Auditing Config

**Goal:** Configure critical local security settings related to accounts, user rights, and auditing using Windows policy editors and command-line tools to enhance system security posture.

**Resources:**

* **Windows Tools:** Local Security Policy (`secpol.msc`), Local Group Policy Editor (`gpedit.msc` - not available on Home editions), Event Viewer (`eventvwr.msc`), `auditpol.exe` (command line).
* **Microsoft Documentation:** Search for specific policy settings names on Microsoft Docs.
* **Test Environment:** Windows VM (Pro/Enterprise/Server edition recommended for `gpedit.msc`, non-domain joined for local policy focus). Administrator privileges required.

---

### 🔹 **Exercise 1: Enforcing Strong Password Policies**

**Goal:** Configure account password policies to meet security best practices using the Local Security Policy editor.

**Instructions:**

1.  Open Local Security Policy (`secpol.msc`).
2.  Navigate to `Account Policies` > `Password Policy`.
3.  Review the current settings.
4.  Configure the following policies to stricter values (document the values you choose):
    * Enforce password history (e.g., 24 passwords remembered).
    * Maximum password age (e.g., 60 days).
    * Minimum password age (e.g., 1 day).
    * Minimum password length (e.g., 14 characters).
    * Password must meet complexity requirements (Enabled).
    * Store passwords using reversible encryption (Ensure **Disabled** - this is critical).
5.  Navigate to `Account Policies` > `Account Lockout Policy`. Configure settings to lock out accounts after a small number of invalid attempts (e.g., 5 attempts) for a specified duration (e.g., 30 minutes).
6.  Explain the purpose and security benefit of each policy category you configured (Password Policy, Lockout Policy).

---

### 🔹 **Exercise 2: Managing User Rights Assignments**

**Goal:** Understand and modify which users or groups are granted specific system privileges using User Rights Assignment policies.

**Instructions:**

1.  Open Local Security Policy (`secpol.msc`).
2.  Navigate to `Local Policies` > `User Rights Assignment`.
3.  Review the list of user rights. Select and research the purpose of the following rights:
    * `Allow log on locally`
    * `Deny log on locally`
    * `Access this computer from the network`
    * `Change the system time`
    * `Shut down the system`
    * `Act as part of the operating system`
4.  Create a new local test user (`TestUserRights`) and add them to the standard `Users` group only.
5.  Modify the `Deny log on locally` policy and *add* your `TestUserRights` user to it. Apply the change.
6.  Try to log in directly to the machine console as `TestUserRights`. What happens? Remove the user from the deny policy.
7.  **Challenge:** Find the "Create symbolic links" right. By default, who has this right? Why might restricting this right be considered a security hardening step? (Hint: Research symbolic link attacks on Windows).

---

### 🔹 **Exercise 3: Configuring Auditing with `auditpol.exe`**

**Goal:** Use the command-line `auditpol` utility to enable detailed security auditing for specific event categories.

**Instructions:**

1.  Open `cmd` or `PowerShell` **as Administrator**.
2.  View the current audit policy settings for all categories: `auditpol /get /category:*`
3.  Enable auditing for specific subcategories useful for security monitoring (enable both Success and Failure where applicable):
    * `auditpol /set /subcategory:"Logon" /success:enable /failure:enable`
    * `auditpol /set /subcategory:"Special Logon" /success:enable`
    * `auditpol /set /subcategory:"Process Creation" /success:enable`
    * `auditpol /set /subcategory:"Security Group Management" /success:enable /failure:enable`
    * `auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable`
4.  Verify your changes using `auditpol /get /category:*` again or focusing on specific categories (e.g., `auditpol /get /category:"Logon/Logoff"`).
5.  **Challenge:** Disable auditing for a specific subcategory using `auditpol /set` with `/success:disable /failure:disable`. How could you back up the entire audit policy configuration using `auditpol /backup` and restore it using `auditpol /restore`?

---

### 🔹 **Exercise 4: Implementing File System Auditing (SACL)**

**Goal:** Configure specific files or folders to generate audit events when accessed, using System Access Control Lists (SACLs).

**Instructions:**

1.  First, ensure the relevant audit policy subcategory is enabled (requires admin privileges): `auditpol /set /subcategory:"File System" /success:enable /failure:enable`.
2.  Create a test folder (e.g., `C:\SensitiveData`) and a file inside it.
3.  Right-click the `C:\SensitiveData` folder, go to Properties > Security tab > Advanced > Auditing tab.
4.  Click "Continue" or provide admin credentials if prompted.
5.  Click "Add". Click "Select a principal" and choose the `Everyone` group (or a specific test user/group).
6.  Set "Type" to "All" (Success and Failure).
7.  Click "Show advanced permissions". Select permissions you want to audit, e.g., "Delete", "Change permissions", "Take ownership", "Write data / Append data". Click OK multiple times.
8.  Perform actions on the folder/file that should trigger the audit rules (e.g., try to delete the file, successfully write to the file, try to change permissions).
9.  Open Event Viewer (`eventvwr.msc`), navigate to `Windows Logs` > `Security`. Look for recent events related to Object Access, typically Event ID `4663` (An attempt was made to access an object) or `4656` (A handle to an object was requested). Examine the event details to see the user, object name, access requested, and whether it was successful.
10. **Challenge:** Modify the SACL to only audit *failed* attempts to *delete* objects in the folder by a specific *non-admin* test user. Verify that only failed delete attempts by that user generate audit logs.

---

### 🔹 **Exercise 5: Analyzing Security Event Logs**

**Goal:** Practice finding and interpreting key security events within the Windows Security Event Log.

**Instructions:**

1.  Ensure relevant auditing is enabled (from previous exercises, especially Logon, Process Creation, Account Management).
2.  Perform several actions: Log off and log back on. Create a new local user account (`net user testacct password /add`). Run a common command like `ipconfig`. Fail a login attempt deliberately.
3.  Open Event Viewer (`eventvwr.msc`) and navigate to the Security log.
4.  Use the "Filter Current Log..." action to find specific events:
    * **Successful Logon:** Event ID `4624`. Find your recent logon event. Examine details like Logon Type (e.g., 2=Interactive, 3=Network), Account Name, Source Network Address.
    * **Failed Logon:** Event ID `4625`. Find your failed attempt. Examine the Account Name and Failure Reason/Status Code.
    * **Process Creation:** Event ID `4688` (if enabled via Audit Policy or Sysmon). Find the `ipconfig.exe` execution. Note the Parent Process Name and Creator Process Name.
    * **User Account Created:** Event ID `4720`. Find the creation event for `testacct`. Who created the account?
5.  **Challenge:** Enable auditing for "Kerberos Authentication Service" and "Kerberos Service Ticket Operations" (Success/Failure). Perform actions in a domain environment (or research typical events) like accessing a network share. Look for Kerberos-related Event IDs (e.g., 4768, 4769, 4771). What information do they provide about ticket granting and authentication?

---