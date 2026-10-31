"""
Test Suite: Navigation, Layout, Responsive UI, and Interactive Elements
Covers MOD-07, REQ-15 (Responsiveness across viewports), and CAT-NAV
"""
import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
try:
    from .base_test import BaseTestCase
except ImportError:
    from base_test import BaseTestCase

class TestNavigation(BaseTestCase):

    def test_01_all_navbar_links_present(self):
        """Verify presence and accessibility of all top-level module navigation links."""
        expected_links = [
            ("nav-home", "Home"),
            ("nav-info", "Overview"),
            ("nav-symptoms", "Symptoms"),
            ("nav-prevention", "Prevention"),
            ("nav-vaccine", "Vaccination"),
            ("nav-test-reg", "Book Test"),
            ("nav-report-search", "Search Report"),
            ("nav-dashboard", "Dashboard"),
            ("nav-comments", "Community")
        ]
        for link_id, text in expected_links:
            element = self.wait_for_element(By.ID, link_id)
            self.assertTrue(element.is_displayed(), f"Nav link #{link_id} should be visible")
            self.assertIn(text, element.text, f"Nav link #{link_id} text mismatch")

    def test_02_navbar_navigation_targets(self):
        """Verify clicking navigation links properly routes to target sections."""
        targets = [
            ("nav-symptoms", "symptoms"),
            ("nav-prevention", "prevention"),
            ("nav-vaccine", "vaccination"),
            ("nav-test-reg", "test-registration"),
            ("nav-report-search", "report-search"),
            ("nav-dashboard", "dashboard")
        ]
        for nav_id, section_id in targets:
            link = self.wait_for_element(By.ID, nav_id)
            self.safe_click(link)
            time.sleep(0.3)
            section = self.wait_for_element(By.ID, section_id)
            self.assertIsNotNone(section, f"Target #{section_id} must exist in DOM")

    def test_03_hero_cta_buttons(self):
        """Verify hero call-to-action buttons are present and functional."""
        cta_buttons = [
            "hero-btn-book-test",
            "hero-btn-check-report",
            "hero-btn-symptoms"
        ]
        for btn_id in cta_buttons:
            btn = self.wait_for_clickable(By.ID, btn_id)
            self.assertTrue(btn.is_displayed(), f"CTA button #{btn_id} must be visible")

    def test_04_mobile_viewport_hamburger_navigation(self):
        """Verify responsiveness (REQ-15): Hamburger button appears and toggles nav on mobile (480px)."""
        self.driver.set_window_size(480, 800)
        time.sleep(0.5)

        nav_toggle = self.wait_for_element(By.ID, "nav-toggle")
        self.assertTrue(nav_toggle.is_displayed(), "Mobile hamburger toggle should be visible on 480px width")

        main_nav = self.wait_for_element(By.ID, "main-nav")
        self.assertNotIn("show", main_nav.get_attribute("class"), "Menu should initially be collapsed")

        self.safe_click(nav_toggle)
        time.sleep(0.4)
        self.assertIn("show", main_nav.get_attribute("class"), "Menu should expand when hamburger is clicked")

        # Restore window size
        self.driver.set_window_size(1366, 768)

    def test_05_modal_escape_key_dismissal(self):
        """Verify modal closes when user presses the Escape key."""
        self.safe_click(self.wait_for_clickable(By.ID, "nav-login"))
        modal = self.wait_for_element(By.ID, "login-modal")
        self.assertNotIn("hidden", modal.get_attribute("class"), "Modal should be open")

        # Press Escape
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(0.4)

        self.assertIn("hidden", modal.get_attribute("class"), "Modal should close on ESC key press")

    def test_06_interactive_symptom_checker(self):
        """Verify interactive symptom risk checker evaluates user inputs."""
        # Check fever and shortness of breath (Emergency alert)
        chk_breath = self.wait_for_element(By.ID, "chk-breath")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chk_breath)
        if not chk_breath.is_selected():
            self.safe_click(chk_breath)

        assess_btn = self.wait_for_clickable(By.ID, "btn-assess-symptoms")
        self.safe_click(assess_btn)

        result_box = self.wait_for_visible(By.ID, "checker-result-box")
        self.assertIn("High Risk", result_box.text, "Dyspnea should flag high risk medical alert")

if __name__ == "__main__":
    unittest.main(verbosity=2)
