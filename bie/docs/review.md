# Comprehensive Codebase Review (Consolidated Architecture)

## 1. Project Overview
**Project Name:** Bonus Intelligence Engine (BIE)
**Architecture:** 7-Layer Consolidated Model
**Goal:** High-performance, observable, and resilient scraping of casino bonus data.

---

## 2. Core System Layers

### [Foundation] `base.py`
- **Role:** Handles environment, state, and persistence.
- **Key Logic:** 
    - Thread-local SQLite connection pooling.
    - JSON-based session serialization (replaces pickle).
    - `SystemState` (Pause/Resume/Stop) via `threading.Event`.
- **Observation:** Extremely robust; centralized logic prevents "spaghetti" database access.

### [Execution] `run.py`
- **Role:** Orchestrates parallelism and worker lifecycles.
- **Key Logic:**
    - `ScrapeWorker` implements the complete site lifecycle (Health -> Auth -> Fetch -> Parse -> Save).
    - `db_write_queue` ensures thread-safe sequential writes to SQLite.
- **Observation:** The use of queues for DB/CSV writes successfully decouples scraping from I/O.

### [Connectivity] `net.py`
- **Role:** Resilient HTTP communication.
- **Key Logic:**
    - Dual-stack Sync (`cloudscraper`) and Async (`aiohttp`) networking.
    - `NetworkHealth` provides IP reputation filtering via AbuseIPDB.
- **Observation:** Proxy "burn" logic and reputation filtering are best-in-class for stealth.

### [Intelligence] `logic.py`
- **Role:** Data scoring and deduplication.
- **Key Logic:**
    - **Algorithm V14:** Sophisticated PV scoring using log rewards and exponential penalties.
    - **Fuzzy Matching:** Uses `difflib` and tier-normalization to catch mirror-site duplicates.
- **Observation:** Business logic is isolated from execution, making it easily testable.

### [Interaction] `flow.py`
- **Role:** Site-specific "rituals" (Auth & Parsing).
- **Key Logic:**
    - `extract_variable` uses tiered regex to find IDs in both HTML and JS bundles.
    - `fetch_sync_data` manages the specific payload requirements of the casino APIs.
- **Observation:** Clean separation of "ritual" logic makes adding new site types easier.

### [Visualization] `ui.py`
- **Role:** Real-time feedback and telemetry.
- **Key Logic:**
    - Multi-panel `Rich` layout showing streaks, logs, and system health.
    - Rolling window (R100) for success rate calculation.
- **Observation:** The TUI provides "Stock Ticker" levels of information density.

### [Communication] `web_server.py`
- **Role:** Remote control and browser mirroring.
- **Key Logic:**
    - `FastAPI` with WebSocket broadcasting.
    - REST endpoints for Pause/Resume/Stop.
- **Observation:** Allows for "headless" operation while maintaining full observability.

---

## 3. Directory Structure
- `in/`: Structured input (config, proxies, targets).
- `db/`: Centralized persistence (SQLite, CSVs).
- `err/`: Diagnostic pillar (Logs, Debug snapshots).
- `lab/`: Experimental tracks and prototypes.
- `docs/`: Unified technical documentation.

---

## 4. Conclusion
The shift from "Golfed" to "Consolidated" has produced a system that is significantly more stable, observable, and maintainable. The 7-layer architecture clearly defines responsibilities, reducing cognitive load for future developers.
