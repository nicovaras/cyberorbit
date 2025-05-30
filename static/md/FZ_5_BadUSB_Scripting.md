## 🐬 Subtopic X.5: Automating Keystrokes: BadUSB & Scripting Fun

**Goal:** Understand the Flipper Zero's BadUSB capabilities, learn the basics of DuckyScript, and write simple scripts for automating benign computer tasks, with a **strong emphasis on ethical use and understanding potential misuse.**

**Resources:**

* **Flipper Zero BadUSB Documentation:** [docs.flipper.net/badusb](https://docs.flipper.net/badusb)
* **DuckyScript Language Reference:** Search "Hak5 DuckyScript Language" or "Flipper Zero DuckyScript syntax".
* **Ethical Considerations:** Read about responsible disclosure and a CISO's perspective on BadUSB devices.

**Test Environment / Tools Needed:**

* Flipper Zero device with MicroSD card.
* Computer with a USB port (a **Virtual Machine is HIGHLY RECOMMENDED** for testing any BadUSB script to contain its effects and prevent accidental impact on your host system).
* A simple text editor (like Notepad, VS Code, etc.) for writing DuckyScript files.
* USB-C cable to transfer scripts to Flipper's SD card (or use qFlipper).
* **Critical:** Full understanding and agreement that scripts will **only be run on computers you own and have explicit permission to test on**, ideally within a VM.

---

### 🔹 **Exercise 1: Understanding BadUSB Concepts**

**Goal:** Research and comprehend what a BadUSB attack is, how it works by emulating a Human Interface Device (HID), and its potential security implications. (Research-focused)

**Instructions:**
1.  Research the term "BadUSB". What type of device does it emulate? Why is this effective in bypassing some traditional security measures?
2.  Explain the difference between a standard USB flash drive and a BadUSB device like the Flipper Zero running a DuckyScript.
3.  List 2-3 potential malicious actions an attacker might attempt with a BadUSB device.
4.  List 2-3 legitimate or benign uses for HID automation scripts (e.g., IT automation, repetitive task execution, accessibility).
5.  What are some common defenses or detection methods against BadUSB attacks?
6.  **Challenge:** Why is it important for security professionals to understand BadUSB capabilities even if they only intend to use them ethically?

---

### 🔹 **Exercise 2: Your First DuckyScript - "Hello, Flipper!"**

**Goal:** Write and execute a very simple DuckyScript payload on the Flipper Zero to type text into a text editor on your test computer/VM.

**Instructions:**
1.  Create a new text file on your computer named `hello.txt`.
2.  Write the following DuckyScript commands in the file:
    ```duckyscript
    REM Simple Hello World Script
    DELAY 1000
    GUI r
    DELAY 500
    STRING notepad.exe
    ENTER
    DELAY 1000
    STRING Hello, Flipper Zero! This is DuckyScript.
    ENTER
    ```
3.  Transfer this `hello.txt` file to your Flipper Zero's SD card in the `badusb/` directory.
4.  **Prepare your VM or test computer:** Open a text editor if you want to modify the script to type directly into it, or just be ready for Notepad to open.
5.  On the Flipper Zero, navigate to `Bad USB`, select your `hello.txt` script, and choose "Run". **Ensure the Flipper is connected to your test computer/VM via USB *before* running.**
6.  Observe the computer. Did Notepad open and type the message?
7.  **Challenge:** Modify the script to open a different application (e.g., `calc.exe` on Windows, `gnome-calculator` or `kcalc` on Linux - adjust GUI r to open run dialog if needed or open terminal first) and then type a simple calculation like "2+2".

---

### 🔹 **Exercise 3: DuckyScript for Web Navigation**

**Goal:** Write a DuckyScript to automatically open a web browser and navigate to a specific benign website.

**Instructions:**
1.  Create a new DuckyScript file (e.g., `goto_site.txt`).
2.  Write a script that:
    * Opens the run dialog (e.g., `GUI r` on Windows, or `SUPER` then type terminal on Linux). Adjust `SUPER` if your key is `WINDOWS` or `COMMAND`.
    * Types the command to open your default web browser followed by a specific URL (e.g., `chrome.exe https://docs.flipper.net` or `firefox https://docs.flipper.net`).
    * Presses Enter.
    * Includes appropriate `DELAY` commands to allow applications to open and load.
3.  Transfer the script to your Flipper Zero (`badusb/` directory).
4.  Run the script on your test computer/VM. Did the browser open and navigate to the site?
5.  **Challenge:** Modify the script to open multiple tabs in the browser, each navigating to a different benign educational website.

---

### 🔹 **Exercise 4: Simple Information Gathering Script (Benign)**

**Goal:** Write a DuckyScript that opens a command prompt/terminal on your test system and runs basic, non-harmful information gathering commands, then attempts to save the output to a file *on the target test system*.

**Instructions:**
1.  Create a new DuckyScript file (e.g., `sys_info.txt`).
2.  Write a script that (adjust commands for your test OS - Windows or Linux VM):
    * Opens a command prompt (`cmd.exe`) or terminal (`gnome-terminal`, `konsole`).
    * Waits for the prompt to appear (`DELAY`).
    * Types a command to display the current user (e.g., `whoami` or `echo %USERNAME%`).
    * Types a command to display network configuration (e.g., `ipconfig /all` or `ip a`).
    * Redirects the output of these commands to a text file *on the target system's desktop* (e.g., `> C:\Users\YourUser\Desktop\info.txt` or `> ~/Desktop/info.txt`). This requires knowing the user path or using relative paths if possible.
    * (Optional) Closes the command prompt/terminal window.
3.  Transfer and run the script on your **VM**. Check if the `info.txt` file was created on the VM's desktop and contains the command output.
4.  **CRITICAL ETHICAL NOTE:** This exercise demonstrates how a BadUSB could exfiltrate data. In a malicious context, the output would be sent to an attacker, not a local file. Understand this power.
5.  **Challenge:** How could you make the script slightly more stealthy by minimizing the command window or attempting to close it quickly after commands run? (e.g., `START MIN cmd /c ...` on Windows).

---

### 🔹 **(Optional) Exercise 5: DuckyScript Delays and Key Combos**

**Goal:** Experiment with different `DELAY` timings and special key combinations in DuckyScript.

**Instructions:**
1.  Create a DuckyScript.
2.  Experiment with the `DEFAULT_DELAY` or `DEFAULTDELAY` command at the beginning of your script to change the delay between each command.
3.  Write a script that uses specific key combinations:
    * `CTRL-ALT-DELETE` (Windows - be careful, might lock screen or show task manager)
    * `ALT F4` (Windows - closes active window)
    * `CTRL SHIFT ESC` (Windows - opens Task Manager)
    * `GUI l` (Windows - locks screen)
    * `CTRL c` (Copy), `CTRL v` (Paste) - try copying text from one auto-typed field to another.
4.  Test these on your VM. Observe what happens.
5.  **Challenge:** Write a script that opens Notepad, types a multi-line message, selects all the text (`CTRL a`), copies it (`CTRL c`), opens a second instance of Notepad, and pastes the text (`CTRL v`). This requires careful timing with `DELAY`.
