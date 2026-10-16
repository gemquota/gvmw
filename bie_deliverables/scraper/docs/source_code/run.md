# `run.py` Documentation (Execution Layer)

## Overview
The "Engine Room" of the application. It contains the main orchestrator that manages concurrency and the `ScrapeWorker` class that executes the site lifecycle.

## Sections

### 1. ORCHESTRATOR
*   **Purpose:** 
    *   Manages `db_write_queue` and `csv_write_queue` to ensure thread-safe sequential writes to `metrics`, `bonuses`, and `targets` tables.
    *   Coordinates worker spawning based on proxy availability.
    *   Handles the high-level `asyncio` event loop.
*   **Key Functions:** `main_async()`, `fail()`, `deduplicate()`.

### 2. WORKER
*   **Purpose:** Implements the `ScrapeWorker` class.
*   **Lifecycle:**
    ```mermaid
    sequenceDiagram
        participant W as ScrapeWorker (run.py)
        participant N as Network (net.py)
        participant F as Flow (flow.py)
        participant L as Logic (logic.py)
        participant DB as Database (base.py)

        Note over W: Task Start
        W->>N: get_next_healthy_proxy()
        N-->>W: Proxy IP

        rect rgb(240, 248, 255)
            Note right of W: Phase 1: Authentication
            W->>N: create_session(proxy)
            W->>DB: load_session(username)
            alt Session Valid
                DB-->>W: Restore Cookies
            else Session Invalid/Expired
                W->>F: login(credentials)
                F->>N: POST /users/login
                N-->>F: Token
                F-->>W: User Data
                W->>DB: save_session()
            end
        end

        rect rgb(255, 240, 245)
            Note right of W: Phase 2: Fetch & Parse
            W->>F: get_api_endpoint(url)
            W->>N: POST /users/syncData
            N-->>W: JSON Response
            loop Every Bonus
                W->>L: normalize(bonus)
                W->>L: score(bonus) -> PV
                W->>L: fingerprint(bonus)
                W->>L: is_duplicate(fingerprint)
                alt Is Unique
                    L-->>W: True
                    W->>DB: Queue Insert (bonuses)
                else Is Duplicate
                    L-->>W: False
                    W->>DB: Queue Update (mirrors)
                end
            end
        end

        W->>DB: Update Target Status (Active)
        W->>W: Update TUI Stats
    ```
    1.  Proxy initialization (verifies IP health).
    2.  Session check (uses `base.load` to bypass login if valid).
    3.  Async API data fetching (`net.AsyncNetworkManager`).
    4.  Response parsing and deduplication.
    5.  Result queueing for database and CSV output.
