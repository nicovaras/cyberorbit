## 🔬 Subtopic 7.7: Endpoint Event Monitoring with Sysmon

**Goal:** Learn to install, configure, and analyze logs from Windows Sysmon (System Monitor) to gain deep visibility into endpoint activities like process creation, network connections, and registry modifications for threat detection and incident response.

**Resources:**

* **Sysinternals Sysmon:** [Official Page & Download](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon), [Sysmon Overview Blog](https://techcommunity.microsoft.com/t5/sysinternals-blog/sysmon-suspicious-activity-guide/ba-p/227416)
* **Sysmon Configuration:** [SwiftOnSecurity Sysmon Config](https://github.com/SwiftOnSecurity/sysmon-config) (Excellent baseline), Olaf Hartong's modular config ([GitHub](https://github.com/olafhartong/sysmon-modular)). XML Schema (`sysmon -s`).
* **Sysmon Event IDs:** List available online (e.g., search "Sysmon event IDs cheat sheet"). Key ones include 1 (Process Create), 3 (Network Connect), 11 (File Create), 12/13 (Registry), 22 (DNS Query).
* **Tools:** `sysmon.exe` (command line), Event Viewer (`eventvwr.msc`), XML editor (for config).

**Test Environment / Tools Needed:**

* A Windows VM (Pro/Enterprise/Server recommended). **Sysmon requires Administrator privileges to install and configure.**
* Downloaded Sysmon executable (`sysmon.exe` or `sysmon64.exe`).
* Downloaded baseline Sysmon configuration file (e.g., SwiftOnSecurity's `sysmonconfig-export.xml`).
* Access to Event Viewer: `Applications and Services Logs` > `Microsoft` > `Windows` > `Sysmon` > `Operational`.

---

### 🔹 **Exercise 1: Installing Sysmon with a Baseline Configuration**

**Goal:** Install the Sysmon service using a well-regarded community configuration file to start logging detailed endpoint events.

**Instructions:**

1.  Download `Sysmon` from the official Sysinternals site.
2.  Download a baseline configuration file (e.g., clone or download the XML from SwiftOnSecurity's GitHub repo). Review the XML structure briefly - notice the `<RuleGroup>` and `<EventFiltering>` sections.
3.  Open `cmd` or `PowerShell` **as Administrator**.
4.  Navigate to the directory containing `Sysmon.exe` (or `Sysmon64.exe`).
5.  Install Sysmon using the `-accepteula` (to bypass the license prompt) and `-i` flags, specifying the configuration file:
    `.\Sysmon64.exe -accepteula -i C:\path\to\your\sysmonconfig-export.xml`
    (Adjust executable name and config file path).
6.  Verify the Sysmon service is installed and running: `sc query Sysmon64` (or `Sysmon`) or check `services.msc`.
7.  Open Event Viewer and navigate to the Sysmon operational log (`Applications and Services Logs > Microsoft > Windows > Sysmon > Operational`). You should start seeing events populate shortly.
8.  **Challenge:** View the currently loaded Sysmon configuration using the command line: `.\Sysmon64.exe -c`. Compare it to the XML file you used for installation.

---

### 🔹 **Exercise 2: Analyzing Process Creation Events (Event ID 1)**

**Goal:** Examine Sysmon's detailed process creation logs (Event ID 1) to understand command lines, parent processes, and hashes.

**Instructions:**

1.  Generate some process activity on the Windows VM (e.g., open `cmd`, run `ipconfig`, open Notepad, browse the web briefly).
2.  In the Sysmon operational log (Event Viewer), filter for **Event ID 1 (Process Create)**.
3.  Examine the details of several recent events:
    * `UtcTime`: When the process started.
    * `ProcessGuid`, `ProcessId`: Unique identifiers for the new process.
    * `Image`: Full path to the executable image.
    * `CommandLine`: The exact command line used to launch the process (very useful!).
    * `CurrentDirectory`: Working directory.
    * `User`: The user context the process is running under.
    * `Hashes`: Hashes (e.g., SHA256, IMPHASH) of the executable file (useful for threat intel).
    * `ParentProcessGuid`, `ParentProcessId`, `ParentImage`, `ParentCommandLine`: Details of the process that *launched* this one (crucial for tracing activity).
4.  Find the event corresponding to your `ipconfig` execution. What was its parent process (likely `cmd.exe` or `powershell.exe`)?
5.  **Challenge:** Look for processes launched by `services.exe` or other system processes. Can you identify any unusual parent-child relationships that might warrant investigation in a real scenario?

---

### 🔹 **Exercise 3: Analyzing Network Connection Events (Event ID 3)**

**Goal:** Examine Sysmon's network connection logs (Event ID 3) to track outbound network activity initiated by processes.

**Instructions:**

1.  Generate some network activity (e.g., open a web browser and visit a site, use `ping google.com`, use `curl` or `powershell -c "iwr http://example.com"`).
2.  In the Sysmon operational log, filter for **Event ID 3 (Network Connect)**.
3.  Examine the details of several recent events:
    * `Image`: The process initiating the connection.
    * `User`: The user context.
    * `Protocol`: (e.g., tcp, udp).
    * `SourceIp`, `SourcePort`, `DestinationIp`, `DestinationPort`: The standard connection tuple.
    * `DestinationHostname`: (If resolved).
4.  Find the event corresponding to your browser accessing a website or your `ping` command. Correlate this with the Process Create event (Event ID 1) for the same process using `ProcessGuid` or `ProcessId` if needed.
5.  **Challenge:** Configure your Sysmon configuration XML (requires updating via `Sysmon64.exe -c config.xml`) to *exclude* common noisy network connections (e.g., browser traffic to known good domains, svchost traffic to Microsoft update servers) while still logging potentially suspicious connections. Apply the updated config and observe the difference in log volume.

---

### 🔹 **Exercise 4: Customizing Sysmon Configuration (Basic Rule)**

**Goal:** Modify the Sysmon XML configuration to add a custom rule, for example, to specifically include or exclude certain events based on criteria.

**Instructions:**

1.  Make a backup copy of your baseline Sysmon configuration XML file.
2.  Edit the XML configuration file. Locate the `<EventFiltering>` section.
3.  **Scenario:** Add a rule to specifically *log* (include) any process creation event (Event ID 1) where the image path contains `powershell.exe` AND the command line contains the string `-enc` (often used for encoded commands).
4.  Find the appropriate rule group for Event ID 1 (e.g., `<ProcessCreate>`). Add a new rule *within* that group. The logic might look something like this (syntax needs to be exact):
    ```xml
    <RuleGroup name="" groupRelation="or">
        <ProcessCreate onmatch="include">
            <Rule groupRelation="and">
                <Image condition="contains">powershell.exe</Image>
                <CommandLine condition="contains">-enc</CommandLine>
            </Rule>
        </ProcessCreate>
    </RuleGroup>
    ```
    *(Note: Ensure this rule is placed correctly relative to existing exclude rules. `onmatch="include"` means log if matched. You might place it before broad excludes).*
5.  Save the modified XML file.
6.  Apply the updated configuration using `cmd` or `PowerShell` **as Administrator**:
    `.\Sysmon64.exe -c C:\path\to\your\modified_config.xml`
7.  Verify the configuration was updated: `.\Sysmon64.exe -c` (should show XML reflecting your changes or hash changes).
8.  Test the rule: Run `powershell.exe -enc <SomeBase64String>` (replace with actual base64). Check the Sysmon Event Log for Event ID 1 related to this execution. It should be logged due to your include rule.
9.  **Challenge:** Add an *exclude* rule for Event ID 3 (Network Connection) to ignore connections made by your corporate browser (`chrome.exe`, `firefox.exe`) to the internal intranet domain (`*.internal.corp`).

---

### 💡 **Project: Sysmon Log Analysis for Threat Hunting**

**Goal:** Analyze Sysmon logs (either generated locally or from a sample dataset) to identify potentially suspicious activity patterns based on known techniques.

**Instructions:**

1.  **Data Source:** Either generate sufficient Sysmon logs on your test VM by performing various actions (running scripts, downloading files, etc.) OR find a sample Sysmon dataset online (e.g., from malware analysis sandboxes, CTFs, or projects like Mordor). Ensure logs are ingested into your ELK/Splunk instance if possible, or analyze directly in Event Viewer/WEF.
2.  **Scenario Research:** Choose 2-3 common MITRE ATT&CK techniques that can be detected using Sysmon data. Examples:
    * T1059.001: PowerShell Execution (Command Line contains `-enc`, `-nop`, suspicious scripts) - Event ID 1.
    * T1053.005: Scheduled Task Creation (`schtasks.exe` execution, Registry modifications related to tasks) - Event IDs 1, 12, 13.
    * T1047: Windows Management Instrumentation (WMI) Execution (`WmiPrvSE.exe` parent process, specific command lines) - Event ID 1.
    * T1547.001: Registry Run Keys / Startup Folder Persistence (Registry Set events for Run keys, File Create events in Startup folder) - Event IDs 11, 13.
    * T1003.001: LSASS Memory Dumping (`mimikatz.exe`, specific arguments to `rundll32`, suspicious access to `lsass.exe` process) - Event ID 1, potentially Event ID 10 (Process Access).
3.  **Analysis:** Using your chosen platform (Kibana/Splunk Querying, or Event Viewer filtering), search/filter your Sysmon logs for events and patterns corresponding to the techniques you researched.
4.  **Documentation:** Create a short report (Markdown) documenting your findings:
    * State the techniques you hunted for.
    * Describe the Sysmon Event IDs and specific indicators (command lines, parent processes, registry keys, etc.) you searched for.
    * Include the queries you used (KQL/SPL if applicable).
    * Present any potentially suspicious events found (anonymize sensitive data if needed). If no suspicious events were found in your test data, describe what you *would* expect to see for a true positive detection.
5.  **Portfolio Guidance:** Host your analysis report on GitHub. The `README.md` should explain the goal (threat hunting using Sysmon), the techniques investigated, the queries/methods used, and summarize the findings or expected findings. This demonstrates practical analysis skills using endpoint data.

---