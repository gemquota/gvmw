# Dashboard API & WebSocket Reference

## 1. Control API (REST)
The web server runs on `http://127.0.0.1:8000`. These endpoints are used to control the engine lifecycle.

### **POST** `/api/control/pause`
Suspends all worker processing after their current site task completes.
*   **Response**: `{"status": "paused"}`

### **POST** `/api/control/resume`
Resumes worker processing immediately.
*   **Response**: `{"status": "running"}`

### **POST** `/api/control/stop`
Signals all workers to terminate immediately and shuts down the engine.
*   **Response**: `{"status": "stopping"}`

### **GET** `/api/control/status`
Returns the current state of the engine.
*   **Response**: `{"is_paused": bool, "is_stopped": bool}`

### **GET** `/api/config`
Retrieves the current settings from `in/config.ini`.
*   **Response**: JSON object of all sections and keys.

---

## 2. Real-time Stream (WebSocket)
The WebSocket endpoint provides a live telemetry feed.

*   **URL**: `ws://127.0.0.1:8000/ws`
*   **Payload Type**: JSON

### Message Schema (Sample)
```json
{
  "index": 12,
  "site_url": "casino-mirror-99.com",
  "status_message": "✅",
  "site_new_bonuses": 2,
  "total_new_bonuses": 45,
  "elapsed": 1.245,
  "ip_score": 0,
  "is_paused": false,
  "is_stopped": false
}
```

---

## 3. Internal Update API
### **POST** `/update`
Used by the TUI (`ui.py`) to push data to the web server.
*   **Payload**: The dashboard data dictionary.
*   **Note**: This endpoint is intended for internal use but can be utilized by external tools to inject status messages into the dashboard.
