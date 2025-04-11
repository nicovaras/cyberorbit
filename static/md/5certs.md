## 🔑 Subtopic 5.5: PKI, Certificates & Trust Chains

**Goal:** Understand the components and concepts of Public Key Infrastructure (PKI), the structure of X.509 digital certificates, certificate authorities (CAs), and how trust chains are validated.

**Resources:**

* **Concepts:** [Cloudflare Learning: What is PKI?](https://www.cloudflare.com/learning/ssl/what-is-public-key-infrastructure/), [Wikipedia X.509](https://en.wikipedia.org/wiki/X.509)
* **Tools:** `openssl x509` command (`man openssl-x509`), `openssl verify` (`man openssl-verify`), Web Browser certificate viewer (click padlock icon).
* **Certificate Files:** Download certificates from websites (using browser export or `openssl s_client`), potentially create your own self-signed/CA certs (advanced project).

**Test Environment / Tools Needed:**

* A command-line environment with `openssl` installed.
* A modern web browser.
* Access to the internet to view websites and potentially download certificates.

---

### 🔹 **Exercise 1: Inspecting X.509 Certificates with OpenSSL**

**Goal:** Use OpenSSL to parse and examine the contents of digital certificates (like those used for HTTPS).

**Instructions:**

1.  Obtain a certificate file in PEM format (e.g., save the certificate from a website like `google.com` using your browser's certificate viewer export function, or use `openssl s_client` - see Subtopic 5.6). Save it as `server_cert.pem`.
2.  Use the `openssl x509` command to view the certificate details:
    `openssl x509 -in server_cert.pem -text -noout`
3.  Analyze the output and identify key fields:
    * **Version:** (e.g., v3)
    * **Serial Number:**
    * **Signature Algorithm:** (e.g., sha256WithRSAEncryption)
    * **Issuer:** (The entity that signed this certificate - the CA)
    * **Validity:** (Not Before, Not After dates)
    * **Subject:** (The entity the certificate identifies - e.g., the website)
    * **Subject Public Key Info:** (Algorithm - RSA/ECC, the public key itself)
    * **X509v3 Extensions:** (e.g., Key Usage, Extended Key Usage, Subject Alternative Name (SAN), Basic Constraints, Certificate Policies, CRL Distribution Points, Authority Information Access).
4.  Focus on the **Subject Alternative Name (SAN)** extension. Why is this extension crucial for modern HTTPS certificates covering multiple hostnames?
5.  **Challenge:** Find the "Authority Information Access" (AIA) extension. What information does it typically contain, and how is it used by clients during certificate validation (Hint: OCSP, CA Issuers)?

---

### 🔹 **Exercise 2: Understanding the Chain of Trust**

**Goal:** Visualize and understand how certificates link together to form a trust chain leading back to a root Certificate Authority (CA).

**Instructions:**

1.  Using your web browser, navigate to an HTTPS website (e.g., `https://www.google.com`, `https://github.com`).
2.  Click the padlock icon in the address bar and find the option to view the certificate details (steps vary by browser, e.g., "Connection secure" > "Certificate is valid" > Details/Hierarchy tab).
3.  Examine the certificate chain/path presented by the browser:
    * Identify the **End-entity certificate** (issued to the website itself).
    * Identify one or more **Intermediate CA certificates**. Note how the "Issued By" field of one certificate matches the "Issued To" (Subject) field of the certificate above it in the chain.
    * Identify the **Root CA certificate** at the top of the chain. Why is this certificate typically self-signed?
4.  How does your browser/OS know whether to trust the Root CA certificate? (Hint: Trusted Root CA store).
5.  Explain conceptually how the browser verifies the entire chain: It checks the signature on the end-entity cert using the intermediate's public key, then checks the signature on the intermediate cert using the root's public key, and finally checks if the root is in its trusted store.
6.  **Challenge:** Use `openssl s_client` (see Subtopic 5.6) or browser tools to download the end-entity certificate *and* the intermediate CA certificate(s) for a website as separate PEM files. Use `openssl verify -CAfile <intermediate_ca.pem> -untrusted <intermediate_ca.pem> <end_entity_cert.pem>` to attempt validation. (You might need to combine intermediate/root into one CAfile or use `-CApath`).

---

### 🔹 **Exercise 3: Certificate Authorities (CAs) and Trust**

**Goal:** Understand the role of Certificate Authorities (CAs) in the PKI ecosystem and the implications of trust. (Conceptual & Research focused)

**Instructions:**

1.  Research the function of a Certificate Authority (CA). What primary services do they provide? (e.g., verifying identity, issuing certificates, managing revocation).
2.  How does a typical CA verify the identity of an organization requesting an SSL/TLS certificate (e.g., for Domain Validation (DV), Organization Validation (OV), Extended Validation (EV) certificates)?
3.  Locate the list of trusted Root CAs stored in your web browser or operating system. (Search browser settings for "Certificates" or "Authorities"; OS certificate stores vary). Recognize some major CA names (e.g., Let's Encrypt, DigiCert, Sectigo, GoDaddy).
4.  What are the potential security risks if a CA is compromised or acts maliciously? (Hint: Issuing fraudulent certificates).
5.  What is the purpose of Certificate Transparency (CT) logs? How do they improve the security of the CA ecosystem?
6.  **Challenge:** What is a "self-signed" certificate? When might it be appropriate to use one (e.g., internal testing, specific non-web protocols)? Why do browsers show security warnings for self-signed certificates on public websites?

---

### 🔹 **Exercise 4: Certificate Revocation (CRL & OCSP)**

**Goal:** Understand why and how certificates might need to be revoked before their expiry date and learn about CRL and OCSP mechanisms. (Conceptual & Research focused)

**Instructions:**

1.  Research reasons why a digital certificate might need to be revoked before its "Not After" date. (e.g., private key compromise, change of information, cessation of operation).
2.  Explain the concept of a Certificate Revocation List (CRL). How is it typically distributed (via URL in certificate)? What information does it contain? What are the potential drawbacks of relying solely on CRLs (e.g., size, timeliness)?
3.  Explain the concept of the Online Certificate Status Protocol (OCSP). How does it allow a client (like a browser) to check the current revocation status of a single certificate in near real-time? What are potential privacy concerns with basic OCSP?
4.  What is "OCSP Stapling"? How does it improve the performance and privacy aspects of OCSP checking by having the web server periodically fetch and attach the OCSP response to the TLS handshake?
5.  Look back at the certificate details from Exercise 1 (`openssl x509 -text`). Can you find extensions related to CRL Distribution Points or OCSP (often under "Authority Information Access")?
6.  **Challenge:** What happens if a browser *cannot* reach the CRL or OCSP server specified in a certificate? Does it typically "fail open" (allow the connection) or "fail closed" (block the connection)? Discuss the security implications of this choice.

---

### 💡 **Project: Mini CA and Certificate Signing**

**Goal:** Use OpenSSL command-line tools to simulate a very basic Certificate Authority, generate a Certificate Signing Request (CSR), and sign the CSR to issue an end-entity certificate.

**Instructions:**

1.  **Create Root CA:**
    * Generate a private key for your Root CA: `openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out rootCA.key`
    * Create a self-signed Root CA certificate using the key (provide Subject details like CN=My Test Root CA): `openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem -subj "/CN=My Test Root CA"`
2.  **Create End-Entity Key & CSR:**
    * Generate a private key for the "website": `openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out website.key`
    * Create a Certificate Signing Request (CSR) for the website using its key (provide Subject details like CN=test.local): `openssl req -new -key website.key -out website.csr -subj "/CN=test.local"`
3.  **Sign the CSR with the Root CA:**
    * Use the Root CA key and certificate to sign the website's CSR, creating the website's certificate: `openssl x509 -req -in website.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out website.crt -days 500 -sha256`
4.  **Verification:**
    * View the website certificate: `openssl x509 -in website.crt -text -noout`. Check the Issuer and Subject fields.
    * Verify the website certificate against the Root CA certificate: `openssl verify -CAfile rootCA.pem website.crt`. It should return "OK".
5.  **Portfolio Guidance:** Document the steps and OpenSSL commands used in a Markdown file on GitHub. Explain the purpose of each step (CA key/cert, entity key/CSR, signing). Include the sample commands. This demonstrates practical understanding of the certificate lifecycle and OpenSSL tooling. **Emphasize this is for educational purposes and does not create real trusted certificates.** Add instructions on how someone could add the `rootCA.pem` to their system/browser trust store (for testing purposes only) to make the `website.crt` appear trusted locally.


---