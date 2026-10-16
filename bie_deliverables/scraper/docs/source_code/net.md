# `net.py` Documentation (Connectivity Layer)

## File Overview
Handles the mechanics of internet communication and proxy reputation.

## Sections

### 1. NETWORK
*   **Purpose:** 
    *   **Sync Stack:** `cloudscraper` session creation for landing page loads and anti-bot bypass.
    *   **Async Stack:** `AsyncNetworkManager` (`aiohttp`) for high-volume API requests.
    *   **Handlers:** `get_html()` (follows redirects), `get_next_healthy_proxy()` (Reputation filtered).
*   **Key Functions:** `create_session()`, `post_json()`, `get_next_healthy_proxy()`.

### 2. HEALTH
*   **Purpose:** Interface for AbuseIPDB reputation checking.
*   **Proxy Lifecycle:**
    ```mermaid
    stateDiagram-v2
        direction LR
        state "Proxy IP" as Proxy {
            [*] --> Unknown
            Unknown --> Active: AbuseIPDB Score < 50
            Unknown --> Burned: AbuseIPDB Score > 50
            Active --> Active: Success
            Active --> Cooling: HTTP 403 / Captcha
            Cooling --> Active: Cooldown Period Expires (12h * Burns)
            Cooling --> Burned: Permanent Block
            Burned --> [*]
        }
    ```
*   **Caching:** Stores IP scores in the `ip_cache` table for 1 hour.
*   **Key Functions:** `check()`, `burned()`, `status()`.
