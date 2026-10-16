# 📊 Aggregate Weighted Metric Priority Ranking

This document ranks the 20 planned features (Expansions & Experiments) based on a weighted scoring algorithm designed for the Termux/Android environment.

**Weighting Logic:**
*   **Critical (x2.0):** Utility (Value), Feasibility (Termux compatibility).
*   **High (x1.5):** Reliability (Stability).
*   **Standard (x1.0):** Ease (Dev time), Interoperability.
*   **Low (x0.5):** Modularity, UX.

---

## 🏆 Tier 1: The "Must-Haves" (Score 9.0+)

These features offer high value with low risk and perfect compatibility.

| Rank | Feature | ID | Score | Rationale |
| :--- | :--- | :--- | :---: | :--- |
| **01** | **Telegram Bot Integration** | `23` | **9.6** | Extremely high utility (remote alerts), 100% feasible (HTTP API), very reliable. |
| **02** | **Priority Engine v2 (Decay)** | `15` | **9.4** | High utility (efficiency), 100% feasible (SQL logic), very easy to implement. |
| **03** | **PV Algorithm v2 (Config)** | `20` | **9.3** | Empowers users, zero risk, perfect reliability. |
| **04** | **Global Search v2 (Export)** | `21` | **9.2** | High data utility, trivial implementation, stable. |
| **05** | **Smart Deduplication v2** | `12` | **9.1** | Critical data quality improvement, pure Python logic (feasible). |

## 🥈 Tier 2: High Value / High Effort (Score 8.0 - 8.9)

Features that are powerful but require more complex implementation.

| Rank | Feature | ID | Score | Rationale |
| :--- | :--- | :--- | :---: | :--- |
| **06** | **IP Health v2 (Auto-Healing)** | `13` | **8.8** | Massive utility, but Feasibility varies by user device (Root/ADB). |
| **07** | **Snapshotting v2 (Smart Diffs)** | `18` | **8.7** | Great for debugging, logic-heavy but safe. |
| **08** | **Discovery v2 (Recursive)** | `17` | **8.6** | High value, but risk of infinite loops (Reliability penalty). |
| **09** | **Geo-Fencing Validator** | `26` | **8.5** | Good safety feature, relies on accurate GeoIP data. |
| **10** | **Honeytoken Detection** | `29` | **8.4** | Stealth upgrade, requires reliable pattern matching. |
| **11** | **Session Persistence v2 (Enc)** | `19` | **8.3** | Security upgrade, adds dependency overhead (`cryptography`). |
| **12** | **Web Dashboard v2** | `14` | **8.1** | Amazing UX, but complex implementation (Frontend + Backend). |

## 🥉 Tier 3: Niche / Experimental (Score 6.0 - 7.9)

Useful for specific use-cases but lower overall priority.

| Rank | Feature | ID | Score | Rationale |
| :--- | :--- | :--- | :---: | :--- |
| **13** | **Console UI v2 (Matrix)** | `16` | **7.9** | Visual upgrade only, medium complexity. |
| **14** | **Crypto Wallet Validator** | `27` | **7.6** | High utility for crypto users, useless for others. |
| **15** | **Native VPN Support** | `25` | **6.8** | High utility, but low Feasibility (Root required). |
| **16** | **OCR / Vision Parsing** | `22` | **6.5** | Heavy dependencies (`tesseract`), slow on mobile. |
| **17** | **Registration Analysis** | `31` | **6.4** | Complex parsing, prone to breakage (Low Reliability). |

## 📉 Tier 4: Moonshots (Score < 6.0)

High risk, difficult to implement on Termux, or questionable ROI.

| Rank | Feature | ID | Score | Rationale |
| :--- | :--- | :--- | :---: | :--- |
| **18** | **P2P Community Sync** | `30` | **5.8** | Complex networking, adoption barrier. |
| **19** | **Fingerprint Evasion** | `28` | **5.5** | Very hard without headless browser (Playwright). |
| **20** | **LLM T&C Parsing** | `24` | **4.2** | Extremely heavy (RAM/CPU), likely to crash Termux. |
