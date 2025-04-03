## 🐍 Subtopic 1.1: Your First Security Script: Network Reachability & Banner Grabbing

**Goal:** Write basic Python scripts to check network connectivity, retrieve initial service data (banners), and interact with web servers using fundamental libraries. This involves learning to use `socket` for basic connections and `requests` for HTTP, including setting up your Python environment properly.

**Resources:**

* **Python `socket` module:** [Official Documentation](https://docs.python.org/3/library/socket.html)
* **Python `requests` library:** [Quickstart Guide](https://requests.readthedocs.io/en/latest/user/quickstart/)
* **Python `venv` (Virtual Environments):** [Tutorial](https://docs.python.org/3/tutorial/venv.html)
* **Python `pip` (Package Installer):** [User Guide](https://pip.pypa.io/en/stable/user_guide/)
* **Test Target (Telnet):** `towel.blinkenlights.nl` (Port 23) - *A fun text-based service.*
* **Test Target (HTTP):** `httpbin.org` - *A useful service for testing HTTP requests.*

---

### 🔹 **Exercise 1: Connect and Grab a Banner**

**Goal:** Write a Python script using the built-in `socket` library to connect to a specific network service and print the first piece of data it sends back (often called a "banner").

**Instructions:**

1.  Create a new Python script.
2.  Use the `socket` library to establish a TCP connection to `towel.blinkenlights.nl` on port `23`.
3.  Receive a small amount of data (e.g., 1024 bytes) from the connection.
4.  Print the received data (decoded from bytes to a string).
5.  Ensure your script closes the connection properly.
6.  **Challenge:** Add basic error handling. What happens if the host is down or the port is closed? Your script should report the issue gracefully instead of crashing.

---

### 🔹 **Exercise 2: Fetch HTTP Headers with `requests`**

**Goal:** Learn to use the popular `requests` library to interact with web servers and retrieve specific information, like HTTP headers. This exercise requires installing an external library.

**Instructions:**

1.  **Setup:** Create a dedicated project directory. Inside it, create a Python virtual environment (`venv`) and activate it. Use `pip` to install the `requests` library within your active virtual environment.
2.  Create a Python script within this environment.
3.  Use the `requests` library to send an HTTP `HEAD` request to `https://httpbin.org/get`. (A `HEAD` request fetches only headers, not the full content).
4.  Check if the request was successful (status code 200).
5.  If successful, print the values of the `Server` and `Content-Type` headers from the response.
6.  **Challenge:** Modify the script to accept a URL as a command-line argument and fetch its headers. Handle potential errors like invalid URLs or connection failures.

---

### 🔹 **Exercise 3: Simple Port Check**

**Goal:** Write a script that attempts to connect to a specified host on a few common ports to see if they appear to be open.

**Instructions:**

1.  Create a Python script that defines a target hostname (e.g., `scanme.nmap.org` - *a host explicitly provided for testing scanners*) and a list of common ports (e.g., `[21, 22, 23, 80, 443]`).
2.  Use the `socket` library within a loop.
3.  For each port in the list, attempt to establish a TCP connection to the target host on that port.
4.  Set a short timeout for the connection attempt (e.g., 1 second) using `socket.settimeout()`. This prevents the script from hanging on unresponsive ports.
5.  Report whether the connection to each port succeeded (implying it's likely open) or failed (timed out, connection refused, etc.).
6.  Ensure sockets are closed after each attempt.
7.  **Challenge:** Instead of hardcoding the host and ports, accept them as command-line arguments (e.g., `-host <hostname> -ports <port1,port2,port3>`). Parse the comma-separated port list.

---

### 💡 **Project: Host Service Identifier**

**Goal:** Combine socket and HTTP requests to identify potential web services running on a target.

**Instructions:**

1.  Write a script that accepts a full URL (e.g., `http://scanme.nmap.org`, `https://google.com`) as input.
2.  Extract the hostname and scheme (http/https) from the URL.
3.  Determine the default port based on the scheme (80 for http, 443 for https).
4.  Use `socket` (with a timeout) to check if a connection can be established to the extracted hostname on the determined port. Report the result.
5.  If the port check was successful *and* the scheme was http or https, use the `requests` library to make a `GET` request to the original URL.
6.  If the `requests` call is successful, print the `Server` header (if present) from the response.
7.  **Portfolio Guidance:** Create a GitHub repository for this script. Include a `README.md` explaining what the script does, how to run it (including setting up `venv` and installing `requests`), and example usage/output.

---