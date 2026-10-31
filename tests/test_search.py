"""
Test Suite: Knowledge Base Search & Diagnostic Patient Report Retrieval
Covers Module C (Search Module) & MOD-04 (REQ-05, REQ-06)
"""
import time
import unittest
from selenium.webdriver.common.by import By
try:
    from .base_test import BaseTestCase
except ImportError:
    from base_test import BaseTestCase

class TestSearch(BaseTestCase):

    def test_01_portal_search_matching_query(self):
        """Verify portal search returns relevant articles for valid search terms."""
        search_input = self.wait_for_element(By.ID, "search-input")
        self.safe_send_keys(search_input, "RT-PCR")
        
        search_btn = self.wait_for_clickable(By.ID, "search-button")
        self.safe_click(search_btn)

        results_box = self.wait_for_visible(By.ID, "search-results")
        self.assertIn("Reverse Transcription", results_box.text, "Search should retrieve RT-PCR information")
        self.assertIn("Diagnostics", results_box.text, "Category badge should be visible")

    def test_02_portal_search_symptoms_query(self):
        """Verify searching for symptom keyword returns symptoms topic."""
        search_input = self.wait_for_element(By.ID, "search-input")
        self.safe_send_keys(search_input, "fever")
        
        self.safe_click(self.wait_for_clickable(By.ID, "search-button"))
        results_box = self.wait_for_visible(By.ID, "search-results")
        self.assertIn("Fever & Chills", results_box.text, "Search should retrieve fever symptom topic")

    def test_03_portal_search_unknown_query_fallback(self):
        """Verify searching for non-existent keyword displays suitable no-results message."""
        search_input = self.wait_for_element(By.ID, "search-input")
        self.safe_send_keys(search_input, "unknownrandomquery999")
        
        self.safe_click(self.wait_for_clickable(By.ID, "search-button"))
        results_box = self.wait_for_visible(By.ID, "search-results")
        self.assertIn("No Results Found", results_box.text, "No results alert should display")
        self.assertIn("No matching information found", results_box.text, "Helper instructions should display")

    def test_04_portal_search_clear_button(self):
        """Verify clear button appears when typing and clears results when clicked."""
        search_input = self.wait_for_element(By.ID, "search-input")
        self.safe_send_keys(search_input, "vaccine")
        
        clear_btn = self.wait_for_element(By.ID, "search-clear")
        self.assertNotIn("hidden", clear_btn.get_attribute("class"), "Clear button should appear")

        self.safe_click(clear_btn)
        time.sleep(0.3)
        self.assertEqual(search_input.get_attribute("value"), "", "Input field should be cleared")

    def test_05_portal_search_trending_quick_tags(self):
        """Verify clicking trending keyword button executes search immediately."""
        quick_tags = self.driver.find_elements(By.CLASS_NAME, "quick-tag")
        self.assertGreater(len(quick_tags), 0, "Quick tags should exist")
        
        self.safe_click(quick_tags[0]) # "Symptoms"
        time.sleep(0.5)

        results_box = self.wait_for_visible(By.ID, "search-results")
        self.assertNotIn("hidden", results_box.get_attribute("class"), "Results should populate on quick tag click")

    def test_06_report_search_registered_mobile(self):
        """Verify REQ-05: Searching registered mobile displays patient diagnostic report."""
        report_input = self.wait_for_element(By.ID, "report-search-input")
        self.safe_send_keys(report_input, "9876543210")
        
        report_btn = self.wait_for_clickable(By.ID, "report-search-btn")
        self.safe_click(report_btn)

        report_card = self.wait_for_visible(By.ID, "report-result-card")
        patient_name = self.wait_for_element(By.ID, "report-patient-name").text
        order_no = self.wait_for_element(By.ID, "report-order-no").text

        self.assertEqual(patient_name, "Anita Sharma", "Patient name should match registered record")
        self.assertIn("ORD-1001", order_no, "Order ID should match registered record")

    def test_07_report_search_by_order_id(self):
        """Verify searching by Order ID retrieves the corresponding laboratory report."""
        report_input = self.wait_for_element(By.ID, "report-search-input")
        self.safe_send_keys(report_input, "ORD-1001")
        
        self.safe_click(self.wait_for_clickable(By.ID, "report-search-btn"))
        report_card = self.wait_for_visible(By.ID, "report-result-card")
        self.assertNotIn("hidden", report_card.get_attribute("class"), "Report card should be displayed")

    def test_08_report_search_unregistered_mobile_not_found(self):
        """Verify REQ-06: Searching unregistered phone number shows 'Not Found' alert without error."""
        report_input = self.wait_for_element(By.ID, "report-search-input")
        self.safe_send_keys(report_input, "9123456780")
        
        self.safe_click(self.wait_for_clickable(By.ID, "report-search-btn"))
        not_found_msg = self.wait_for_visible(By.ID, "report-not-found-msg")
        self.assertIn("No Patient Report Found", not_found_msg.text, "Not found message should be displayed")
        
        # Verify report card is hidden
        report_card = self.wait_for_element(By.ID, "report-result-card")
        self.assertIn("hidden", report_card.get_attribute("class"), "Report card should remain hidden")

if __name__ == "__main__":
    unittest.main(verbosity=2)
