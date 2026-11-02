"""
Test Runner API Engine
Provides programmatically callable test execution with live event streaming callbacks,
failure screenshot capturing, and JSON execution report persistence.
"""
import os
import sys
import time
import json
import unittest
from datetime import datetime

try:
    from .test_catalog import TEST_METADATA
    from .test_registration import TestRegistration
    from .test_login import TestLogin
    from .test_search import TestSearch
    from .test_comments import TestComments
    from .test_navigation import TestNavigation
except ImportError:
    from test_catalog import TEST_METADATA
    from test_registration import TestRegistration
    from test_login import TestLogin
    from test_search import TestSearch
    from test_comments import TestComments
    from test_navigation import TestNavigation

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class LiveStreamingResult(unittest.TestResult):
    def __init__(self, on_event=None):
        super().__init__()
        self.on_event = on_event
        self.test_records = []
        self.bugs = []

    def startTest(self, test):
        super().startTest(test)
        self._test_start = time.time()
        method_name = test._testMethodName
        meta = TEST_METADATA.get(method_name, {})
        test_id = meta.get("id", method_name)

        if self.on_event:
            self.on_event({
                "type": "test_start",
                "test_id": test_id,
                "method": method_name,
                "suite": test.__class__.__name__,
                "title": meta.get("title", method_name),
                "feature": meta.get("feature", "Web Application"),
                "expected": meta.get("expected", test._testMethodDoc or method_name)
            })

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - self._test_start
        method_name = test._testMethodName
        meta = TEST_METADATA.get(method_name, {})
        test_id = meta.get("id", method_name)

        record = {
            "test_id": test_id,
            "method": method_name,
            "suite": test.__class__.__name__,
            "title": meta.get("title", method_name),
            "feature": meta.get("feature", "Web Application"),
            "expected": meta.get("expected", test._testMethodDoc or method_name),
            "actual": "Expected behavior verified successfully without discrepancies.",
            "status": "PASS",
            "duration": f"{elapsed:.2f}s",
            "duration_secs": round(elapsed, 2),
            "error": "",
            "screenshot": ""
        }
        self.test_records.append(record)

        if self.on_event:
            self.on_event({
                "type": "test_complete",
                "record": record
            })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record_failure_or_error(test, err, status="FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        self._record_failure_or_error(test, err, status="ERROR")

    def _record_failure_or_error(self, test, err, status="FAIL"):
        elapsed = time.time() - self._test_start
        method_name = test._testMethodName
        meta = TEST_METADATA.get(method_name, {})
        test_id = meta.get("id", method_name)

        error_msg = self._exc_info_to_string(err, test)
        lines = [line.strip() for line in error_msg.splitlines() if line.strip()]
        short_reason = lines[-1] if lines else "Assertion Error"

        screenshot_path = ""
        screenshot_url = ""
        if hasattr(test, "capture_screenshot"):
            try:
                screenshot_path = test.capture_screenshot(f"{method_name}_{status}")
                screenshot_url = f"/tests/screenshots/{os.path.basename(screenshot_path)}"
            except Exception:
                pass

        record = {
            "test_id": test_id,
            "method": method_name,
            "suite": test.__class__.__name__,
            "title": meta.get("title", method_name),
            "feature": meta.get("feature", "Web Application"),
            "expected": meta.get("expected", test._testMethodDoc or method_name),
            "actual": f"FAILED: {short_reason}",
            "status": status,
            "duration": f"{elapsed:.2f}s",
            "duration_secs": round(elapsed, 2),
            "error": error_msg,
            "screenshot": screenshot_url
        }
        self.test_records.append(record)

        bug = {
            "bug_id": f"BUG-{test_id.replace('TC-', '')}",
            "test_id": test_id,
            "method": method_name,
            "feature": meta.get("feature", "Web Application"),
            "severity": meta.get("severity", "S2 (Major)"),
            "priority": meta.get("priority", "P2 (High)"),
            "expected": meta.get("expected", "Expected behavior"),
            "actual": short_reason,
            "error_details": error_msg,
            "screenshot": screenshot_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.bugs.append(bug)

        if self.on_event:
            self.on_event({
                "type": "test_complete",
                "record": record,
                "bug": bug
            })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        elapsed = time.time() - self._test_start
        method_name = test._testMethodName
        meta = TEST_METADATA.get(method_name, {})
        test_id = meta.get("id", method_name)

        record = {
            "test_id": test_id,
            "method": method_name,
            "suite": test.__class__.__name__,
            "title": meta.get("title", method_name),
            "feature": meta.get("feature", "Web Application"),
            "expected": meta.get("expected", test._testMethodDoc or method_name),
            "actual": f"Skipped: {reason}",
            "status": "SKIPPED",
            "duration": f"{elapsed:.2f}s",
            "duration_secs": round(elapsed, 2),
            "error": "",
            "screenshot": ""
        }
        self.test_records.append(record)

        if self.on_event:
            self.on_event({
                "type": "test_complete",
                "record": record
            })

def build_test_suite(suite_name="all"):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite_lower = suite_name.lower().strip()
    if suite_lower in ("all", "regression"):
        suite.addTests(loader.loadTestsFromTestCase(TestRegistration))
        suite.addTests(loader.loadTestsFromTestCase(TestLogin))
        suite.addTests(loader.loadTestsFromTestCase(TestSearch))
        suite.addTests(loader.loadTestsFromTestCase(TestComments))
        suite.addTests(loader.loadTestsFromTestCase(TestNavigation))
    elif suite_lower == "registration":
        suite.addTests(loader.loadTestsFromTestCase(TestRegistration))
    elif suite_lower == "login":
        suite.addTests(loader.loadTestsFromTestCase(TestLogin))
    elif suite_lower == "search":
        suite.addTests(loader.loadTestsFromTestCase(TestSearch))
    elif suite_lower == "comments":
        suite.addTests(loader.loadTestsFromTestCase(TestComments))
    elif suite_lower == "navigation":
        suite.addTests(loader.loadTestsFromTestCase(TestNavigation))
    elif suite_lower in ("validation", "form_validation"):
        # Select validation-specific test cases from Registration and Login
        for method in [
            "test_02_registration_empty_fields_validation",
            "test_03_registration_invalid_email_regex",
            "test_04_registration_short_password_validation",
            "test_05_registration_password_mismatch",
            "test_07_registration_duplicate_email_prevention",
            "test_09_covid_test_registration_invalid_phone_regex"
        ]:
            suite.addTest(TestRegistration(method))
        for method in [
            "test_02_login_empty_fields_validation",
            "test_03_login_invalid_email_regex",
            "test_05_login_wrong_password"
        ]:
            suite.addTest(TestLogin(method))
        for method in [
            "test_03_comment_empty_validation",
            "test_05_comment_xss_protection_and_escaping"
        ]:
            suite.addTest(TestComments(method))
    else:
        # Default fallback
        suite.addTests(loader.loadTestsFromTestCase(TestRegistration))

    return suite

def execute_suite(suite_name="all", headless=True, on_event=None):
    """
    Executes the specified test suite.
    - headless=True: Headless Chrome (no popup windows, silent background execution)
    - headless=False: Visible Chrome
    """
    os.environ["HEADLESS"] = "true" if headless else "false"

    suite = build_test_suite(suite_name)
    total_tests = suite.countTestCases()
    start_time = time.time()
    start_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if on_event:
        on_event({
            "type": "suite_start",
            "suite": suite_name,
            "total": total_tests,
            "start_time": start_iso,
            "headless": headless
        })

    result_collector = LiveStreamingResult(on_event=on_event)
    runner = unittest.TextTestRunner(resultclass=lambda *args, **kwargs: result_collector, verbosity=1)
    
    # Run the tests
    runner.run(suite)

    elapsed_total = time.time() - start_time
    end_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    passed_count = sum(1 for r in result_collector.test_records if r["status"] == "PASS")
    failed_count = sum(1 for r in result_collector.test_records if r["status"] in ("FAIL", "ERROR"))
    skipped_count = sum(1 for r in result_collector.test_records if r["status"] == "SKIPPED")
    pass_rate = round((passed_count / len(result_collector.test_records) * 100), 1) if result_collector.test_records else 0.0

    summary = {
        "suite_name": suite_name,
        "run_id": f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "start_time": start_iso,
        "end_time": end_iso,
        "duration": f"{elapsed_total:.2f}s",
        "duration_secs": round(elapsed_total, 2),
        "total": len(result_collector.test_records),
        "passed": passed_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "pass_rate": pass_rate,
        "headless": headless,
        "records": result_collector.test_records,
        "bugs": result_collector.bugs
    }

    # Save execution run to JSON file
    run_file = os.path.join(RESULTS_DIR, f"{summary['run_id']}.json")
    try:
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save run report JSON: {e}")

    if on_event:
        on_event({
            "type": "suite_complete",
            "summary": summary
        })

    return summary
