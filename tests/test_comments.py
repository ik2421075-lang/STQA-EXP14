"""
Test Suite: Community Comments & Discussion Forum
Covers MOD-06 (REQ-12)
"""
import time
import unittest
from selenium.webdriver.common.by import By
try:
    from .base_test import BaseTestCase
except ImportError:
    from base_test import BaseTestCase

class TestComments(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.reset_local_storage()

    def test_01_comments_locked_when_logged_out(self):
        """Verify comment posting is restricted and auth lock notice is shown to guests."""
        lock_banner = self.wait_for_visible(By.ID, "comment-auth-lock")
        self.assertIn("Authentication Required", lock_banner.text, "Lock notice should inform user to log in")
        
        post_form = self.wait_for_element(By.ID, "comment-post-form")
        self.assertIn("hidden", post_form.get_attribute("class"), "Post form must be hidden when logged out")

    def test_02_comments_unlocked_when_logged_in(self):
        """Verify logging in displays comment form with active user name badge."""
        # Log in
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        post_form = self.wait_for_visible(By.ID, "comment-post-form")
        self.assertNotIn("hidden", post_form.get_attribute("class"), "Comment form should be unlocked")

        author_name = self.wait_for_element(By.ID, "comment-author-name").text
        self.assertEqual(author_name, "Anita Sharma", "Author badge should show logged in user name")

    def test_03_comment_empty_validation(self):
        """Verify submitting empty or whitespace comment is rejected."""
        # Log in
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        submit_btn = self.wait_for_clickable(By.ID, "comment-submit")
        self.safe_click(submit_btn)

        msg_box = self.wait_for_visible(By.ID, "comment-msg")
        self.assertIn("Comment cannot be empty", msg_box.text, "Empty comment must be rejected")

    def test_04_comment_successful_posting(self):
        """Verify valid comment is posted, added to feed, and author/timestamp displayed."""
        # Log in
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        test_comment = "Fully vaccinated with precautionary dose. Smooth experience!"
        self.safe_send_keys(self.wait_for_element(By.ID, "comment-input"), test_comment)
        self.safe_click(self.wait_for_clickable(By.ID, "comment-submit"))

        msg_box = self.wait_for_visible(By.ID, "comment-msg")
        self.assertIn("posted successfully", msg_box.text, "Success message should display")

        comments_list = self.wait_for_visible(By.ID, "comments-list")
        self.assertIn(test_comment, comments_list.text, "Posted comment should appear in list")
        self.assertIn("Anita Sharma", comments_list.text, "Author name should appear with comment")

    def test_05_comment_xss_protection_and_escaping(self):
        """Verify REQ-12: Script and HTML characters are escaped to prevent XSS injection."""
        # Log in
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        malicious_input = '<script>alert("XSS")</script><b>Sanitized Text</b>'
        self.safe_send_keys(self.wait_for_element(By.ID, "comment-input"), malicious_input)
        self.safe_click(self.wait_for_clickable(By.ID, "comment-submit"))

        comments_list = self.wait_for_visible(By.ID, "comments-list")
        # Ensure the raw script tag was not executed or inserted unescaped
        html_content = comments_list.get_attribute("innerHTML")
        self.assertNotIn('<script>alert("XSS")</script>', html_content, "Raw script tags must not be injected")
        self.assertIn('&lt;script&gt;', html_content, "Script tags must be safely HTML escaped")

    def test_06_comment_author_deletion(self):
        """Verify author has delete button and can delete their own comment."""
        # Log in as Anita Sharma
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "anita.sharma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        # Pre-seeded comment by Anita is 'cmt-1'
        delete_btn = self.wait_for_element(By.ID, "delete-comment-cmt-1")
        self.assertTrue(delete_btn.is_displayed(), "Delete button must be visible to comment author")

        # Automatically accept confirmation dialog
        self.driver.execute_script("window.confirm = function() { return true; };")
        self.safe_click(delete_btn)
        time.sleep(0.5)

        # Verify comment is removed
        comments_list = self.wait_for_element(By.ID, "comments-list")
        self.assertNotIn("delete-comment-cmt-1", comments_list.get_attribute("innerHTML"), "Deleted comment should be removed")

    def test_07_comment_non_author_cannot_delete(self):
        """Verify users cannot see delete buttons for comments authored by others."""
        # Pre-seeded comment 'cmt-1' is by Anita Sharma.
        # Log in as Rahul Verma
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        self.safe_send_keys(self.wait_for_element(By.ID, "login-email"), "rahul.verma@example.com")
        self.safe_send_keys(self.wait_for_element(By.ID, "login-password"), "password123")
        self.safe_click(self.wait_for_clickable(By.ID, "login-submit"))
        time.sleep(1)

        # Check that delete button for Anita's comment does not exist
        anita_delete_btns = self.driver.find_elements(By.ID, "delete-comment-cmt-1")
        self.assertEqual(len(anita_delete_btns), 0, "Rahul should not see delete button for Anita's comment")

if __name__ == "__main__":
    unittest.main(verbosity=2)
