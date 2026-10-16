# `web_server.py` Documentation (Communication Layer)

## Overview
The "Air Traffic Control" for remote monitoring. Built with `FastAPI`, it provides a REST API for controlling the engine and a WebSocket stream for real-time telemetry.

## Key Components

### 1. Connection Management
*   `ConnectionManager`: Handles active WebSocket clients. It supports broadcasting messages to all connected browsers simultaneously.
*   `active_connections`: A list of `WebSocket` objects representing currently open dashboard sessions.

### 2. API Endpoints

#### Control Layer
*   `/api/control/pause`: Sets a global `is_paused` flag in `base.py`.
*   `/api/control/resume`: Clears the pause flag.
*   `/api/control/stop`: Signals the orchestrator to shutdown.

#### Configuration Layer
*   `/api/config`: Dynamically reads `in/config/config.ini` and returns it as JSON.
*   `/api/config/update`: (Endpoint for `ConfigUpdate` model) Allows updating specific settings like delays and API keys.

### 3. Real-time Telemetry
*   **Data Flow:**
    ```mermaid
    graph LR
        subgraph "CLI (Producer)"
            TUI[ui.py]
            Updater[update_dashboard()]
        end

        subgraph "Web Server (Hub)"
            Endpoint[POST /update]
            Mgr[ConnectionManager]
            Pool[Active Connections]
        end

        subgraph "Browser (Consumer)"
            Client1[Client A]
            Client2[Client B]
        end

        TUI -->|Snapshot| Updater
        Updater -->|JSON| Endpoint
        Endpoint -->|Broadcast| Mgr
        Mgr -->|Iterate| Pool
        Pool -->|WebSocket Msg| Client1
        Pool -->|WebSocket Msg| Client2
    ```
*   `/ws`: The primary WebSocket endpoint. When `ui.py` sends an update, the web server broadcasts it to all `/ws` clients.
*   `/update`: Receives the dashboard "snapshot" from the CLI and triggers the broadcast.

## Lifecycle
1.  Started as a background thread by `run.py` (or as a standalone process via `python run.py dash`).
2.  Listens on `0.0.0.0:8000` (allowing local or LAN access).
3.  Acts as a stateless relay between the `ScrapeWorker` threads and the browser UI.
