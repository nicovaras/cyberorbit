## 🐍 Subtopic 1.6: Basic Data Encoding & Transformation

**Goal:** Understand and implement common data encoding and simple transformation techniques frequently used in data transmission, storage, and basic obfuscation or CTF challenges.

**Resources:**

* **Python `base64` module:** [Documentation](https://docs.python.org/3/library/base64.html)
* **Python `binascii` module:** [Documentation](https://docs.python.org/3/library/binascii.html) (For Hex)
* **Python `urllib.parse` module:** [Documentation](https://docs.python.org/3/library/urllib.parse.html) (For URL encoding)
* **Character Encoding Basics:** [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) (Understanding bytes vs strings is crucial)
* **CyberChef:** [Online Tool](https://gchq.github.io/CyberChef/) (Excellent for experimenting with various encodings/decodings)

---

### 🔹 **Exercise 1: Base64 Playground**

**Goal:** Practice encoding and decoding data using Base64.

**Instructions:**

1.  Write a Python script.
2.  Take a simple string (e.g., "Practical Python Security").
3.  Encode the string into Base64 bytes using the `base64` module. Remember to encode the initial string to bytes first (e.g., using `.encode('utf-8')`). Print the Base64 encoded bytes.
4.  Take a sample Base64 encoded string (e.g., `UHl0aG9uIGlzIGZ1biE=`).
5.  Decode this Base64 string back into bytes using the `base64` module.
6.  Decode the resulting bytes back into a readable string (e.g., using `.decode('utf-8')`). Print the final string.
7.  **Challenge:** Handle potential `binascii.Error` exceptions that might occur if you try to decode an invalid Base64 string.

---

### 🔹 **Exercise 2: Hexadecimal Conversion**

**Goal:** Convert data between its raw byte representation and hexadecimal format.

**Instructions:**

1.  Write a Python script.
2.  Take a string (e.g., "Network Forensics"). Encode it to bytes.
3.  Use `binascii.hexlify()` to convert the bytes into their hexadecimal representation (as bytes). Decode this hex representation into a readable string for printing.
4.  Take a hexadecimal string (e.g., `"4a4f4b4552"`).
5.  Use `binascii.unhexlify()` to convert the hex string back into the original bytes. Remember `unhexlify` typically takes bytes, so you might need to encode your hex string first.
6.  Decode the resulting bytes back into a readable string. Print it.
7.  **Challenge:** What happens if you try to unhexlify a string with an odd number of hex characters or characters that are not valid hex digits (0-9, a-f)? Add error handling for `binascii.Error`.

---

### 🔹 **Exercise 3: URL Encoding for Safety**

**Goal:** Understand why and how special characters are encoded in URLs and practice using `urllib.parse`.

**Instructions:**

1.  Write a Python script using `urllib.parse`.
2.  Take a string containing characters that are typically unsafe or have special meaning in URLs (e.g., `query=security research&param=a/b c`).
3.  Use `urllib.parse.quote()` or `urllib.parse.quote_plus()` to URL-encode the string. Print the result. Note the difference (especially how space is handled).
4.  Take a URL-encoded string (e.g., `search%3Fq%3Dpython%26safe%3Dactive`).
5.  Use `urllib.parse.unquote()` or `urllib.parse.unquote_plus()` to decode it back to its original form. Print the result.
6.  **Challenge:** Manually create a dictionary representing URL parameters (e.g., `{'query': 'security tools', 'lang': 'python'}`) and use `urllib.parse.urlencode()` to correctly format it as a query string suitable for appending to a URL.

---

### 🔹 **Exercise 4: Simple XOR Cipher & Brute-Force**

**Goal:** Implement a basic XOR transformation and understand how easily single-byte XOR can be broken.

**Instructions:**

1.  **XOR Function:** Write a Python function `xor_cipher(data_bytes, key_byte)` that takes data as bytes and a single integer key (0-255) and returns the XORed bytes. Remember that XORing `a ^ b ^ b` gives back `a`.
2.  **Test:** Take a string, encode it to bytes, XOR it with a chosen key byte (e.g., `0x55`), and print the result (it might look like gibberish or have unprintable chars). Then, XOR the result *again* with the same key byte and verify you get the original bytes back.
3.  **Brute-Force:** Now, take a sample piece of text that has been XORed with an *unknown* single byte key (e.g., find a "crypto/xor" challenge on a CTF practice site, or create your own like `xor_cipher(b'This is a secret message', 0x2A)`).
4.  Write code that iterates through all possible single-byte keys (0 to 255). For each key, XOR the ciphertext with that key byte.
5.  Print the potential plaintext for each key. Manually inspect the output – one of the results should look like readable English text, revealing both the original message and the key.
6.  **Challenge:** Can you automate the detection of the correct plaintext? Look for characteristics of English text (e.g., common letters like 'e', 't', 'a', spaces, printable ASCII characters). Score each potential plaintext based on these heuristics and print the highest-scoring result and the corresponding key.

---

### 💡 **Project: Multi-Encoding/Decoding Tool**

**Goal:** Create a simple command-line tool that can perform various encoding/decoding operations based on user input.

**Instructions:**

1.  Write a Python script using `argparse` to create a command-line tool.
2.  The tool should accept arguments like:
    * `--encode` or `--decode` to specify the operation.
    * `--type` to specify the encoding type (e.g., `base64`, `hex`, `url`, `xor`).
    * `--input` to provide the string or data to process.
    * `--key` (optional) needed for `xor` type.
3.  Implement the logic using functions from the previous exercises to perform the requested encoding or decoding based on the arguments.
4.  Handle potential errors gracefully (e.g., invalid type, missing key for xor, invalid input data for decoding).
5.  Print the result of the operation.
6.  Example usage:
    * `python coder.py --encode --type base64 --input "hello"`
    * `python coder.py --decode --type hex --input "4a4f4b4552"`
    * `python coder.py --encode --type xor --key 55 --input "secret"`
7.  **Portfolio Guidance:** Add this tool to GitHub. Include a clear README explaining all the supported encoding types, command-line arguments, and examples. This demonstrates practical tool development.