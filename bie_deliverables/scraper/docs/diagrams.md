# System Diagrams

This page provides a visual overview of the Bonus Intelligence Engine's architecture, processes, and data structures.

## 🏛️ Core Architecture
The 7-layer model separating foundation, execution, and visualization.

```mermaid
graph TD
    subgraph "Execution Layer (run.py)"
        Orch[Orchestrator]
        Worker[ScrapeWorker]
    end

    subgraph "Foundation Layer (base.py)"
        Config[Config Manager]
        DB[DB Pool]
        IO[IO Manager]
        State[System State]
    end

    subgraph "Interaction Layer (flow.py)"
        Auth[Auth Logic]
        Parse[Parser Logic]
        API[API Rituals]
    end

    subgraph "Intelligence Layer (logic.py)"
        Scorer[PV Scorer V14]
        Dedup[Deduplicator]
        Models[Data Models]
    end

    subgraph "Connectivity Layer (net.py)"
        Net[Network Manager]
        Health[Proxy Health]
    end

    subgraph "Visualization Layer (ui.py)"
        TUI[Rich Dashboard]
        Stats[Rolling Metrics]
    end

    subgraph "Communication Layer (web_server.py)"
        FastAPI[Web Server]
        WS[WebSocket Stream]
    end

    %% Key Flows
    Orch -->|Spawns| Worker
    Worker -->|Network Req| Net
    Worker -->|API Rituals| flow
    Worker -->|Scoring| logic
    Worker -->|Writes| base

    Net -->|Health Check| Health
    Health -->|Cache| DB

    Worker -->|Update UI| TUI
    TUI -->|Broadcast| FastAPI
    FastAPI -->|WebSocket| WS
    WS -->|Remote Dashboard| Browser

    %% Dependencies
    base -->|Config| Orch
    base -->|DB Connection| Net
    logic -->|Models| Worker
    flow -->|Parsing| Worker
```

---

## 🔄 Scrape Sequence
The lifecycle of a single scrape task, from proxy acquisition to data persistence.

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

---

## 🚦 State Lifecycles
How the system manages the health and transitions of targets and proxies.

```mermaid
stateDiagram-v2
    direction LR

    %% Target Lifecycle
    state "Target URL (targets table)" as Target {
        [*] --> New
        New --> Active: Initial Discovery
        Active --> Active: Success (200 OK)
        Active --> Purgatory: 5 Consecutive Failures
        Purgatory --> Active: Success (Redemption)
        Purgatory --> Pruned: 5 Retest Failures
        Pruned --> [*]
    }

    %% Proxy Lifecycle
    state "Proxy IP (proxy_health table)" as Proxy {
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

---

## 🗄️ Database Schema (ERD)
The relational structure of the SQLite persistence layer.

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

---

## 🧮 PV Algorithm Flow
Visualizing the input variables and mathematical transformations in the Perceived Value scorer.

```mermaid
graph TD
    subgraph Inputs
        Amt[Amount]
        MaxW[Max Withdraw]
        MinW[Min Withdraw]
        Roll[Rollover]
    end

    subgraph "Reward Calculation (Logarithmic)"
        R1["log2(MaxW + 1) * 10"]
        R2["log10(Amt + 1) * 0.2 + 1"]
        Reward["Reward = R1 * R2"]
    end

    subgraph "Difficulty Calculation (Exponential)"
        D1["max(1, max(MinW, Amt*Roll)/Amt)"]
        D2["pow(D1, 1.25)"]
        D3["1 + (Roll / 20)"]
        Diff["Difficulty = D2 * D3"]
    end

    Result["PV = Reward / Difficulty"]

    Amt --> R2
    Amt --> D1
    MaxW --> R1
    MinW --> D1
    Roll --> D1
    Roll --> D3

    R1 --> Reward
    R2 --> Reward

    D1 --> D2
    D2 --> Diff
    D3 --> Diff

    Reward --> Result
    Diff --> Result
```

---

## 🧬 Deduplication Logic
How the system identifies duplicate bonuses across mirror sites.

```mermaid
flowchart TD
    Start([New Bonus Data]) --> FP{Check Fingerprint}
    FP -- Match --> Update[Update Mirrors & Verified]
    FP -- No Match --> Fuzzy{Fuzzy Name Match?}
    
    Fuzzy -- "> 80% Similarity" --> Update
    Fuzzy -- No Match --> Hash{Check Raw JSON Hash}
    
    Hash -- Match --> Update
    Hash -- No Match --> Insert([Insert New Record])
    
    Update --> Done([Return Unique ID])
    Insert --> Done
```

---

## 🔎 Extraction Ritual
The fallback mechanism for finding Merchant IDs in obscure site structures.

```mermaid
sequenceDiagram
    participant Worker
    participant Flow
    participant Parser
    participant Net

    Worker->>Flow: get_merchant_details(html)
    Flow->>Parser: extract_variable("MERCHANTID")
    alt Found in HTML
        Parser-->>Flow: ID
    else Not Found
        Flow->>Parser: Scan <script src=...>
        Parser->>Net: Fetch JS Bundles
        Net-->>Parser: JS Content
        Parser-->>Flow: ID from JS
    end
    Flow-->>Worker: Merchant ID

    Worker->>Flow: get_api_endpoint(base_url)
    Flow-->>Worker: "/api/v1/index.php"
```

---

## 📡 WebSocket Broadcast
The data flow for real-time dashboard updates.

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