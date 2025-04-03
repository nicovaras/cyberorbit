## 🌐 Subtopic 2.3: Packet Analysis with Wireshark

**Goal:** Develop practical skills using Wireshark to capture, filter, and interpret network traffic, focusing on understanding common protocols and conversations.

**Resources:**

* **Wireshark:** [Download](https://www.wireshark.org/download.html)
* **Wireshark Display Filters:** [Reference Sheet](https://wiki.wireshark.org/DisplayFilters), [Cheat Sheet](https://www.comparitech.com/net-admin/wireshark-cheat-sheet/)
* **Sample Captures:** [Wireshark Wiki Samples](https://wiki.wireshark.org/SampleCaptures) (Download relevant captures like HTTP, DNS, TCP)
* **Your Own Traffic:** Generate traffic by Browse, pinging, etc.

---

### 🔹 **Exercise 1: Capture, Filter, Isolate**

**Goal:** Practice the basic workflow of capturing live traffic and using display filters to find specific packets.

**Instructions:**

1.  Launch Wireshark and select your primary network interface (e.g., Ethernet, Wi-Fi).
2.  Start a capture (click the shark fin icon).
3.  Generate some network traffic:
    * Open a web browser and visit a simple **HTTP** website (if you can find one, e.g., `http://info.cern.ch/` or `http://neverssl.com/`). If not, HTTPS is fine, but some analysis will differ.
    * Open a command prompt and `ping google.com`.
    * Perform a DNS lookup using `nslookup tryhackme.com` or `dig tryhackme.com`.
4.  Stop the Wireshark capture after a minute or two.
5.  Use the display filter bar at the top to apply the following filters one by one, observing the results:
    * `ip.addr == <IP_address_of_google.com>` (Replace with the actual IP you pinged)
    * `tcp.port == 80` (or `tcp.port == 443` if you only used HTTPS)
    * `dns`
    * `icmp`
6.  **Challenge:** Combine filters: Find only DNS requests (`dns.flags.response == 0`) originating from your machine's IP address (`ip.src == <your_ip>`).

---

### 🔹 **Exercise 2: Dissecting the TCP Handshake**

**Goal:** Analyze the sequence numbers, flags, and acknowledgments involved in establishing a TCP connection.

**Instructions:**

1.  Open a Wireshark capture file that contains TCP traffic (either one you captured or a sample from the Wireshark Wiki). Using an HTTP capture is often easiest.
2.  Find the start of a TCP conversation. A simple way is to filter for `tcp.flags.syn == 1 && tcp.flags.ack == 0` to find the initial SYN packet from a client.
3.  Select the SYN packet. Observe the source/destination ports, the Sequence Number (Seq), and that the SYN flag is set.
4.  Find the next packet in the conversation (usually the SYN-ACK from the server). Observe the Seq number, the Acknowledgment number (Ack - how does it relate to the client's initial Seq?), and the SYN and ACK flags being set.
5.  Find the third packet (usually the ACK from the client). Observe the Seq number, the Ack number (how does it relate to the server's Seq?), and that only the ACK flag is set.
6.  **Challenge:** Explain in your own words the purpose of the sequence and acknowledgment numbers in ensuring reliable data transfer in TCP.

---

### 🔹 **Exercise 3: Following Conversations**

**Goal:** Use Wireshark's features to reconstruct and view the application-layer data exchanged within a TCP session.

**Instructions:**

1.  Open a capture file containing **unencrypted HTTP** traffic (e.g., the `http.cap` sample from the Wireshark Wiki, or traffic you generated to an HTTP site).
2.  Apply a display filter for `http`.
3.  Find an HTTP GET request packet in the packet list.
4.  Right-click on that packet and choose "Follow" > "TCP Stream" (or HTTP Stream if available).
5.  A new window will pop up showing the reconstructed conversation. Observe:
    * The client's request (e.g., `GET /path HTTP/1.1`, Host header, User-Agent header, etc.).
    * The server's response (e.g., `HTTP/1.1 200 OK`, Content-Type header, Server header, followed by the actual HTML or content).
6.  Close the "Follow Stream" window.
7.  **Challenge:** Find a DNS query and its corresponding response in your capture. Can you "Follow" a UDP or DNS stream in the same way? Explore the options available for following different protocol types.

---

### 🔹 **Exercise 4: Exporting Transferred Files**

**Goal:** Learn how to extract files transferred over certain protocols directly from a packet capture using Wireshark.

**Instructions:**

1.  Obtain a capture file known to contain file transfers over HTTP (e.g., captures involving image downloads, CSS files, JS files). The `http.cap` sample or a capture of Browse a media-rich website might work.
2.  Open the capture in Wireshark.
3.  Go to "File" > "Export Objects" > "HTTP...".
4.  Wireshark will analyze the capture and list the HTTP objects (files) it detected.
5.  Select one or more objects from the list (e.g., a JPEG image or a text file).
6.  Click "Save As..." or "Save All..." to export the detected file(s) to your computer.
7.  Try opening the exported file(s) to verify they were reconstructed correctly.
8.  **Challenge:** Explore the other "Export Objects" options (e.g., IMF for email attachments, SMB for file shares). Can you find sample captures online for these protocols and try exporting objects from them?

---

### 🧪 **(Optional) Lab: Wireshark Fundamentals**

**Goal:** Practice Wireshark skills in a structured lab environment.

**Instructions:**

* Sign up or log in to [TryHackMe](https://tryhackme.com/).
* Complete the **[Wireshark: The Basics](https://tryhackme.com/room/wiresharkthebasics)** room.
* Pay close attention to filtering, TCP analysis, and protocol inspection tasks.

---