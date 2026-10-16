# Application Features

This document outlines the core capabilities of the Bonus Intelligence Engine (BIE).

## Core Architecture

### 1. Multi-Threaded Scraping (`run.py`)
- **Concurrency:** Uses a `ThreadPoolExecutor` to process dozens of sites simultaneously.
- **Safety:** Utilizes a centralized `db_write_queue` to ensure thread-safe, sequential writes to the SQLite database, preventing lock errors.
- **Resilience:** Automatically detects dead proxies and rotates them out of the pool.

### 2. Session Persistence (`base.py`)
- **State Management:** Automatically saves and restores user sessions (cookies, tokens) to the `sessions` table in SQLite.
- **Security:** Serializes session data as JSON (avoiding `pickle` vulnerabilities) to prevent Remote Code Execution risks.
- **Efficiency:** Reduces login frequency by reusing valid sessions (TTL 6 hours).

### 3. Smart Deduplication (`logic.py`)
- **Fingerprinting:** Generates a unique SHA-256 fingerprint for every bonus based on its core attributes (Amount, Wager, Limits).
- **Fuzzy Matching:** Uses `difflib` to identify identical bonuses across different mirror domains (e.g., `casino-88.com` vs `casino-99.com`) and consolidates them into a single database record.

### 4. Priority Engine (`base.py`)
- **Dynamic Scheduling:** Sites are prioritized based on their historical "Perceived Value" (PV) yield.
- **Lifecycle Management:** Automatically moves failing sites to a "Purgatory" state for re-testing, and eventually "Prunes" them if they remain dead.

## Data Intelligence

### 5. IP Health Monitoring (`net.py`)
- **Reputation Check:** proactive monitoring against AbuseIPDB to prevent using "burned" proxies.
- **Auto-Healing:** If a proxy is blocked (`403 Forbidden`), it is marked for a cooldown period, and the worker seamlessly switches to a fresh IP.

### 6. Perceived Value (PV) Algorithm (`logic.py`)
- **Logic:** A sophisticated formula (V14) that ranks bonuses based on "Beatability."
- **Math:** Balances Logarithmic Rewards (High Max Cashout) against Exponential Penalties (High Rollover/Wager).

### 7. Global Search (`lab/util/search.py`)
- **Full-Text Search:** Utilizes SQLite's FTS5 extension for instant querying of thousands of historical bonuses.

## User Interface

### 8. Web Dashboard (`web_server.py`)
- **Live Monitor:** A WebSocket-based real-time dashboard served at `http://127.0.0.1:8000`.
- **Control:** Remote Pause, Resume, and Stop functionality.

### 9. Console TUI (`ui.py`)
- **Rich Interface:** A beautiful terminal UI with live progress bars, success rate gradients, and scrolling logs.
- **Telemetry:** Displays real-time CPU/RAM usage and network throughput.

## Diagnostics

### 10. Error Snapshotting
- **Automated Debugging:** When specific errors (E201, E202) occur, the system automatically saves a raw HTML snapshot to `err/debug/`.
- **Purpose:** Allows for post-mortem analysis of layout changes or Cloudflare blocks.

### 11. Discovery (`lab/util/discover.py`)
- **Crawler:** A standalone tool that scans seed affiliate sites to find and extract new casino mirror URLs.