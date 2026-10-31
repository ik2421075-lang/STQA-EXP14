"""
Comprehensive Automated Selenium Verification Suite for COVID-19 Portal
Tests all modules, validations, local storage sessions, searches, and comments.
"""
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def run_tests():
    print("=" * 60)
    print("STARTING COVID-19 PORTAL AUTOMATED SELENIUM TEST SUITE")
    print("=" * 60)

    # 1. Start Python HTTP server on port 8000
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(1.5)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    passed_tests = 0
    total_tests = 0

    def assert_test(name, condition, details=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] {name}")
        else:
            print(f" [FAIL] {name}: {details}")

    def safe_click(element):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        try:
            element.click()
        except Exception:
            driver.execute_script("arguments[0].click();", element)

    try:
        url = "http://localhost:8000"
        driver.get(url)
        time.sleep(1)

        # TEST 1: Page Load & Title
        assert_test("TC-01: Page Load & Title", "COVID-19" in driver.title, f"Title was: {driver.title}")

        # TEST 2: Navigation Bar Links Presence
        nav_ids = ['nav-home', 'nav-info', 'nav-symptoms', 'nav-prevention', 'nav-vaccine', 'nav-test-reg', 'nav-report-search', 'nav-dashboard', 'nav-comments']
        all_nav_present = all(driver.find_element(By.ID, nid) is not None for nid in nav_ids)
        assert_test("TC-02: Navigation Bar Links Present", all_nav_present)

        # TEST 3: User Registration - Invalid Email Regex
        safe_click(driver.find_element(By.ID, "nav-register"))
        time.sleep(0.5)
        
        driver.find_element(By.ID, "register-name").send_keys("Test User")
        driver.find_element(By.ID, "register-email").send_keys("testuser@@invalid") # Invalid email
        driver.find_element(By.ID, "register-password").send_keys("secret123")
        driver.find_element(By.ID, "register-confirm-password").send_keys("secret123")
        safe_click(driver.find_element(By.ID, "register-submit"))
        time.sleep(0.5)

        reg_msg = driver.find_element(By.ID, "register-msg").text
        assert_test("TC-03: Register Email Regex Validation (Rejects invalid email)", "Invalid email format" in reg_msg, reg_msg)

        # TEST 4: User Registration - Password Mismatch
        driver.find_element(By.ID, "register-email").clear()
        driver.find_element(By.ID, "register-email").send_keys("valid.user@example.com")
        driver.find_element(By.ID, "register-confirm-password").clear()
        driver.find_element(By.ID, "register-confirm-password").send_keys("mismatch123")
        safe_click(driver.find_element(By.ID, "register-submit"))
        time.sleep(0.5)
        reg_msg = driver.find_element(By.ID, "register-msg").text
        assert_test("TC-04: Register Password Confirmation Check", "do not match" in reg_msg, reg_msg)

        # TEST 5: User Registration - Successful Registration
        driver.find_element(By.ID, "register-confirm-password").clear()
        driver.find_element(By.ID, "register-confirm-password").send_keys("secret123")
        safe_click(driver.find_element(By.ID, "register-submit"))
        time.sleep(1.8) # Wait for success message & modal transition
        login_modal = driver.find_element(By.ID, "login-modal")
        assert_test("TC-05: Valid User Registration & Transition to Login", "hidden" not in login_modal.get_attribute("class"))

        # TEST 6: User Registration - Duplicate Email Prevention
        driver.execute_script("switchModal('login-modal', 'register-modal')")
        time.sleep(0.5)
        driver.find_element(By.ID, "register-name").send_keys("Another User")
        driver.find_element(By.ID, "register-email").send_keys("valid.user@example.com") # Already registered!
        driver.find_element(By.ID, "register-password").send_keys("secret123")
        driver.find_element(By.ID, "register-confirm-password").send_keys("secret123")
        safe_click(driver.find_element(By.ID, "register-submit"))
        time.sleep(0.5)
        reg_msg = driver.find_element(By.ID, "register-msg").text
        assert_test("TC-06: Duplicate Email Registration Blocked", "already registered" in reg_msg, reg_msg)

        # TEST 7: User Login - Invalid Credentials
        driver.execute_script("switchModal('register-modal', 'login-modal')")
        time.sleep(0.5)
        driver.find_element(By.ID, "login-email").clear()
        driver.find_element(By.ID, "login-email").send_keys("valid.user@example.com")
        driver.find_element(By.ID, "login-password").clear()
        driver.find_element(By.ID, "login-password").send_keys("wrongpass")
        safe_click(driver.find_element(By.ID, "login-submit"))
        time.sleep(0.5)
        login_msg = driver.find_element(By.ID, "login-msg").text
        assert_test("TC-07: Login Rejection of Invalid Password", "Invalid email or password" in login_msg, login_msg)

        # TEST 8: User Login - Successful Login & Session Creation
        driver.find_element(By.ID, "login-password").clear()
        driver.find_element(By.ID, "login-password").send_keys("secret123")
        safe_click(driver.find_element(By.ID, "login-submit"))
        time.sleep(1.2)

        user_display = driver.find_element(By.ID, "user-display-name").text
        assert_test("TC-08: Successful Login & Greeting UI Display", "Welcome, Test User" in user_display, user_display)

        # TEST 9: Portal Search Engine
        search_input = driver.find_element(By.ID, "search-input")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
        search_input.clear()
        search_input.send_keys("RT-PCR")
        safe_click(driver.find_element(By.ID, "search-button"))
        time.sleep(0.5)
        results = driver.find_element(By.ID, "search-results")
        assert_test("TC-09: Portal Search with Keyword 'RT-PCR'", "Reverse Transcription" in results.text, results.text)

        # TEST 10: Portal Search - Unknown Query Fallback
        search_input.clear()
        search_input.send_keys("xyzunknownword999")
        safe_click(driver.find_element(By.ID, "search-button"))
        time.sleep(0.5)
        results = driver.find_element(By.ID, "search-results")
        assert_test("TC-10: Portal Search Fallback for Unknown Query", "No matching information found" in results.text, results.text)

        # TEST 11: Patient Search & Report - Known Mobile (Anita Sharma: 9876543210)
        report_search_input = driver.find_element(By.ID, "report-search-input")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", report_search_input)
        report_search_input.clear()
        report_search_input.send_keys("9876543210")
        safe_click(driver.find_element(By.ID, "report-search-btn"))
        time.sleep(0.5)

        report_card = driver.find_element(By.ID, "report-result-card")
        patient_name = driver.find_element(By.ID, "report-patient-name").text
        assert_test("TC-11: Patient Report Search for 9876543210 (Found)", "hidden" not in report_card.get_attribute("class") and patient_name == "Anita Sharma", f"Name: {patient_name}")

        # TEST 12: Patient Search & Report - Unknown Mobile (9123456780)
        report_search_input.clear()
        report_search_input.send_keys("9123456780")
        safe_click(driver.find_element(By.ID, "report-search-btn"))
        time.sleep(0.5)
        not_found_msg = driver.find_element(By.ID, "report-not-found-msg")
        assert_test("TC-12: Patient Report Search for Unregistered Mobile (Not Found)", "hidden" not in not_found_msg.get_attribute("class"))

        # TEST 13: Comments - Post Comment as Logged In User with XSS Script Tag
        comment_input = driver.find_element(By.ID, "comment-input")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_input)
        comment_input.clear()
        xss_comment = "Testing awareness info <script>alert(1)</script> safe comment"
        comment_input.send_keys(xss_comment)
        safe_click(driver.find_element(By.ID, "comment-submit"))
        time.sleep(0.5)

        comments_list = driver.find_element(By.ID, "comments-list")
        assert_test("TC-13: Comment Posted & XSS Script Tag Escaped", "Testing awareness info" in comments_list.text and "<script>" not in comments_list.get_attribute("innerHTML").replace("&lt;script&gt;", ""))

        # TEST 14: Comments - Delete Comment by Author
        delete_btns = driver.find_elements(By.CLASS_NAME, "delete-comment-btn")
        initial_count = len(delete_btns)
        if initial_count > 0:
            driver.execute_script("window.confirm = function() { return true; };")
            safe_click(delete_btns[0])
            time.sleep(0.5)
            remaining_btns = driver.find_elements(By.CLASS_NAME, "delete-comment-btn")
            assert_test("TC-14: Comment Author Deletion", len(remaining_btns) == initial_count - 1)
        else:
            assert_test("TC-14: Comment Author Deletion", False, "No delete button found")

        # TEST 15: COVID-19 Test Registration Form (MOD-03: new-user-testing)
        patient_name_input = driver.find_element(By.ID, "patient-name")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", patient_name_input)
        patient_name_input.send_keys("Suresh Kumar")
        driver.find_element(By.ID, "patient-phone").send_keys("9823456789")
        
        # Set Date of birth via ISO format value directly
        driver.execute_script("document.getElementById('patient-dob').value = '1996-05-12';")
        
        # Select Govt ID PAN
        driver.execute_script("document.getElementById('govt-id-type').value = 'PAN'; updateGovtIdPlaceholder();")
        driver.find_element(By.ID, "govt-id-num").send_keys("ABCDE5678K")
        driver.execute_script("document.getElementById('patient-state').value = 'Maharashtra';")
        driver.find_element(By.ID, "patient-address").send_keys("Shivaji Nagar, Pune")
        driver.execute_script("document.getElementById('test-type').value = 'RT-PCR';")
        driver.execute_script("document.getElementById('patient-slot').value = '2026-11-20T11:00';")
        
        safe_click(driver.find_element(By.ID, "test-reg-submit"))
        time.sleep(0.5)
        test_reg_msg = driver.find_element(By.ID, "test-reg-msg").text
        assert_test("TC-15: COVID-19 Diagnostic Test Booking (MOD-03)", "Test registered successfully" in test_reg_msg, test_reg_msg)

        # TEST 16: State-Wise Dashboard Sync
        dashboard_body = driver.find_element(By.ID, "state-dashboard-body")
        assert_test("TC-16: State Dashboard Loaded & Synchronized", "Maharashtra" in dashboard_body.text)

        # TEST 17: User Logout
        logout_btn = driver.find_element(By.ID, "logout-button")
        safe_click(logout_btn)
        time.sleep(0.5)
        comment_lock = driver.find_element(By.ID, "comment-auth-lock")
        logged_out_actions = driver.find_element(By.ID, "logged-out-actions")
        assert_test("TC-17: User Logout & Locking of Comments Module", "hidden" not in comment_lock.get_attribute("class") and "hidden" not in logged_out_actions.get_attribute("class"))

        # TEST 18: Responsiveness - Mobile Viewport (480px width)
        driver.set_window_size(480, 800)
        time.sleep(0.5)
        nav_toggle = driver.find_element(By.ID, "nav-toggle")
        assert_test("TC-18: Mobile Viewport (480px) Hamburger Toggle Visible", nav_toggle.is_displayed())

    finally:
        driver.quit()
        server_proc.terminate()
        server_proc.wait()

    print("=" * 60)
    print(f"AUTOMATED VERIFICATION SUMMARY: {passed_tests} / {total_tests} TESTS PASSED")
    print("=" * 60)
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
