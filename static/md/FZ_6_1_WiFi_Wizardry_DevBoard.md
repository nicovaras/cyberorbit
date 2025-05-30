## 🐬 Subtopic X.6.1: Wi-Fi Wizardry: Exploring with the Development Board

**Goal:** Learn to set up the Flipper Zero Wi-Fi Development Board, flash custom firmware like Marauder, perform basic Wi-Fi network scanning, and understand the capabilities and **extreme ethical/legal responsibilities** associated with Wi-Fi testing tools.

**Resources:**

* **Flipper Zero Wi-Fi Dev Board Documentation:** (Check official Flipper docs or Dev Board product page for setup)
* **Marauder Firmware:** [GitHub - justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder) (Read its documentation thoroughly)
* **ESP32 Flashing Tools:** ESPTool-PY, ESP Web Flasher (as recommended by Marauder docs).
* **Ethical Hacking & Wi-Fi Usage Laws:** CRITICAL to research and understand for your specific region. **Never test on networks you do not own or have explicit, written permission to test.**

**Test Environment / Tools Needed:**

* Flipper Zero device.
* Flipper Zero Wi-Fi Development Board (ensure it's the ESP32-S2 based version if using Marauder).
* Computer with USB port for flashing the Dev Board.
* MicroUSB cable for the Dev Board (typically).
* **Your OWN Wi-Fi network and devices for any active testing.**
* Internet access for firmware downloads and research.
* **Critical:** This subtopic involves tools that can be highly disruptive and illegal if misused. Proceed with extreme caution, understand all warnings, and strictly limit any active testing to your own isolated network.

---

### 🔹 **Exercise 1: Setting Up the Wi-Fi Dev Board & Flashing Marauder**

**Goal:** Prepare the Wi-Fi Dev Board and flash it with the Marauder firmware.

**Instructions:**
1.  Carefully connect the Wi-Fi Dev Board to your Flipper Zero (if designed for direct connection) or prepare it for standalone flashing via USB to your computer. Refer to the Dev Board's specific instructions.
2.  Download the latest release of the Marauder firmware (`.bin` file) compatible with your Dev Board version (e.g., for ESP32-S2).
3.  Follow the Marauder documentation instructions to flash the firmware onto the Dev Board using a recommended flashing tool (e.g., ESPTool-PY command line, or a web flasher if available for your board). This usually involves putting the ESP32 into bootloader mode.
    Example (conceptual for esptool.py): `esptool.py --port /dev/ttyUSB0 write_flash 0x10000 marauder.bin` (port and addresses will vary).
4.  Once flashed successfully, connect the Dev Board to the Flipper Zero (if not already).
5.  On the Flipper Zero, navigate to `GPIO` > `ESP32 WiFi Marauder` (or the FAP for controlling it). The Flipper should detect and interface with the Marauder firmware on the Dev Board.
6.  **Challenge:** If flashing fails, what are common troubleshooting steps? (e.g., checking serial port, ensuring bootloader mode, correct baud rate, correct firmware file for the ESP32 variant).

---

### 🔹 **Exercise 2: Wi-Fi Network Scanning with Marauder**

**Goal:** Use Marauder via the Flipper Zero interface to perform passive Wi-Fi network scanning (detecting APs and clients). **Only scan for networks; do not attempt to connect or interact actively unless it's your own test network.**

**Instructions:**
1.  With the Marauder FAP active on your Flipper Zero and connected to the Dev Board:
2.  Select a scan option like "Scan APs" or "Probe Sniff".
3.  Observe the list of Wi-Fi networks (Access Points - APs) detected in your vicinity. Note the information displayed:
    * SSID (Network Name)
    * BSSID (MAC Address of the AP)
    * Channel
    * RSSI (Signal Strength)
    * Security/Encryption Type (WPA2, WPA3, etc.)
4.  If using "Probe Sniff" or a similar client scanning function, observe if any client devices probing for networks are detected.
5.  **Challenge:** How can you use the "Select AP" feature in Marauder (if available) to focus sniffing or other functions on a specific BSSID (again, **only your own test AP**)?

---

### 🔹 **Exercise 3: Understanding Marauder's Capabilities (Conceptual & Ethical)**

**Goal:** Research the various functions offered by Marauder (e.g., Deauth, Beacon Spam, Probe Request Flooding) and understand their purpose in Wi-Fi testing, as well as their significant potential for misuse and legal consequences. **NO ACTIVE ATTACKS TO BE PERFORMED ON ANY NETWORK YOU DO NOT OWN.**

**Instructions:**
1.  Review the Marauder GitHub documentation and any available guides.
2.  List 3-4 different "attack" or "testing" functions Marauder provides (e.g., Deauthentication, Beacon Spam, Rick Roll Beacon, Probe Request Sniffing/Flooding).
3.  For each function listed:
    * Briefly explain what it does at a technical level (e.g., a deauth attack sends forged deauthentication frames).
    * Describe a *legitimate security testing scenario* where a penetration tester might use this function (with proper authorization) to assess network vulnerabilities.
    * Describe how this same function could be *misused* to cause disruption, violate privacy, or break laws.
4.  Reiterate the importance of **explicit, written permission** before using any active Wi-Fi testing tools on any network not personally owned by you and isolated for testing.
5.  **Challenge:** Some Wi-Fi attack tools can target specific client devices rather than just APs. Why is targeting individual clients potentially more disruptive or invasive?

---

### 🔹 **Exercise 4: Connecting Flipper to Wi-Fi (via Dev Board or Internal if future FW supports)**

**Goal:** (If supported by current Flipper firmware + Dev Board FAP combination) Attempt to connect the Flipper Zero itself to a Wi-Fi network using the Dev Board as the interface, for FAPs that might require internet connectivity.

**Instructions:**
1.  Research if your current Flipper firmware version, in conjunction with the Wi-Fi Dev Board and a specific FAP (e.g., a "WiFi Manager" FAP or similar), allows the Flipper Zero to connect as a client to a Wi-Fi network.
2.  If this functionality exists:
    * Navigate to the relevant FAP or settings menu on the Flipper.
    * Scan for available Wi-Fi networks.
    * Attempt to connect to **your own** Wi-Fi network by providing the SSID and password.
    * Verify if the Flipper successfully connects and obtains an IP address.
3.  If direct Wi-Fi client connectivity for the Flipper OS via the Dev Board is not a standard feature, discuss conceptually how the ESP32 on the Dev Board *could* be programmed (as a standalone project, separate from Marauder) to connect to Wi-Fi and potentially relay information to/from the Flipper via UART over GPIO.
4.  **Challenge:** What are some potential use cases for having the Flipper Zero itself connected to the internet via Wi-Fi (e.g., time synchronization, fetching data for FAPs, remote control - consider both benefits and security risks)?

---