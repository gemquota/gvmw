# UI Display Value Audit: Categorized (v2.0 - Dynamic Update)

This report lists every value displayed in the Initialization and Finalization screens, now upgraded to minimize static placeholders in favor of real telemetry.

## 1. Static Values
*Values that are still hardcoded as they describe fixed architectural traits.*

| Context | Label | Displayed Value | Explanation |
| :--- | :--- | :--- | :--- |
| **Init Panel 2** | Proxy Logic | `Sticky-Session` | Describes the session persistence strategy. |
| **Init Panel 6** | SSL Check | `Disabled` | Currently reflects that SSL verification is bypassed for speed/compatibility. |
| **Final Panel 4** | Threads | `Clean Exit` | Status indicator for thread pool shutdown. |
| **Final Panel 5** | Files Saved | `2 (CSV/JSON)` | Count of output formats generated. |
| **Final Panel 5** | Audit | `PASSED` | Final integrity check status. |

## 2. Calculated Values
*Values derived from runtime logic, system calls, or real-time measurements.*

| Context | Label | Definition / Logic |
| :--- | :--- | :--- |
| **Init Panel 1** | Concurrency | **Formula:** `min(available_proxy_count + 1, task_count)`<br>Determined by healthy proxy availability. |
| **Init Panel 1** | Throughput (Est) | **Formula:** `int((60 / avg_delay) * workers)`<br>Estimated URLs per minute based on config. |
| **Init Panel 2** | Network Type | **Logic:** Detects if `uvloop` is active in the environment. |
| **Init Panel 3** | Priority | **Logic:** "Randomized" if shuffle is on, otherwise "Sequential". |
| **Init Panel 3** | Shuffle | **Logic:** "ENABLED" or "DISABLED" based on launch flags. |
| **Init Panel 4** | OS/Py Version | **System:** Dynamic `platform` calls. |
| **Init Panel 5** | System Health | **System:** Real-time `psutil` metrics for CPU/RAM. |
| **Init Panel 5** | IO Status | **Logic:** Tests `db/base.db` for write permissions. |
| **Final Panel 1** | Duration | **Formula:** `time.time() - START_TIME`. Formatted as `H:MM:SS`. |
| **Final Panel 1** | Throughput | **Formula:** `total_processed / total_duration`. |
| **Final Panel 3** | Health Rates | **Formula:** Percentage of success vs failure. |
| **Final Panel 3** | Avg Latency | **Formula:** Mean of `DURATION_SAMPLES` collected by workers. |
| **Final Panel 4** | Resource Peak | **System:** Captures RAM/CPU usage at the end of the run. |

## 3. Configuration & Data Values
*Values sourced directly from configuration files, DB lookups, or runtime counters.*

| Context | Label | Source |
| :--- | :--- | :--- |
| **Init Panel 1** | Delays/Timeout | `in/config.ini` -> `base.py`. |
| **Init Panel 2** | Proxy Pool | DB Query count of active/cooling proxies. |
| **Init Panel 3** | Total Tasks | Final count of target URLs after parsing. |
| **Init Panel 6** | Auth User | `UI_USER` from config/environment. |
| **Init Panel 6** | IP Reputation | `ip_score` from AbuseIPDB check in `net.py` / `run.py`. |
| **Final Panel 1** | Total Requests | `stats['index']`. |
| **Final Panel 2** | Volume Stats | Cumulative counters for bonuses and new findings. |
| **Final Panel 5** | DB Updates | `stats['successes']`. |