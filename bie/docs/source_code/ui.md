# `ui.py` Documentation (Interaction Layer)

## Overview
The "Dashboard Terminal" of the application. It uses the `Rich` library to create a dynamic, multi-panel TUI (Terminal User Interface) that displays live metrics, streaks, and logs. It also acts as the bridge that pushes data to the web dashboard.

## Key Components

### 1. Dashboard State
*   `STATUS_MARKERS`: A mapping of success rates to heart/circle emojis (♥️, 🔴, 🟢) used to visualize system health.
*   `ROLLING_HISTORY`: A deque that stores the success/failure status of the last 100 tasks to calculate a "Moving Health Score."
*   `DURATION_SAMPLES`: Tracks request latencies to provide a "Mean Latency" metric.

### 2. Rendering Logic
*   `render_dashboard()`: The core function that constructs the UI layout using `rich.layout.Layout`.
    *   **Header:** Shows system stats (CPU/MEM via `psutil`) and overall run metrics.
    *   **Main Table:** Lists the most recent site tasks, their results, and bonuses found.
    *   **Log Panel:** Shows timestamped events and internal error codes (e.g., E101).
*   `init_dashboard_data()`: Calculates derived stats (like throughput estimates) for the initial splash screen.

### 3. Data Integration
*   `update_web_dashboard()`: An asynchronous-friendly wrapper that sends the current TUI state to the `web_server.py` via a POST request to `/update`.
*   `update_stats()`: Thread-safe function that updates the global counters and triggers a re-render.

## Visual Legend
*   **Health Gradient:** `🟥` → `🔴` → `♥️` → `🟧` → `🟠` → `🧡` → `🟨` → `🟡` → `💛` → `🟩` → `🟢` → `💚`
    *   Visualizes the "Rolling Health Score" (Success Rate of last 100 requests).
    *   `🟥` = 0% Success
    *   `♥️` = ~20% Success
    *   `🟨` = ~50% Success
    *   `💚` = 100% Success
*   `✅`: Target successfully processed.
*   `💨`: Duplicate bonus detected and ignored.
*   `❌`: Fatal error (Network or Parsing).
