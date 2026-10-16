# Next Phase: The "Evolution" Update

Following the successful implementation of the core architecture, this plan outlines 20 targeted updates: 10 expansions to harden existing systems, and 10 experimental features to push the boundaries of what the scraper can do.

## Part 1: Feature Expansions (The Hardening)

These updates focus on making the current feature set smarter, more robust, and easier to control.

1.  **Smart Deduplication v2 (Fuzzy Matching)**
    *   **Goal:** Catch duplicates that are *slightly* different (e.g., "Welcome Bonus" vs "Welcome Offer").
    *   **Tech:** Implement Levenshtein distance matching on bonus names.

2.  **IP Health v2 (Auto-Healing)**
    *   **Goal:** Active defense. Instead of just "Warning" you about a bad IP, the system fixes it.
    *   **Tech:**
        *   **Proxy Rotation:** If `IP Score > 50`, the current proxy is marked "cooldown" and the network module forces a switch to the next available proxy immediately.
        *   **Mobile IP Reset (Termux):** If running on 4G/5G without proxies, it calls `termux-api` or `adb shell` to toggle Airplane Mode ON/OFF. This forces the carrier to assign a fresh, clean IP address automatically.

3.  **Web Dashboard v2 (Full Remote Control)**
    *   **Goal:** Complete management without needing SSH.
    *   **Tech:**
        *   **Control:** Stop/Pause/Restart buttons.
        *   **Config Editor:** A UI form to edit `config.ini` settings (Delays, User Agents, API Keys) directly from the browser.
        *   **Live Preview:** View the `latest.html` snapshot in a browser modal.

4.  **Priority Engine v2 (Dynamic Decay)**
    *   **Goal:** Stop wasting time on "dead" high-priority sites.
    *   **Tech:** If a site fails X times, temporarily lower its priority score for 24h.

5.  **Console UI v2 (Thread Matrix)**
    *   **Goal:** Visualize parallelism.
    *   **Tech:** Add a live "Thread Status Bar" to the CLI, showing which site each worker is currently processing.

6.  **Discovery v2 (Recursive Crawling)**
    *   **Goal:** Find deeper links.
    *   **Tech:** Allow `discover.py` to crawl depth > 1 (follow links within affiliate pages).

7.  **Snapshotting v2 (Smart Diffs)**
    *   **Goal:** Pinpoint *why* a scraper failed.
    *   **Tech:** Compare the failed HTML against a known-good template and highlight structure changes.

8.  **Session Persistence v2 (Encrypted Storage)**
    *   **Goal:** Security.
    *   **Tech:** Encrypt session cookies in the SQLite DB using a local key.

9.  **PV Algorithm v2 (User Weights)**
    *   **Goal:** Customization.
    *   **Tech:** Move the PV formula constants into `config.ini` so users can tune the algorithm without coding.

10. **Global Search v2 (Export)**
    *   **Goal:** Data portability.
    *   **Tech:** Add `--export` to `search.py` to dump query results to CSV/JSON.

---

## Part 2: Experimental Features (The Lab)

These are novel, high-risk/high-reward features to explore next-generation capabilities.

1.  **OCR / Vision Parsing**
    *   **Concept:** Use a lightweight OCR model to read bonus terms from banner images, which often contain data missing from the text.

2.  **Telegram Bot Integration**
    *   **Concept:** a "Push Notification" system. The bot messages you immediately when a "Whale" bonus (PV > 90) is found or if the system crashes.

3.  **LLM T&C Parsing (TinyLlama)**
    *   **Concept:** Pipe unstructured "Terms and Conditions" text into a local LLM to extract structured JSON data (Max Bet, Excluded Games).

4.  **Native VPN/WireGuard Support**
    *   **Concept:** Instead of just HTTP proxies, control the system's network interface directly to rotate VPN servers.

5.  **Geo-Fencing Validator**
    *   **Concept:** Parse T&Cs for "Restricted Countries" lists and warn if the current IP/Profile matches a banned region.

6.  **Crypto Wallet Validator**
    *   **Concept:** For crypto-casinos, regex-match deposit addresses to validate which coins are *actually* supported vs advertised.

7.  **Fingerprint Evasion (Canvas/Audio)**
    *   **Concept:** Instead of just User-Agent rotation, inject noise into HTML5 Canvas and AudioContext to defeat advanced browser fingerprinting.

8.  **Honeytoken Detection**
    *   **Concept:** Detect "Trap" bonuses that are only visible to bots (high value, hidden CSS) to avoid getting banned.

9.  **P2P Community Sync**
    *   **Concept:** A decentralized way for scrapers to share "Dead Link" lists or "Working Proxy" lists without a central server.

10. **Registration Flow Analysis**
    *   **Concept:** Attempt to load the "Sign Up" form and log which fields are required (e.g., "Phone Number" vs "Just Email") to grade site accessibility.
