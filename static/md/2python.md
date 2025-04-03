## 🌐 Subtopic 2.6: Applying Python for Recon Automation

**Goal:** Integrate Python scripting capabilities (developed in Sprint 1) with networking and reconnaissance concepts to automate information gathering tasks and process results from tools like Nmap.

**Resources:**

* **Python Libraries:** `socket`, `requests`, `subprocess`, `argparse`, `ipaddress`, `xml.etree.ElementTree` (or `lxml`), `python-nmap` (optional library), `shodan` (optional library)
* **Your Previous Scripts:** Port scanner (Sprint 1, Subtopic 1.3), OSINT/passive recon knowledge (Subtopic 2.4)
* **Nmap XML Output:** Generate `-oX` output from Nmap scans.
* **APIs (Optional):** VirusTotal API, Shodan API (require free keys)

---

### 🔹 **Exercise 1: Python Banner Grabbing Scanner**

**Goal:** Enhance your previous Python port scanner to include basic banner grabbing for identified open ports.

**Instructions:**

1.  Refine your multi-threaded TCP port scanner project from Sprint 1 (Subtopic 1.3, Project).
2.  Modify the thread function that checks a port: If a connection *succeeds*, attempt to receive a small amount of data (e.g., 1024 bytes) from the socket immediately after connecting, using a short timeout (`socket.settimeout()`). This is the banner.
3.  Decode the received banner (if any) from bytes to a string (handle potential decoding errors).
4.  Store or print the banner information alongside the open port number.
5.  Test against `scanme.nmap.org` or other targets known to provide banners (e.g., FTP port 21, SMTP port 25 on some servers).
6.  **Challenge:** Implement very basic service identification based on common banner patterns (e.g., if banner starts with "SSH-", identify as SSH; if it contains "FTP", identify as FTP). Make this identification best-effort.

---

### 🔹 **Exercise 2: Automated Subdomain Enumerator**

**Goal:** Build a Python script to discover subdomains for a target domain using multiple techniques.

**Instructions:**

1.  Write a Python script that takes a domain name (e.g., `example.com`) as a command-line argument (`argparse`).
2.  Implement at least two passive subdomain discovery methods within the script:
    * **Method 1 (Web Scrape):** Use `requests` to query `crt.sh` (e.g., `https://crt.sh/?q=%.example.com`). Parse the HTML response (using `BeautifulSoup4` or basic string searching/regex) to extract subdomain names.
    * **Method 2 (API - Optional):** Use `requests` to query an API like VirusTotal (requires free API key and reading their API docs) or another public DNS aggregation service API.
    * **(Alternative Method) DNS Brute-Force:** Include an option to use a provided wordlist (e.g., `subdomains.txt`). For each word in the list, try to resolve `word.targetdomain.com` using `socket.gethostbyname()`. If successful, add it to the list. (Be mindful of DNS rate limits).
3.  Use a Python `set` to store unique subdomains found across all methods.
4.  Print the final list of unique subdomains.
5.  **Challenge:** Add basic error handling for network requests and rate limiting considerations if using APIs or brute-forcing. Allow the user to specify which methods to use via command-line flags.

---

### 🔹 **Exercise 3: Parsing Nmap XML Output**

**Goal:** Write a Python script to programmatically extract specific information from Nmap's XML output format.

**Instructions:**

1.  Run an Nmap scan against one or more hosts (e.g., `scanme.nmap.org` and your `localhost`) with service detection (`-sV`) and save the output in XML format (`-oX output.xml`).
2.  Write a Python script using `xml.etree.ElementTree` (built-in) or `lxml` (`pip install lxml`) to parse the `output.xml` file.
3.  Navigate the XML structure to:
    * Find all hosts (`<host>`) that are reported as "up".
    * For each "up" host, find all open ports (`<port>` with `<state state="open">`).
    * For each open port, extract the port number (`portid`), service name (`<service name=...`), and version (`<service version=...>` if available).
4.  Print the extracted information in a clear format (e.g., "Host: [IP] | Port: [PortID] | Service: [Name] | Version: [Version]").
5.  **Challenge:** Modify the script to specifically list all hosts that have port 22 open with a service name containing "OpenSSH".

---

### 🔹 **(Optional) Exercise 4: Interacting with Shodan API**

**Goal:** Use the official Shodan Python library to query the Shodan search engine programmatically.

**Instructions:**

1.  Get a free API key from your Shodan account page.
2.  Install the Shodan library: `pip install shodan`
3.  Write a Python script that initializes the Shodan API client using your key.
4.  Implement functionality to:
    * Perform a basic search using `api.search('query')` (e.g., search for `apache`). Print the number of results found and details for the first few results (IP, port, banner).
    * Look up details for a specific IP address known to be in Shodan using `api.host('ip_address')`. Print the open ports and vulnerabilities (if any listed).
5.  Explore other simple API calls available (check `shodan` library documentation).
6.  **Challenge:** Combine Shodan search with Nmap. Use Shodan to find hosts matching certain criteria (e.g., running a specific old version of a service), then feed those IPs into an Nmap scan (using `subprocess`) for deeper verification.

---

### 💡 **Project: Comprehensive Recon Script**

**Goal:** Create a unified Python script that performs multiple reconnaissance steps against a target and generates a structured report.

**Instructions:**
1.  Write a Python script that accepts a target domain or IP address via `argparse`.
2.  Integrate functionalities developed in previous exercises/sprints:
    * **Port Scanning:** Use your Python port scanner (Exercise 1) or wrap Nmap using `subprocess` (e.g., `nmap -sS -sV -T4 target`) to scan common ports. Parse the results (either your scanner's output or Nmap's XML).
    * **Subdomain Enumeration (if domain provided):** Use your subdomain enumerator script's logic (Exercise 2) to find subdomains.
    * **(Optional) WHOIS Lookup:** Use `subprocess` to run the `whois` command or a library if available. Parse basic info like Registrar and Name Servers.
    * **(Optional) Shodan Lookup:** If an API key is configured, perform a `shodan.host()` lookup for the target IP (or resolved IPs of domain/subdomains).
3.  Structure the script to run these steps sequentially.
4.  Collect the results from each step.
5.  Generate a final report, either printed to the console in a clean, readable format with sections for each recon step (Open Ports, Subdomains, WHOIS, etc.) or saved to a text file.
6.  **Portfolio Guidance:** Create a dedicated GitHub repository for this "Comprehensive Recon Script". Your `README.md` must be detailed:
    * Explain the script's purpose and the recon techniques it integrates.
    * Provide clear usage instructions (command-line arguments).
    * List all dependencies (`requirements.txt` including `requests`, `lxml`, potentially `shodan`, etc.).
    * Include example output.
    * **Crucially, add an ethical use disclaimer:** Emphasize that the script should only be used on targets where permission has been granted.

---