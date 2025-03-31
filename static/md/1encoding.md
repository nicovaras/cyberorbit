## 📄 PDF: Topic 1 – Subtopic: Encoding & Obfuscation  
**Resource:** [The Python Standard Library – `base64`, `codecs`, and `string`](https://docs.python.org/3/library/base64.html)

---

### 🔹 **Exercise: Encode and Decode Messages with Base64**  
**Goal:** Learn to hide and recover information using Base64 encoding.  

**Instructions:**  
- Ask the user for a message using `input()`.  
- Encode the message into Base64.  
- Decode it back and print the result.  
- Try encoding special characters. Do they survive the round trip?

---

### 🔹 **Exercise: Build a ROT13 Encryptor/Decryptor**  
**Goal:** Implement a simple letter-shifting cipher that scrambles text.  

**Instructions:**  
- Accept a string of lowercase text.  
- Shift each letter by 13 positions (a↔n, b↔o, etc).  
- Print both the scrambled and unscrambled version.  
- Try with phrases from your favorite book or quote.

---

### 🔹 **Exercise: Detect Obfuscated Commands in a Log**  
**Goal:** Write a Python script that detects base64-like strings inside logs.  

**Instructions:**  
- Generate or download a log file with some random Base64 strings in it.  
- Use a regex to search for suspicious-looking strings (e.g., length > 20, alphanumeric, ends in `=`).  
- Highlight the lines with possible encoded commands.  
- Try injecting your own fake payloads and catching them.

---

### 🔹 **Exercise: Obfuscate and Deobfuscate a Python Script**  
**Goal:** Make a script unreadable, then recover it.  

**Instructions:**  
- Write a small script that prints “Access Granted.”  
- Encode its content using Base64 and save it to another `.py` file.  
- Write a decoder script that runs the obfuscated version using `exec()`.  
- Would someone understand what it does just by looking at it?

---

### ✨ **Bonus: Create a Self-Decoding Payload**  
**Goal:** Build a small encoded script that prints its own source code.  

**Instructions:**  
- Combine encoding, string manipulation, and `exec()` to create a script that decodes and prints itself when run.  
- Extra: make it readable only after decoding.

---