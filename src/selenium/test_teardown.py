__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.16.13"

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumTeardown(SeleniumTestCase):
    def test_1_delete_example_schedule(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Wait for getting started modal to show
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        # Click this to fire request to not show it on next login
        show_getting_started_checkbox = self.driver.find_element(By.ID, "delete-example-schedule")
        show_getting_started_checkbox.click()

        # Ensure all items on the calendar were deleted
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) == 0
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_2_delete_user(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'settings'))

        account_tab = self.driver.find_element(By.CSS_SELECTOR, "#settings-tabs > li:nth-child(3) > a")
        account_tab.click()

        delete_account_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "delete-account"))
        )
        delete_account_button.click()

        delete_account_password_field = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "delete-account-password"))
        )
        delete_account_password_field.send_keys(self.test_password)

        delete_account_ok_button = self.driver.find_element(By.CSS_SELECTOR,
                                                            "body > div.bootbox.modal.fade.in > div > div > div.modal-footer > button.btn.btn-danger")
        delete_account_ok_button.click()

        # Delete will log us out and redirect to login page
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Login")
        )

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))

        success_status = self.driver.find_element(By.CSS_SELECTOR, "#status")
        self.assertTrue(success_status.is_displayed())
        self.assertIn("Sorry to see you go!", success_status.text)
