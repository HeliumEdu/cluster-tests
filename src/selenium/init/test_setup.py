__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import os

from emailhelper import get_verification_code
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.seleniumtestcase import SeleniumTestCase
from workspacehelper import init_workspace


class TestSeleniumAuth(SeleniumTestCase):
    def test_1_init_workspace(self):
        init_workspace(self.get_info(), self.api_host, self.test_username, self.test_email, self.test_password)

    def test_2_register_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'register'))

        username_field = self.driver.find_element(By.ID, "id_username")
        email_field = self.driver.find_element(By.ID, "id_email")
        password_field = self.driver.find_element(By.ID, "id_password1")
        confirm_password_field = self.driver.find_element(By.ID, "id_password2")
        terms_checkbox = self.driver.find_element(By.CSS_SELECTOR,
                                                  "#register-form > div:nth-child(1) > div > fieldset > label:nth-child(6) > input")

        username_field.send_keys(self.test_username)
        email_field.send_keys(self.test_email)
        password_field.send_keys(self.test_password)
        confirm_password_field.send_keys(self.test_password)
        terms_checkbox.click()

        login_button = self.driver.find_element(By.CSS_SELECTOR, "#register-form > div:nth-child(2) > div > button")
        login_button.click()

        # Registration will redirect us to the login page and await verification
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Login")
        )

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))

        success_status = self.driver.find_element(By.CSS_SELECTOR, "#status")
        self.assertTrue(success_status.is_displayed())
        self.assertIn("The last step is to verify your email address.", success_status.text)

        email_verification_code = get_verification_code(self.get_info(), self.test_username)[
            'email_verification_code']

        self.driver.get(os.path.join(self.app_host, "verify") +
                        f"?username={self.test_username}&code={email_verification_code}&welcome-email=false")

        # Verification will redirect us to the login page
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Login")
        )

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))
        success_status = self.driver.find_element(By.CSS_SELECTOR, "#status")
        self.assertTrue(success_status.is_displayed())
        self.assertIn("Your email address has been verified.", success_status.text)

    def test_3_login_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'login'))

        username_field = self.driver.find_element(By.ID, "id_username")
        password_field = self.driver.find_element(By.ID, "id_password")

        username_field.send_keys(self.test_username)
        password_field.send_keys(self.test_password)

        login_button = self.driver.find_element(By.CSS_SELECTOR, "#login-form > fieldset > div.clearfix > button")
        login_button.click()

        # Login will redirect us to the planner
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Calendar")
        )

        # Wait for calendar to load
        getting_started_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        self.assertEqual(os.path.join(self.app_host, 'planner', 'calendar'), self.driver.current_url.strip('/'))

        # Click this to fire request to not show it on next login
        show_getting_started_checkbox = self.driver.find_element(By.ID, "show-getting-started")
        show_getting_started_checkbox.click()

        close_getting_started_button = self.driver.find_element(By.ID, "close-getting-started")
        close_getting_started_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element(getting_started_modal)
        )
