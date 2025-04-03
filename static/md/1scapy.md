## 🐍 Subtopic 1.7: (Optional Bonus) Introduction to Scapy for Packet Crafting

**Goal:** Get hands-on experience with Scapy, a powerful Python library for manipulating network packets, allowing you to build, send, sniff, and dissect custom packets. *Note: Packet sniffing and sending raw packets often requires root/administrator privileges.*

**Resources:**

* **Scapy:** [Official Documentation](https://scapy.readthedocs.io/en/latest/)
* **Privilege Requirements:** Running Scapy for sniffing/sending usually requires administrator rights (e.g., using `sudo python your_script.py` on Linux/macOS, or running as Administrator on Windows with Npcap installed).
* **Network Interface:** You may need to specify the correct network interface for sniffing/sending. Use `scapy.get_if_list()` or OS commands (`ip addr`, `ifconfig`, `ipconfig`) to find your active interface name.

---

### 🔹 **Exercise 1: Installation and Interactive Mode**

**Goal:** Install Scapy and explore its basic interactive features.

**Instructions:**

1.  **Setup:** Ensure you have Python and pip in your environment (preferably a `venv`).
2.  **Installation:** Install Scapy: `pip install scapy`
3.  **Windows:** You will also likely need Npcap: [Download Npcap](https://npcap.com/#download) (Install with "WinPcap API-compatible Mode").
4.  **Run Interactive:** Open a terminal *with administrator privileges* (`sudo scapy` or run terminal as Admin and type `scapy`).
5.  **Explore:**
    * Type `ls()` to see supported protocols.
    * Type `IP()` to see the default IP packet structure.
    * Type `IP().show()` for a detailed view.
    * Try `Ether()/IP(dst="1.1.1.1")/ICMP()`. Store it in a variable: `pkt = _`. Use `pkt.summary()` and `pkt.show()`.
6.  Exit the interactive shell (`exit()`).

---

### 🔹 **Exercise 2: Sniffing Network Traffic**

**Goal:** Use Scapy within a script to capture and display basic information about network packets.

**Instructions:**

1.  Write a Python script using Scapy. Remember to run it with administrator privileges.
2.  Define a simple function, say `packet_handler(packet)`, that takes a Scapy packet object as input and prints its summary (`packet.summary()`).
3.  Use the `sniff()` function from Scapy:
    * Pass your `packet_handler` function to the `prn` argument (`prn=packet_handler`).
    * Optionally, use `count=10` to capture only 10 packets.
    * Optionally, use `iface='YourInterfaceName'` to specify the network interface if Scapy doesn't pick the right one automatically.
    * Optionally, use a `filter` (BPF syntax) like `filter="icmp"` or `filter="port 53"` to capture only specific traffic.
4.  Run the script and generate some relevant traffic (e.g., ping a host, run `nslookup google.com`) to see your handler function print packet summaries.
5.  **Challenge:** Modify your `packet_handler` to display more details, e.g., check if the packet has IP and TCP layers (`packet.haslayer(IP)`, `packet.haslayer(TCP)`) and print source/destination IP/ports if they exist.

---

### 🔹 **Exercise 3: Crafting and Sending ICMP (Ping)**

**Goal:** Build an ICMP Echo Request packet from scratch using Scapy and send it, receiving the reply.

**Instructions:**

1.  Write a Python script (run with admin privileges).
2.  Construct an ICMP Echo Request packet destined for a reachable IP address (e.g., `1.1.1.1`, `8.8.8.8`, or your default gateway). Remember Scapy layers stack like directories: `Ether()/IP(dst="1.1.1.1")/ICMP()`. You might not need `Ether()` if sending directly via IP. Let Scapy fill in source IP/MAC or specify if needed.
3.  Use the `sr1()` function (Send/Receive 1 packet) to send your crafted packet and capture the first reply received. Assign the result to a variable (e.g., `reply = sr1(pkt, timeout=1, verbose=0)`). `verbose=0` suppresses Scapy's default output.
4.  Check if a reply was received (i.e., `reply` is not `None`).
5.  If a reply was received, print its summary (`reply.summary()`) or show its details (`reply.show()`).
6.  **Challenge:** Add some payload data to your ICMP packet (e.g., `ICMP()/"Hello Scapy"`). Check if the payload is present in the reply packet you receive.

---

### 🔹 **Exercise 4: Basic TCP SYN Scan Packet**

**Goal:** Understand the concept of SYN scanning by crafting and sending just the TCP SYN packet using Scapy. *Note: This is just sending the probe; interpreting responses accurately for a full scanner is more complex.*

**Instructions:**

1.  Write a Python script (run with admin privileges).
2.  Choose a target host and port known to be open (e.g., `google.com` port 80 or 443, or `scanme.nmap.org` port 80).
3.  Craft a TCP SYN packet: `IP(dst="target_ip")/TCP(dport=target_port, flags='S')`. (`'S'` stands for SYN flag).
4.  Use `sr1()` to send this packet and capture the reply, similar to the ICMP exercise (use a short timeout).
5.  Print the summary of the reply packet if received.
6.  **Observe:** What flags are set in the reply packet if the port is open (usually SYN-ACK - 'SA')? Try sending to a known *closed* port (e.g., port 81 on google.com). What flags are set in the reply then (usually RST-ACK - 'RA')?
7.  **Challenge:** Write a loop to send SYN packets to a small range of ports on a target host and print the flags observed in the replies, giving a basic indication of open/closed status based on SYN-ACK vs RST-ACK. *This is a simplified view of scanning.*

---

### 💡 **Project: Simple ARP Monitor**

**Goal:** Use Scapy to sniff ARP traffic on the local network and detect potential new devices or IP/MAC changes.

**Instructions:**

1.  Write a Python script (run with admin privileges).
2.  Create a dictionary or other structure to store known MAC-to-IP mappings observed on the network (e.g., `{'mac_address': 'ip_address'}`).
3.  Define a packet handler function `arp_monitor_callback(packet)`.
4.  Inside the handler:
    * Check if the packet is an ARP packet (`packet.haslayer(ARP)`).
    * Check if it's an ARP reply (`packet[ARP].op == 2`).
    * Extract the source MAC (`packet[ARP].hwsrc`) and source IP (`packet[ARP].psrc`).
    * Check your known mappings:
        * If the MAC address is new, print a message "New device detected: [IP] at [MAC]" and add it to your known mappings.
        * If the MAC address is known but the IP address associated with it is *different* from the stored one, print a warning "IP change detected for [MAC]: Old IP [stored_ip], New IP [packet_ip]" and update the mapping.
5.  Use `sniff()` with `filter="arp"` and `prn=arp_monitor_callback`, running indefinitely (`store=0`).
6.  Run the script. Observe ARP traffic on your network (connecting/disconnecting devices might generate some).
7.  **Portfolio Guidance:** Document this ARP monitor on GitHub. Explain what ARP is and why monitoring it can be useful for network awareness. Detail how to run the script (requires root/admin) and its limitations (only sees traffic the sniffing machine receives, passive).