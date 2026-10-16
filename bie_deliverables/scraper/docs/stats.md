# Codebase Statistics & Evolution (Consolidated Architecture)

## 1. Current File Sizes (Consolidated Release)
| File | Lines | Responsibility |
|---|---|---|
| `base.py` | 217 | Foundation: Config, DB, IO, State |
| `run.py` | 308 | Execution: Orchestrator, Workers |
| `ui.py` | 518 | Visualization: Rich TUI, Telemetry |
| `logic.py` | 208 | Intelligence: Scorer, Deduplication |
| `net.py` | 144 | Connectivity: Sync/Async Networking |
| `flow.py` | 104 | Interaction: API Rituals, Parsing |
| `web_server.py`| 135 | Communication: FastAPI, WebSockets |
| **Total** | **1,634** | **Production Grade Engine** |

## 2. Evolution: From "Golfed" to "Consolidated"

The project underwent a significant transformation from a ultra-minimalist "Golfed" script to a production-ready, thread-safe, and observable engine.

- **Golfed Phase (Jan 2026):** ~30 lines. Focused on absolute minimal footprint.
- **Consolidated Phase (Feb 2026):** ~1,600 lines. Focused on reliability, observability, and remote control.

### Why the increase?
1.  **Observability:** 500+ lines in `ui.py` provide deep insight into system health.
2.  **Reliability:** Thread-safe database pools and robust error handling in `base.py`.
3.  **Concurrency:** A sophisticated orchestrator in `run.py` to handle hundreds of targets.
4.  **Remote Control:** A full `FastAPI` server in `web_server.py` for remote management.

## 3. Density Analysis

*   **Average Lines per Module:** ~233 lines.
*   **Most Complex Module:** `ui.py` (31% of codebase) - reflecting the priority placed on user feedback.
*   **Leanest Module:** `flow.py` - showing the efficiency of the "Conversation" logic.

## 4. Documentation Footprint

| Directory | Files | Total Lines (Est) |
|---|---|---|
| `docs/` | 15 | ~1,200 |
| `docs/source_code/` | 7 | ~350 |
| **Total** | **22** | **~1,550** |

*Observation: The documentation volume is now nearly 1:1 with the code volume, fulfilling the "Self-Documenting System" goal.*