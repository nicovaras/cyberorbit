## 🐬 Subtopic X.3: Tap, Read, & Emulate: NFC & RFID Adventures

**Goal:** Explore Near Field Communication (NFC) and Radio-Frequency Identification (RFID 125kHz) technologies using Flipper Zero to read card information, understand different card types, and (ethically) emulate basic UIDs.

**Resources:**

* **Flipper Zero NFC Documentation:** [docs.flipper.net/nfc](https://docs.flipper.net/nfc)
* **Flipper Zero RFID Documentation:** [docs.flipper.net/rfid](https://docs.flipper.net/rfid)
* **NFC Card Types Overview:** [Wikipedia NFC](https://en.wikipedia.org/wiki/Near-field_communication#NFC_tags)
* **Mifare Classic Info:** (Understand it's a common but older NFC type) [Wikipedia Mifare](https://en.wikipedia.org/wiki/MIFARE)
* **EM4100 RFID Info:** (Common 125kHz tag type)

**Test Environment / Tools Needed:**

* Flipper Zero device.
* A variety of **NFC cards** you own and have permission to test with (e.g., public transport cards for UID reading, loyalty cards, hotel key cards (old/expired), personal NFC tags – **DO NOT USE BANK/CREDIT CARDS for any active interaction beyond basic type detection from a safe distance if supported**).
* A variety of **125kHz RFID cards/fobs** you own (e.g., older office access fobs, EM4100 based tags).
* (Optional) An Android phone with NFC capabilities and an NFC information reader app (like "NFC Tools") for comparison.

---

### 🔹 **Exercise 1: Reading NFC Card Information**

**Goal:** Use Flipper Zero to read and identify basic information from various NFC cards.

**Instructions:**
1.  On your Flipper Zero, navigate to `NFC`.
2.  Select `Read`.
3.  Hold different NFC cards you own (one at a time) near the back of the Flipper Zero (where the NFC antenna is).
4.  Observe the information displayed by the Flipper when it successfully reads a card:
    * Card Type (e.g., Mifare Classic, NTAG21x, Mifare Ultralight).
    * UID (Unique ID).
    * Other available information (e.g., memory size, specific sector data if readable without keys).
5.  Save the information from at least two different types of NFC cards. Give them descriptive names.
6.  **Challenge:** If you have an NFC-enabled Android phone and an app like "NFC Tools", read the same cards with your phone. Compare the information presented by the phone app versus the Flipper Zero. Are there any differences or additional details?

---

### 🔹 **Exercise 2: Emulating Basic NFC Card UID (Known Safe Card)**

**Goal:** Practice emulating the UID of a *simple, known, non-sensitive* NFC card that you have previously read and saved. **Only emulate cards you own and for testing purposes where no harm can be caused (e.g., a personal blank NTAG21x, NOT a transit or access card for actual use).**

**Instructions:**
1.  Using a card you read and saved in Exercise 1 (e.g., a personal NFC tag, a simple loyalty card *after verifying its type and data are basic*):
    * On your Flipper Zero, navigate to `NFC` > `Saved`.
    * Select the saved card file.
    * Choose the `Emulate UID` (or similar basic emulation) option.
2.  Test the emulation:
    * If you have an NFC-enabled Android phone, use an app like "NFC Tools" to try and read the UID being emulated by the Flipper. Does it match the original card's UID?
    * If you have a very simple reader device that uses this card (e.g., a personal NFC project), test if it recognizes the Flipper's emulated UID.
3.  **Important:** Discuss situations where emulating a UID might be unethical or illegal, even if technically possible.
4.  **Challenge:** Some saved NFC card types might offer different emulation modes (e.g., "Emulate specific type" vs. "Emulate UID"). If available for one of your saved cards, explore what these different modes might do.

---

### 🔹 **Exercise 3: Reading 125kHz RFID (LF-RFID) Tags**

**Goal:** Use Flipper Zero to read and identify the UID from common 125kHz Low-Frequency RFID tags (e.g., EM4100, HID Prox II).

**Instructions:**
1.  On your Flipper Zero, navigate to `125 kHz RFID`.
2.  Select `Read`. The Flipper will start trying to detect a nearby 125kHz tag.
3.  Hold various 125kHz RFID cards or fobs you own (one at a time) near the Flipper's RFID antenna area (bottom back).
4.  When a tag is successfully read, the Flipper should display its protocol (e.g., EM4100, HIDProx) and its unique ID (often a hexadecimal or decimal number).
5.  Read and save the data from at least two different 125kHz tags. Give them descriptive names.
6.  Examine the saved data for each.
7.  **Challenge:** Do all your 125kHz tags use the same protocol? If you have HID Prox tags, does the Flipper read the full card number or just a facility code and card number? (Research HID Prox format).

---

### 🔹 **Exercise 4: Manually Adding and Emulating an EM4100 UID**

**Goal:** Learn to manually input a known EM4100 UID into the Flipper Zero and emulate it. **Only use UIDs you own or are given for testing.**

**Instructions:**
1.  Assume you have an EM4100 tag's UID written down (e.g., `A1B2C3D4E5` - this is a 5-byte hex UID typical for EM4100).
2.  On your Flipper Zero, navigate to `125 kHz RFID`.
3.  Select `Add Manually`.
4.  Choose the `EM4100` protocol (or similar EM Marin).
5.  Enter the known UID value (e.g., `A1B2C3D4E5`) using the Flipper's keypad.
6.  Save this manually added card with a descriptive name.
7.  Navigate to `Saved` under `125 kHz RFID`, select your manually added card, and choose `Emulate`.
8.  Test the emulation against a 125kHz EM4100 reader if you have one (e.g., a USB RFID reader, a simple access control test unit). Does it read the UID you entered?
9.  **Challenge:** Can you find a way to represent the EM4100 UID in different formats (e.g., decimal, reversed byte order) and see if your reader still interprets it the same way as the Flipper's standard emulation?

---

### 🔹 **Exercise 5: Understanding Mifare Classic (Conceptual)**

**Goal:** Research the structure of Mifare Classic NFC cards and understand why simply reading/emulating their UID is often not enough to bypass security that relies on them. (Research-based)

**Instructions:**
1.  Research "Mifare Classic 1K" or "Mifare Classic 4K" cards.
2.  What is the typical memory structure of a Mifare Classic card? (Sectors, Blocks, Keys A/B).
3.  While Flipper (especially with custom firmware) can read UIDs and attempt to read sectors using default or known keys, why is a full "clone" of a securely configured Mifare Classic card (that uses non-default keys for its data sectors) difficult?
4.  What information, beyond the UID, would an access control system typically check on a Mifare Classic card to grant access?
5.  **Challenge:** The Flipper Zero (especially with custom firmware) has features related to "Mifare Classic key dictionary attacks" or "nested attacks". Conceptually, what are these attacks trying to achieve, and why are they computationally intensive? **No actual attack execution required.**
