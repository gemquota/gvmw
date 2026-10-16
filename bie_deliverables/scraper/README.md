# Bonus Intelligence Engine (BIE)

A high-performance, multi-threaded casino bonus scraper and analysis engine designed for Android/Termux environments.

## Features
- **Multi-threaded Scraping:** Concurrent worker pool for high-throughput discovery.
- **Smart Deduplication:** Fuzzy matching and fingerprinting to identify identical bonuses across domains.
- **Self-Healing Proxies:** Automatic health monitoring and rotation via AbuseIPDB reputation checks.
- **Perceived Value (PV) Algorithm:** Ranks bonuses based on beatability and ROI.
- **Web Dashboard:** Real-time monitoring via FastAPI and WebSockets.
- **Persistence:** SQLite-backed state management with thread-safe operations and WAL mode enabled.

## Quick Start
1. **Configure:** Copy `in/meta/config.ini.example` to `in/config/config.ini` and fill in your credentials and API keys.
   - **SECURITY WARNING:** You MUST change the default `ui_user` and `ui_pass` in `in/config/config.ini` to secure your dashboard.
2. **Run:** Start the scraper.
   ```bash
   python run.py
   ```
3. **Dashboard:** Launch the web interface standalone.
   ```bash
   python run.py dash
   ```
   Then open `http://127.0.0.1:8000` in your browser.

## Security
- **Local Binding:** The web server binds to `127.0.0.1` by default.
- **Authentication:** Control API endpoints require Basic Auth.
- **Input Validation:** API configuration updates are strictly validated using Pydantic schemas.
- **Safe Serialization:** Uses JSON for session storage instead of Pickle to prevent RCE vulnerabilities.

## Directory Structure
- `in/`: Input configuration, proxies, and seed URLs.
- `db/`: SQLite database and CSV exports.
- `err/`: Diagnostic snapshots and application logs.
- `lab/`: Experimental tracks and prototypes.
- `docs/`: Technical references and source code guides.

## Architecture (7-Layer Model)
- **`base.py`**: Foundation. Config, DB Pool, IO, and System State.
- **`run.py`**: Execution. Orchestrator and Scrape Worker lifecycle.
- **`net.py`**: Connectivity. Sync/Async Networking and Proxy Health.
- **`logic.py`**: Intelligence. PV Scorer, Deduplication, and Fingerprinting.
- **`flow.py`**: Interaction. API Rituals and HTML/JS Parsing.
- **`ui.py`**: Visualization. Rich TUI and Live Telemetry.
- **`web_server.py`**: Communication. FastAPI and WebSocket broadcasting.

## License
Proprietary / Research Only.
