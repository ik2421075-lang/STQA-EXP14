"""
Base Test Case and Utilities for COVID-19 Portal Automated Testing
Provides reusable WebDriver setup, explicit wait helpers, and failure screenshot capture.
"""
import os
import time
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("PORTAL_URL", "http://localhost:8000")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class BaseTestCase(unittest.TestCase):
    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        if os.environ.get("HEADLESS", "true").lower() in ("1", "true", "yes"):
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1366,768")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(2)
        cls.wait = WebDriverWait(cls.driver, 5)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        self.driver.get(BASE_URL)
        time.sleep(0.4)

    def tearDown(self):
        pass

    def capture_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        try:
            self.driver.save_screenshot(filepath)
            print(f"\n [SCREENSHOT SAVED]: {filepath}")
        except Exception as e:
            print(f"\n [SCREENSHOT FAILED]: {e}")
        return filepath

    def wait_for_element(self, by, value, timeout=5):
        """Wait explicitly for element presence."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_visible(self, by, value, timeout=5):
        """Wait explicitly for element visibility."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))

    def wait_for_clickable(self, by, value, timeout=5):
        """Wait explicitly for element clickability."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def wait_for_text(self, by, value, text, timeout=5):
        """Wait explicitly for specific text to appear inside element."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element((by, value), text))

    def safe_click(self, element):
        """Scroll element into center view and click safely."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def safe_send_keys(self, element, text):
        """Scroll into view, clear existing value, and send keys."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.clear()
        element.send_keys(text)

    def reset_local_storage(self):
        """Clear local storage and reload portal to restore clean seed state."""
        self.driver.execute_script("localStorage.clear();")
        self.driver.get(BASE_URL)
        time.sleep(0.4)
