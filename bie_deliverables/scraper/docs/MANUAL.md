# Bonus Intelligence Engine - Operator Manual

## 1. Introduction
The **Bonus Intelligence Engine (BIE)** is a high-performance, multi-threaded scraper and analysis tool designed for discovering, tracking, and evaluating online casino bonuses. Built for Termux/Android environments, it features asynchronous networking, smart deduplication, and a sophisticated "Perceived Value" (PV) algorithm to rank opportunities.

## 2. Command Line Interface (CLI)

### Main Engine (`run.py`)
The primary entry point for the application.

**Usage:**
```bash
python run.py [OPTIONS]
```

**Options:**
| Flag | Long Flag | Value | Description |
| :--- | :--- | :--- | :--- |
| `-h` | `--help` | N/A | Displays the help message. |
| `-v` | `--verbose`| `min`, `med`, `max` | **Verbosity Level**. Controls CLI output depth. |
| `-r` | `--raw` | N/A | **Raw Mode**. Saves JSON responses to `err/debug/`. |
| `-s` | `--shuffle`| N/A | **Shuffle Mode**. Randomizes target order. |
|      | `dash`    | N/A | **Dashboard Mode**. Starts the web server only. |

**Examples:**
```bash
python run.py                  # Standard run with min verbosity
python run.py -v med -s        # Medium verbosity with target shuffling
python run.py dash             # Start web dashboard only (no scraping)
```

---

## 3. Dashboard & User Interface

### Console TUI (Rich)
When running `run.py`, a real-time dashboard is rendered in the terminal using the `Rich` library.
- **Header:** Shows system stats (CPU/MEM), total runtime, and session counts.
- **Streak Tracker:** Displays current success/fail streaks with visual status markers (♥️, 🟢, 🔴).
- **Log Panel:** Displays the 10 most recent activity logs with timestamps and status codes.
- **Status Markers:**
    - `✅`: Success (Data extracted)
    - `💨`: Skipped (Deduplicated)
    - `❌`: Failed (Network or Merchant identification error)

### Web Dashboard (FastAPI)
Accessible at `http://127.0.0.1:8000`.
- **Live Feed:** Mirrors the console output in a browser-friendly format.
- **Control Panel:** Pause, Resume, or Stop the engine remotely.
- **Config Editor:** (Planned) Update delays and API keys on the fly.

---

## 4. Data & Persistence

### SQLite Database (`db/base.db`)
The core storage for all discovered bonuses and engine metrics.
- **`bonuses` table:** Stores name, merchant, raw value, and the calculated PV (Perceived Value).
- **`metrics` table:** Tracks performance data per site (latency, status codes).
- **`targets` table:** Management of discovery URLs and their current status.

### CSV Exports
The engine automatically exports fresh data to CSV for easy analysis:
- `db/bonuses.csv`: All unique bonuses found in the current session.
- `db/highvalue.csv`: Filtered list of bonuses with PV > 70.

---

## 5. Best Practices & Safety

### OpSec (Operational Security)
- **Proxy Usage:** Always use proxies (`in/config/proxies.txt`) to avoid IP bans.
- **Delays:** Maintain a minimum delay of 1-3 seconds (`min_delay` in `config.ini`) to mimic human behavior.
- **User Agents:** The engine automatically rotates User-Agents from `in/config/user_agents.txt`.

### IP Health
If you see consistent `E403` or `E202` (Captcha) errors:
1. Stop the engine.
2. Flush the `proxies.txt` or rotate your mobile IP.
3. Use the `dash` mode to monitor health scores before resuming.

---

## 6. Directory Structure
- **`in/`** (The Input Pillar):
    - `config/`: settings, targets, and proxies.
    - `meta/`: blueprints and examples.
    - `templates/`: web layouts.
- **`db/`** (The Persistence Pillar):
    - `base.db`: SQLite database.
    - `bonuses.csv`: Discovery results.
    - `highvalue.csv`: Filtered results.
- **`err/`** (The Diagnostic Pillar):
    - `debug/`: HTML/JSON snapshots of failed requests.
    - `log/`: Persistent application logs.
- **`lab/`** (The Experimental Pillar):
    - Development tracks and utilities.
- **`docs/`**: Technical references and source code guides.


