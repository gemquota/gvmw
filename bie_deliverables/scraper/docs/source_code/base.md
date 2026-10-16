# `base.py` Documentation (Foundation Layer)

## File Overview
The foundational layer of the engine. It handles configuration loading, database connection pooling (thread-local), session persistence, and global system state control.

## Sections

### 1. CONFIG
*Consolidates logic from original `config.py`.*
*   **Purpose:** Reads `in/config/config.ini`, parses target URLs from `in/config/urls.txt`, and manages proxy lists from `in/config/proxies.txt`.
*   **Key Identifiers:** `agent`, `timeout`, `proxies`, `parse`, `reader`.

### 2. DB (Database)
*Consolidates logic from original `db.py`.*
*   **Purpose:** Manages the SQLite connection. Uses `threading.local()` to ensure each thread has its own connection. Supports synchronous `query()` and asynchronous `async_query()`.
*   **Database Path:** `db/base.db`.
*   **Tables:** `targets`, `bonuses`, `sessions`, `metrics`, `logs`.
*   **Method:** `setup()` initializes the schema with descriptive column names.

### 3. IO (Input/Output)
*Consolidates logic from original `io_manager.py`.*
*   **Purpose:** Handles JSON serialization of cookies for session persistence and CSV management for discovery results.
*   **Paths:** Discovery results are saved to `db/bonuses.csv` and `db/highvalue.csv`.
*   **Key Identifiers:** `init`, `append`, `log`, `load`, `save`.

### 4. STATE
*Consolidates logic from original `shared_state.py`.*
*   **Purpose:** Provides a `SystemState` object using `threading.Event` to coordinate Pause, Resume, and Stop signals across the entire engine.

### 5. ERRORS
*Consolidates logic from original `error_definitions.py`.*
*   **Purpose:** Maps integer error codes (1xx-5xx) to brief labels and verbose descriptions for the UI.
