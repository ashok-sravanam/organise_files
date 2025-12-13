from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from auth import Token, FAKE_USERS_DB, verify_password, create_access_token, get_current_user, get_user_from_token, ACCESS_TOKEN_EXPIRE_MINUTES
from text_watcher import IndexWatcher

import sys
import os
# Add parent dir to sys.path to import from src
sys.path.append(str(Path(__file__).resolve().parent.parent))
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
import time

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "migration_index.json"
SOURCE_DIR = Path("/Users/ashoks/Downloads") # Hardcoded for PoC

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Background File Watcher
index_watcher = None
source_watcher = None

def run_extractor():
    """Runs the main extraction script."""
    print("Change detected! Running extraction...")
    # We run main.py as a subprocess to keep it isolated/clean for this PoC
    try:
        subprocess.run(["python3", str(BASE_DIR / "main.py")], check=True)
    except Exception as e:
        print(f"Extraction failed: {e}")

class SourceHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.cooldown = 10 # Seconds to wait before re-running to avoid spam

    def on_created(self, event):
        if event.is_directory: return
        self._trigger(event.src_path)

    def on_modified(self, event):
        if event.is_directory: return
        # Ignore the index file itself to prevent loops if it was in the same dir
        if "migration_index.json" in event.src_path: return
        # Ignore dotfiles
        if "/." in event.src_path: return
        self._trigger(event.src_path)

    def _trigger(self, path):
        current_time = time.time()
        if current_time - self.last_run > self.cooldown:
             print(f"File change detected at: {path}")
             self.last_run = current_time
             threading.Thread(target=run_extractor).start()

def on_index_changed():
    """Callback when JSON file changes."""
    print("Detected change in migration_index.json")
    try:
        with open(INDEX_FILE, 'r') as f:
            data = json.load(f)
        # Broadcast new data to all connected clients
        asyncio.run(manager.broadcast(json.dumps({"type": "UPDATE", "data": data})))
    except Exception as e:
        print(f"Error broadcasting update: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global index_watcher, source_watcher
    
    # 1. Watch for Index Updates (Push to WebSocket)
    print(f"Starting Index Watcher for {INDEX_FILE}")
    index_watcher = IndexWatcher(str(INDEX_FILE.parent), str(INDEX_FILE.name), on_index_changed)
    index_watcher.start()

    # 2. Watch for NEW FILES in Downloads (Trigger Extraction)
    # WARNING: Watching entire Downloads folder might be noisy. Restricting to non-hidden.
    print(f"Starting Source Watcher for {SOURCE_DIR}")
    event_handler = SourceHandler()
    source_watcher = Observer()
    source_watcher.schedule(event_handler, str(SOURCE_DIR), recursive=False)
    source_watcher.start()

    yield
    # Shutdown
    if index_watcher: index_watcher.stop()
    if source_watcher:
        source_watcher.stop()
        source_watcher.join()

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, set to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/documents")
async def get_documents(current_user: str = Depends(get_current_user)):
    """Secure endpoint to get all documents."""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    return []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """Secure WebSocket Endpoint."""
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
