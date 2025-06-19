from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import subprocess
import threading
import os

app = Flask(__name__)
CORS(app)

# Serve the frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)

# API endpoints
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "backend": "running"})

# stratum data endpoints here
@app.route('/api/stratum-data')
def stratum_data():
    # logic to get stratum data
    return jsonify({"message": "Backend is working!"})

# existing run.py logic
def run_backend():
    try:
        # Import and run existing backend logic
        import run
    except Exception as e:
        print(f"Error running backend: {e}")

# Start backend in a thread
backend_thread = threading.Thread(target=run_backend)
backend_thread.daemon = True
backend_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)