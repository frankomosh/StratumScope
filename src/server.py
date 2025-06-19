from flask import Blueprint, jsonify
import asyncio
import json
import threading

from src.clients.websocket_clients import start_all_clients
from src.normalizer import normalize
from src.comparator import update_jobs, get_latest_jobs, get_differences

bp = Blueprint('backend', __name__)

# Flask doesn't support native async, so run this outside request context
def start_ws_clients():
    with open("config/sources.json") as f:
        config = json.load(f)

    async def message_handler(source_type, data):
        normalized = normalize(source_type, data)
        if normalized:
            update_jobs(normalized)

    def runner():
        asyncio.run(start_all_clients(config, message_handler))

    threading.Thread(target=runner, daemon=True).start()

# Call the websocket starter immediately when the module loads
start_ws_clients()

@bp.route("/api/jobs")
def jobs():
    return jsonify(get_latest_jobs())

@bp.route("/api/differences")
def differences():
    return jsonify(get_differences())
