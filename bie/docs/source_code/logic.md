# `logic.py` Documentation (Intelligence Layer)

## File Overview
The intelligence layer. Defines data structures, the mathematical scoring algorithm, and the logic for identifying unique bonuses.

## Sections

### 1. MODELS
*   **Purpose:** Defines `BONUS_HEADERS`. Handles normalization of API keys (`normalize`) and mapping raw data to rows (`map`).
*   **Key Identifiers:** `headers`, `extended`, `norm`, `row`.

### 2. DEDUPLICATION
*   **Purpose:** Implements fuzzy matching (`is_fuzzy_match`) and string cleaning to prevent mirror-site data collision.
*   **Logic Flow:**
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

### 3. FILTER & PV
*   **Purpose:** 
    *   **Algorithm V14:** The `score()` function calculates Perceived Value.
    *   **Filtering:** `filter()` discards "junk" bonuses based on business rules.
    *   **Fingerprinting:** `fingerprint()` generates unique IDs.
*   **Key Functions:** `score()`, `numeric()`, `fuzzy()`, `highvalue()`.