## 🔑 Subtopic 5.4: Digital Signatures for Authenticity & Integrity

**Goal:** Understand how digital signatures work using asymmetric key pairs (hashing then encrypting with a private key) and use tools like OpenSSL and GnuPG to create and verify signatures, ensuring message authenticity and integrity.

**Resources:**

* **Concepts:** [Wikipedia Digital Signature](https://en.wikipedia.org/wiki/Digital_signature)
* **Tools:** `openssl dgst` command (`man openssl-dgst`), GnuPG (`gpg`) command (`man gpg`), `sha256sum`
* **Keys:** Requires asymmetric key pairs generated previously (Subtopic 5.3) or generate new ones (RSA or ECC for OpenSSL, default GPG type).

**Test Environment / Tools Needed:**

* A command-line environment with `openssl` and `gpg` installed.
* Asymmetric key pairs (RSA or ECC for OpenSSL, GPG keys for GPG exercises) generated in Subtopic 5.3 or newly generated.
* A text editor.

---

### 🔹 **Exercise 1: Signing Data with OpenSSL `dgst`**

**Goal:** Use OpenSSL to create a digital signature for a file using an RSA or ECC private key.

**Instructions:**

1.  Create a sample data file (`message.txt`) containing "This message needs signing.".
2.  Ensure you have an RSA or ECC private key file (e.g., `private_rsa.pem` from Subtopic 5.3).
3.  Use the `openssl dgst` command to create a signature. This involves hashing the file (e.g., with SHA256) and then signing that hash with the private key:
    `openssl dgst -sha256 -sign private_rsa.pem -out message.sig message.txt`
4.  Examine the output file `message.sig`. This is the binary signature.
5.  Discuss: Why do we sign the *hash* of the message, rather than the entire message itself (especially for large files)?
6.  **Challenge:** Re-sign the file but use a different hashing algorithm (e.g., `-sha512`). Does the resulting signature file (`message_sha512.sig`) differ from the SHA256 signature?

---

### 🔹 **Exercise 2: Verifying Signatures with OpenSSL `dgst`**

**Goal:** Use OpenSSL and the corresponding public key to verify the authenticity and integrity of a signed file.

**Instructions:**

1.  You need the original file (`message.txt`), the signature file (`message.sig` from Ex1), and the **public key** corresponding to the private key used for signing (e.g., `public_rsa.pem` derived in Subtopic 5.3).
2.  Use the `openssl dgst` command to verify the signature:
    `openssl dgst -sha256 -verify public_rsa.pem -signature message.sig message.txt`
3.  Observe the output. It should print "Verified OK" if the signature is valid for the file using that public key.
4.  **Test Failure Cases:**
    * Modify the `message.txt` file *slightly* (add a character) and try verifying again using the *original* signature (`message.sig`). What is the result?
    * Restore `message.txt`. Try verifying using a *different* public key file. What is the result?
    * Try verifying using the correct public key and message, but the signature generated with a different hash algorithm (e.g., `message_sha512.sig` from Ex1 challenge, while still using `-sha256` in the verify command). What happens?
5.  Explain what a successful verification proves about the message and its origin.

---

### 🔹 **Exercise 3: Signing and Verifying with GnuPG (GPG)**

**Goal:** Use the GnuPG suite to manage keys and create/verify digital signatures, often used for email and software package signing.

**Instructions:**

1.  **Setup:** If you don't have a GPG key pair, generate one: `gpg --full-gen-key` (follow prompts, choose RSA or ECC, set a passphrase). List your keys: `gpg --list-keys`, `gpg --list-secret-keys`.
2.  Create a sample data file (`gpg_message.txt`).
3.  **Create a Detached Signature:** Sign the file using your secret key. This creates a separate signature file (`.sig`).
    `gpg --detach-sign --armor -u <Your_Key_ID_or_Email> gpg_message.txt`
    (`--armor` creates an ASCII armored signature, `-u` specifies your key). You'll need your GPG passphrase. Note the `gpg_message.txt.asc` file created.
4.  **Verify the Signature:** Verify the signature using GPG. It automatically uses the public key associated with the signature (if available in your keyring).
    `gpg --verify gpg_message.txt.asc gpg_message.txt`
5.  Observe the output, looking for "Good signature from..."
6.  **Test Failure:** Modify `gpg_message.txt` slightly and try verifying again. What message do you get (e.g., "BAD signature")?
7.  **(Optional) Clear Signing:** Create a "clear signed" message where the signature is embedded within the text file itself: `gpg --clearsign -u <Your_Key_ID_or_Email> gpg_message.txt`. Examine the resulting `gpg_message.txt.asc` file. Verify it using `gpg --verify gpg_message.txt.asc`.
8.  **Challenge:** Export your GPG public key (`gpg --export --armor <Your_Key_ID> > my_pubkey.asc`). Imagine sending `gpg_message.txt` and `gpg_message.txt.asc` to someone else. What would they need (besides the files) to verify the signature? How would they import your public key (`gpg --import my_pubkey.asc`)?

---

### 🔹 **Exercise 4: Code Signing Concepts**

**Goal:** Understand the purpose and process of code signing as a practical application of digital signatures. (Conceptual & Research focused)

**Instructions:**

1.  Research how code signing is used for software distribution (e.g., Windows Authenticode, macOS Gatekeeper, signed Android APKs, signed Linux packages).
2.  Explain the main goals of code signing from both the developer's and the end-user's perspective. (Hint: Authenticity, Integrity).
3.  Describe the typical high-level process:
    * Who generates the public/private key pair?
    * How is the software vendor's identity typically verified (role of Certificate Authorities - CAs)?
    * How is the signature applied to the software package or installer?
    * How does the end-user's operating system verify the signature upon download or installation?
4.  What happens if the OS detects an invalid signature or a signature from an untrusted source?
5.  **Challenge:** What is "timestamping" in the context of code signing? Why is it important for validating signatures even after the signing certificate itself has expired?

---

### 💡 **Project: Sign and Verify a Script**

**Goal:** Create a workflow (possibly scripted) to digitally sign a script file and then verify its integrity before execution.

**Instructions:**

1.  Write a simple script (e.g., a Bash or Python script, `my_script.sh`).
2.  Use OpenSSL `dgst` (with your RSA/ECC key) or `gpg` (with your GPG key) to:
    * **Sign:** Create a detached signature for `my_script.sh` (e.g., `my_script.sh.sig` or `my_script.sh.asc`).
3.  Write a second "wrapper" script (`run_verified.sh`) that:
    * Takes the script name (`my_script.sh`) as an argument.
    * Automatically looks for the corresponding signature file (`my_script.sh.sig` or `.asc`).
    * Uses OpenSSL `dgst -verify` or `gpg --verify` to check if the signature is valid for the script file using the appropriate public key (you might hardcode the public key path or GPG key ID in the wrapper for simplicity).
    * If verification succeeds, it executes the original script (`bash my_script.sh`).
    * If verification fails (or signature/key is missing), it prints an error message and refuses to execute the script.
4.  Test the workflow: Verify it runs the script when unmodified. Modify the script slightly and verify the wrapper script now refuses to run it.
5.  **Portfolio Guidance:** Host both scripts (`my_script.sh` example, `run_verified.sh`) and instructions on GitHub. Explain the purpose (ensuring script integrity/authenticity), how to generate the 
required keys/signatures, and how to use the verification wrapper. Discuss limitations (e.g., assumes public key is trusted, wrapper script itself needs protection).

---