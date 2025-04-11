## 🔑 Subtopic 5.2: Symmetric Encryption in Practice

**Goal:** Understand the principles of symmetric encryption (shared secret key), learn about common algorithms like AES, explore block cipher modes (ECB, CBC, GCM), and practice encryption/decryption using standard tools and libraries.

**Resources:**

* **OpenSSL Command Line:** `openssl enc` command documentation (`man openssl-enc`)
* **Python Library:** `cryptography` - [Fernet (High Level)](https://cryptography.io/en/latest/fernet/), [Hazmat (Low Level - AES)](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/)
* **Block Cipher Modes:** [Wikipedia Article](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation) (Focus on ECB, CBC, GCM concepts)
* **AES Overview:** [Wikipedia Article](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

**Test Environment / Tools Needed:**

* A command-line environment with `openssl` installed.
* Python 3 environment with the `cryptography` library installed (`pip install cryptography`).
* A sample BMP image file (e.g., Tux logo) for Exercise 2.
* An image viewer capable of attempting to render raw data (optional, for visual effect in Ex2).

---

### 🔹 **Exercise 1: Symmetric Encryption/Decryption with OpenSSL CLI**

**Goal:** Use the `openssl enc` command to encrypt and decrypt a file using AES with a password-derived key.

**Instructions:**

1.  Create a sample text file (`plaintext.txt`) with some secret content.
2.  Use the `openssl enc` command to encrypt the file using AES-256 in CBC mode. You will be prompted for a password, which OpenSSL uses to derive the key and IV.
    `openssl enc -aes-256-cbc -salt -pbkdf2 -in plaintext.txt -out ciphertext.enc`
    (The `-salt` and `-pbkdf2` options enhance key derivation security).
3.  Examine the `ciphertext.enc` file. Can you read the original content?
4.  Now, decrypt the file using the *same* password you provided during encryption:
    `openssl enc -d -aes-256-cbc -pbkdf2 -in ciphertext.enc -out decrypted.txt`
5.  Verify that `decrypted.txt` contains the original content of `plaintext.txt`.
6.  Try decrypting again but enter the wrong password when prompted. What happens?
7.  **Challenge:** Encrypt the file again, but this time use a different AES mode like GCM (`-aes-256-gcm`). Decrypt it. Research the primary security advantage of GCM mode over CBC mode (Hint: Authenticated Encryption - AEAD).

---

### 🔹 **Exercise 2: The ECB Penguin Problem (Why ECB is Bad)**

**Goal:** Visually demonstrate why the Electronic Codebook (ECB) mode is insecure for encrypting data with patterns.

**Instructions:**

1.  Obtain a simple bitmap image (`.bmp`) file with distinct areas of solid color (e.g., "tux.bmp").
2.  Use `openssl enc` to encrypt the BMP image using AES (e.g., AES-128) in **ECB mode**. You'll need to provide a key explicitly or use a password (note that OpenSSL might still derive a key/IV even for ECB, focus on the `-aes-128-ecb` part):
    `openssl enc -aes-128-ecb -nosalt -K $(openssl rand -hex 16) -iv 0000000000000000 -in tux.bmp -out tux_ecb.bmp.enc` (Provide a 16-byte hex key, IV is ignored but required by syntax for some versions)
    *Alternatively, handle password derivation if `-K` doesn't work:*
    `openssl enc -aes-128-ecb -pbkdf2 -in tux.bmp -out tux_ecb.bmp.enc` (Use a password)
3.  Use `openssl enc` to encrypt the *same* BMP image using AES-128 in **CBC mode**:
    `openssl enc -aes-128-cbc -pbkdf2 -in tux.bmp -out tux_cbc.bmp.enc` (Use the same password as step 2 if applicable)
4.  Open the original `tux.bmp` file in an image viewer.
5.  Try to open the encrypted files (`tux_ecb.bmp.enc`, `tux_cbc.bmp.enc`) directly in an image viewer that can handle raw data or rename them to `.bmp` (the header might be invalid, but you might see patterns).
6.  Compare the appearance (or raw data patterns) of the ECB-encrypted file versus the CBC-encrypted file. Can you still discern the outline or pattern of the original image in the ECB version? Why does this happen with ECB but not CBC?
7.  **Challenge:** Explain how CBC mode uses an Initialization Vector (IV) and chaining to prevent the pattern repetition seen with ECB.

---

### 🔹 **Exercise 3: Symmetric Encryption with Python `cryptography` (Fernet)**

**Goal:** Use the high-level `Fernet` recipe from the Python `cryptography` library for simple, secure symmetric encryption.

**Instructions:**

1.  Ensure the `cryptography` library is installed (`pip install cryptography`).
2.  Write a Python script.
3.  Import `Fernet` from `cryptography.fernet`.
4.  **Key Generation:** Generate a new Fernet key: `key = Fernet.generate_key()`. **Important:** Store this key securely! For this exercise, you can print it and hardcode it back into the script for decryption, but understand this is insecure for real applications.
5.  Create a `Fernet` instance using the key: `f = Fernet(key)`.
6.  Define a message (as bytes): `message = b"My secret message."`
7.  **Encrypt:** Encrypt the message: `encrypted_token = f.encrypt(message)`. Print the resulting token (it's URL-safe base64 encoded).
8.  **Decrypt:** Decrypt the token: `decrypted_message = f.decrypt(encrypted_token)`. Print the decrypted bytes.
9.  Verify the decrypted message matches the original.
10. **Challenge:** Try decrypting the token using a *different* Fernet key. What happens? What security feature does Fernet provide besides confidentiality? (Hint: It includes authentication/integrity checking).

---

### 🔹 **Exercise 4: Understanding Padding (Conceptual)**

**Goal:** Understand why padding is necessary for block ciphers when plaintext length isn't a multiple of the block size, and recognize common padding schemes.

**Instructions:**

1.  Research the block size for AES (it's 128 bits / 16 bytes).
2.  Consider encrypting the plaintext message "This is 15 bytes" (which is 15 bytes long) using AES in CBC mode. Why can't this be directly encrypted without modification?
3.  Research common padding schemes like PKCS#7 padding. How does PKCS#7 work? If you needed to pad the 15-byte message to a 16-byte block boundary using PKCS#7, what byte value would be added, and how many times?
4.  How does the receiving side know how many padding bytes to remove after decryption with PKCS#7?
5.  **Challenge:** Research "padding oracle attacks". Briefly explain how improper handling of padding errors during decryption in CBC mode can lead to vulnerabilities allowing an attacker to decrypt ciphertext without knowing the key.

---

### 💡 **Project: Secure Configuration File Encryptor/Decryptor**

**Goal:** Create a Python tool using the `cryptography` library to securely encrypt and decrypt a configuration file containing sensitive information.

**Instructions:**

1.  Design a simple configuration file format (e.g., JSON or INI) that might contain sensitive data like API keys or passwords. Create a sample `config.json` file.
2.  Write a Python script (`config_crypto.py`) using `argparse` that accepts modes (`--encrypt`, `--decrypt`), input file path (`--in`), output file path (`--out`), and password (`--password`).
3.  **Encryption (`--encrypt`):**
    * Read the input configuration file content.
    * Prompt for a password (or take from `--password`). **Do not hardcode passwords.**
    * **Secure Key Derivation:** Use `hashlib.pbkdf2_hmac` to derive a strong encryption key from the password (use a random salt and store/embed the salt alongside the ciphertext).
    * **Authenticated Encryption:** Use the `cryptography` library's AES-GCM mode (low-level "hazmat" interface) to encrypt the configuration data using the derived key. You'll need to generate a random nonce/IV for GCM.
    * Store the salt, nonce/IV, and the resulting ciphertext (and GCM tag) together in the output file (e.g., in a JSON structure or concatenating bytes).
4.  **Decryption (`--decrypt`):**
    * Read the encrypted file, extracting the salt, nonce/IV, ciphertext, and tag.
    * Prompt for the password.
    * Re-derive the *same* encryption key using the *stored salt* and the provided password via PBKDF2HMAC.
    * Use AES-GCM to decrypt and *verify* the ciphertext using the derived key, nonce/IV, and tag. The GCM verification step is crucial.
    * If decryption and verification succeed, write the original configuration data to the output file. If not, report an error (authentication failed/wrong password).
5.  **Portfolio Guidance:** Host your script on GitHub. Include a `README.md` explaining how to use it for encrypting/decrypting config files, the cryptographic primitives used (PBKDF2, AES-GCM), the importance of password security, and the format of the encrypted file (how salt/IV/tag are stored). Include `requirements.txt` (`cryptography`).

---