## 🔑 Subtopic 5.7: Techniques for Data-at-Rest Encryption

**Goal:** Understand conceptual approaches (like Full Disk Encryption) and apply practical tools (like GPG and encrypted archives) to encrypt sensitive files and folders, protecting data confidentiality when stored.

**Resources:**

* **GnuPG (GPG):** `gpg` command documentation (`man gpg`), [GnuPG Website](https://gnupg.org/), [GnuPG Mini Howto](https://www.gnupg.org/documentation/howtos.html)
* **Archive Tools:** `zip` command (`man zip` - check for `-e` option), `7z` command (`man 7z` - check for `-p` and `-mhe` options) or GUI tools like 7-Zip.
* **FDE Concepts:** Articles explaining BitLocker (Windows) and LUKS (Linux). Search "How BitLocker Works", "Linux LUKS tutorial".
* **Keys:** Requires GPG key pair generated previously (Subtopic 5.4 / Exercise 3) for asymmetric encryption exercises.

**Test Environment / Tools Needed:**

* A command-line environment with `gpg` installed.
* Standard archive tools (`zip`/`unzip`, `7z`) installed.
* A text editor.
* Access to the internet for research.
* **(Optional)** GPG key pair generated in previous subtopics.

---

### 🔹 **Exercise 1: Symmetric File Encryption with GPG (`--symmetric`)**

**Goal:** Use GPG to encrypt and decrypt a file using a symmetric cipher secured by a passphrase.

**Instructions:**

1.  Create a sample file (`secret_data.txt`) with sensitive content.
2.  Use the `gpg` command with the `--symmetric` option to encrypt the file. You will be prompted to enter a passphrase twice. Use the default AES256 cipher if prompted.
    `gpg --symmetric --cipher-algo AES256 --output secret_data.gpg secret_data.txt`
    (The `--cipher-algo` might be optional if AES256 is default).
3.  This creates the encrypted file `secret_data.gpg`. Try to view its content (`cat secret_data.gpg` or open in text editor) - it should be unreadable binary or armored text.
4.  Decrypt the file using GPG. You will be prompted for the passphrase you set during encryption:
    `gpg --decrypt --output decrypted_data.txt secret_data.gpg`
    (or simply `gpg -o decrypted_data.txt secret_data.gpg`).
5.  Verify that `decrypted_data.txt` matches the original `secret_data.txt`.
6.  Try decrypting again but enter an incorrect passphrase. Observe the error message.
7.  **Challenge:** What key derivation function does GPG typically use when deriving a key from a passphrase for symmetric encryption? (Hint: Research GPG S2K - String-to-Key specifiers). How does this protect against brute-force attacks on the passphrase?

---

### 🔹 **Exercise 2: Asymmetric File Encryption with GPG (`--encrypt`)**

**Goal:** Use GPG with a recipient's public key to encrypt a file so that only the recipient (who holds the corresponding private key) can decrypt it.

**Instructions:**

1.  **Setup:** Ensure you have generated a GPG key pair (from Subtopic 5.4 or `gpg --full-gen-key`). You need your own public key ID or email address associated with it. For testing, you'll encrypt *to yourself*.
2.  Create another sample file (`confidential_report.txt`).
3.  Encrypt the file for a specific recipient using their GPG public key ID (use your own key ID/email for this test):
    `gpg --encrypt --recipient <Your_Key_ID_or_Email> --armor --output confidential_report.asc confidential_report.txt`
    (`--armor` makes the output ASCII, easier to view/share).
4.  Examine the `confidential_report.asc` file. Note the "BEGIN PGP MESSAGE" header.
5.  Decrypt the file using your GPG private key. You will be prompted for the passphrase protecting your private key:
    `gpg --decrypt --output report_decrypted.txt confidential_report.asc`
6.  Verify `report_decrypted.txt` matches the original.
7.  **Challenge:** Encrypt the file for *multiple* recipients simultaneously by adding multiple `--recipient` flags with different public key IDs (if you have access to other public keys or create another test key pair). How does GPG handle this internally? (Hint: Session key encryption wrapped with each recipient's public key).

---

### 🔹 **Exercise 3: Creating Encrypted Archives (`zip`/`7z`)**

**Goal:** Use common archiving tools to create password-protected archives for encrypting multiple files or folders, comparing methods.

**Instructions:**

1.  Create a test directory (`archive_test`) containing a few sample files.
2.  **Using `zip` (if available with encryption):**
    * Use the `zip` command with the encryption flag (`-e` or similar, check your version's `man zip`) to create a password-protected archive:
        `zip -e -r archive_test.zip archive_test/`
        (You will be prompted for a password).
    * Try to list or extract the contents without the password (`unzip -l archive_test.zip`, `unzip archive_test.zip`). It should fail or prompt for the password.
    * Extract the archive using the correct password: `unzip archive_test.zip` (enter password when prompted).
3.  **Using `7z` (Recommended for stronger encryption):**
    * Install `p7zip` or `7-Zip` if necessary.
    * Use the `7z` command to create an archive with AES-256 encryption (`-mhe=on` encrypts headers too):
        `7z a -t7z -mhe=on -p<YourPassword> archive_test.7z archive_test/`
        (**Note:** `-p` directly on the command line might expose password in history; omitting `-p` usually prompts interactively). Replace `<YourPassword>` with a strong password.
    * List (`7z l archive_test.7z`) or extract (`7z x archive_test.7z`) the archive, providing the password when prompted.
4.  Research the different encryption methods supported by `zip` (e.g., traditional ZipCrypto vs. AES) and `7z` (AES-256). Why is 7-Zip's AES encryption generally considered much stronger than traditional zip encryption?
5.  **Challenge:** Create an encrypted archive using one method. Try to open it using a different tool (e.g., open a `7z` archive with `unzip`, or vice-versa). Are the formats and encryption methods compatible?

---

### 🔹 **Exercise 4: Full Disk Encryption Concepts (BitLocker/LUKS)**

**Goal:** Understand the purpose, basic operation, and security considerations of Full Disk Encryption (FDE) technologies like Windows BitLocker and Linux LUKS. **(Conceptual & Research focused - No installation required)**

**Instructions:**

1.  Research Windows BitLocker:
    * What is its primary purpose?
    * What components does it encrypt (entire volume, specific partitions)?
    * How is the encryption key typically protected (e.g., TPM, startup key on USB, password/PIN)?
    * What is a "recovery key" and why is it essential?
2.  Research Linux Unified Key Setup (LUKS):
    * What is its primary purpose?
    * How does it typically integrate with the Linux boot process (e.g., prompting for passphrase at boot)?
    * What underlying encryption cipher is commonly used (dm-crypt/AES)?
    * How are keys managed (key slots, passphrases)?
3.  Compare BitLocker and LUKS conceptually. What are the main similarities and differences in their approach to FDE?
4.  Explain the primary threat model FDE protects against (e.g., offline attacks, stolen laptops/drives). Does FDE protect data from malware running *while* the operating system is booted and the disk is unlocked? Why or why not?
5.  **Challenge:** Research the role of the Trusted Platform Module (TPM) in conjunction with BitLocker or LUKS. How does a TPM enhance the security of key storage and protect against certain types of offline attacks (like evil maid attacks) compared to just using a passphrase?

---

### 💡 **Project: GPG Data Protection Workflow**

**Goal:** Document and potentially script a repeatable workflow for using GPG to protect sensitive data files using both signing and encryption.

**Instructions:**

1.  Define a scenario where a user needs to send a sensitive report file (`report.docx`) to a specific colleague securely. The requirements are:
    * The colleague must be sure the report came from the user (authenticity).
    * The colleague must be sure the report wasn't tampered with in transit (integrity).
    * Only the intended colleague should be able to read the report (confidentiality).
2.  Assume both the user and the colleague have exchanged GPG public keys and trust them.
3.  Document the sequence of GPG commands the *sender* needs to run to achieve all three goals (authenticity, integrity, confidentiality) for the `report.docx` file, sending the result(s) to the colleague. (Hint: You might need to sign first, then encrypt, or use combined commands).
4.  Document the sequence of GPG commands the *recipient* needs to run to verify the signature and decrypt the report.
5.  **(Optional Scripting Challenge):** Create separate Bash or Python scripts (`send_secure.sh`, `receive_secure.sh`) that automate these command sequences, taking filenames and recipient/sender key IDs as arguments.
6.  **Portfolio Guidance:** Create a Markdown document (`gpg_workflow.md`) on GitHub detailing the scenario, the security goals, and the step-by-step GPG commands (or script usage) for both sender and receiver. Explain *why* each step (signing, encrypting) contributes to the overall security goals. If scripted, include the scripts and usage instructions in the repository.


---