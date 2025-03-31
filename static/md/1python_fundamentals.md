
## 📄 PDF: Topic 1 – Python Language Fundamentals

**📚 Resource:**  
*“Automate the Boring Stuff with Python” – Chapters 1, 2, 3 & 10*  
[https://automatetheboringstuff.com/](https://automatetheboringstuff.com/)

---

### 🔹 Exercise: Functions and Error Handling  
**Goal:** Build a reusable tool that doesn't die on garbage input.  
**Instructions:**  
- Create a file with dozens of IPs—some valid, some broken, some just nonsense.  
- Write a function that decides if an IP address looks like a local network address.  
- Loop through the file and feed the entries into the function.  
- If something breaks, don’t crash—handle it.  
- At the end, show how many valid, invalid, and local IPs you found.

---

### 🔹 Exercise: Reading CLI Arguments with `argparse`  
**Goal:** Make your script behave like a real Linux tool.  
**Instructions:**  
- Accept a path to a file with `--file`, and a keyword with `--filter`.  
- Print only the lines in that file that match the keyword.  
- Add a `--count` flag that shows how many matching lines were found.  
- Don’t print anything unless the user passes at least one valid argument—handle it smartly.

---

### ✨ Bonus: Write Your Own `grep` Clone in Python  
**Goal:** Build a tiny but powerful text search utility.  
**Instructions:**  
- Create a script that takes a keyword and a file path.  
- Print only the lines that match, optionally ignoring case.  
- Add your own `--help` message with usage examples.  
- Extra: support a flag to show line numbers, and highlight the matched keyword.  
- Test it on a large file (like a log or a book). Try to break it.

