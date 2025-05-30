## 🐬 Subtopic X.4: The Universal Remote on Steroids: Infrared (IR) Magic

**Goal:** Master the Flipper Zero's Infrared (IR) capabilities to learn signals from existing remotes, replay them to control devices, and explore universal remote databases.

**Resources:**

* **Flipper Zero Infrared Documentation:** [docs.flipper.net/infrared](https://docs.flipper.net/infrared)
* **Universal Remote Databases:** Search "Flipper Zero IR Remote Database" (e.g., on GitHub), [IRDB.tk](https://irdb.tk/) (general IR codes)
* **Pronto Hex Codes:** Research "Pronto Hex IR codes" format.

**Test Environment / Tools Needed:**

* Flipper Zero device.
* Various standard IR remote controls (e.g., for TV, air conditioner, stereo, DVD player).
* Devices that are controllable by these IR remotes.
* Internet access for database lookups and research.

---

### 🔹 **Exercise 1: Learning IR Signals from Existing Remotes**

**Goal:** Use the Flipper Zero's "Learn New Remote" feature to capture and save IR signals from your physical remote controls.

**Instructions:**
1.  Navigate to `Infrared` > `Learn New Remote` on your Flipper Zero.
2.  Point an IR remote control (e.g., your TV remote) at the Flipper's IR port (top edge).
3.  Press a button on the physical remote (e.g., "Power", "Volume Up").
4.  The Flipper should indicate it has captured a signal and may show the decoded protocol and data.
5.  Assign a name to the button (e.g., `TV_Power`, `TV_VolUp`) and save it within a new or existing virtual remote on the Flipper.
6.  Repeat this process to learn and save several different buttons from one or two different physical remotes.
7.  **Challenge:** Some remotes use long press or multi-press signals that might be harder to capture or might be interpreted as multiple different signals by the Flipper. Try capturing a "long press" button. Does the Flipper capture it as one signal or multiple?

---

### 🔹 **Exercise 2: Sending and Organizing Saved IR Signals**

**Goal:** Test the IR signals you've learned and organize them effectively on the Flipper Zero.

**Instructions:**
1.  Navigate to `Infrared` > `Saved Remotes` on your Flipper Zero.
2.  Select the virtual remote you created in Exercise 1.
3.  Select a saved button (e.g., `TV_Power`).
4.  Point the Flipper Zero at the target device (e.g., your TV).
5.  Press "Send". Observe if the device responds correctly.
6.  Test all the buttons you saved for that remote. If some don't work, try re-learning them (Exercise 1), ensuring a clear line of sight and appropriate distance.
7.  Rename or reorder buttons within your virtual remote on the Flipper for better usability.
8.  **Challenge:** Create a new virtual remote named "Living Room" and try to consolidate the most frequently used buttons from different physical remotes (e.g., TV Power, Soundbar Volume, AC On/Off) into this single virtual remote on the Flipper.

---

### 🔹 **Exercise 3: Using Universal IR Databases**

**Goal:** Explore and utilize community-sourced or pre-built universal IR remote databases with your Flipper Zero.

**Instructions:**
1.  Connect your Flipper Zero to qFlipper, or directly access its SD card.
2.  Research and download a Flipper Zero compatible IR database file (often `.ir` files within a specific directory structure, e.g., from GitHub repositories like `Flipper-IRDB` or similar community collections).
3.  Copy the downloaded IR files/folders into the correct location on your Flipper's SD card (usually `infrared/assets/` or following the specific database's instructions).
4.  On your Flipper Zero, navigate to `Infrared` > `Universal Remotes` (or similar, depending on firmware/FAP).
5.  Browse the database by device type (e.g., TV, AC, Projector) and manufacturer.
6.  Select a device type and manufacturer for a device you own or have access to.
7.  Try sending some of the pre-listed commands (Power, Channel Up/Down, Volume Up/Down) to your device.
8.  Does it work? If not, try a different code set for the same manufacturer, as variations exist.
9.  **Challenge:** Find a device you own that is *not* well-supported by the Flipper's built-in universal remote FAP but for which you can find discrete IR codes online (e.g., on IRDB.tk or RemoteCentral). Can you manually add these codes to an existing or new `.ir` file on your Flipper's SD card (research the Flipper IR file format)?

---

### 🔹 **Exercise 4: Understanding and Using Pronto Hex Codes (Optional)**

**Goal:** Learn what Pronto Hex codes are and how they can sometimes be used to control IR devices via Flipper Zero (often requires a specific FAP or manual conversion).

**Instructions:**
1.  Research the "Pronto Hex" IR code format. What does it represent? Why was it a common standard among universal remote enthusiasts?
2.  Find a Pronto Hex code online for a simple function of a common device (e.g., power toggle for a Sony TV). The codes are long strings of hexadecimal numbers.
3.  Check if your Flipper Zero firmware or an available FAP has a feature to directly send/save Pronto Hex codes.
4.  If such a feature exists:
    * Enter the Pronto Hex code you found.
    * Save it with a descriptive name.
    * Try sending it to the target device.
5.  If direct Pronto input isn't available, research if there are tools or methods to convert Pronto Hex codes into the Flipper's native `.ir` file format (this is more advanced).
6.  **Challenge:** Explain why a direct Pronto Hex sending feature can be powerful for controlling obscure devices not covered by standard Flipper universal remote databases.

---

### 🔹 **(Optional) Exercise 5: IR Signal Strength and Range Test**

**Goal:** Experiment with the effective range and factors affecting the Flipper Zero's IR transmission.

**Instructions:**
1.  Use a reliably learned IR signal (from Exercise 1 or 2) for a device where you can easily see its response (e.g., TV power LED).
2.  Stand close to the device (e.g., 1 meter) and send the signal. Confirm it works.
3.  Gradually increase your distance from the device, sending the signal at each new distance (e.g., 2m, 3m, 5m, 7m, 10m). Note the maximum distance at which the signal reliably works.
4.  Try sending the signal with partial obstructions between the Flipper and the device (e.g., a hand partially covering the IR port, a thin piece of paper, sending at an angle). How do these affect performance?
5.  If your Flipper has IR power settings (some custom firmware might), try changing it and re-testing the range.
6.  Compare the Flipper's effective range to that of the original physical remote for the same device.
7.  **Challenge:** How does ambient lighting (e.g., bright sunlight vs. a dark room) theoretically affect IR communication? Can you devise a simple test to see if it makes a noticeable difference with the Flipper?
