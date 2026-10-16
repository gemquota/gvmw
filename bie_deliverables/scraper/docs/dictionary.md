# Codebase Dictionary (v2.0)
Mapping of terms and abbreviations used in the consolidated architecture.

## 🏛️ Core Modules
- `base`: Foundation Layer (`base.py`). Config, DB, IO, State.
- `flow`: Interaction Layer (`flow.py`). Auth, API rituals, Parsing.
- `logic`: Intelligence Layer (`logic.py`). PV Scorer, Deduplication, Fingerprinting.
- `net`: Connectivity Layer (`net.py`). Network Managers, Proxy Health.
- `run`: Execution Layer (`run.py`). Orchestrator, Scrape Workers.
- `ui`: Visualization Layer (`ui.py`). Rich TUI, Live Telemetry.
- `web`: Communication Layer (`web_server.py`). FastAPI, WebSockets.

## 🔑 Common Abbreviations

### Data & Objects
- `b`: Bonus object (dictionary).
- `cfg`: Configuration object.
- `ctx`: Context (often a dictionary passed between layers).
- `db`: Database connection or proxy.
- `fp`: Fingerprint (unique SHA256 hash).
- `mc`: Merchant (the casino brand).
- `pv`: Perceived Value (result of Algorithm V14).
- `px`: Proxy string or object.
- `st`: System state or statistics.
- `tgt`: Target URL.

### Function Prefixes
- `get_`: Fetches data (usually read-only).
- `set_`: Updates state or configuration.
- `init_`: Initializes a component or session.
- `calc_`: Performs mathematical calculations (like PV).
- `is_`: Boolean check (e.g., `is_new`, `is_fuzzy_match`).
- `sync_`: Handles synchronous API calls.
- `async_`: Handles asynchronous operations.

## 🏷️ UI Status Codes
- `✅`: SUCCESS. Data extracted and saved.
- `💨`: DUPLICATE. Bonus already exists in DB.
- `❌`: ERROR. Fatal failure (Network/Parser).
- `♥️ `: STREAK. High success rate (Success > 95%).
- `🔴`: CRITICAL. Low health (Success < 20%).

## 📂 Directory Roles
- `in/`: **Input Pillar**. Configs, URL lists, Proxies.
- `db/`: **Persistence Pillar**. SQLite DB, CSV Exports.
- `err/`: **Diagnostic Pillar**. Debug snapshots, Logs.
- `lab/`: **Experimental Pillar**. Development tracks and prototypes.
- `docs/`: **Technical Pillar**. Manuals, Specs, and Code References.
