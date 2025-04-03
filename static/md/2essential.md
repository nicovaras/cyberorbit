## 🌐 Subtopic 2.2: Essential Protocols (DNS, DHCP, ARP)

**Goal:** Understand the function, operational steps, and potential security implications of fundamental protocols that underpin network infrastructure: DNS (Domain Name System), DHCP (Dynamic Host Configuration Protocol), and ARP (Address Resolution Protocol).

**Resources:**

* **Command Line Tools:** `dig`, `nslookup`, `arp` / `ip neigh` (Check man pages or help output)
* **DHCP DORA Process:** [Article explaining Discover, Offer, Request, Ack](https://www.geeksforgeeks.org/dynamic-host-configuration-protocol-dhcp/)
* **Sample PCAPs:** (You may need to find sample .pcap/.pcapng files online containing DHCP and ARP traffic, or generate your own using Wireshark/tcpdump)
    * Search: "sample dhcp pcap file", "sample arp pcap file" - e.g., [Wireshark Sample Captures](https://wiki.wireshark.org/SampleCaptures)

---

### 🔹 **Exercise 1: DNS Deep Dive with `dig`**

**Goal:** Use command-line tools to query DNS records and understand the information they provide.

**Instructions:**

1.  Open your command line/terminal.
2.  Use `dig` (preferred on Linux/macOS) or `nslookup` (available on Windows) for the following tasks:
    * Find the A record(s) (IPv4 addresses) for `www.google.com`.
    * Find the MX record(s) (Mail Exchanger) for `google.com`. What does the number next to the server name signify?
    * Find the NS record(s) (Name Server) for `google.com`. Who hosts Google's DNS?
    * Find any TXT record(s) for `google.com`. What kind of information is often stored in TXT records (e.g., SPF)?
3.  Analyze the output sections (Question, Answer, Authority, Additional).
4.  **Challenge:** Use `dig +trace google.com` (or equivalent lookup process) and describe the steps your resolver takes to find the IP address for `google.com`, starting from the root servers.

---

### 🔹 **Exercise 2: Decoding a DHCP Exchange**

**Goal:** Analyze the four steps of the DHCP DORA process by examining packet details.

**Instructions:**

1.  Obtain a sample Wireshark capture file (.pcap or .pcapng) containing a full DHCP (DORA) exchange. If you can't find one, you can try capturing traffic on your own network when a device joins (e.g., filter Wireshark on `bootp` or `udp port 67 or udp port 68`).
2.  Open the capture file in Wireshark.
3.  Filter for `bootp` protocol.
4.  Identify the four packets corresponding to Discover, Offer, Request, and Acknowledge.
5.  Examine the details of each packet in the sequence:
    * **Discover:** What is the source MAC? Destination MAC? Source IP? Destination IP? What IP address is requested (if any)?
    * **Offer:** Which server sends the offer? What IP address is offered? What is the lease duration? What gateway and DNS server IPs are offered?
    * **Request:** Which offered IP does the client formally request?
    * **Acknowledge:** What information does the server confirm in the final ACK?
6.  **Challenge:** What is the 'Transaction ID' field used for in DHCP? How does it help match requests and replies?

---

### 🔹 **Exercise 3: ARP Cache Investigation**

**Goal:** Understand how your local machine maps IP addresses to MAC addresses for communication on the local network segment.

**Instructions:**

1.  Open your command line/terminal.
2.  Execute `arp -a` (Windows/macOS/Linux) or `ip neigh show` (Linux) to display your system's current ARP cache/neighbor table.
3.  Identify the entry for your default gateway (find your gateway IP using `ipconfig` or `ip route`). What is its MAC address?
4.  Identify entries for other devices on your local network if any are present.
5.  Ping another device on your local network (if available) or ping your default gateway. Re-run the `arp -a` / `ip neigh show` command. Did any entries change or get added?
6.  **Challenge:** (Use caution) Find the command for your OS to clear the ARP entry for a *specific* IP address (e.g., your gateway). Clear it, then immediately try to ping that IP address again. Use Wireshark (filter `arp`) while doing this. Describe the ARP Request ('Who has IP X? Tell IP Y') and ARP Reply ('IP X is at MAC Z') packets you observe.

---

### 🔹 **(Optional) Exercise 4: DNS Zone Transfer Attempt (Ethical)**

**Goal:** Understand the concept and risk of DNS zone transfers by attempting one against a permissive target. **Warning:** Only perform AXFR queries against servers/domains you have explicit permission to test, or designated test targets. Unauthorized AXFR queries can be logged and may violate terms of service.

**Instructions:**

1.  Research DNS zone transfers (AXFR). Why are they useful for administrators? Why are they a security risk if misconfigured to allow public transfers?
2.  Research online for lists of domains/servers explicitly set up for *testing* zone transfers (e.g., `zonetransfer.me` is a known service for this). **Do not target random domains.**
3.  Using the test domain (e.g., `zonetransfer.me`), first find its Name Servers (NS records) using `dig ns zonetransfer.me`.
4.  Attempt a zone transfer using `dig AXFR @<nameserver_address> zonetransfer.me` (replace `<nameserver_address>` with one of the NS servers found).
5.  If successful, analyze the output. What kind of records and internal host information might be revealed in a zone transfer?
6.  **Challenge:** Write a simple shell script or Python script that takes a domain, finds its NS servers, and then attempts an AXFR query against each NS server for that domain. (*Remember the ethical use warning!*)

---