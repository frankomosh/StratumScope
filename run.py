"""
Notic: This file has been left here intentionally for developers who want to run the FastAPI backend standalone.
In the current setup, Flask (`app.py`) wraps this server and serves both frontend and API.
"""

from server import start_server

if __name__ == "__main__":
    start_server()
