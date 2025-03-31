## 📄 PDF: Topic 2 – Network Fundamentals

**📚 Resource:**  
*“Computer Networking: A Top-Down Approach” – Chapters 1, 3 & 4 (Application, Transport & Network Layers)*  
💡Use [Stanford’s CS144 notes](https://cs144.github.io) for free summaries  
💡YouTube resource: [Hussein Nasser – Networking Basics Series](https://www.youtube.com/playlist?list=PLQnljOFTspQX8Gcg1nKyBa6U4bL3dR3fS)

---

### 🔹 Exercise: Simulate TCP Handshake Visually  
**Goal:** Internalize how TCP connects hosts.  
**Instructions:**  
- Draw the SYN → SYN-ACK → ACK sequence.  
- Use `tcpdump` or Wireshark to capture the real thing (`tcp.port == 80`)  
- Write which host sends each packet and what flags it uses.  
- Bonus: Capture a failed handshake (blocked port or dropped SYN).

---

### 🔹 Exercise: Deep DNS Resolution  
**Goal:** Follow the DNS lookup chain manually.  
**Instructions:**  
- Use `dig +trace openai.com`  
- Observe and list the recursive servers, root, TLD, and authoritative responses  
- Explain the role of each  
- Bonus: Change `/etc/resolv.conf` to a non-default resolver and test

---

### 🔹 Exercise: Map Traceroute as Graph  
**Goal:** Visualize how packets travel across networks.  
**Instructions:**  
- Run `traceroute 8.8.8.8`  
- Extract each hop’s IP  
- Use `ipinfo.io` to get geolocation  
- Draw the route as a graph (hand-drawn or `graphviz`)  
- Bonus: Do the same for `google.com` and compare

---

### 🔹 Exercise: Port Scanning Modes (Nmap + Theory)  
**Goal:** Understand the real difference between scan types.  
**Instructions:**  
- Run and compare:  
  - `nmap -sS` (SYN)  
  - `nmap -sT` (TCP connect)  
  - `nmap -sU` (UDP scan)  
- For each, capture traffic with Wireshark  
- Explain how the scan behaves and what packets are sent/received

---

### 🔹 Exercise: Decode ARP & MAC Behavior  
**Goal:** Understand Layer 2 devices and how ARP works.  
**Instructions:**  
- Run `arping` to ping a local device  
- Use `arp -a` and `ip neigh` to examine your ARP table  
- Clear the table and observe it rebuild live  
- Bonus: Poison your own ARP cache using a tool like `arpspoof` in a VM (be careful, offline only)

---

### 🔹 Exercise: Identify Protocols and Layers  
**Goal:** Associate protocols with OSI layers.  
**Instructions:**  
- Create a 3-column table: **Protocol**, **Layer**, **Purpose**  
- Fill in: TCP, UDP, DNS, ARP, ICMP, HTTP, TLS, DHCP, etc.  
- Save as `network_protocols_by_layer.md`  
- Bonus: Add tools used to observe or manipulate each one

---

### ✨ Bonus: Build a Ping Flood Simulation (Safe)  
**Goal:** See how traffic overload affects latency.  
**Instructions:**  
- Use `ping -f` on localhost or test VM  
- Monitor CPU and network with `htop` and `iftop`  
- Write down how the system responds  
- Optional: Run `ping` with `-i 0.2` to simulate different flood rates

---

### ✨ Bonus: Identify Firewall Blocking Behavior  
**Goal:** Understand what "filtered" really means in scans.  
**Instructions:**  
- Run `nmap -p 22,23,80,443 scanme.nmap.org`  
- Compare results with and without `-Pn`  
- Try the same from a cloud instance with different outbound rules  
- Document what "filtered", "closed", and "open" actually look like

