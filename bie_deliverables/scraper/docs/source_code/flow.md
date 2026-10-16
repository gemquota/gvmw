# `flow.py` Documentation (Interaction Layer)

## File Overview
Handles the "Conversation" logic required to extract data from casino mirror sites.

## Sections

### 1. AUTH
*   **Purpose:** Formulates login payloads and handles credential authentication via the API.
*   **Key Function:** `login()`.

### 2. API
*   **Purpose:** Manages endpoint construction (`get_api_endpoint`) and `syncData` synchronization requests.
*   **Key Function:** `fetch_sync_data()`.

### 3. PARSER
*   **Purpose:** Uses regex to extract `MERCHANTID` and `MERCHANTNAME` from HTML landing pages or JavaScript bundles.
*   **Key Functions:** `extract_variable()`, `get_merchant_details()`.
*   **Extraction Ritual:**
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
