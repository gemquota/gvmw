# OpSec & Fingerprinting Guide

## 1. Fingerprint Evasion
The engine uses several layers to avoid detection by anti-bot services like Cloudflare or Akamai.

*   **Dual-Stack Networking**: Initial landing page loads use `cloudscraper`, which solves basic Javascript challenges and mimics common browser TLS fingerpints.
*   **Header Consistency**: The `USER_AGENT` is constant across sync and async requests to maintain session "identity."
*   **Insecure SSL Bypassing**: `ssl=False` is used in `aiohttp` to avoid "Handshake Failed" errors common when scraping mirrors with mismatched or expired certs—a common trait of casino mirror domains.

---

## 2. Proxy Strategy & Reputation
The `network_health` module is the engine's primary defensive tool.

*   **AbuseIPDB Integration**: Every proxy is checked before use. If the `abuseConfidenceScore` is > 50, the proxy is rejected.
*   **Burn Logic**: If a site returns a `403 Forbidden` or `101 Connection Reset`, the specific proxy is marked as "Burned."
*   **Cooldown Periods**: Burned proxies aren't deleted; they enter a "Cooling" state. The cooldown duration grows linearly with the `burn_count` (12 hours per burn), allowing them to recover reputation over time.

---

## 3. Session Security & Hygiene
*   **JSON Serialization**: Unlike many scrapers that use `pickle` (vulnerable to RCE), this engine stores cookies as sanitized JSON strings in the database.
*   **Session Reuse (6h TTL)**: By reusing valid sessions for 6 hours, the engine minimizes the number of login requests—the most common point of detection for scrapers.
*   **Local Binding**: The web dashboard binds strictly to `127.0.0.1` to prevent exposing your discovery data to the open internet.

---

## 4. Operational Best Practices
*   **Avoid Residential Overuse**: While tempting, residential proxies are slow. Use them only for initial discovery; switch to high-speed datacenter proxies for bulk data fetching (`/users/syncData`).
*   **Randomized Delays**: Never set `min_delay` and `max_delay` to the same value. The resulting fixed rhythm is an instant giveaway to behavioral analysis bots.
