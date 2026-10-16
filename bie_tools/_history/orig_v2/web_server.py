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
import base

# --- Security ---
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != base.UI_USER or credentials.password != base.UI_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

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

app = FastAPI()

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
    """Public WebSocket endpoint for real-time data."""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/update")
async def update_dashboard_data(data: dict):
    """Internal endpoint for pushing real-time updates."""
    data['is_paused'] = base.state.is_paused
    data['is_stopped'] = base.state.is_stopped
    await manager.broadcast(json.dumps(data))
    return {"status": "ok"}

@app.post("/api/control/pause")
async def pause_scraper():
    base.state.pause()
    return {"status": "paused"}

@app.post("/api/control/resume")
async def resume_scraper():
    base.state.resume()
    return {"status": "running"}

@app.post("/api/control/stop")
async def stop_scraper():
    base.state.stop()
    return {"status": "stopping"}

@app.get("/api/control/status")
async def get_system_status():
    return {
        "is_paused": base.state.is_paused,
        "is_stopped": base.state.is_stopped
    }

@app.get("/api/config")
async def get_current_config():
    import configparser
    config_parser = configparser.ConfigParser()
    config_parser.read('in/config/config.ini')
    return {section: dict(config_parser.items(section)) for section in config_parser.sections()}

@app.post("/api/config")
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

@app.get("/")
async def get_dashboard():
    with open("in/templates/index.html", "r") as f:
        return HTMLResponse(f.read())

def start_server():
    print(f"[*] Dashboard active at: http://0.0.0.0:8000 (No Authentication Required)")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
