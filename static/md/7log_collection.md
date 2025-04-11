## 🔬 Subtopic 7.2: Log Collection, Forwarding & Shipping

**Goal:** Configure standard OS logging daemons (rsyslog, syslog-ng) for remote forwarding and set up log shippers (like Beats) to collect logs from files and system sources.

**Resources:**

* **Syslog:** `rsyslog.conf` documentation (`man rsyslog.conf`), `syslog-ng.conf` documentation (`man syslog-ng.conf`)
* **Elastic Beats:** [Filebeat Overview](https://www.elastic.co/beats/filebeat), [Winlogbeat Overview](https://www.elastic.co/beats/winlogbeat) (Check specific setup guides for your OS)
* **Tools:** `systemctl`, text editors, `netcat` (`nc`) or `tcpdump` for verifying network traffic.

**Test Environment / Tools Needed:**

* **Two** Linux VMs (e.g., Ubuntu Server) on the same network for syslog forwarding exercises. Let's call them `log-client` and `log-server`.
* (Optional) One Windows VM for Winlogbeat exercise.
* Root/sudo privileges on all VMs.
* Ensure network connectivity between VMs (check firewalls if necessary - allow UDP/514 or TCP/514 for syslog).

---

### 🔹 **Exercise 1: Configure Rsyslog Remote Forwarding (Client)**

**Goal:** Configure the rsyslog daemon on one Linux machine (`log-client`) to send its logs to another machine (`log-server`) over the network.

**Instructions:**

1.  On the `log-client` VM:
    * Ensure `rsyslog` is installed and running (`systemctl status rsyslog`).
    * Edit the rsyslog configuration file (`/etc/rsyslog.conf` or files in `/etc/rsyslog.d/`).
    * Add a forwarding rule at the end of the configuration (or in a new `.conf` file in `/etc/rsyslog.d/`). This rule tells rsyslog to send all logs (`*.*`) to the remote server. Replace `<log_server_ip>` with the actual IP of your `log-server` VM.
        * For UDP (common, simpler, less reliable): `*.* @<log_server_ip>:514`
        * For TCP (more reliable): `*.* @@<log_server_ip>:514` (Requires receiver configured for TCP too). Let's start with UDP.
    * Save the configuration file.
    * Restart the rsyslog service: `sudo systemctl restart rsyslog`.
2.  Generate some log messages on `log-client` (e.g., `logger "Testing syslog forwarding from client"`).
3.  On the `log-server` VM (temporarily), use `tcpdump` or `nc` to listen on the syslog port to verify traffic is arriving:
    * `sudo tcpdump -i any -n udp port 514`
    * Or potentially `nc -ul 514` (may not show continuous stream well).
    * You should see packets arriving from `log-client`'s IP when you generate logs on the client.
4.  **Challenge:** Modify the client configuration to *only* forward messages with priority `*.info` or higher. Test again.

---

### 🔹 **Exercise 2: Configure Rsyslog Remote Receiving (Server)**

**Goal:** Configure the rsyslog daemon on the `log-server` VM to listen for incoming remote logs and write them to a specific file.

**Instructions:**

1.  On the `log-server` VM:
    * Ensure `rsyslog` is installed and running.
    * Edit the rsyslog configuration (`/etc/rsyslog.conf` or files in `/etc/rsyslog.d/`).
    * Uncomment or add lines to enable the UDP (and/or TCP) syslog input module:
        ```
        # Provides UDP syslog reception
        module(load="imudp")
        input(type="imudp" port="514")

        # Provides TCP syslog reception (Optional - if using TCP forwarding)
        # module(load="imtcp")
        # input(type="imtcp" port="514")
        ```
    * Add a rule (typically placed *before* default rules that write to `/var/log/syslog`) to capture remote logs into a separate file based on the sending host. Create a template first:
        ```
        # Template for remote logs (creates files like /var/log/remote/HOSTNAME.log)
        template(name="RemoteHost" type="string" string="/var/log/remote/%HOSTNAME%.log")

        # Log messages from remote hosts to specific files
        if $FROMHOST_IP != '127.0.0.1' then action(type="omfile" dynaFile="RemoteHost")
        # Optional: Stop processing this message further if you don't want it in local logs too
        # if $FROMHOST_IP != '127.0.0.1' then stop
        ```
    * Ensure the `/var/log/remote/` directory exists and has appropriate permissions for `syslog` user/group.
    * Save the configuration file.
    * Restart the rsyslog service: `sudo systemctl restart rsyslog`.
2.  Generate log messages on the `log-client` VM again (`logger "Testing log writing on server"`).
3.  On the `log-server` VM, check the `/var/log/remote/` directory. You should find a file named after the `log-client`'s hostname (e.g., `/var/log/remote/log-client.log`). View this file (`tail -f ...`) and verify the test messages are appearing.
4.  **Challenge:** Modify the server template and rules to store logs based on the *sending application name* (`%programname%`) instead of, or in addition to, the hostname.

---

### 🔹 **Exercise 3: Installing and Configuring Filebeat (Linux)**

**Goal:** Use Filebeat (an Elastic Beat) to read log data directly from a file and configure it to output (initially just to the console for testing).

**Instructions:**

1.  **Setup:** On your `log-client` Linux VM, ensure you have a log file being written to (e.g., the Apache/Nginx access log from Subtopic 7.1 Ex2, or `/var/log/syslog`).
2.  **Install Filebeat:** Download and install the Filebeat DEB or RPM package from the Elastic website ([Downloads Page](https://www.elastic.co/downloads/beats/filebeat)). Follow their installation instructions.

3.  **Configure Filebeat:** Edit the main configuration file (`/etc/filebeat/filebeat.yml`).
    * Find the `filebeat.inputs:` section. Disable the default system log input if present (or modify it).
    * Add or enable an input of type `log` (previously `filestream`). Specify the `paths` to the log file(s) you want to collect (e.g., `/var/log/apache2/access.log` or `/var/log/syslog`).
        ```yaml
        filebeat.inputs:
        - type: log
          enabled: true
          paths:
            - /var/log/syslog
            #- /var/log/apache2/*.log
        ```
    * Find the `output:` section. For initial testing, **comment out** the Elasticsearch output (`output.elasticsearch:`) and **enable** the Console output:
        ```yaml
        #output.elasticsearch:
        #  hosts: ["localhost:9200"]
        output.console:
          pretty: true
        ```
    * Save the file.
4.  **Run Filebeat:** Start Filebeat directly in the foreground for testing: `sudo filebeat -e -c /etc/filebeat/filebeat.yml` (`-e` logs to stderr, `-c` specifies config).
5.  Generate new log entries in the file(s) Filebeat is monitoring (e.g., `logger "Testing filebeat pickup"`, access the web server).
6.  Observe the output in the Filebeat console. You should see JSON objects representing the log events being read from the file. Note the fields Filebeat adds (like `@timestamp`, `agent`, `log.file.path`). Press `Ctrl+C` to stop Filebeat.
7.  **Challenge:** Configure Filebeat to read *multiple* log files (e.g., both `syslog` and `apache access.log`) using multiple input entries or path globbing.

---

### 🔹 **(Optional) Exercise 4: Installing and Configuring Winlogbeat (Windows)**

**Goal:** Use Winlogbeat to collect Windows Event Logs and output them to the console.

**Instructions:**

1.  **Setup:** On your Windows VM.
2.  **Install Winlogbeat:** Download the Winlogbeat ZIP file from the Elastic website. Extract it (e.g., to `C:\Program Files\Winlogbeat`).
3.  **Configure Winlogbeat:** Edit the `winlogbeat.yml` file in the extracted directory.
    * Review the `winlogbeat.event_logs:` section. By default, it often collects Application, Security, System logs. You can keep these defaults or customize the list (e.g., add `Microsoft-Windows-Sysmon/Operational` if Sysmon is installed).
    * Find the `output:` section. Comment out `output.elasticsearch:` and enable `output.console:` with `pretty: true` (similar to Filebeat).
    * Save the file.
4.  **Run Winlogbeat:** Open PowerShell **as Administrator**, navigate to the Winlogbeat directory, and run it in the foreground:
    `.\winlogbeat.exe -e -c .\winlogbeat.yml`
5.  Generate some events on the Windows machine (e.g., log in/out, start/stop a service - things that would write to Application, Security, or System logs).
6.  Observe the console output. You should see JSON objects representing Windows Event Log entries. Note the fields provided (e.g., `winlog.event_id`, `message`, `user.name`). Press `Ctrl+C` to stop.
7.  **Challenge:** Configure Winlogbeat to collect logs only for specific Event IDs from the Security log (e.g., only logon success/failure events 4624, 4625). Use the `include_event_ids` option within the `winlogbeat.event_logs:` section for the Security log.

---

### 🔹 **Exercise 5: Comparing Collection Methods**

**Goal:** Reflect on the practical differences between agent-less (syslog) and agent-based (Beats) log collection.

**Instructions:**

1.  Based on your experience in Exercises 1-4, compare Syslog forwarding vs. Beats agents in terms of:
    * Ease of initial setup and configuration.
    * Reliability of transport (UDP vs. TCP potential in Syslog vs. Beats internal handling).
    * Log enrichment (Which method adds more metadata automatically? Refer to console output from Beats).
    * Resource usage on the client machine (conceptual - agents consume some resources).
    * Flexibility (Which can more easily collect from arbitrary files vs. system logs?).
2.  Write a short summary (2-3 paragraphs) outlining the pros and cons of each approach and scenarios where you might prefer one over the other.
3.  **Challenge:** Research how secure log transport can be achieved with both methods (e.g., TLS for Syslog, native TLS in Beats configuration).

---