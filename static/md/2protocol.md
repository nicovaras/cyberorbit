## 📄 PDF: Topic 2 – Protocol Observation

**📚 Resource:**  
*“Wireshark 101: Essential Skills” – Chapter 1–3*  
[https://www.wireshark.org/docs/wsug_html_chunked/](https://www.wireshark.org/docs/wsug_html_chunked/)

---

### 🔹 Exercise: Use Wireshark to Capture Basic HTTP Traffic  
**Goal:** Watch unencrypted web requests live.  
**Instructions:**  
- Start Wireshark, filter: `http`  
- Visit `neverssl.com` (HTTP site)  
- Look at request/response headers, status codes  
- Export one request as raw text and write what it contains

---

### 🔹 Exercise: Identify Protocols in `.pcap`  
**Goal:** Recognize common protocols by behavior.  
**Instructions:**  
- Download a `.pcap` from malware-traffic-analysis.net  
- Open it in Wireshark  
- Identify 5 different protocols (e.g., DNS, TCP, ICMP, HTTP, ARP)  
- Count how many packets each one uses

---

### 🔹 Exercise: Follow TCP Streams and Extract Credentials  
**Goal:** Track sessions through packet data.  
**Instructions:**  
- Use `Follow TCP Stream` in Wireshark on an HTTP POST  
- Find a login or comment field  
- Extract any visible username/password  
- Explain why this isn’t secure (and how to fix it)

---

### 🔹 Exercise: Create a Basic `.pcap` Filter Cheatsheet  
**Goal:** Build a ready-to-use reference.  
**Instructions:**  
- Collect 5 useful filters (e.g., `http`, `ip.addr == 8.8.8.8`, etc)  
- Test each filter on a sample capture  
- Save in `pcap_filters.txt` for reuse

---

### ✨ Bonus: Create Your Own `tcpdump` Wrapper in Python  
**Goal:** Automate packet capture.  
**Instructions:**  
- Use `subprocess.run()` to call `tcpdump -i eth0 -w capture.pcap`  
- Add CLI args: interface, output name  
- Optional: Automatically open in Wireshark when done
