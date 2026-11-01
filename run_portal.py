"""
Single-Command Project Entry Point & Auto-Launcher
Usage: python run_portal.py (or double-click RUN_PROJECT.bat)
Starts the local server and automatically launches Google Chrome.
"""
import os
import sys
import subprocess

def ensure_selenium():
    try:
        import selenium
    except ImportError:
        print("=" * 68)
        print(" [SETUP] Selenium is not installed. Installing automatically...")
        print("=" * 68)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
            print(" [SUCCESS] Selenium installed successfully!\n")
        except Exception as e:
            print(f" [WARNING] Could not auto-install Selenium: {e}")
            print(" The portal will still load, but automated tests require 'pip install selenium'.\n")

if __name__ == "__main__":
    ensure_selenium()
    try:
        from server import start_server, PORT
        start_server(PORT)
    except Exception as ex:
        print("\n" + "=" * 68)
        print(f" [ERROR] Server encountered an issue: {ex}")
        print("=" * 68)
        input("\nPress Enter to exit...")
