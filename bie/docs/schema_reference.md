# Database Schema & Analytics Guide

## 1. Entity Relationship Overview
The system uses a flat but relational SQLite structure designed for high-concurrency access (WAL mode).

```mermaid
erDiagram

    targets {
        TEXT url PK
        TEXT merchant_name
        TEXT status "active | purgatory | pruned"
        INT failure_count
        INT retest_count
        DATETIME last_checked
        JSON alts_tried
    }

    bonuses {
        TEXT unique_id PK "fingerprint"
        TEXT url FK
        REAL perceived_value
        REAL amount
        DATETIME expiration_date
        TEXT mirrors "url1,url2"
        TEXT fingerprint
        JSON raw_json_hash
        TEXT conf_rollover
        TEXT conf_min_withdraw
        TEXT conf_max_withdraw
        BOOL verified
    }

    sessions {
        TEXT username PK
        TEXT url FK
        JSON cookie_jar
        JSON session_data
        DATETIME timestamp
        INT is_valid
    }

    metrics {
        INT id PK
        DATETIME timestamp
        INT total_scraped
        INT new_bonuses
        INT errors
        REAL avg_latency
        REAL peak_ram
    }

    proxy_health {
        TEXT proxy PK
        TEXT status "active | cooling | burned"
        INT burn_count
        DATETIME last_burn_ts
        INT abuse_score
    }

    %% Relationships
    targets ||--o{ bonuses : "discovered_on"
    targets ||--o{ sessions : "authenticated_as"
    proxy_health ||--o{ metrics : "used_in"
```

*   **Database Path:** `db/base.db`
*   **`targets`**: The master list of mirror URLs.
*   **`bonuses`**: Discovery table. Multiple bonuses per target.
*   **`sessions`**: Persistence layer. Stores JSON cookies.
*   **`metrics`**: Historical performance tracking.
*   **`logs`**: Error and system events.

---

## 2. Data Dictionary

### Table: `targets`
| Column | Type | Description |
| :--- | :--- | :--- |
| `url` | TEXT (PK) | Unique site URL. |
| `merchant_name` | TEXT | Human-readable name. |
| `status` | TEXT | 'active', 'purgatory', 'pruned'. |
| `failure_count` | INT | Sequential errors before penalty. |

### Table: `bonuses`
| Column | Type | Description |
| :--- | :--- | :--- |
| `unique_id` | TEXT (PK) | Fingerprint ID. |
| `perceived_value`| REAL | The score() result. |
| `amount` | REAL | Raw gift value. |
| `conf_*` | TEXT | Flattened JSON terms. |

### Table: `sessions`
| Column | Type | Description |
| :--- | :--- | :--- |
| `username` | TEXT | Account identifier. |
| `is_valid` | INT | Binary health flag (1/0). |
| `last_used_at` | DATETIME | Expiry check baseline. |

---

## 3. Analytics Cookbook (SQL)

### Find "Golden" Mirrors
```sql
SELECT url, COUNT(*) as bonus_count, AVG(perceived_value) as avg_pv
FROM bonuses
GROUP BY url
HAVING bonus_count > 2
ORDER BY avg_pv DESC;
```

### Rollover Heatmap
```sql
SELECT merchant_name, AVG(CAST(conf_rollover AS FLOAT)) as avg_rollover
FROM bonuses
WHERE conf_rollover IS NOT NULL
GROUP BY merchant_name
ORDER BY avg_rollover DESC;
```
