## 🐍 Subtopic 1.3: Network Socket Programming Basics

**Goal:** Gain a deeper understanding of network communication fundamentals by programming directly with TCP and UDP sockets. Builds upon the basic connection concept from Subtopic 1.1.

**Resources:**

* **Python `socket` module:** [Official Documentation](https://docs.python.org/3/library/socket.html)
* **Python `argparse` module:** [Documentation](https://docs.python.org/3/library/argparse.html) (For command-line arguments)
* **Network Target:** Use `localhost` (127.0.0.1) for client/server exercises. Use `scanme.nmap.org` or another test host for the scanner.

---

### 🔹 **Exercise 1: TCP Echo Client**

**Goal:** Implement a client that connects to a server, sends data, and receives the same data back.

**Instructions:**

1.  Write a Python script for a TCP client.
2.  The client should connect to a specified host and port (you'll build the server in the next exercise; use `localhost` and a high port number like 9999 for now).
3.  Once connected, prompt the user to enter a message.
4.  Send the encoded message to the server.
5.  Receive the response from the server (up to a certain buffer size, e.g., 1024 bytes).
6.  Decode and print the received response.
7.  Close the connection.
8.  **Challenge:** Allow the user to send multiple messages in a loop until they type 'exit'.

---

### 🔹 **Exercise 2: TCP Echo Server (Single Connection)**

**Goal:** Implement a server that listens for a connection, receives data, and sends it back (echoes) to the client.

**Instructions:**

1.  Write a Python script for a TCP server.
2.  The server should bind to `localhost` (or `0.0.0.0` to listen on all interfaces) and the same port used by the client (e.g., 9999).
3.  Set the socket to listen for incoming connections.
4.  Accept *one* incoming connection.
5.  Enter a loop: receive data from the connected client (handle potential disconnection).
6.  If data is received, send the exact same data back (echo).
7.  If the client disconnects (e.g., `recv` returns empty bytes), close the client connection and optionally exit the server or wait for a new connection (keep it simple first: exit after one client).
8.  **Challenge:** Test this server with your client from Exercise 1. Ensure they communicate correctly.

---

### 🔹 **Exercise 3: Enhanced Port Scanner**

**Goal:** Improve the basic port checker from Subtopic 1.1 by adding command-line argument parsing and better error handling.

**Instructions:**

1.  Start with the port checking script from Subtopic 1.1 (Exercise 3).
2.  Use the `argparse` module to allow the user to specify the target host and a comma-separated list of ports via command-line arguments (e.g., `python scanner.py --host scanme.nmap.org --ports 80,22,443`).
3.  Implement error handling for potential `socket.gaierror` if the hostname cannot be resolved (DNS lookup failure).
4.  Print more informative messages (e.g., "Port X is open", "Port Y is closed/filtered", "Hostname Z could not be resolved").
5.  **Challenge:** Add an option (`--timeout`) to allow the user to specify the connection timeout value via the command line.

---

### 🔹 **Exercise 4: Simple UDP Client & Server**

**Goal:** Understand the basics of connectionless communication using UDP sockets.

**Instructions:**

1.  **UDP Server:** Write a script that creates a UDP socket, binds it to `localhost` and a port (e.g., 9998), and enters a loop. Inside the loop, use `recvfrom()` to wait for and receive data (up to a buffer size). Print the received data and the address of the client that sent it.
2.  **UDP Client:** Write a separate script that creates a UDP socket. Prompt the user for a message. Use `sendto()` to send the encoded message to the server's address (`localhost`, 9998).
3.  Run the server, then run the client. Verify the server receives and prints the message.
4.  **Challenge:** What happens if you run the client multiple times? What happens if you run the client *before* the server is running? Observe the differences compared to TCP.

---

### 💡 **Project: Multi-threaded TCP Port Scanner**

**Goal:** Improve scanning speed by checking multiple ports concurrently using basic threading.

**Instructions:**

1.  Start with your enhanced port scanner (Exercise 3).
2.  Import the `threading` module.
3.  Design a function that takes a single port number as an argument and performs the socket connection attempt (including timeout and error handling) for that specific port on the target host. This function will be run by each thread.
4.  In your main script logic, after parsing the target host and port list:
    * Create an empty list to hold thread objects.
    * Loop through the ports to be scanned. For each port, create a `threading.Thread` targeting your connection-checking function, passing the port number as an argument. Add the thread to your list and start it.
    * After starting all threads, loop through your list of thread objects and call `join()` on each one. This ensures the main script waits for all threads to finish before exiting.
5.  You'll need a way for threads to report results back (e.g., appending open ports to a shared list - consider using `threading.Lock` around list appends for thread safety, or use a thread-safe structure like `queue.Queue`).
6.  Print the list of open ports found after all threads have completed.
7.  **Portfolio Guidance:** Document this multi-threaded scanner on GitHub. Explain the benefits of threading for I/O-bound tasks like port scanning. Discuss the concept of thread safety and how you addressed it (even if simply).