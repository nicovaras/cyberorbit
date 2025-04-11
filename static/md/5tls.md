## 🔑 Subtopic 5.6: Analyzing TLS/SSL & SSH Handshakes

**Goal:** Apply knowledge of asymmetric cryptography and certificates to understand the key exchange and authentication steps within TLS/SSL (for HTTPS) and SSH secure communication protocols using analysis tools.

**Resources:**

* **Tools:** `openssl s_client` command (`man openssl-s_client`), Wireshark (`man wireshark`), Browser DevTools, `ssh` client, `ssh-keyscan`.
* **TLS Handshake Overview:** [Cloudflare Learning](https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/), [Illustrated TLS Connection](https://tls.ulfheim.net/)
* **SSH Protocol Overview:** [Wikipedia SSH article](https://en.wikipedia.org/wiki/Secure_Shell#Key_management)
* **Target Servers:** Any public HTTPS website (e.g., `google.com:443`, `github.com:443`), an SSH server you have access to (or `localhost` if running `sshd`).

**Test Environment / Tools Needed:**

* A command-line environment with `openssl` and an `ssh` client installed.
* Wireshark installed (requires appropriate privileges for packet capture).
* A modern web browser.
* Access to the internet or a local SSH server for testing connections.

---

### 🔹 **Exercise 1: Exploring TLS Connection Details with `openssl s_client`**

**Goal:** Use `openssl s_client` to connect to an HTTPS server, view the server's certificate chain, and inspect handshake details like protocol version and cipher suite negotiated.

**Instructions:**

1.  Open your terminal.
2.  Connect to a public HTTPS server using `openssl s_client`. The `-connect` option specifies host and port. Use `-servername` for SNI:
    `openssl s_client -connect google.com:443 -servername google.com -showcerts`
3.  Analyze the extensive output:
    * Look for the "Certificate chain" section. Identify the end-entity certificate and intermediate/root CA certificates.
    * Find the "SSL-Session" section. Identify the `Protocol` negotiated (e.g., TLSv1.2, TLSv1.3).
    * Identify the `Cipher` suite negotiated (e.g., `TLS_AES_256_GCM_SHA384`).
    * Look for information about session resumption (Session-ID, TLS Ticket).
4.  Run the command again, connecting to a different major HTTPS site (e.g., `github.com:443`). Compare the certificate chain, protocol, and cipher suite.
5.  **Challenge:** Use options like `-tls1_2` or `-no_tls1_3` with `s_client` to attempt to force specific TLS versions. Does the server allow negotiation to the specified version? Observe changes in the negotiated cipher suite list. What happens if you try to force an outdated version like `-ssl3` (it should fail)?

---

### 🔹 **Exercise 2: Visualizing TLS Handshake with Wireshark**

**Goal:** Use Wireshark to capture and visually inspect the sequence of messages exchanged during a TLS handshake.

**Instructions:**

1.  Start a Wireshark capture on your main network interface (requires privileges).
2.  Use a capture filter `tcp port 443` or apply a display filter `tls.handshake` after capturing.
3.  In your browser, navigate to a simple `https://` website (clear cache if needed to force a full handshake).
4.  Stop the capture shortly after the page starts loading.
5.  Apply the display filter `tls.handshake` if not already done.
6.  Examine the sequence of packets:
    * Identify the `Client Hello`. Expand its TLS record details. Look at the list of Cipher Suites offered and supported TLS version(s).
    * Identify the `Server Hello`. What Cipher Suite and TLS version did the server select?
    * Identify the `Certificate` packet(s) from the server.
    * Identify key exchange related packets (e.g., `Server Key Exchange`, `Client Key Exchange` in TLS 1.2; often part of encrypted extensions in TLS 1.3).
    * Identify the `Change Cipher Spec` and `Encrypted Handshake Message` packets.
7.  **Challenge:** Compare the handshake flow for a TLS 1.2 connection versus a TLS 1.3 connection (capture both if possible). How does TLS 1.3 reduce the number of round trips required compared to TLS 1.2?

---

### 🔹 **Exercise 3: Understanding SSH Host Key Verification**

**Goal:** Understand the purpose of SSH host keys and the process of verifying a server's identity on first connection to prevent Man-in-the-Middle attacks.

**Instructions:**

1.  Locate your SSH `known_hosts` file (usually `~/.ssh/known_hosts`). View its contents. What information is stored for each host entry?
2.  If you have an SSH server available you've *never* connected to before, or if you manually remove a known server's entry from `known_hosts` using a text editor:
    * Attempt to connect using the `ssh` command: `ssh username@hostname`
    * Carefully read the warning message: "The authenticity of host '[hostname]' can't be established. [...] Are you sure you want to continue connecting (yes/no/[fingerprint])?"
3.  Explain the security risk involved if you simply type `yes` without verifying the fingerprint through an independent, trusted channel (e.g., asking the admin, checking a known-good list).
4.  Type `yes`. Connect successfully. Check your `known_hosts` file again. Has the server's public key fingerprint been added?
5.  **Challenge:** Use `ssh-keyscan <hostname>` to fetch the public host keys from an SSH server. Then use `ssh-keygen -lf <(ssh-keyscan <hostname> 2>/dev/null)` to display the fingerprints of the fetched keys. Compare these fingerprints to the one presented by the `ssh` client during the first connection attempt. Do they match?

---

### 🔹 **Exercise 4: SSH Key-Based Authentication Flow Analysis**

**Goal:** Understand the conceptual steps involved when using an SSH key pair for passwordless login, focusing on the cryptographic operations.

**Instructions:**

1.  Ensure you have an SSH key pair generated (e.g., `~/.ssh/id_ed25519` and `id_ed25519.pub`).
2.  **Setup Recap:** Briefly describe the one-time setup step involving placing the *public key* onto the remote server's `~/.ssh/authorized_keys` file.
3.  **Authentication Process:** When you run `ssh user@host` using key authentication, explain the following conceptual exchange (research needed):
    * Does the client send its private key to the server? (No)
    * The server likely has the client's public key (from `authorized_keys`). It sends a random challenge (e.g., a nonce or session ID) to the client.
    * What does the client do with this challenge and its **private key**? (Hint: Digital Signature)
    * The client sends the result (the signature) back to the server.
    * What does the server do with the received signature, the original challenge data, and the client's **public key** to verify the client's identity?
4.  Why is this process secure against eavesdroppers (they don't see the private key) and replay attacks (the challenge is unique)?
5.  **Challenge:** Enable verbose output for an SSH key-based connection: `ssh -v user@host`. Analyze the debug messages related to authentication. Can you identify messages indicating the offering of public keys, the signing challenge/response ("sign_and_send_pubkey", "server_input_userauth_pk_ok"), and successful authentication?

---

### 🔹 **(Optional) Exercise 5: Comparing TLS Cipher Suites**

**Goal:** Investigate different TLS cipher suites and understand their components (key exchange, authentication, encryption, hashing).

**Instructions:**

1.  Use `openssl ciphers -v 'ALL:COMPLEMENTOFALL'` or visit a site like [SSL Labs Client Test](https://clienttest.ssllabs.com:8443/ssltest/viewMyClient.html) to see the list of cipher suites supported by your system/browser.
2.  Choose two different cipher suites reported by `openssl s_client` (Exercise 1) when connecting to different websites (e.g., one ECDHE-RSA-AESGCM based, one potentially older like TLS_RSA_WITH_AES_128_CBC_SHA).
3.  Research the components of each chosen cipher suite name:
    * Key Exchange algorithm (e.g., `ECDHE`, `RSA`). What is its purpose? Which provides Forward Secrecy?
    * Authentication algorithm (e.g., `RSA`, `ECDSA`). Whose identity is usually authenticated with this?
    * Symmetric Encryption algorithm (e.g., `AES128`, `AES256`, `CHACHA20`). What key size? What mode (GCM, CBC)?
    * Hashing/MAC algorithm (e.g., `SHA256`, `SHA384`). What is its role (integrity/authentication)?
4.  Compare the two cipher suites based on security