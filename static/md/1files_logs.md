## 🐍 Subtopic 1.2: Working with Data: Files, Logs & Structured Formats

**Goal:** Read, parse, and manipulate common text-based data formats frequently encountered in security analysis, such as configuration files, logs, and tool outputs.

**Resources:**

* **Python File I/O:** [Reading and Writing Files (Official Tutorial)](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
* **Python `csv` module:** [Documentation](https://docs.python.org/3/library/csv.html)
* **Python `json` module:** [Documentation](https://docs.python.org/3/library/json.html)
* **Python `re` module (Regular Expressions):** [Documentation](https://docs.python.org/3/library/re.html) & [Tutorial](https://docs.python.org/3/howto/regex.html)
* **Online Regex Tester:** [Regex101](https://regex101.com/) (Useful for building and testing patterns)
* **Sample Apache Log:** [Example Log File](https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs) (Save this raw file for Exercise 4)

---

### 🔹 **Exercise 1: Wordlist Processing**

**Goal:** Practice basic file reading and string manipulation.

**Instructions:**

1.  Find a common wordlist file online (e.g., search for "rockyou.txt sample" - use a small sample for testing) or create a simple text file with words on separate lines, some with leading/trailing whitespace.
2.  Write a Python script to open and read the file line by line.
3.  For each line, remove any leading or trailing whitespace.
4.  Print only the words that meet a specific criterion (e.g., longer than 8 characters).
5.  **Challenge:** Count the occurrences of each processed word and print the top 5 most frequent words.

---

### 🔹 **Exercise 2: Parsing CSV Data**

**Goal:** Use the `csv` module to read and extract specific information from CSV files, a common export format for security tools.

**Instructions:**

1.  Create a sample CSV file representing vulnerability data (e.g., `scan_results.csv`) with columns like `IPAddress`, `Hostname`, `Port`, `VulnerabilityName`, `Severity`. Populate it with a few rows of fake data.
2.  Write a Python script using the `csv` module (`csv.reader` or `csv.DictReader`) to read this file.
3.  Print only the rows where the `Severity` column is "High" or "Critical".
4.  **Challenge:** Modify the script to group the results by `IPAddress` and list all high/critical vulnerabilities found for each IP.

---

### 🔹 **Exercise 3: Navigating JSON Data**

**Goal:** Use the `json` module to parse and access data within JSON structures, common in APIs and threat intelligence feeds.

**Instructions:**

1.  Find a sample JSON dataset online (e.g., search for "sample security threat feed json" or use a simple example from `httpbin.org/json`) or create your own nested JSON structure representing system information.
2.  Write a Python script to load the JSON data from a file or a string.
3.  Navigate the JSON structure to extract specific nested values (e.g., extract all 'indicator' values from a list of threat objects).
4.  Print the extracted values.
5.  **Challenge:** Handle potential `KeyError` exceptions gracefully if expected keys are missing in the JSON structure.

---

### 🔹 **Exercise 4: Extracting IPs with Regex**

**Goal:** Use regular expressions (`re` module) to find patterns like IP addresses within unstructured text, such as log files.

**Instructions:**

1.  Use the sample Apache log file linked in the Resources.
2.  Write a Python script that reads the log file line by line.
3.  Develop a regular expression pattern to match IPv4 addresses. Use Regex101 (linked above) to help test and refine your pattern.
4.  Use the `re.findall()` or `re.search()` method to find all IP addresses on each line. Remember that Apache logs often contain two IPs per line (client and server) - your pattern should ideally capture the client IP at the start of the line.
5.  Collect all unique IP addresses found across the entire log file.
6.  Print the list of unique IP addresses.
7.  **Challenge:** Refine the regex or script logic to specifically capture only the *first* IP address (the client IP) on each line of the Apache log format.

---

### 💡 **Project: Log File IP Extractor**

**Goal:** Combine file handling and regular expressions to process multiple log files and consolidate findings.

**Instructions:**

1.  Create a directory containing a few copies or variations of the sample Apache log file (or other sample log files).
2.  Write a script that takes a directory path as a command-line argument.
3.  The script should iterate through all files in the specified directory.
4.  For each file, it should apply the IP address extraction logic developed in Exercise 4.
5.  Aggregate all *unique* IP addresses found across *all* files in the directory.
6.  Write the final list of unique IP addresses to an output file named `unique_ips.txt`.
7.  **Portfolio Guidance:** Add this script to your GitHub repository. Update the README to explain its purpose (aggregating unique IPs from log directories), usage (command-line arguments), and requirements. Include sample input/output if helpful.