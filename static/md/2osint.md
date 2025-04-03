## 🌐 Subtopic 2.4: Passive Reconnaissance & OSINT

**Goal:** Master techniques for gathering intelligence about target systems, networks, and organizations using publicly available information sources without directly interacting with the target's infrastructure (Open Source Intelligence - OSINT).

**Resources:**

* **WHOIS Tools:** Command line `whois`, or web-based lookups (e.g., [ICANN Lookup](https://lookup.icann.org/))
* **Google Search Operators:** [Google Guide](https://support.google.com/websearch/answer/2466433), [Google Hacking Database (GHDB)](https://www.exploit-db.com/google-hacking-database)
* **Shodan:** [Shodan.io](https://www.shodan.io/) (Requires free account for basic searching)
* **Certificate Transparency:** [crt.sh](https://crt.sh/), [Censys](https://search.censys.io/certificates)
* **Passive Subdomain Tools:** [VirusTotal](https://www.virustotal.com/) (Domain search), [DNSdumpster](https://dnsdumpster.com/)
* **Target for Practice:** Use large, well-known organizations or platforms explicitly allowing security research/bug bounties (e.g., Google, Facebook, GitHub, HackerOne), or use `example.com` / `example.org`. **Act responsibly.**

---

### 🔹 **Exercise 1: Domain Ownership Trail**

**Goal:** Use WHOIS records to investigate domain registration details and potential contact points.

**Instructions:**

1.  Choose a target domain (e.g., `github.com`, `harvard.edu`).
2.  Use a WHOIS tool (command line or web) to look up the registration record for the chosen domain.
3.  Analyze the output. Identify:
    * Registrar information.
    * Registration, update, and expiration dates.
    * Registrant organization and contact details (often redacted or privacy-protected).
    * Administrative and Technical contact details (if available and not redacted).
    * Name Server (NS) records listed in the WHOIS data.
4.  Perform the same lookup for a domain in a different TLD (e.g., a `.io` domain, a country-specific domain like `.de` or `.uk`). Note any differences in the format or amount of information provided.
5.  **Challenge:** Some registrars offer "WHOIS History". Can you find a tool or service (some may require payment) that shows historical WHOIS records for a domain? What kind of information could historical data reveal?

---

### 🔹 **Exercise 2: Google Fu for Secrets**

**Goal:** Practice using Google Dorking techniques to uncover potentially sensitive information or specific types of resources related to a target.

**Instructions:**

1.  Choose a large organization suitable for educational searching (e.g., a major university, a large tech company). **Do not target small organizations or attempt to access sensitive data.**
2.  Formulate Google Dorks to try and find the following (replace `targetsite.com`):
    * Login portals: `site:targetsite.com intitle:"login" | inurl:"login"`
    * Specific document types: `site:targetsite.com filetype:pdf "internal report"` (use generic terms)
    * Potentially exposed configuration files: `site:targetsite.com filetype:yml | filetype:conf | filetype:cfg -github.com` (Exclude common code repos)
    * Subdomains: `site:*.targetsite.com -www`
    * Error messages: `site:targetsite.com "SQL syntax error" | "warning:"`
3.  Analyze the search results. Understand *why* certain results appear based on your query. **Do not click on or download anything suspicious.**
4.  **Challenge:** Explore the Google Hacking Database (GHDB) linked in resources. Find 3 dorks listed there for finding potentially interesting information (e.g., network devices, specific software exposures). Understand what type of information each dork targets. **Use extreme caution and ethical judgment if testing any GHDB dorks.**

---

### 🔹 **Exercise 3: Peeking with Shodan**

**Goal:** Utilize Shodan to discover internet-connected devices, open ports, and service banners associated with an organization or technology.

**Instructions:**

1.  Create a free account on [Shodan.io](https://www.shodan.io/).
2.  Use the Shodan search bar to explore:
    * Devices associated with an organization: `org:"Target Organization Name"` (e.g., `org:"Google LLC"`, `org:"Harvard University"`)
    * Specific technologies: `product:"Apache httpd"`, `port:"22" "OpenSSH"`
    * Devices in a specific geographic area: `country:"DE" city:"Berlin"`
    * Combine filters: `org:"Example Org" port:"80"`
3.  Analyze the search results. What information does Shodan provide for each device (IP, Hostname, ISP, Open Ports, Service Banners)?
4.  Click on a few results (related to large, known entities) to view the detailed information Shodan has collected.
5.  **Challenge:** Use Shodan filters to find devices with specific vulnerabilities (use the `vuln:` filter, e.g., `vuln:CVE-2021-44228` for Log4j - results may be limited now). How could this information be useful for both attackers and defenders?

---

### 🔹 **Exercise 4: Passive Subdomain Discovery**

**Goal:** Employ various online tools and techniques that passively gather subdomain information without sending packets directly to the target's nameservers.

**Instructions:**

1.  Choose a target domain (e.g., `tryhackme.com`, `github.com`).
2.  Use at least three different *passive* sources/tools to find its subdomains:
    * **VirusTotal:** Go to virustotal.com, select "Search", enter the domain name, and look at the "Relations" tab or details section for subdomains.
    * **crt.sh:** Enter the domain name (e.g., `%.example.com`) and search. Examine the results for unique subdomains listed in certificates.
    * **DNSDumpster:** Enter the domain name and analyze the results, particularly the DNS records map and collected hostnames.
3.  Compare the lists of subdomains found by each tool. Did they find different ones?
4.  Consolidate the findings into a single list of unique subdomains discovered passively.
5.  **Challenge:** Research other passive techniques. How might analyzing search engine results, examining HTML source code (for links), or analyzing historical DNS data contribute to passive subdomain discovery?

---

### 💡 **Project: OSINT Profile Compilation**

**Goal:** Gather and structure publicly available information about a chosen organization using various OSINT techniques.

**Instructions:**

1.  Select a **large, public organization** (e.g., a Fortune 500 company, a major university, a well-known tech platform) as your target for this exercise. **Focus only on information relevant to its technical infrastructure and online presence.**
2.  Using the techniques practiced in the exercises (WHOIS, Google Dorking, Shodan, Passive Subdomain tools, Certificate Transparency), gather information about the organization, including:
    * Primary domain(s).
    * Known subdomains.
    * Associated IP address ranges (if discoverable via WHOIS history, DNS A records for subdomains, or Shodan `org` searches).
    * Key technologies potentially in use (based on Shodan banners, server headers in DNS records, job postings - optional).
    * Public contact points related to technical infrastructure (e.g., abuse contact from WHOIS, security reporting email if found).
3.  Organize the gathered information into a structured report (e.g., a Markdown file). Use headings for different categories of information (Domains, IPs, Technologies, etc.).
4.  **Crucially, document the source/tool used to find each piece of information.**
5.  **Portfolio Guidance:** Create a GitHub repository for your OSINT report. The `README.md` should *clearly state* the target organization and emphasize that all information was gathered using *publicly available, passive techniques only*. Explain the purpose (demonstrating OSINT skills) and the tools/methods used. **Do not include any sensitive or non-public data.** The value is in the *process* and *structured presentation* of public info.

---