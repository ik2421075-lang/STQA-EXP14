"""
Test Suite: User Registration & COVID-19 Diagnostic Test Booking
Covers MOD-01, MOD-02 (Regex Validation), and MOD-03 (Test Registration)
"""
import time
import unittest
from selenium.webdriver.common.by import By
try:
    from .base_test import BaseTestCase
except ImportError:
    from base_test import BaseTestCase

class TestRegistration(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Ensure fresh state
        self.reset_local_storage()

    def test_01_registration_modal_toggle(self):
        """Verify Register button opens modal and close button closes it."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)
        
        modal = self.wait_for_element(By.ID, "register-modal")
        self.assertNotIn("hidden", modal.get_attribute("class"), "Registration modal should be visible")
        
        close_btn = modal.find_element(By.CLASS_NAME, "modal-close")
        self.safe_click(close_btn)
        time.sleep(0.3)
        self.assertIn("hidden", modal.get_attribute("class"), "Registration modal should be hidden after closing")

    def test_02_registration_empty_fields_validation(self):
        """Verify form validation rejects submission when required fields are empty."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        submit_btn = self.wait_for_clickable(By.ID, "register-submit")
        self.safe_click(submit_btn)

        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("All fields are mandatory", msg_box.text, "Validation error should alert for missing fields")

    def test_03_registration_invalid_email_regex(self):
        """Verify REQ-07: Email regex rejects malformed email addresses."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        self.safe_send_keys(self.wait_for_element(By.ID, "register-name"), "Anita Sharma")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "anita.example.com") # Missing @
        self.safe_send_keys(self.wait_for_element(By.ID, "register-password"), "secret123")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-confirm-password"), "secret123")

        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("Invalid email format", msg_box.text, "Email without @ must be rejected")

        # Boundary Test: Double @
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "anita@@example.com")
        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        self.assertIn("Invalid email format", msg_box.text, "Email with @@ must be rejected")

    def test_04_registration_short_password_validation(self):
        """Verify password requirement enforces minimum 6 characters."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        self.safe_send_keys(self.wait_for_element(By.ID, "register-name"), "Anita Sharma")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "anita.valid@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-password"), "12345") # 5 chars
        self.safe_send_keys(self.wait_for_element(By.ID, "register-confirm-password"), "12345")

        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("at least 6 characters", msg_box.text, "Password < 6 chars must be rejected")

    def test_05_registration_password_mismatch(self):
        """Verify confirmation password must match primary password."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        self.safe_send_keys(self.wait_for_element(By.ID, "register-name"), "Anita Sharma")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "anita.valid@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-password"), "password123")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-confirm-password"), "differentpass")

        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("do not match", msg_box.text, "Mismatched passwords must be flagged")

    def test_06_registration_successful_and_auto_transition(self):
        """Verify valid details register successfully and switch to login modal."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        self.safe_send_keys(self.wait_for_element(By.ID, "register-name"), "Sunita Rao")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "sunita.rao@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-password"), "securePass123")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-confirm-password"), "securePass123")

        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("Registration successful", msg_box.text, "Success alert should confirm registration")

        # Wait for auto-transition to login modal
        login_modal = self.wait_for_element(By.ID, "login-modal")
        time.sleep(1.5)
        self.assertNotIn("hidden", login_modal.get_attribute("class"), "Should transition to login modal")

    def test_07_registration_duplicate_email_prevention(self):
        """Verify REQ-14: Duplicate email registrations are strictly prevented."""
        reg_btn = self.wait_for_clickable(By.ID, "nav-register")
        self.safe_click(reg_btn)

        # Pre-seeded user is 'anita.sharma@example.com'
        self.safe_send_keys(self.wait_for_element(By.ID, "register-name"), "Anita Sharma")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-password"), "password123")
        self.safe_send_keys(self.wait_for_element(By.ID, "register-confirm-password"), "password123")

        self.safe_click(self.wait_for_clickable(By.ID, "register-submit"))
        msg_box = self.wait_for_visible(By.ID, "register-msg")
        self.assertIn("already registered", msg_box.text, "Duplicate email registration must be blocked")

    def test_08_covid_test_registration_valid_submission(self):
        """Verify MOD-03: Booking a COVID diagnostic appointment with valid regex fields."""
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-name"), "Karan Singh")
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-phone"), "9812345678")
        
        # Set DOB via script
        self.driver.execute_script("document.getElementById('patient-dob').value = '1995-10-15';")
        self.driver.execute_script("document.getElementById('govt-id-type').value = 'PAN'; updateGovtIdPlaceholder();")
        self.safe_send_keys(self.wait_for_element(By.ID, "govt-id-num"), "ABCDE6789K")
        self.driver.execute_script("document.getElementById('patient-state').value = 'Maharashtra';")
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-address"), "Sector 4, Vashi, Navi Mumbai")
        self.driver.execute_script("document.getElementById('test-type').value = 'RT-PCR';")
        self.driver.execute_script("document.getElementById('patient-slot').value = '2026-11-25T10:30';")

        submit_btn = self.wait_for_clickable(By.ID, "test-reg-submit")
        self.safe_click(submit_btn)

        msg_box = self.wait_for_visible(By.ID, "test-reg-msg")
        self.assertIn("Test registered successfully", msg_box.text, "Diagnostic booking should succeed")
        self.assertIn("ORD-", msg_box.text, "Order ID should be generated")

    def test_09_covid_test_registration_invalid_phone_regex(self):
        """Verify REQ-08: Phone number regex rejects numbers starting with < 6 or non-10 digits."""
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-name"), "Vikram Joshi")
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-phone"), "5876543210") # Starts with 5
        self.driver.execute_script("document.getElementById('patient-dob').value = '1992-06-20';")
        self.driver.execute_script("document.getElementById('govt-id-type').value = 'Aadhaar'; updateGovtIdPlaceholder();")
        self.safe_send_keys(self.wait_for_element(By.ID, "govt-id-num"), "234567890123")
        self.driver.execute_script("document.getElementById('patient-state').value = 'Delhi';")
        self.safe_send_keys(self.wait_for_element(By.ID, "patient-address"), "Connaught Place, Delhi")
        self.driver.execute_script("document.getElementById('test-type').value = 'Rapid Antigen';")
        self.driver.execute_script("document.getElementById('patient-slot').value = '2026-11-25T11:00';")

        self.safe_click(self.wait_for_clickable(By.ID, "test-reg-submit"))
        msg_box = self.wait_for_visible(By.ID, "test-reg-msg")
        self.assertIn("Invalid Mobile Number", msg_box.text, "Phone starting with 5 must be rejected")

if __name__ == "__main__":
    unittest.main(verbosity=2)
