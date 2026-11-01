"""
Single-Command Project Entry Point
Usage: python run_portal.py
Starts the local server and automatically launches Google Chrome at http://localhost:8000.
"""
from server import start_server, PORT

if __name__ == "__main__":
    start_server(PORT)
