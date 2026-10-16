from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import Dict, Optional
import json
import uvicorn
import asyncio
import os
import secrets
import base

# --- Security ---
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user_ok = secrets.compare_digest(credentials.username.encode(), str(base.UI_USER).encode())
    pass_ok = secrets.compare_digest(credentials.password.encode(), str(base.UI_PASS).encode())
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def websocket_authorized(websocket: WebSocket) -> bool:
    """Basic Auth check for the WebSocket handshake (browsers resend cached Basic credentials)."""
    import base64
    header = websocket.headers.get("authorization", "")
    if not header.lower().startswith("basic "): return False
    try: username, _, password = base64.b64decode(header[6:]).decode().partition(":")
    except Exception: return False
    return secrets.compare_digest(username.encode(), str(base.UI_USER).encode()) and secrets.compare_digest(password.encode(), str(base.UI_PASS).encode())

AUTH = [Depends(get_current_user)]

# --- Models ---

class ScraperSettings(BaseModel):
    workers: Optional[int] = Field(None, ge=1, le=100)
    min_delay: Optional[float] = Field(None, ge=0, le=3600)
    max_delay: Optional[float] = Field(None, ge=0, le=3600)
    abuseipdb_key: Optional[str] = None
    default_max_withdraw: Optional[float] = Field(None, ge=0)

class ConfigUpdate(BaseModel):
    SETTINGS: Optional[ScraperSettings] = None

# --- Configuration ---

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # no unauthenticated auto-docs

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Connection Management ---

class ConnectionManager:
    """Manages active WebSocket connections for the dashboard."""
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# --- Endpoints ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Authenticated WebSocket endpoint for real-time data."""
    if not websocket_authorized(websocket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/update", dependencies=AUTH)
async def update_dashboard_data(data: dict):
    """Internal endpoint for pushing real-time updates."""
    data['is_paused'] = base.state.is_paused
    data['is_stopped'] = base.state.is_stopped
    await manager.broadcast(json.dumps(data))
    return {"status": "ok"}

@app.post("/api/control/pause", dependencies=AUTH)
async def pause_scraper():
    base.state.pause()
    return {"status": "paused"}

@app.post("/api/control/resume", dependencies=AUTH)
async def resume_scraper():
    base.state.resume()
    return {"status": "running"}

@app.post("/api/control/stop", dependencies=AUTH)
async def stop_scraper():
    base.state.stop()
    return {"status": "stopping"}

@app.get("/api/control/status", dependencies=AUTH)
async def get_system_status():
    return {
        "is_paused": base.state.is_paused,
        "is_stopped": base.state.is_stopped
    }

@app.get("/api/config", dependencies=AUTH)
async def get_current_config():
    import configparser
    config_parser = configparser.ConfigParser()
    config_parser.read('in/config/config.ini')
    return {section: dict(config_parser.items(section)) for section in config_parser.sections()}

@app.post("/api/config", dependencies=AUTH)
async def update_config(new_config: ConfigUpdate):
    """Updates config.ini with validated settings."""
    import configparser
    config_parser = configparser.ConfigParser()
    config_parser.read('in/config/config.ini')
    
    if new_config.SETTINGS:
        if not config_parser.has_section('SETTINGS'):
            config_parser.add_section('SETTINGS')
        
        updates = new_config.SETTINGS.dict(exclude_unset=True)
        for key, value in updates.items():
            config_parser.set('SETTINGS', key, str(value))
            
    with open('in/config/config.ini', 'w', encoding='utf-8') as f:
        config_parser.write(f)
        
    return {"status": "updated"}

@app.get("/", dependencies=AUTH)
async def get_dashboard():
    with open("in/templates/index.html", "r") as f:
        return HTMLResponse(f.read())

def start_server():
    host = os.getenv("BIE_HOST", "127.0.0.1")
    port = int(os.getenv("BIE_PORT", "8000"))
    print(f"[*] Dashboard active at: http://{host}:{port} (HTTP Basic Auth: ui_user/ui_pass)")
    uvicorn.run(app, host=host, port=port, log_level="error")
