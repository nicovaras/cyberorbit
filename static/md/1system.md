## 🐍 Subtopic 1.5: System Interaction & Automation

**Goal:** Learn how to use Python to execute operating system commands, manage files and processes, and automate local administrative or security-related tasks.

**Resources:**

* **Python `subprocess` module:** [Documentation](https://docs.python.org/3/library/subprocess.html)
* **Python `os` module:** [Documentation](https://docs.python.org/3/library/os.html)
* **Python `shutil` module:** [Documentation](https://docs.python.org/3/library/shutil.html) (High-level file operations)

---

### 🔹 **Exercise 1: Running OS Commands & Capturing Output**

**Goal:** Execute common OS diagnostic commands from Python and process their output.

**Instructions:**

1.  Write a Python script using `subprocess.run()`.
2.  Execute a basic command relevant to your OS (e.g., `ipconfig` or `ip a` for network info, `ps aux` or `tasklist` for processes, `ls -l` or `dir` for directory listing).
3.  Capture the command's standard output and standard error. Set `capture_output=True` and `text=True` in `subprocess.run()`.
4.  Print the captured standard output.
5.  Check the return code of the command (`result.returncode`) to see if it executed successfully (usually 0).
6.  **Challenge:** Parse the captured output of the network information command (`ipconfig`/`ip a`) to extract and print only the primary IPv4 address of your machine. This will likely involve string splitting or regular expressions.

---

### 🔹 **Exercise 2: File System Navigation & Checks**

**Goal:** Use the `os` module to interact with the file system, listing directories and checking file properties.

**Instructions:**

1.  Write a Python script.
2.  Use `os.listdir()` to get a list of all files and directories in the current working directory (`.`) or another specified path.
3.  Iterate through the list obtained.
4.  For each item, use `os.path.isfile()` and `os.path.isdir()` to determine if it's a file or a directory.
5.  Use `os.path.getsize()` to find the size (in bytes) of each file.
6.  Print the name, type (file/dir), and size (for files) of each item.
7.  **Challenge:** Modify the script to recursively explore subdirectories and list their contents as well. Use `os.walk()`.

---

### 🔹 **Exercise 3: File Operations based on Criteria**

**Goal:** Use `os` and `shutil` to organize files based on their properties.

**Instructions:**

1.  Create a test directory and populate it with a few empty files of different types (e.g., `report.txt`, `image.jpg`, `script.py`, `data.log`, `archive.zip`).
2.  Write a Python script that scans this directory.
3.  For each file found, determine its extension using `os.path.splitext()`.
4.  Create subdirectories within the test directory based on file types found (e.g., `txt_files`, `img_files`, `log_files`). Use `os.makedirs(exist_ok=True)`.
5.  Use `shutil.move()` to move each file into the corresponding subdirectory based on its extension.
6.  Print messages indicating which files were moved where.
7.  **Challenge:** Add error handling in case file moves fail (e.g., permissions issues). Only move files, skip directories.

---

### 🔹 **Exercise 4: Basic Process Interaction**

**Goal:** Use `subprocess` to start and potentially interact with another process.

**Instructions:**

1.  Write a Python script using `subprocess.Popen()` to start a simple, long-running process in the background. A good candidate is Python's built-in web server: `python -m http.server 8080`. `Popen` allows the main script to continue running.
2.  Store the process object returned by `Popen`. Print its Process ID (`process.pid`).
3.  Wait for a few seconds (`time.sleep(5)`).
4.  Use `process.poll()` to check if the process is still running (it should be).
5.  Use `process.terminate()` or `process.kill()` to stop the background web server process.
6.  Wait briefly again and use `process.poll()` to confirm it has terminated.
7.  **Challenge:** Modify the script to capture the standard output of the background process *while it runs* (requires working with `proc.stdout` potentially using threads or non-blocking reads - this might be more advanced). Alternatively, redirect the process output to a file using `stdout=subprocess.PIPE` or `stdout=open(...)` in `Popen`.

---

### 💡 **Project: Directory Change Monitor**

**Goal:** Create a script that monitors a specified directory for newly created files and logs information about them.

**Instructions:**

1.  Write a script that takes a directory path to monitor as a command-line argument.
2.  The script should periodically (e.g., every 5 seconds using `time.sleep()`) scan the directory.
3.  Maintain a set of filenames known to exist in the directory from the previous scan.
4.  On each scan, compare the current list of files with the known set to identify any newly created files.
5.  For each new file found:
    * Log a message to the console (or a log file) indicating the new file's name.
    * Use `subprocess.run()` to execute the `file` command (Linux/macOS) or a similar basic check (Windows - perhaps just log timestamp and size) on the new file and log its output.
    * Add the new filename to the set of known files.
6.  Run this script in a loop (e.g., `while True:`). Include instructions on how to stop it (Ctrl+C).
7.  **Portfolio Guidance:** Add this monitor script to GitHub. Explain its purpose (detecting new files), how to run it, and potential use cases (e.g., monitoring a download folder, watching for indicator drops). Mention its limitations (e.g., basic polling method, doesn't detect modifications/deletions).