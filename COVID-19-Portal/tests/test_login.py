"""
Test Suite: User Authentication, Session Management, and Admin Login
Covers MOD-01, REQ-01, REQ-03
"""
import time
import unittest
from selenium.webdriver.common.by import By
try:
    from .base_test import BaseTestCase
except ImportError:
    from base_test import BaseTestCase

class TestLogin(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.reset_local_storage()

    def test_01_login_modal_toggle(self):
        """Verify Login button opens modal and close button dismisses it."""
        login_btn = self.wait_for_clickable(By.ID, "nav-login")
        self.safe_click(login_btn)

        modal = self.wait_for_element(By.ID, "login-modal")
        self.assertNotIn("hidden", modal.get_attribute("class"), "Login modal should be displayed")

        close_btn = modal.find_element(By.CLASS_NAME, "modal-close")
        self.safe_click(close_btn)
        time.sleep(0.3)
        self.assertIn("hidden", modal.get_attribute("class"), "Login modal should be dismissed")

    def test_02_login_empty_fields_validation(self):
        """Verify submitting blank login credentials shows error message."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))

        msg_box = self.wait_for_visible(By.ID, "login-msg")
        self.assertIn("Please enter both email and password", msg_box.text, "Blank fields should trigger error")

    def test_03_login_invalid_email_regex(self):
        """Verify email format regex check on login."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "invaliduser-email")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))

        msg_box = self.wait_for_visible(By.ID, "login-msg")
        self.assertIn("Invalid email format", msg_box.text, "Malformed email on login must be rejected")

    def test_04_login_unregistered_email(self):
        """Verify error message when attempting login with non-existent account."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "nonexistent.person@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "randomPass999")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))

        msg_box = self.wait_for_visible(By.ID, "login-msg")
        self.assertIn("Invalid email or password", msg_box.text, "Unregistered user must be rejected")

    def test_05_login_wrong_password(self):
        """Verify rejection of registered email with incorrect password."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "wrongPassword123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))

        msg_box = self.wait_for_visible(By.ID, "login-msg")
        self.assertIn("Invalid email or password", msg_box.text, "Wrong password must be rejected")

    def test_06_login_successful_and_session_display(self):
        """Verify successful login creates session, updates greeting, and displays logout button."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))

        # Wait for modal close and UI update
        greeting = self.wait_for_visible(By.ID, "user-display-name")
        self.assertIn("Welcome, Anita Sharma", greeting.text, "Header should display user greeting")

        logout_btn = self.wait_for_visible(By.ID, "logout-button")
        self.assertTrue(logout_btn.is_displayed(), "Logout button should be visible")

    def test_07_user_logout_clears_session(self):
        """Verify logout destroys session, clears greeting, and restores login/register buttons."""
        # 1. Log in first
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        self.wait_for_visible(By.ID, "logout-button")

        # 2. Click Logout
        logout_btn = self.wait_for_clickable(By.ID, "logout-button")
        self.safe_click(logout_btn)
        time.sleep(0.5)

        # 3. Verify logged-out controls are restored
        logged_out_box = self.wait_for_element(By.ID, "logged-out-actions")
        self.assertNotIn("hidden", logged_out_box.get_attribute("class"), "Logged out actions should be visible")
        
        login_btn = self.wait_for_element(By.ID, "nav-login")
        self.assertTrue(login_btn.is_displayed(), "Login button should be visible after logout")

    def test_08_admin_login_verification(self):
        """Verify administrative login modal and authentication check."""
        self.driver.execute_script("openModal('admin-modal');")
        modal = self.wait_for_element(By.ID, "admin-modal")
        self.assertNotIn("hidden", modal.get_attribute("class"), "Admin modal should open")

        self.safe_send_keys(self.wait_for_element(By.ID, "admin-username"), "admin")
        self.safe_send_keys(self.wait_for_element(By.ID, "admin-password"), "admin123")
        self.safe_click(self.wait_for_clickable(By.ID, "admin-submit"))

        msg_box = self.wait_for_visible(By.ID, "admin-msg")
        self.assertIn("Admin authentication verified", msg_box.text, "Admin credentials should be accepted")

if __name__ == "__main__":
    unittest.main(verbosity=2)
