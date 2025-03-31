## 📄 PDF: Topic 2 – Subtopic: Active Network Attacks (Ethical)  
**Resource:** [Kali Linux Revealed – Chapter 10: Network Scanning & Attacks](https://kali.training/downloads/Kali-Linux-Revealed-1st-edition.pdf)  
⚠️ *All exercises must be done in a local VM or lab environment only.*  

---

### 🔹 **Exercise: Simulate a SYN Flood Attack (locally)**  
**Goal:** Understand how a denial-of-service attack works by sending a high number of TCP SYN packets to a local service.  

**Instructions:**  
- Use `hping3` inside a Kali VM.  
- Choose a safe local IP and port (e.g., another VM’s port 80 with no active service).  
- Send a burst of SYN packets using `hping3 -S`.  
- Observe the CPU and network impact in real time using `htop` and `iftop`.  
- Bonus: try setting a rate limit and compare effects.

---

### 🔹 **Exercise: Perform ARP Spoofing in a Controlled Lab**  
**Goal:** Trick a local device into routing its traffic through your machine.  

**Instructions:**  
- Create two VMs on the same virtual network.  
- Install `arpspoof` or `ettercap` on your attack VM.  
- Enable IP forwarding.  
- Spoof the ARP table of your victim VM to reroute traffic.  
- Run Wireshark on your attacker VM and capture the victim's HTTP requests.

---

### 🔹 **Exercise: MITM HTTP Traffic Using Ettercap**  
**Goal:** Intercept HTTP communication between two devices.  

**Instructions:**  
- Set up a small local site on one VM (`python3 -m http.server`).  
- Use `ettercap -G` to launch a graphical MITM attack between victim and gateway.  
- Intercept HTTP GET/POST requests from the victim to the test server.  
- Identify credentials or data in transit.  
- Try modifying a response (HTML injection).

---

### 🔹 **Exercise: DNS Spoofing in a Virtual Lab**  
**Goal:** Redirect DNS queries to a fake site.  

**Instructions:**  
- Set up `dnschef` or `ettercap` in DNS spoofing mode.  
- Configure your victim VM to use your attacker VM as its DNS resolver.  
- Spoof a domain like `test.local` or `labsite.com` and redirect it to your own IP.  
- Host a fake site and verify the redirection in the victim’s browser.  

---

### 🕹️ **Lab: TryHackMe – Network Exploitation Basics**  
**Instructions:**  
- Go to [Network Exploitation Basics Room](https://tryhackme.com/room/networkexploitationbasics).  
- Complete the packet sniffing, spoofing, and MITM modules.  
- Take notes on tools used, attack vectors, and defenses mentioned.

