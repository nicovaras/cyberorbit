
## 📄 PDF: Topic 2 – Subtopic: OSINT & Passive Recon  
**Resource:** [Chapter 1 of “Open Source Intelligence Techniques” by Michael Bazzell](https://inteltechniques.com/book7.html) *(Use sample resources & tools mentioned freely online)*

---

### 🔹 **Exercise: Identify Subdomains Using Public Tools**

**Goal:** Discover subdomains of a given domain using passive OSINT techniques.  

**Instructions:**

- Choose a domain you like (e.g., `mozilla.org`, `hackerone.com`) — nothing sensitive.
- Use tools like [crt.sh](https://crt.sh), [SecurityTrails](https://securitytrails.com), and [DNSdumpster](https://dnsdumpster.com).
- Write down all subdomains you can find.
- Which tools find the most? Which ones disagree?

---

### 🔹 **Exercise: Google Dorks to Find Sensitive Files**

**Goal:** Use search engine tricks to discover misconfigured or exposed files on public domains.  

**Instructions:**

- Try `site:` searches combined with `filetype:`, `intitle:`, or `inurl:` operators.
- Use non-sensitive domains (e.g., `site:gov.uk filetype:pdf`, `intitle:index.of site:edu`)
- Can you find PDFs with exposed metadata or “index of” pages?
- Create a short list of your most interesting Dorks.

---

### 🔹 **Exercise: Extract Metadata from Local Files**

**Goal:** Reveal hidden metadata in local documents using ExifTool.  

**Instructions:**

- Download a public government PDF, image, or document (e.g. from `https://www.whitehouse.gov/briefing-room/`).
- Install [ExifTool](https://exiftool.org/).
- Run it on the file and examine the output.
- What unexpected fields or artifacts can you find?

---

### 🔹 **Exercise: Find Public AWS Buckets**

**Goal:** Discover open or misconfigured S3 buckets.  

**Instructions:**

- Pick a company name or domain name (e.g., `acme`, `xyzcorp`).
- Use a wordlist to generate potential bucket names (`acme-assets`, `xyzcorp-media`, etc.).
- Try accessing via browser or CLI (`http://<bucketname>.s3.amazonaws.com`)
- How many return errors vs. valid buckets?

---

### ✨ **Bonus: Automate Subdomain Discovery**

**Goal:** Write a Python script that uses a passive API to find subdomains.  

**Instructions:**

- Use the [SecurityTrails API (free tier)](https://securitytrails.com/corp-api) or [urlscan.io](https://urlscan.io/docs/api/)
- Input a domain name.
- Output all discovered subdomains in a clean format.
- Extra: Export as JSON.
