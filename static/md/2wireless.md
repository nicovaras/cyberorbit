## 📄 PDF: Topic 2 – Subtopic: Wireless Network Basics  
**Resource:** [Aircrack-ng Documentation](https://www.aircrack-ng.org/doku.php)  

---

### 🔹 **Exercise: Capture Wi-Fi Handshake Using Aircrack-ng**  
**Goal:** Capture the 4-way WPA2 handshake from your own home router.  

**Instructions:**  
- Use a VM with Wi-Fi passthrough or run directly on a compatible laptop.  
- Use `airmon-ng` to enable monitor mode on your wireless interface.  
- Run `airodump-ng` to scan for networks.  
- Lock onto your router and wait for a device to reconnect.  
- Capture the `.cap` file with the handshake.  
- Do not attempt to crack or access unknown networks.

---

### 🔹 **Exercise: Identify Local Wi-Fi Devices with Python**  
**Goal:** Detect devices in your Wi-Fi network using Python and `scapy`.  

**Instructions:**  
- Run a scan using `ARP` packets over your local subnet (e.g. `192.168.1.0/24`).  
- Collect IP and MAC addresses of all responding devices.  
- Display them in a table sorted by IP.  
- Extra: detect vendor from MAC prefix using a public API or database.

---

### 🔹 **Exercise: Analyze Wi-Fi Traffic Using Wireshark**  
**Goal:** Understand Wi-Fi protocol behavior by inspecting real packets.  

**Instructions:**  
- Capture traffic using monitor mode and open in Wireshark.  
- Filter for `wlan.fc.type_subtype == 0x08` (beacon frames).  
- Identify SSIDs, signal strengths, and BSSIDs.  
- Count how many unique networks and devices you can see.

---

### ✨ **Bonus: Visualize Wi-Fi Signal Coverage at Home**  
**Goal:** Build a heatmap of Wi-Fi strength in your apartment.  

**Instructions:**  
- Use a mobile phone app (like WiFiAnalyzer) or `iwconfig` on Linux to measure signal strength at different locations.  
- Draw or digitally sketch your apartment layout.  
- Record dBm values at different points.  
- Color-code zones by signal strength and plot a basic heatmap.
