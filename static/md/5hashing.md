## 🔑 Subtopic 5.1: Hashing for Integrity & Passwords

**Goal:** Understand the properties of cryptographic hash functions (MD5, SHA families), use them for verifying data integrity, understand HMAC for authentication, and learn best practices for password hashing (salting, modern algorithms).

**Resources:**

* **Commands:** `sha1sum`, `sha256sum`, `md5sum` (Linux/macOS/WSL), `openssl dgst` (Multi-platform)
* **Python:** `hashlib` module documentation
* **Password Hashing:** [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
* **HMAC:** [RFC 2104](https://tools.ietf.org/html/rfc2104), [Wikipedia HMAC](https://en.wikipedia.org/wiki/HMAC)
* **Online Tools:** (Use for verification) Online hash generators, CyberChef.

**Test Environment / Tools Needed:**

* A command-line environment (Linux, macOS, WSL on Windows) with standard utilities like `md5sum`, `sha1sum`, `sha256sum`, and `openssl` installed.
* Python 3 environment for Python-based exercises.
* Access to the internet for research and online tool verification.

---

### 🔹 **Exercise 1: Calculating and Verifying Hashes**

**Goal:** Use command-line tools to compute cryptographic hashes (MD5, SHA-1, SHA-256) for files and verify file integrity.

**Instructions:**

1.  Create a simple text file (`testfile.txt`) with some content.
2.  Use command-line tools to calculate its hash using MD5, SHA-1, and SHA-256 (use `md5sum`/`sha1sum`/`sha256sum` or `openssl dgst`).
3.  Record the calculated hash values.
4.  Make a *very small* change to the content of `testfile.txt`.
5.  Recalculate the SHA-256 hash of the modified file. Compare it to the original SHA-256 hash. What property of hash functions does this demonstrate?
6.  Find an example online of a software download providing a checksum file (`.sha256`, `.md5`). Download both the software file and its checksum file. Use the appropriate command-line tool's check feature (e.g., `sha256sum -c checksumfile.sha256`) to verify the integrity of the downloaded file.
7.  **Challenge:** Explain why MD5 and SHA-1 are no longer recommended for security-critical applications like digital signatures or password hashing, even though they are still sometimes used for basic integrity checks. (Hint: Research "collision attacks").

---

### 🔹 **Exercise 2: Hashing with Python `hashlib`**

**Goal:** Use Python's built-in `hashlib` library to compute hashes programmatically.

**Instructions:**

1.  Write a Python script that takes a filename as a command-line argument (`argparse`).
2.  The script should open the file in binary read mode (`'rb'`).
3.  Read the file content (handle large files efficiently, e.g., read in chunks).
4.  Use the `hashlib` module to calculate the SHA-256 hash of the file content.
5.  Print the resulting hexadecimal hash digest.
6.  Verify the output of your script matches the output of the `sha256sum` command-line tool for the same file.
7.  **Challenge:** Modify the script to accept an optional second argument representing an expected hash value. The script should calculate the file's hash and compare it to the expected value, printing "Match" or "Mismatch".

---

### 🔹 **Exercise 3: Understanding HMAC for Message Authentication**

**Goal:** Learn how Hash-based Message Authentication Codes (HMAC) provide both integrity and authenticity using a shared secret key.

**Instructions:**

1.  Research the concept of HMAC (HMAC-SHA256 is common). How does it differ from a simple hash? What additional input does it require?
2.  Use the `openssl dgst` command with the `-hmac <key>` option to calculate the HMAC-SHA256 of a simple message string or file, using a secret key (e.g., `mysecretkey`):
    * `echo -n "message data" | openssl dgst -sha256 -hmac "mysecretkey"`
    * `openssl dgst -sha256 -hmac "mysecretkey" testfile.txt`
3.  Calculate the HMAC-SHA256 again using a *different* secret key (e.g., `otherkey`). Does the output change?
4.  Calculate the HMAC-SHA256 using the original key but modify the input message/file slightly. Does the output change?
5.  Explain how HMAC prevents a third party (who doesn't know the secret key) from modifying the message *and* recalculating a matching hash, thus providing authenticity in addition to integrity.
6.  **Challenge:** Use Python's `hmac` module along with `hashlib` to replicate the HMAC-SHA256 calculation from step 2 programmatically.

---

### 🔹 **Exercise 4: Exploring Password Hashing Concepts (Salt, Stretching)**

**Goal:** Understand why simply hashing passwords is insufficient and learn the importance of salting and key stretching algorithms (like bcrypt, scrypt, Argon2). **(Conceptual & Research focused)**

**Instructions:**

1.  **Hashing Weakness:** Calculate the SHA-256 hash of a common password like "password". Now imagine an attacker obtains a database dump containing SHA-256 hashes of user passwords. How could they use precomputed "rainbow tables" for SHA-256 to quickly find users with common passwords like "password"?
2.  **Salting:** Research what a cryptographic "salt" is in the context of password hashing. Explain how adding a *unique*, random salt to each user's password *before* hashing prevents attackers from using precomputed rainbow tables effectively.
3.  **Key Stretching:** Research algorithms like bcrypt, scrypt, or Argon2. What is "key stretching" or increasing the "work factor"? How do these algorithms make brute-forcing or dictionary attacks against password hashes much slower and more computationally expensive for attackers compared to simple fast hashes like SHA-256?
4.  Consult the OWASP Password Storage Cheat Sheet (linked in resources). What are the current recommendations for storing user passwords securely?
5.  **Challenge:** Use Python's `hashlib.pbkdf2_hmac` function (a key derivation function, related to stretching) or install the `bcrypt` library (`pip install bcrypt`). Generate a salted hash for a password using one of these methods. Observe the format of the resulting hash string – can you identify the salt and the work factor/iterations encoded within it?

---

### 💡 **Project: File Integrity Monitor**

**Goal:** Create a Python script that calculates and stores baseline hashes for files in a directory and later checks for modifications.

**Instructions:**

1.  Write a Python script (`integrity_monitor.py`) that takes a directory path and a mode (`--baseline` or `--check`) as command-line arguments.
2.  **Baseline Mode (`--baseline`):**
    * Recursively scan the specified directory.
    * For each file found, calculate its SHA-256 hash.
    * Store the filepath and its corresponding hash in a "baseline" file (e.g., `baseline.json` or `baseline.csv`) in a structured format. Overwrite any existing baseline file.
3.  **Check Mode (`--check`):**
    * Load the previously generated baseline file.
    * Recursively scan the specified directory again.
    * For each file found:
        * Calculate its current SHA-256 hash.
        * Compare the current hash to the hash stored in the baseline for that filepath.
        * Report any files that are:
            * **MODIFIED:** Present in baseline but hash differs.
            * **NEW:** Present in directory but not in baseline.
            * **MISSING:** Present in baseline but not in directory.
4.  Handle errors gracefully (e.g., baseline file not found in check mode, permission errors).
5.  **Portfolio Guidance:** Host your script on GitHub. Include a `README.md` explaining its purpose (detecting file changes), usage (baseline and check modes), the format of the baseline file, and potential use cases (simple intrusion detection, configuration monitoring). Discuss limitations (e.g., doesn't detect *what* changed, susceptible to baseline file tampering if not protected).

---