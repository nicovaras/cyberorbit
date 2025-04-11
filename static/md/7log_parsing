## 🔬 Subtopic 7.4: Log Parsing & Normalization (Grok/JSON)

**Goal:** Learn techniques to parse unstructured log data into meaningful fields (using Grok) and handle structured formats like JSON, preparing logs for effective searching and analysis within your centralized logging platform.

**Resources:**

* **Grok Pattern Debugger:** Kibana Dev Tools > Grok Debugger (if using ELK), online Grok debuggers (e.g., `grokdebug.herokuapp.com`).
* **Grok Patterns:** [Logstash Grok Filter Plugin Docs](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html), [Common Grok Patterns](https://github.com/logstash-plugins/logstash-patterns-core/tree/main/patterns).
* **Logstash/Ingest Node Config:** For applying Grok/JSON parsing (if using ELK).
* **Splunk Docs:** Search for "props.conf", "transforms.conf", "INDEXED_EXTRACTIONS" for field extraction at index time or "KV_MODE" for key-value/JSON parsing at search time.
* **Sample Logs:** Apache/Nginx access logs, Linux syslog messages, sample JSON logs.

**Test Environment / Tools Needed:**

* Running basic ELK Stack or Splunk Free instance (from Subtopic 7.3) accessible via browser.
* Sample log lines (Apache, syslog, JSON) for testing in debuggers or sending to your platform.
* Text editor for configuration files (Logstash pipeline, Splunk props/transforms).
* **Important:** Assumes logs (or at least samples) can be ingested into your chosen platform.

---

### 🔹 **Exercise 1: Parsing Web Server Logs with Grok**

**Goal:** Use Grok patterns to extract key fields (IP address, timestamp, request path, status code, user agent) from standard Apache/Nginx access logs.

**Instructions:**

1.  Obtain a sample line from an Apache Combined Log Format or Nginx default access log.
2.  Use the Kibana Grok Debugger (or an online one) to interactively build a Grok pattern that correctly parses the sample line.
    * Start with pre-defined patterns like `%{IPORHOST:clientip}`, `%{USER:ident}`, `%{USER:auth}`, `\[%{HTTPDATE:timestamp}\]`, `%{WORD:verb}`, `%{URIPATHPARAM:request}`, `HTTP/%{NUMBER:httpversion}`, `%{NUMBER:response:int}`, `%{NUMBER:bytes:int}`, `%{QS:referrer}`, `%{QS:agent}`.
    * Combine these patterns, adjusting for spaces and delimiters (`"`, `\[`, `\]`), until the debugger successfully extracts all desired fields from your sample line.
3.  **(If using ELK):** Integrate your working Grok pattern into a Logstash `filter` section or an Elasticsearch Ingest Node pipeline using the `grok` processor. Re-ingest some web server logs and verify the fields appear correctly structured in Kibana Discover.
4.  **(If using Splunk):** Research how to use the Field Extractor utility in the Splunk UI or configure `props.conf` / `transforms.conf` with regular expressions (similar logic to Grok but different syntax) to achieve similar field extraction at search time or index time. Test on ingested web logs.
5.  **Challenge:** Modify your Grok pattern to also handle logs where the referrer or user agent might be missing (represented by `"-"`), ensuring it still parses correctly.

---

### 🔹 **Exercise 2: Parsing Syslog Messages with Grok**

**Goal:** Apply Grok patterns to parse standard RFC 3164 or RFC 5424 syslog messages.

**Instructions:**

1.  Obtain sample Linux syslog lines (e.g., from `/var/log/syslog` or `journalctl`), including messages from different programs (sshd, cron, kernel).
2.  Use a Grok Debugger with common syslog patterns (`%{SYSLOGTIMESTAMP:timestamp}`, `%{SYSLOGHOST:hostname}`, `%{PROG:program}(?:\[%{POSINT:pid}\])?`, `%{GREEDYDATA:message}`).
3.  Construct a Grok pattern to parse the timestamp, hostname, program name, PID (if present), and the remaining message content for typical syslog formats. Test with different sample lines.
4.  **(If using ELK/Splunk):** Integrate this pattern into your Logstash/Ingest/Splunk configuration for syslog sources. Verify fields are extracted correctly for ingested syslog data.
5.  **Challenge:** Some syslog messages might have slightly different timestamp formats or structures. How can you make your Grok pattern more robust using alternations (`|`) or optional groups (`(?:...)?`) to handle variations?

---

### 🔹 **Exercise 3: Handling JSON Formatted Logs**

**Goal:** Configure your logging platform to automatically parse logs already formatted in JSON.

**Instructions:**

1.  Find or create sample log lines formatted as JSON (many modern applications can log directly in JSON). Example:
    `{"timestamp": "2025-04-09T17:00:00Z", "level": "INFO", "service": "auth-svc", "user_id": "alice", "event": "login_success", "source_ip": "192.168.1.100"}`
2.  **(If using ELK):**
    * In Logstash, use the `json` filter plugin: `filter { json { source => "message" } }`. This parses the entire log line (usually in the `message` field) as JSON.
    * Alternatively, if Filebeat is shipping JSON logs, it can often parse them directly (configure Filebeat input).
    * In Elasticsearch Ingest Node, use the `json` processor.
3.  **(If using Splunk):**
    * Splunk often automatically detects and parses JSON logs at search time (check `KV_MODE=json` in `props.conf` for the relevant sourcetype).
    * Alternatively, configure index-time JSON parsing if needed.
4.  Send your sample JSON logs to your configured platform (e.g., using `netcat` to send to a Logstash TCP input, or have Filebeat read a file of JSON logs).
5.  Verify in Kibana Discover or Splunk Search that the JSON fields (timestamp, level, service, user_id, etc.) are automatically extracted as separate fields.
6.  **Challenge:** What happens if a log line *claims* to be JSON but is malformed? How can you configure error handling in Logstash (e.g., using `tags_on_failure`) or Splunk to identify parsing errors?

---

### 🔹 **Exercise 4: Introduction to Log Normalization (ECS/CIM)**

**Goal:** Understand the concept and importance of normalizing parsed log data into a common schema for easier correlation and analysis. **(Conceptual & Exploration focused)**

**Instructions:**

1.  Research the concept of log normalization and common schemas:
    * **Elastic Common Schema (ECS):** [ECS Website](https://www.elastic.co/guide/en/ecs/current/index.html). Explore the defined field names for common concepts (e.g., `source.ip`, `destination.ip`, `user.name`, `event.action`).
    * **Splunk Common Information Model (CIM):** [Splunk CIM Docs](https://docs.splunk.com/Documentation/CIM/latest/User/Overview). Explore its standard field names and data models (e.g., Authentication, Network Traffic).
2.  Consider the logs you parsed in previous exercises (Web, Syslog, JSON). Identify fields that represent the same concept but might have different names in the raw logs (e.g., `clientip` vs `source_ip` vs `remote_addr`; `user` vs `user_id` vs `uid`).
3.  Explain why mapping these different source field names to a common schema name (like `source.ip` or `user.name`) during parsing (e.g., using Logstash `mutate` filter, Ingest Node `rename` processor, or Splunk field aliases/calculated fields) makes cross-source analysis much easier.
4.  Provide 2-3 examples of queries or correlations that become simpler when using a normalized schema compared to querying raw, unnormalized field names.
5.  **Challenge:** Browse the ECS or CIM documentation. Find the recommended field names for: Process ID, Destination Port, File Path, and Event Outcome (e.g., success/failure).

---

### 💡 **(Optional) Project: Advanced Log Parser Configuration**

**Goal:** Develop and document a robust parsing configuration (Logstash filter block, Ingest Node pipeline, or Splunk props/transforms) for a specific, non-trivial log type not covered by default patterns.

**Instructions:**

1.  Choose a specific log format (e.g., a particular firewall brand's logs, VPN logs, custom application logs, multi-line Java stack traces). Obtain realistic sample log lines.
2.  Using your chosen platform's tools (Grok Debugger, Regex testers, platform documentation), develop the necessary parsing logic (Grok patterns, regex extractions, JSON handling, potentially date/mutate/geoip filters in Logstash) to extract all relevant fields.
3.  Handle potential variations or optional fields in the log format gracefully.
4.  If possible, normalize the extracted fields to align with ECS or CIM naming conventions.
5.  Create a configuration file (e.g., `my_firewall_parser.conf` for Logstash, Splunk config stanzas, or JSON for Ingest Pipeline) containing your parsing logic.
6.  **Portfolio Guidance:** Create a GitHub repository containing:
    * Your parsing configuration file(s).
    * Sample *anonymized* input log lines used for testing.
    * A `README.md` file that:
        * Describes the log source and format being parsed.
        * Explains the parsing logic used (key Grok patterns, regex, filters).
        * Lists the key fields extracted and how they map to a common schema (if normalization was done).
        * Provides instructions on how to integrate this configuration into Logstash/Elasticsearch/Splunk.

---