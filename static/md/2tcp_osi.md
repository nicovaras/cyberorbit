## 🌐 Subtopic 2.1: TCP/IP & OSI Model Fundamentals

**Goal:** Understand the conceptual frameworks (OSI and TCP/IP models) that describe network communication, including layering, encapsulation, and basic addressing schemes.

**Resources:**

* **OSI Model Explained:** [Cloudflare Learning](https://www.cloudflare.com/learning/ddos/what-is-the-osi-model/)
* **TCP/IP Model Explained:** [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Glossary/TCP/IP)
* **Subnetting:** [Subnet Calculator](https://www.subnet-calculator.com/) (Use for checking work), [Subnetting Tutorial](https://www.practicalnetworking.net/series/subnetting/subnetting/)
* **RFC 1918 (Private Addresses):** [RFC Document](https://tools.ietf.org/html/rfc1918)

---

### 🔹 **Exercise 1: Layer Mapping**

**Goal:** Map network protocols and functions to their corresponding layers in both the OSI and TCP/IP models.

**Instructions:**

1.  Consider the process of loading a webpage (`https://example.com`) in your browser.
2.  Identify the key protocols involved at different stages (e.g., Ethernet, IP, TCP, TLS/SSL, HTTP, DNS).
3.  For each protocol identified, determine which layer it primarily operates at according to the **OSI Model**.
4.  Repeat step 3, but map the protocols to the layers of the **TCP/IP Model** (e.g., Link, Internet, Transport, Application).
5.  Present your mappings clearly (e.g., in a table).
6.  **Challenge:** Explain where functions like data encryption/decryption (TLS/SSL) and data formatting/translation (like character encoding) fit within the OSI model.

---

### 🔹 **Exercise 2: Subnet Calculations**

**Goal:** Practice calculating network details from IP addresses and subnet masks.

**Instructions:**

1.  Given the following IP address and CIDR notation: `172.16.55.131/26`
2.  Calculate:
    * The Subnet Mask in dotted-decimal notation.
    * The Network Address (Network ID).
    * The Broadcast Address.
    * The total number of host addresses available in this subnet.
    * The range of usable host IP addresses.
3.  Repeat the calculations for `10.100.0.15/22`.
4.  Use an online subnet calculator (linked in resources) to verify your manual calculations.
5.  **Challenge:** You are given a Class C block `192.168.10.0/24`. You need to create at least 5 separate subnets, each capable of supporting at least 25 hosts. Determine an appropriate subnet mask to achieve this and list the Network ID and usable IP range for the first 5 resulting subnets.

---

### 🔹 **Exercise 3: Understanding Encapsulation**

**Goal:** Visualize or describe how data is wrapped with headers as it passes down the network stack.

**Instructions:**

1.  Imagine sending a simple email using SMTP. The email body is your Application layer data.
2.  Describe or draw the process of encapsulation as this data moves down the typical TCP/IP stack (Application -> Transport -> Internet -> Link).
3.  For each layer (Transport, Internet, Link), specify the key header information that gets added (e.g., Source/Destination Ports for TCP, Source/Destination IPs for IP, Source/Destination MACs for Ethernet). Don't worry about exact header field names, focus on the core addressing/control information added at each stage.
4.  **Challenge:** Explain what happens to these headers during decapsulation when the email arrives at the recipient's machine.

---

### 🔹 **Exercise 4: Public vs. Private IP Addresses**

**Goal:** Identify and understand the purpose of private IP address ranges defined in RFC 1918.

**Instructions:**

1.  Identify which of the following IP addresses are private (RFC 1918) and which are public:
    * `10.1.5.10`
    * `172.16.31.254`
    * `172.32.0.1`
    * `192.168.0.15`
    * `169.254.10.10` (What is this range called?)
    * `8.8.8.8`
2.  Explain the primary reason organizations use private IP addresses internally.
3.  What technology allows devices using private IPs to communicate with the public internet? Briefly explain how it works conceptually.
4.  **Challenge:** If two different companies both use the `192.168.1.0/24` network internally, how can a computer in Company A (`192.168.1.50`) send traffic specifically to a computer in Company B (`192.168.1.60`) assuming they need to communicate over the internet?

---

### 🧪 **(Optional) Lab: Foundational Networking Theory**

**Goal:** Reinforce theoretical networking concepts through guided exercises.

**Instructions:**
* Sign up or log in to [TryHackMe](https://tryhackme.com/).
* Complete the **[Introductory Networking](https://tryhackme.com/room/introductorynetworking)** room.
* Focus on understanding the OSI model, TCP/IP model, and subnetting sections within the room.

---