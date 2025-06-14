import asyncio
import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.clients.websocket_clients import start_all_clients
from src.normalizer import normalize
from src.comparator import update_jobs, get_latest_jobs, get_differences

app = FastAPI()

static_dir = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(static_dir / "index.html") as f:
        return f.read()

@app.get("/api/jobs")
async def jobs():
    return JSONResponse(get_latest_jobs())

@app.get("/api/differences")
async def differences():
    return JSONResponse(get_differences())

def start_server():
    import threading
    import yaml

    with open("config/sources.json") as f:
        config = json.load(f)

    async def message_handler(source_type, data):
        # print(f"[{source_type}] RAW INCOMING:\n{json.dumps(data, indent=2)}")
        normalized = normalize(source_type, data)
        if normalized:
            update_jobs(normalized)

    def run_ws_clients():
        asyncio.run(start_all_clients(config, message_handler))

    threading.Thread(target=run_ws_clients, daemon=True).start()
    # use this for local testing
    uvicorn.run(app, host="0.0.0.0", port=8000)
