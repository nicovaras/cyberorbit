
## 📄 PDF: Topic 4 – Subtopic: Kernel & Driver Security  
**Resource:** [Linux Kernel Modules Guide – The Geek Stuff](https://www.thegeekstuff.com/2013/06/linux-kernel-modules/)  

---

### 🔹 **Exercise: Identify Loaded Kernel Modules Using `lsmod` and Detect Suspicious Ones**  
**Goal:** Investigate which modules are currently loaded into the kernel and spot any anomalies.  

**Instructions:**  
- Run `lsmod` and review all active kernel modules.  
- Use `modinfo <module>` to learn what each does.  
- Cross-check module names with your distro’s default list.  
- Research one module you don’t recognize—was it expected, third-party, or injected?

---

### 🔹 **Exercise: Log Kernel Module Loading Events**  
**Goal:** Monitor and record when new kernel modules are loaded or removed.  

**Instructions:**  
- Use `auditd` or check `/var/log/kern.log` or `journalctl -k` for load/unload events.  
- Insert a module manually with `modprobe dummy` and then remove it.  
- Filter logs for keywords like “module”, “insmod”, or “rmmod”.  
- Store events in a separate file for later analysis.

---

### 🔹 **Exercise: Detect and Log Attempts to Load Unsigned Kernel Modules**  
**Goal:** Try to load a non-whitelisted or unsigned module and log the attempt.  

**Instructions:**  
- Set up your kernel with module signature enforcement (if available).  
- Attempt to load a fake or dummy module (`make -C /lib/modules/...` with no signature).  
- Watch for failure logs in `dmesg`, `journalctl`, or audit logs.  
- Capture timestamp, module name, and user who triggered the load.
