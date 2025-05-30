## 🐬 Subtopic X.6: Beyond the Case: GPIO & Hardware Hacking Intro

**Goal:** Understand the purpose and basic usage of the Flipper Zero's General Purpose Input/Output (GPIO) pins for interfacing with external electronic components and modules.

**Resources:**

* **Flipper Zero GPIO Documentation:** [docs.flipper.net/gpio](https://docs.flipper.net/gpio) (Pinout diagram is crucial)
* **Basic Electronics Tutorials:** Search "LED resistor calculator", "button pull-up resistor", "GPIO basics".
* **Component Datasheets:** (If using specific sensors later, e.g., DHT11).

**Test Environment / Tools Needed:**

* Flipper Zero device.
* Breadboard.
* Jumper wires (male-male, male-female).
* Basic electronic components:
    * LEDs (various colors).
    * Resistors (e.g., 220 Ohm or 330 Ohm for LEDs with 3.3V).
    * Push buttons.
* (Optional for later exercises) Simple sensors like DHT11 (temperature/humidity).
* **Safety:** Understand that connecting GPIO pins incorrectly can potentially damage the Flipper Zero or components. Always double-check pinouts and voltages. Start with simple LED circuits.

---

### 🔹 **Exercise 1: Identifying GPIO Pins and Functions**

**Goal:** Locate the GPIO header on the Flipper Zero and understand the function of its different pins (power, ground, digital I/O, specific protocols).

**Instructions:**
1.  Physically locate the GPIO pin header on your Flipper Zero.
2.  Refer to the official Flipper Zero pinout diagram (from docs.flipper.net/gpio).
3.  Identify and list the pin numbers/names associated with:
    * 3.3V Power Output.
    * 5V Power Output (if available and when USB is connected).
    * Ground (GND) pins.
    * General Purpose Digital I/O pins (e.g., PA7, PB2, PC0, etc.).
    * Pins associated with specific hardware protocols (SPI, I2C, UART) if labeled.
4.  What is the typical voltage level for the Flipper Zero's digital GPIO pins (e.g., for a HIGH signal)?
5.  **Challenge:** Explain the difference between a "digital" GPIO pin and an "analog" GPIO pin. Which type are most of the Flipper's GPIOs? Does it have any dedicated analog inputs?

---

### 🔹 **Exercise 2: Blinking an LED (Manual GPIO Control)**

**Goal:** Use the Flipper Zero's built-in GPIO application (or a simple FAP) to manually control a GPIO pin and blink an external LED.

**Instructions:**
1.  **Circuit Setup:**
    * Connect one leg of a resistor (e.g., 220 Ohm) to a digital GPIO pin on the Flipper (e.g., PA7).
    * Connect the other leg of the resistor to the longer leg (anode) of an LED.
    * Connect the shorter leg (cathode) of the LED to a GND pin on the Flipper.
    * **Double-check your circuit before powering on or enabling GPIO.**
2.  On the Flipper Zero, navigate to `GPIO` > `USB-UART Bridge` (or a dedicated GPIO control FAP if you have one installed that allows manual pin toggling). Some firmware might have a "GPIO Manual Control" under the main GPIO menu.
3.  Configure the chosen GPIO pin (e.g., PA7) as an "Output".
4.  Manually toggle the pin's state between HIGH (3.3V) and LOW (0V/GND). The LED should turn on when the pin is HIGH and off when LOW.
5.  Try blinking it on and off a few times manually.
6.  **Challenge:** What happens if you connect the LED without the resistor? Why is the resistor important in an LED circuit?

---

### 🔹 **Exercise 3: Reading a Button Press (Input)**

**Goal:** Configure a GPIO pin as an input and read the state of an external push button.

**Instructions:**
1.  **Circuit Setup (Pull-up or Pull-down):**
    * **Pull-up (common):** Connect one pin of a push button to a digital GPIO pin (e.g., PA6). Connect the *same* GPIO pin to 3.3V via a pull-up resistor (e.g., 10k Ohm). Connect the other pin of the push button to GND. When the button is *not* pressed, the GPIO reads HIGH. When pressed, it reads LOW.
    * **Pull-down:** Connect one pin of button to GPIO. Connect *same* GPIO to GND via pull-down resistor. Connect other pin of button to 3.3V. Reads LOW normally, HIGH when pressed.
    * *Alternatively, some Flipper firmware/GPIO apps allow enabling internal pull-up/pull-down resistors on certain pins, simplifying the external circuit.*
2.  On the Flipper Zero, navigate to the GPIO application used in Exercise 2.
3.  Configure the chosen GPIO pin (e.g., PA6) as an "Input" (with internal pull-up if available and you're not using an external one, otherwise match your circuit).
4.  Observe the displayed state of the input pin.
5.  Press and release the push button. The displayed state of the pin on the Flipper should change accordingly (e.g., from 1 to 0 if using pull-up and pressing).
6.  **Challenge:** If you are *not* using an internal pull-up/pull-down resistor on the Flipper, what is a "floating input" and why is it problematic? How do pull-up or pull-down resistors prevent this?

---

### 🔹 **Exercise 4: Scripting GPIO (Conceptual or Simple FAP)**

**Goal:** Understand how GPIO pins can be controlled programmatically, either through Flipper Applications (FAPs) or by sending commands via the CLI/USB-UART bridge.

**Instructions:**
1.  Research if your current Flipper Zero firmware or available FAPs allow for simple scripting or sequenced control of GPIO pins (e.g., a "GPIO Sequencer" FAP, or basic commands via the Flipper CLI if it exposes GPIO control).
2.  If a simple scripting FAP is found:
    * Try writing a very basic script within that FAP's environment to make the LED from Exercise 2 blink automatically (e.g., ON for 500ms, OFF for 500ms, repeat).
3.  If direct scripting on Flipper isn't straightforward, connect the Flipper in USB-UART Bridge mode (`GPIO` > `USB-UART Bridge`).
4.  On your computer, open a serial terminal (PuTTY, minicom, Arduino IDE Serial Monitor) connected to the Flipper's serial port.
5.  Explore if the Flipper's CLI (accessible via serial) has commands to directly set GPIO pin states (e.g., `gpio set PA7 1`, `gpio set PA7 0`). If so, write a sequence of these commands to blink the LED.
6.  **Challenge:** How could you use Python on your computer, communicating with the Flipper over the USB-UART serial bridge (using the `pyserial` library), to control the GPIO pins on the Flipper? Outline the basic logic.

---

### 🔹 **(Optional) Exercise 5: Exploring GPIO for Specific Protocols (Conceptual)**

**Goal:** Learn which GPIO pins on the Flipper are typically used for common communication protocols like UART, SPI, and I2C.

**Instructions:**
1.  Refer to the Flipper Zero GPIO pinout diagram again.
2.  Identify the pins specifically labeled for:
    * UART (TX, RX)
    * SPI (MOSI, MISO, SCK, CS)
    * I2C (SDA, SCL)
3.  Research the basic purpose of each of these protocols (UART for serial communication, SPI and I2C for communication with sensors and other integrated circuits).
4.  If you have an external module that uses one of these protocols (e.g., an I2C sensor, an SPI display - **do not connect yet unless you are experienced**), note down which Flipper GPIO pins you would theoretically connect to the corresponding pins on the module.
5.  **Challenge:** Many hardware modules (like RFID readers, displays) come as "breakout boards" designed for microcontrollers. Explain why these breakout boards are useful when interfacing such modules with the Flipper's GPIO, as opposed to connecting directly to a bare chip.
