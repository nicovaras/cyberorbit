## 🔬 Subtopic 7.5: Log Analysis & Querying (Kibana/Splunk)

**Goal:** Learn fundamental techniques for searching, filtering, aggregating, and visualizing log data within Kibana (using KQL) or Splunk (using SPL) to identify patterns, anomalies, and specific events.

**Resources:**

* **Kibana Query Language (KQL):** [Kibana Query Language Docs](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)
* **Splunk Search Processing Language (SPL):** [SPL Tutorial](https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/WelcometotheSearchTutorial), [Search Command Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Commands)
* **Your Logging Platform:** Running ELK Stack with Kibana or Splunk Free instance (from 7.3) with ingested & parsed logs (from 7.2, 7.4).

**Test Environment / Tools Needed:**

* Running ELK Stack (with Kibana access) or Splunk Free instance (from 7.3).
* Ingested logs from various sources (Syslog, Web Server, Windows Events, potentially Sysmon) ideally parsed/normalized from Subtopic 7.4.
* Web browser access to Kibana or Splunk Web UI.

---

### 🔹 **Exercise 1: Basic Searching and Filtering**

**Goal:** Practice using the core search/query languages (KQL or SPL) to find specific log events based on keywords and field values.

**Instructions:**

1.  Access Kibana Discover or Splunk Search. Select the appropriate index pattern/source/index.
2.  Perform basic keyword searches for terms likely present in your logs (e.g., `error`, `failed`, `login`, `sshd`, a specific username, a specific IP address).
3.  Use field-based filtering:
    * **Kibana (KQL):** `host.name : "log-client"`, `response : 404`, `process.name : "sshd"`, `winlog.event_id : 4625`
    * **Splunk (SPL):** `host="log-client"`, `status=404`, `process="sshd"`, `EventCode=4625`
4.  Combine filters using boolean logic:
    * **Kibana (KQL):** `event.original : "failed" and user.name : "admin"`
    * **Splunk (SPL):** `failed user=admin` OR `"failed" AND user="admin"`
5.  Use wildcard searches (use cautiously on large datasets):
    * **Kibana (KQL):** `source.ip : "192.168.1.*"`
    * **Splunk (SPL):** `source_ip="192.168.1.*"` OR `cidrmatch("192.168.1.0/24", source_ip)`
6.  **Challenge:** Construct a query to find all web server access log entries that are *NOT* HTTP status code 200 (Success) and originate from a specific IP address.

---

### 🔹 **Exercise 2: Working with Time Ranges**

**Goal:** Use the time range selector and time-based query operators effectively.

**Instructions:**

1.  Use the graphical time range selector in Kibana/Splunk to view logs from specific periods (e.g., Last 15 minutes, Last 24 hours, a specific date range).
2.  Observe how the event counts and timeline visualization change as you adjust the time range.
3.  Perform searches within specific timeframes (e.g., find all `error` messages that occurred between 2 AM and 4 AM yesterday).
4.  **(Splunk Specific):** Learn basic time modifiers in SPL searches, e.g., `earliest=-1h latest=now`, `earliest="04/09/2025:10:00:00" latest="04/09/2025:11:00:00"`.
5.  **(Kibana Specific):** Use the time filter in the KQL bar if needed, though the graphical selector is more common.
6.  **Challenge:** Construct a query to find events that occurred *exactly* 3 days ago, within a one-hour window.

---

### 🔹 **Exercise 3: Basic Aggregations and Visualizations**

**Goal:** Use aggregation functions and visualization tools to summarize log data and identify trends or outliers.

**Instructions:**

1.  **Using Kibana Lens / Visualize or Splunk Aggregation Commands:**
2.  **Count Events Over Time:** Create a simple line chart showing the count of all log events (or specific event types like errors) over the selected time range.
3.  **Top Values:** Generate a data table or pie chart showing the top 10 source IP addresses hitting your web server (`source.ip` or equivalent field).
4.  **Grouped Counts:** Create a stacked bar chart showing the count of web server status codes (e.g., 200, 404, 500) broken down by client IP address for the top offenders.
5.  **Failed Logins:** Create a metric visualization showing the total count of failed login events (e.g., `winlog.event_id: 4625` or `syslog message contains 'Failed password'`) in the last hour.
6.  **(Splunk Specific):** Use SPL commands like `stats count by <field>`, `top <field>`, `rare <field>`. For example: `index=* sourcetype=access_combined | stats count by status` or `index=wineventlog EventCode=4625 | top limit=10 user`.
7.  **(Kibana Specific):** Use the Lens editor or Aggregation-based visualizations. Drag-and-drop fields and choose aggregation types (Count, Top Values, etc.).
8.  **Challenge:** Create a visualization showing the average web server response time (`response_time` field, if parsed) broken down by requested URL path (`url.path` or equivalent). Identify potentially slow endpoints.

---

### 🔹 **Exercise 4: Correlating Events Across Sources (Basic)**

**Goal:** Manually correlate related events from different log sources to trace user or system activity.

**Instructions:**

1.  **Scenario:** Investigate a user (`testuser`) accessing a web application.
2.  **Step 1 (Login):** Search your OS authentication logs (Linux `auth.log`/`secure` or Windows Security Event Log ID 4624) for successful login events for `testuser` around a specific time. Note the source IP address used for login.
3.  **Step 2 (Web Access):** Search your web server access logs for requests originating from the IP address found in Step 1, occurring *after* the login time. What resources did `testuser` (or the IP associated with their session) access?
4.  **Step 3 (Potential Errors):** Search web server error logs or OS system logs around the same time frame for any errors potentially related to the user's activity or the resources they accessed.
5.  Document the sequence of events found across the different log sources for this single activity. Explain how having logs in a central place simplifies this type of manual correlation.
6.  **Challenge:** Add firewall logs to the mix (if available). Can you correlate the web access requests (Step 2) with corresponding "allow" entries in the firewall logs based on source/destination IP and port?

---

### 🧪 **(Optional) Lab: Splunk/ELK Search Practice**

**Goal:** Utilize guided labs to practice querying and analyzing data in Splunk or ELK.

**Instructions:**

* **Splunk:**
    * Sign up for a free Splunk account if needed.
    * Use Splunk's own [Search Tutorial](https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/WelcometotheSearchTutorial) using their sample data.
    * Explore TryHackMe rooms like "[Splunk](https://tryhackme.com/room/splunk)" or "[Splunk 2](https://tryhackme.com/room/splunk2)" (content may vary).
* **ELK:**
    * Explore Elastic's documentation and tutorials for Kibana Discover and KQL.
    * Look for TryHackMe rooms focused on ELK or Kibana if available (less common than Splunk labs usually).
* Focus on mastering basic filtering, field extraction (at search time if needed), and simple statistics/aggregations.

---