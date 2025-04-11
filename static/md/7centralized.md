## 🔬 Subtopic 7.3: Basic Centralized Logging Platform Setup

**Goal:** Deploy basic instances of common centralized logging platforms (ELK Stack, Splunk Free) using Docker for testing log ingestion from forwarders/agents configured previously.

**Resources:**

* **Docker & Docker Compose:** [Installation Guides](https://docs.docker.com/engine/install/), [Compose Overview](https://docs.docker.com/compose/)
* **ELK Stack (Elastic):** [Official Docker Guide](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html), Simplified compose files available online (e.g., [deviantony/docker-elk](https://github.com/deviantony/docker-elk) - use with caution, review config).
* **Splunk:** [Official Splunk Docker Image](https://hub.docker.com/r/splunk/splunk/), [Splunk Free License limitations](https://docs.splunk.com/Documentation/Splunk/latest/Admin/MoreaboutSplunkFree)
* **Configuration Files:** Basic `logstash.conf`, `filebeat.yml`/`winlogbeat.yml` pointing to Logstash/Splunk, potentially Splunk `inputs.conf`.

**Test Environment / Tools Needed:**

* A machine (can be your host OS or a dedicated Linux VM) with **Docker and Docker Compose installed** and sufficient resources (RAM, CPU - ELK/Splunk can be resource-intensive, recommend at least 4GB+ RAM available for the containers).
* Network connectivity between the Docker host and the VMs running log forwarders (from Subtopic 7.2). Ensure relevant ports are open/mapped (e.g., 5044 for Beats, 9200 for Elasticsearch, 5601 for Kibana, 8000/8089/9997 for Splunk).
* Log sources (VMs from 7.2) configured to forward logs (Filebeat/Winlogbeat/Rsyslog).

---

### 🔹 **Exercise 1: Deploying Basic ELK Stack with Docker Compose**

**Goal:** Use Docker Compose to quickly set up a minimal Elasticsearch, Logstash, and Kibana stack for testing.

**Instructions:**

1.  Find a simple, trusted `docker-compose.yml` file for a basic ELK setup. The official Elastic guide or reputable GitHub repositories (like `deviantony/docker-elk` - review carefully) are good starting points. Ensure it defines services for `elasticsearch`, `logstash`, and `kibana`, linking them appropriately and mapping necessary ports (e.g., 9200, 5601, and a port for Logstash input like 5044).
2.  Review the compose file. Note the image versions used and default configurations (especially memory limits for Elasticsearch).
3.  Save the `docker-compose.yml` file to a directory on your Docker host.
4.  From within that directory, run `docker-compose up -d` to download images and start the containers in detached mode.
5.  Use `docker ps` to verify the three containers (elasticsearch, logstash, kibana) are running. Check logs using `docker-compose logs -f <service_name>` if needed (especially for Elasticsearch startup).
6.  Access Kibana in your web browser by navigating to `http://<YourDockerHostIP>:5601`. It might take a few minutes for Kibana to fully initialize.
7.  **Challenge:** Modify the `docker-compose.yml` file to adjust the memory allocated to the Elasticsearch container (e.g., change `ES_JAVA_OPTS`). Why is managing Elasticsearch memory important?

---

### 🔹 **Exercise 2: Configuring Logstash Pipeline for Beats Input**

**Goal:** Create a simple Logstash pipeline configuration to receive events sent by Filebeat/Winlogbeat and output them to the Elasticsearch instance running in Docker.

**Instructions:**

1.  If using a pre-built ELK compose file (like `deviantony/docker-elk`), locate the Logstash pipeline configuration directory mounted into the container (e.g., `./logstash/pipeline/`). If starting from scratch, you'll need to mount a local directory containing your pipeline config into the Logstash container in `docker-compose.yml`.
2.  Create or edit a Logstash configuration file (e.g., `logstash.conf` or `02-beats-input.conf`) inside that pipeline directory.
3.  Define an `input` section using the `beats` plugin, listening on the port Filebeat/Winlogbeat will send to (default is 5044):
    ```conf
    input {
      beats {
        port => 5044
      }
    }
    ```
4.  Define an `output` section targeting the Elasticsearch container (use the service name from `docker-compose.yml`, typically `elasticsearch`, and port 9200):
    ```conf
    output {
      elasticsearch {
        hosts => ["http://elasticsearch:9200"]
        index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
        #user => "elastic" # Add user/password if security is enabled
        #password => "changeme"
      }
      # Optional: Output to console for debugging
      # stdout { codec => rubydebug }
    }
    ```
5.  Save the configuration file.
6.  If Logstash is already running, you might need to restart the container for it to pick up the new pipeline: `docker-compose restart logstash`. Check logs (`docker-compose logs -f logstash`) for configuration errors.
7.  **Challenge:** Modify your Filebeat/Winlogbeat configuration (from Subtopic 7.2) - comment out the `output.console` and uncomment/configure `output.elasticsearch:`. Set the `hosts:` to point to your Docker host's IP address and the Logstash input port (e.g., `hosts: ["<YourDockerHostIP>:5044"]`). Restart Filebeat/Winlogbeat.

---

### 🔹 **Exercise 3: Verifying Log Ingestion in Kibana**

**Goal:** Confirm that logs sent from Filebeat/Winlogbeat via Logstash are successfully indexed in Elasticsearch and viewable in Kibana.

**Instructions:**

1.  Ensure your ELK stack (Ex1) and Logstash pipeline (Ex2) are running, and Filebeat/Winlogbeat (from 7.2, configured to output to Logstash) is running and sending data.
2.  Access Kibana in your browser (`http://<YourDockerHostIP>:5601`).
3.  Navigate to the management / Stack Management section (often via side menu) > Index Patterns (or Data Views).
4.  Kibana should detect the new indices being created by Logstash (e.g., `filebeat-*-...` or `winlogbeat-*-...`). Create an index pattern (e.g., `filebeat-*` or `winlogbeat-*`) matching these indices. Select `@timestamp` as the time field.
5.  Navigate to the Discover section (often via side menu).
6.  Select the index pattern you just created.
7.  You should see log events appearing. Expand individual documents to see the parsed fields added by Beats and potentially Logstash.
8.  Use the Kibana Query Language (KQL) search bar to filter logs (e.g., `host.name : "log-client"`, `event.original : *error*`).
9.  **Challenge:** Create a simple visualization in Kibana (e.g., a Data Table or Pie chart) showing the count of log events over time or the distribution of events by hostname.

---

### 🔹 **(Optional) Exercise 4: Deploying Basic Splunk Free with Docker**

**Goal:** Set up a standalone Splunk instance using Docker and configure a basic input method.

**Instructions:**

1.  Pull the official Splunk image: `docker pull splunk/splunk:latest`.
2.  Run a Splunk container. Map necessary ports (8000 for Web UI, 8089 for management, potentially 9997 for forwarders or 514 for syslog). Accept the license and set an admin password via environment variables.
    ```bash
    docker run -d -p 8000:8000 -p 8089:8089 -p 9997:9997 \
      -e "SPLUNK_START_ARGS=--accept-license" \
      -e "SPLUNK_PASSWORD=YourSecurePassword" \
      --name splunk \
      splunk/splunk:latest
    ```
    (Replace `YourSecurePassword`!).
3.  Wait a few minutes for Splunk to initialize. Access the web UI at `http://<YourDockerHostIP>:8000`. Log in as `admin` with the password you set.
4.  Configure a data input: Go to Settings > Data inputs. Choose a method:
    * **TCP/UDP:** Configure Splunk to listen on a specific port (e.g., UDP 514 for syslog). You would then configure `rsyslog` (from 7.2) to forward to `udp://<YourDockerHostIP>:514`.
    * **Splunk Forwarder:** (More complex setup) Install Splunk Universal Forwarder on a source VM/container, configure it to monitor files/logs, and forward data to the Splunk indexer on port 9997 (requires enabling the receiver on port 9997 in Splunk: Settings > Forwarding and receiving).
5.  Configure a source (like `rsyslog` or a Universal Forwarder) to send data to the input you configured.
6.  Go to the Splunk Search & Reporting app. In the search bar, type `index=*` (or specify the index you configured for your input) and search. Verify that log events are arriving.
7.  **Challenge:** Explore the Splunk interface. How does its Search Processing Language (SPL) differ from Kibana's KQL for basic filtering (e.g., finding events from a specific host or containing a keyword)?

---

### 🔹 **(Optional) Exercise 5: Platform Comparison (Initial Feel)**

**Goal:** Formulate initial impressions on the setup and basic usability of ELK vs. Splunk Free based on the deployment exercises.

**Instructions:**

1.  Reflect on your experience setting up the basic ELK stack (Ex 1-3) and the basic Splunk instance (Ex 4).
2.  Consider the following aspects for each platform:
    * Ease of initial deployment using Docker.
    * Clarity/complexity of initial configuration for log ingestion (Logstash pipeline vs. Splunk inputs).
    * Resource consumption observed (if monitored via `docker stats`).
    * Initial feel of the user interface (Kibana vs. Splunk Web UI) for viewing logs.
3.  Write a short comparison (1-2 paragraphs) summarizing your first impressions. Note that this is based on minimal setup; advanced features and scaling differ significantly.
4.  **Challenge:** Research the primary licensing differences between the free/basic tiers of ELK (fully open source components) and Splunk Free (ingestion limits). How might these differences impact choosing a platform for a larger project?

---

### 💡 **Project: Documented Basic Logging Lab Setup**

**Goal:** Create a well-documented configuration using Docker Compose to set up a minimal, functional logging environment (either ELK or Splunk) suitable for personal lab use.

**Instructions:**

1.  Choose either the ELK stack or Splunk Free.
2.  Refine your `docker-compose.yml` file (for ELK) or Docker run command/compose file (for Splunk) for clarity and basic persistence (e.g., using Docker volumes to persist Elasticsearch data or Splunk configuration/indexes across container restarts).
3.  If using ELK, include a basic, well-commented `logstash.conf` pipeline file (e.g., in `./logstash/pipeline/`) configured for Beats input.
4.  If using Splunk, document the necessary steps to configure a common input (e.g., TCP/UDP listener or enabling the HEC/Forwarder receiver) after initial startup.
5.  Create a `README.md` file that:
    * Explains the purpose of the setup (basic centralized logging lab).
    * Lists prerequisites (Docker, Docker Compose).
    * Provides clear step-by-step instructions on how to launch the environment (`docker-compose up -d` or `docker run ...`).
    
    * Explains how to access the UI (Kibana/Splunk Web).
    * Shows a basic example of how to configure a log shipper (like Filebeat or rsyslog) to send data *to* this lab environment.
    * Mentions any default credentials (and strongly advises changing them for Splunk).
    * Notes resource considerations (RAM/CPU).
6.  **Portfolio Guidance:** Host this configuration (docker-compose.yml, logstash.conf if ELK, README.md) on GitHub. This demonstrates your ability to set up standard logging tools and document infrastructure-as-code configurations.

---