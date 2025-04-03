## 🌐 Subtopic 2.7: (Optional Bonus) Introduction to Wireless Networking Concepts

**Goal:** Gain a foundational understanding of WiFi standards, security mechanisms (WEP, WPA/WPA2/WPA3), and basic wireless reconnaissance tools. *Practical exercises require a compatible wireless network adapter capable of monitor mode.*

**Resources:**

* **WiFi Security Overview:** [Articles/videos comparing WEP, WPA, WPA2, WPA3](https://www.cloudflare.com/learning/security/wireless-security/wpa-vs-wpa2-vs-wep/)
* **Aircrack-ng Suite:** [Documentation](https://www.aircrack-ng.org/doku.php) (Focus on `airmon-ng`, `airodump-ng`)
* **Wireless Adapter:** A USB WiFi adapter known to support monitor mode and packet injection on your OS (e.g., Alfa AWUS036 series, Panda PAU09 - check compatibility lists online).
* **Operating System:** Linux (like Kali, Parrot) often has the best driver support for monitor mode. Windows requires specific drivers/tools (like Npcap for Wireshark sniffing, Acrylic WiFi for scanning).

---

### 🔹 **Exercise 1: WiFi Security Theory Comparison**

**Goal:** Research and articulate the differences and evolution of WiFi security protocols.

**Instructions:**

1.  Research the following WiFi security protocols: WEP, WPA (TKIP), WPA2 (CCMP/AES), WPA3 (SAE).
2.  For each protocol, identify:
    * The encryption algorithm(s) used.
    * The authentication method(s) used.
    * Key known vulnerabilities or weaknesses.
    * Its general security standing today (e.g., broken, weak, secure, recommended).
3.  Summarize your findings in a clear comparison table or short descriptive paragraphs.
4.  **Challenge:** What is the "WPA Handshake" (4-way handshake)? Why is capturing it important for attacking WPA/WPA2 networks (conceptually)?

---

### 🔹 **Exercise 2: Discovering Local WiFi Networks**

**Goal:** Use standard operating system tools to list nearby wireless networks and identify their basic properties.

**Instructions:**

1.  Use the appropriate command for your operating system to scan for wireless networks:
    * **Windows:** `netsh wlan show networks mode=bssid`
    * **Linux:** `sudo iwlist <interface> scan` (replace `<interface>` with your wireless interface name, e.g., wlan0) or use Network Manager GUI/CLI.
    * **macOS:** Hold `Option` key and click the WiFi icon in the menu bar, or use `sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s`.
2.  Analyze the output. For several nearby networks, identify:
    * SSID (Network Name).
    * BSSID (Access Point MAC Address).
    * Signal Strength / Quality.
    * Channel.
    * Security/Authentication Type (e.g., WPA2-Personal, WPA3, Open).
3.  **Challenge:** Can you determine if a network is operating on the 2.4 GHz band or the 5 GHz band based on the channel number listed? (Research typical channel ranges for each band).

---

### 🔹 **(Monitor Mode Required) Exercise 3: Scanning with `airodump-ng`**

**Goal:** Use `airodump-ng` to passively discover WiFi networks and associated clients by capturing beacon and probe frames. **Requires a compatible adapter in monitor mode.**

**Instructions:**

1.  **Setup:**
    * Plug in your compatible USB WiFi adapter.
    * Identify its interface name (e.g., `wlan0`, `wlan1`).
    * Put the adapter into monitor mode. On Linux with Aircrack-ng suite: `sudo airmon-ng start <interface>`. Note the new monitor interface name (e.g., `wlan0mon`).
2.  **Scan:** Run `airodump-ng` on the monitor interface: `sudo airodump-ng <monitor_interface>` (e.g., `sudo airodump-ng wlan0mon`).
3.  Observe the output:
    * **Top Section:** Lists Access Points (APs) detected (BSSID, Power, Beacons, Data, Channel, Encryption, ESSID).
    * **Bottom Section:** Lists Clients associated with APs (Station MAC, BSSID it's connected to, Power, Packets).
4.  Let it run for a few minutes to populate the lists. Press `Ctrl+C` to stop.
5.  **Challenge:** How does `airodump-ng` determine the "Encryption" type listed (WEP, WPA, WPA2)? (Hint: It analyzes beacon frames and probe responses).

---

### 🔹 **(Monitor Mode Required) Exercise 4: Targeting a Specific Network**

**Goal:** Focus `airodump-ng` on a specific access point and observe client interactions. **Only target networks you own or have explicit permission to test.**

**Instructions:**

1.  Run `airodump-ng` (as in Exercise 3) briefly to identify the BSSID and Channel of your target network (e.g., your home network).
2.  Stop the general scan (`Ctrl+C`).
3.  Run `airodump-ng` again, but this time target the specific network:
    `sudo airodump-ng --bssid <Target_BSSID> --channel <Target_Channel> <monitor_interface>`
    (e.g., `sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF --channel 6 wlan0mon`)
4.  Observe the client list (bottom section). You should see only clients connected to your target BSSID.
5.  Optional: If you want to capture data (including potentially the WPA handshake if a client connects/reconnects), add the `-w <output_prefix>` flag:
    `sudo airodump-ng --bssid <Target_BSSID> --channel <Target_Channel> -w capturefile <monitor_interface>`
    This will create `capturefile-XX.cap` files containing the raw packet data.
6.  **Challenge:** While running the targeted `airodump-ng`, disconnect and reconnect a device (e.g., your phone) from the target WiFi network. Did you see any specific messages or packet counts change significantly in the `airodump-ng` output related to that device? If you were capturing with `-w`, examine the resulting `.cap` file in Wireshark – can you find EAPOL packets related to the handshake?

---