"""
COVID-19 Portal & Integrated Selenium QA Server
Python standard-library HTTP server with automatic browser launch,
REST API for test execution, Server-Sent Events (SSE) streaming, and report persistence.
"""
import os
import sys
import json
import time
from datetime import datetime
import queue
import socket
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# Ensure tests directory is on path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

RESULTS_DIR = os.path.join(BASE_DIR, "tests", "results")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "tests", "screenshots")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

execute_suite = None
IMPORT_ERROR_DETAILS = ""

def get_test_runner():
    global execute_suite, IMPORT_ERROR_DETAILS
    if execute_suite is not None:
        return execute_suite, ""
    try:
        from test_runner_api import execute_suite as runner
        execute_suite = runner
        return execute_suite, ""
    except Exception as e1:
        try:
            from tests.test_runner_api import execute_suite as runner
            execute_suite = runner
            return execute_suite, ""
        except Exception as e2:
            IMPORT_ERROR_DETAILS = str(e2)
            return None, str(e2)

PORT = 8000
HOST = "127.0.0.1"

# Global Test Runner State
class TestStateManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.is_running = False
        self.suite_name = "idle"
        self.total = 0
        self.completed = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.current_test = ""
        self.start_time = ""
        self.end_time = ""
        self.duration = "0.00s"
        self.pass_rate = 0.0
        self.records = []
        self.bugs = []
        self.subscribers = []

    def subscribe(self):
        q = queue.Queue(maxsize=100)
        with self.lock:
            self.subscribers.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.subscribers:
                self.subscribers.remove(q)

    def broadcast(self, event):
        with self.lock:
            dead_queues = []
            for q in self.subscribers:
                try:
                    q.put_nowait(event)
                except queue.Full:
                    dead_queues.append(q)
            for dq in dead_queues:
                if dq in self.subscribers:
                    self.subscribers.remove(dq)

    def on_runner_event(self, event):
        etype = event.get("type")
        with self.lock:
            if etype == "suite_start":
                self.is_running = True
                self.suite_name = event.get("suite", "all")
                self.total = event.get("total", 0)
                self.completed = 0
                self.passed = 0
                self.failed = 0
                self.skipped = 0
                self.records = []
                self.bugs = []
                self.start_time = event.get("start_time", "")
                self.end_time = ""
                self.duration = "0.00s"
                self.pass_rate = 0.0
                self.current_test = "Initializing Chrome Browser..."

            elif etype == "test_start":
                self.current_test = f"{event.get('title', '')} ({event.get('test_id', '')})"

            elif etype == "test_complete":
                rec = event.get("record", {})
                self.completed += 1
                if rec.get("status") == "PASS":
                    self.passed += 1
                elif rec.get("status") in ("FAIL", "ERROR"):
                    self.failed += 1
                elif rec.get("status") == "SKIPPED":
                    self.skipped += 1

                self.records.append(rec)
                if event.get("bug"):
                    self.bugs.append(event["bug"])

                self.pass_rate = round((self.passed / self.completed * 100), 1) if self.completed > 0 else 0.0
                self.current_test = f"Finished {rec.get('title', '')}"

            elif etype == "suite_complete":
                summary = event.get("summary", {})
                self.is_running = False
                self.end_time = summary.get("end_time", "")
                self.duration = summary.get("duration", "0.00s")
                self.total = summary.get("total", len(self.records))
                self.passed = summary.get("passed", self.passed)
                self.failed = summary.get("failed", self.failed)
                self.skipped = summary.get("skipped", self.skipped)
                self.pass_rate = summary.get("pass_rate", self.pass_rate)
                self.current_test = "Suite Execution Complete."

        # Broadcast event to frontend SSE subscribers
        self.broadcast(event)

    def get_snapshot(self):
        with self.lock:
            return {
                "is_running": self.is_running,
                "suite_name": self.suite_name,
                "total": self.total,
                "completed": self.completed,
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "pass_rate": self.pass_rate,
                "current_test": self.current_test,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.duration,
                "records": self.records,
                "bugs": self.bugs
            }

STATE_MANAGER = TestStateManager()

class PortalRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def handle(self):
        try:
            super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError, OSError):
            pass

    def log_message(self, format, *args):
        # Keep terminal output clean as requested:
        # Only log server errors or unexpected codes, ignore routine 200/304 GET requests
        code = args[1] if len(args) > 1 else ""
        if str(code).startswith(("4", "5")):
            sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]} - Code {code}\n")

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. API: Current test execution state snapshot
        if path == "/api/test-status":
            snapshot = STATE_MANAGER.get_snapshot()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(json.dumps(snapshot).encode("utf-8"))
            return

        # 2. API: Server-Sent Events (SSE) live progress stream
        elif path == "/api/test-events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            client_queue = STATE_MANAGER.subscribe()
            try:
                # Send initial snapshot
                init_event = {"type": "init", "snapshot": STATE_MANAGER.get_snapshot()}
                self.wfile.write(f"data: {json.dumps(init_event)}\n\n".encode("utf-8"))
                self.wfile.flush()

                while True:
                    try:
                        event = client_queue.get(timeout=1.5)
                        self.wfile.write(f"data: {json.dumps(event)}\n\n".encode("utf-8"))
                        self.wfile.flush()
                    except queue.Empty:
                        # Send periodic keep-alive comment
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                pass
            finally:
                STATE_MANAGER.unsubscribe(client_queue)
            return

        # 3. API: Test run history
        elif path == "/api/history":
            params = parse_qs(parsed.query)
            target_file = params.get("file", [None])[0]

            if target_file:
                safe_name = os.path.basename(target_file)
                file_path = os.path.join(RESULTS_DIR, safe_name)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode("utf-8"))
                    return
                else:
                    self.send_error(404, "Report file not found")
                    return
            else:
                files = []
                if os.path.exists(RESULTS_DIR):
                    for fn in sorted(os.listdir(RESULTS_DIR), reverse=True):
                        if fn.endswith(".json"):
                            fp = os.path.join(RESULTS_DIR, fn)
                            try:
                                with open(fp, "r", encoding="utf-8") as f:
                                    d = json.load(f)
                                files.append({
                                    "filename": fn,
                                    "run_id": d.get("run_id", fn),
                                    "suite_name": d.get("suite_name", "all"),
                                    "start_time": d.get("start_time", ""),
                                    "total": d.get("total", 0),
                                    "passed": d.get("passed", 0),
                                    "failed": d.get("failed", 0),
                                    "pass_rate": d.get("pass_rate", 0)
                                })
                            except Exception:
                                pass
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(files).encode("utf-8"))
                return

        # Default: Serve static assets / HTML / CSS / JS / screenshots
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/run-tests":
            # Prevent multiple concurrent test runs
            if STATE_MANAGER.is_running:
                self.send_response(409)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "A test suite is already executing. Please wait for completion."
                }).encode("utf-8"))
                return

            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len) if content_len > 0 else b"{}"
            try:
                payload = json.loads(post_data.decode("utf-8"))
            except Exception:
                payload = {}

            suite_name = payload.get("suite", "all")
            # Default headless to False so Chrome opens visibly as requested by user
            headless = payload.get("headless", False)

            runner_fn, runner_err = get_test_runner()
            if runner_fn is None:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "error": f"Test runner not available: {runner_err}. Run 'pip install selenium' to enable testing."
                }).encode("utf-8"))
                return

            # Start background execution thread
            def _runner():
                try:
                    runner_fn(
                        suite_name=suite_name,
                        headless=headless,
                        on_event=STATE_MANAGER.on_runner_event
                    )
                except Exception as ex:
                    print(f"Error during test execution: {ex}")
                    STATE_MANAGER.on_runner_event({
                        "type": "suite_complete",
                        "summary": {
                            "suite_name": suite_name,
                            "error": str(ex),
                            "duration": "0s",
                            "records": [],
                            "bugs": []
                        }
                    })

            thread = threading.Thread(target=_runner, daemon=True)
            thread.start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "started",
                "suite": suite_name,
                "headless": headless,
                "message": f"Test suite '{suite_name}' initiated in separate Chrome browser."
            }).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

def find_free_port(desired_port=PORT):
    for p in range(desired_port, desired_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, p))
                return p
            except OSError:
                continue
    return desired_port

def start_server(port=PORT):
    actual_port = find_free_port(port)
    server = ThreadingHTTPServer((HOST, actual_port), PortalRequestHandler)
    target_url = f"http://localhost:{actual_port}"
    print("=" * 68)
    print(" COVID-19 INFORMATION PORTAL & INTEGRATED SELENIUM QA LAB")
    print(f" Web Server Active at: {target_url}")
    print(" Launching Google Chrome automatically...")
    print(" Press Ctrl+C in terminal to stop.")
    print("=" * 68)

    # Launch Chrome automatically after short delay
    def _open_browser():
        time.sleep(1.2)
        try:
            opened = webbrowser.open(target_url)
            if not opened and sys.platform.startswith("win"):
                os.system(f'start {target_url}')
        except Exception:
            if sys.platform.startswith("win"):
                os.system(f'start {target_url}')
            else:
                print(f"Note: Open {target_url} in your browser.")

    threading.Thread(target=_open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    start_server(PORT)
