"""
Master Automated Regression Test Suite Runner
Orchestrates and executes all functional test suites:
- test_registration.py
- test_login.py
- test_search.py
- test_comments.py
- test_navigation.py

Generates detailed console output and self-contained HTML test execution report.
"""
import os
import sys
import time
import socket
import unittest
import subprocess
from datetime import datetime

# Import test cases
from test_registration import TestRegistration
from test_login import TestLogin
from test_search import TestSearch
from test_comments import TestComments
from test_navigation import TestNavigation

PORT = 8000
BASE_URL = f"http://localhost:{PORT}"
REPORT_PATH = os.path.join(os.path.dirname(__file__), "test_execution_report.html")

def is_server_running(host="localhost", port=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def start_server_if_needed():
    if not is_server_running():
        print(f"[*] Starting local HTTP server on port {PORT}...")
        proc = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(PORT)],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(1.2)
        return proc
    return None

class DetailedTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_records = []

    def startTest(self, test):
        super().startTest(test)
        self._start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - self._start_time
        doc = test._testMethodDoc or test._testMethodName
        self.test_records.append({
            "name": test._testMethodName,
            "suite": test.__class__.__name__,
            "description": doc.strip(),
            "status": "PASS",
            "time": f"{elapsed:.2f}s",
            "error": ""
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        elapsed = time.time() - self._start_time
        doc = test._testMethodDoc or test._testMethodName
        if hasattr(test, "capture_screenshot"):
            test.capture_screenshot(f"{test._testMethodName}_FAIL")
        self.test_records.append({
            "name": test._testMethodName,
            "suite": test.__class__.__name__,
            "description": doc.strip(),
            "status": "FAIL",
            "time": f"{elapsed:.2f}s",
            "error": self._exc_info_to_string(err, test)
        })

    def addError(self, test, err):
        super().addError(test, err)
        elapsed = time.time() - self._start_time
        doc = test._testMethodDoc or test._testMethodName
        if hasattr(test, "capture_screenshot"):
            test.capture_screenshot(f"{test._testMethodName}_ERR")
        self.test_records.append({
            "name": test._testMethodName,
            "suite": test.__class__.__name__,
            "description": doc.strip(),
            "status": "ERROR",
            "time": f"{elapsed:.2f}s",
            "error": self._exc_info_to_string(err, test)
        })

def generate_html_report(records, total_time):
    total = len(records)
    passed = sum(1 for r in records if r["status"] == "PASS")
    failed = sum(1 for r in records if r["status"] == "FAIL")
    errors = sum(1 for r in records if r["status"] == "ERROR")
    pass_pct = (passed / total * 100) if total > 0 else 0

    rows_html = ""
    for r in records:
        status_class = "pass" if r["status"] == "PASS" else "fail"
        badge = f'<span class="badge {status_class}">{r["status"]}</span>'
        error_html = f'<div class="error-msg"><pre>{r["error"]}</pre></div>' if r["error"] else ""
        rows_html += f"""
        <tr>
          <td><strong>{r["suite"]}</strong></td>
          <td><code>{r["name"]}</code></td>
          <td>{r["description"]}{error_html}</td>
          <td>{badge}</td>
          <td>{r["time"]}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>STQA Regression Test Report - Experiment 14</title>
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 24px; }}
    .container {{ max-width: 1200px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); padding: 32px; border: 1px solid #e2e8f0; }}
    h1 {{ color: #0369a1; margin-top: 0; }}
    .meta-box {{ background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; margin-bottom: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }}
    .metric strong {{ font-size: 1.5rem; color: #0284c7; display: block; }}
    .metric span {{ font-size: 0.85rem; color: #64748b; text-transform: uppercase; font-weight: 600; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9rem; }}
    th {{ background: #0369a1; color: #ffffff; text-align: left; padding: 12px; }}
    td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    tr:hover {{ background: #f1f5f9; }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
    .badge.pass {{ background: #dcfce7; color: #15803d; }}
    .badge.fail {{ background: #fee2e2; color: #b91c1c; }}
    .error-msg {{ background: #fff1f2; border: 1px solid #fca5a5; padding: 8px; border-radius: 6px; margin-top: 6px; font-size: 0.8rem; overflow-x: auto; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>STQA Regression Test Execution Report</h1>
    <p>Project: <strong>COVID-19 Information & Awareness Portal</strong> | STQA Experiment 14</p>
    <div class="meta-box">
      <div class="metric"><strong>{total}</strong><span>Total Tests</span></div>
      <div class="metric"><strong>{passed}</strong><span style="color: #16a34a;">Passed</span></div>
      <div class="metric"><strong>{failed + errors}</strong><span style="color: #dc2626;">Failed / Errors</span></div>
      <div class="metric"><strong>{pass_pct:.1f}%</strong><span>Pass Rate</span></div>
      <div class="metric"><strong>{total_time:.2f}s</strong><span>Total Execution Time</span></div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Test Suite</th>
          <th>Test Identifier</th>
          <th>Objective / Details</th>
          <th>Status</th>
          <th>Duration</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[REPORT GENERATED]: {REPORT_PATH}")

def run_regression_suite():
    server_proc = start_server_if_needed()
    start_time = time.time()

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestRegistration))
    suite.addTests(loader.loadTestsFromTestCase(TestLogin))
    suite.addTests(loader.loadTestsFromTestCase(TestSearch))
    suite.addTests(loader.loadTestsFromTestCase(TestComments))
    suite.addTests(loader.loadTestsFromTestCase(TestNavigation))

    runner = unittest.TextTestRunner(resultclass=DetailedTestResult, verbosity=2)
    print("=" * 70)
    print("EXECUTIVE REGRESSION SUITE EXECUTION - COVID-19 PORTAL")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target URL: {BASE_URL}")
    print("=" * 70)

    result = runner.run(suite)
    total_time = time.time() - start_time

    # Generate HTML Report
    generate_html_report(result.test_records, total_time)

    # Teardown background server if we started it
    if server_proc:
        server_proc.terminate()
        server_proc.wait()

    print("\n" + "=" * 70)
    print(f"REGRESSION SUITE COMPLETED: {result.testsRun} Tests Run in {total_time:.2f}s")
    print(f"PASSED: {result.testsRun - len(result.failures) - len(result.errors)} | FAILED: {len(result.failures)} | ERRORS: {len(result.errors)}")
    print("=" * 70)

    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_regression_suite()
    sys.exit(0 if success else 1)
