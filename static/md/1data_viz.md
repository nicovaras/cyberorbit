## 📄 PDF: Topic 1 – Subtopic: Data Visualization for Security  
**Resource:** [Real Python – Data Visualization with Matplotlib](https://realpython.com/python-matplotlib-guide/)

---

### 🔹 **Exercise: Visualize Failed Logins from Sample Log**  
**Goal:** Create a bar chart showing the number of failed logins per IP.  

**Instructions:**  
- Use a sample log from `https://github.com/logpai/loghub`.  
- Parse the log and extract IPs from failed SSH login lines.  
- Count occurrences per IP.  
- Plot a bar chart using `matplotlib.pyplot`.

---

### 🔹 **Exercise: Plot Process Memory Usage Over Time**  
**Goal:** Watch and visualize memory usage of a process.  

**Instructions:**  
- Use `psutil` to get memory usage of a specific PID (e.g., your terminal).  
- Sample data every 2 seconds for 30 seconds.  
- Plot the results on a line graph.  
- Optional: add CPU usage to the same graph.

---

### 🔹 **Exercise: Geo-Plot Login Attempts by IP**  
**Goal:** Map failed login attempts on a world map.  

**Instructions:**  
- Use the same log as above, extract IPs.  
- Use a free GeoIP API (like `ip-api.com`) to get lat/lon.  
- Plot points on a simple world map using `Basemap` or `folium`.  
- Color-code by number of attempts.

---

### 🔹 **Exercise: Visualize User Activity by Hour**  
**Goal:** Plot a histogram showing login attempts per hour.  

**Instructions:**  
- From a sample log, extract timestamps of login attempts.  
- Parse hour from each timestamp.  
- Count and plot as a histogram: hour vs number of logins.  
- What time of day sees the most action?

---

### ✨ **Bonus: Animate Process Tree Growth Over Time**  
**Goal:** Create a simple animation of system processes spawning.  

**Instructions:**  
- Use `psutil` to capture a snapshot of active processes every few seconds.  
- Track parent/child relationships.  
- Use `networkx` + `matplotlib.animation` to create a simple time-lapse of how processes evolve.  
- Try visualizing a live script that spawns subprocesses.

