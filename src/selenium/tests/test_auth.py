__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import os
import unittest

from selenium.webdriver.common.by import By
from utils.seleniumtestcase import SeleniumTestCase

ENVIRONMENT = os.environ.get('ENVIRONMENT')
ENVIRONMENT_PREFIX = f'{ENVIRONMENT}.' if 'prod' not in ENVIRONMENT else ''


class TestSeleniumAuth(SeleniumTestCase):
    def test_register_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'register'))

        username_field = self.driver.find_element(By.ID, "id_username")
        email_field = self.driver.find_element(By.ID, "id_email")
        password_field = self.driver.find_element(By.ID, "id_password1")
        confirm_password_field = self.driver.find_element(By.ID, "id_password2")

        username_field.send_keys("heliumedu-ci-selenium-test")
        email_field.send_keys(f'heliumedu-ci-test@{ENVIRONMENT_PREFIX}heliumedu.dev')
        password_field.send_keys("test_pass_1!")
        confirm_password_field.send_keys("test_pass_1!")

        login_button = self.driver.find_element(By.XPATH, "//*[@id=\"register-form\"]/div[2]/div/button")

        login_button.click()

        self.driver.quit()

    def test_delete_user(self):
        self.driver.get(os.path.join(self.app_host, 'settings'))

        password_field = self.driver.find_element(By.ID, "delete-account")
        password_field.send_keys("test_pass_1!")

        delete_button = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]")

        delete_button.click()

        self.driver.quit()

    # TODO: add a test that logs in / logs out
    # TODO: add a test that ensures that /planner/calendar renders the example schedule


if __name__ == '__main__':
    unittest.main()
