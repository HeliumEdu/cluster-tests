__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import os
import time
import unittest

from selenium.webdriver.common.by import By
from utils.seleniumtestcase import SeleniumTestCase

ENVIRONMENT = os.environ.get('ENVIRONMENT')
ENVIRONMENT_PREFIX = f'{ENVIRONMENT}.' if 'prod' not in ENVIRONMENT else ''


class TestSeleniumAuth(SeleniumTestCase):
    def test_1_register_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'register'))

        username_field = self.driver.find_element(By.ID, "id_username")
        email_field = self.driver.find_element(By.ID, "id_email")
        password_field = self.driver.find_element(By.ID, "id_password1")
        confirm_password_field = self.driver.find_element(By.ID, "id_password2")
        terms_checkbox = self.driver.find_element(By.XPATH, "//*[@id=\"register-form\"]/div[1]/div/fieldset/label[6]/input")

        username_field.send_keys("heliumedu-ci-selenium-test")
        email_field.send_keys(f'heliumedu-ci-test@{ENVIRONMENT_PREFIX}heliumedu.dev')
        password_field.send_keys("test_pass_1!")
        confirm_password_field.send_keys("test_pass_1!")
        terms_checkbox.click()

        login_button = self.driver.find_element(By.XPATH, "//*[@id=\"register-form\"]/div[2]/div/button")

        login_button.click()

        time.sleep(5)

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))

        success_status = self.driver.find_element(By.XPATH, "//*[@id=\"status\"]")
        self.assertTrue(success_status.isDisplayed())
        self.assertIn("The last step is to verify your email address.", success_status.text)

        # TODO: reuse Tavern script to find verification email, click link

    # TODO: add a test that logs in,

    # TODO: test logged in user has planner item on screen, checks reminder is on screen

    def test_2_delete_user(self):
        self.driver.get(os.path.join(self.app_host, 'settings'))

        password_field = self.driver.find_element(By.ID, "delete-account")
        password_field.send_keys("test_pass_1!")

        delete_button = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]")

        # TODO: this is a JS intercept, ensure it works with Chrome driver
        delete_button.click()

        time.sleep(5)

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))

        success_status = self.driver.find_element(By.XPATH, "//*[@id=\"status\"]")
        self.assertTrue(success_status.isDisplayed())
        self.assertIn("Sorry to see you go!", success_status.text)


if __name__ == '__main__':
    unittest.main()
