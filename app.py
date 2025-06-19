from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
from pathlib import Path

from src.server import bp as backend_bp  # import the backend blueprint

app = Flask(__name__)
CORS(app)

# Register backend routes
app.register_blueprint(backend_bp)

# Serve frontend
frontend_dir = Path(__file__).parent / "frontend"

@app.route("/")
def index():
    return send_from_directory(frontend_dir, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(frontend_dir, path)

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "backend": "running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)