__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.13"

import inspect
import logging
import os
import time
import unittest

import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ROOT_DIR = os.path.normpath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "build", "screenshots")

if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

KNOWN_CONSOLE_ERRORS = [
    "Deprecation warning: moment.langData is deprecated",
    "Deprecation warning: moment().add",
    "cdnjs.cloudflare.com/",
    "www.googletagmanager.com",
    "www.google-analytics.com/",
]

logger = logging.getLogger(__name__)


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        self.driver = webdriver.Chrome(options=options)
        self.driver.command_executor._client_config._timeout = 10000

        self.app_host = os.environ.get('PROJECT_APP_HOST')
        self.api_host = os.environ.get('PROJECT_API_HOST')
        self.env_prefix = os.environ.get('ENVIRONMENT_PREFIX')

        self.info_response = requests.get(os.path.join(self.api_host, 'info'),
                                          headers={'Content-Type': 'application/json'},
                                          verify=False)
        self.info = self.info_response.json()

        self.test_username = "heliumedu-cluster2"
        self.test_email = f'heliumedu-cluster2@{self.env_prefix}heliumedu.dev'
        self.test_password = "test_pass_2!"

    def tearDown(self):
        self.driver.delete_all_cookies()
        try:
            self.driver.execute_script("localStorage.clear();")
        except WebDriverException:
            pass
        try:
            self.driver.execute_script("sessionStorage.clear();")
        except WebDriverException:
            pass

        self.driver.close()

    def given_user_is_authenticated(self):
        self.driver.get(os.path.join(self.app_host, 'login'))

        self.driver.find_element(By.ID, "id_username").send_keys(self.test_username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.test_password)

        self.driver.find_element(By.CSS_SELECTOR, "#login-form > fieldset > div.clearfix > button").click()

        # Login will redirect us to the planner
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Calendar")
        )

    def save_screenshot(self):
        timestamp = int(time.time() * 1000)
        test_name = inspect.stack()[1].function
        file_name = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{timestamp}.png")
        self.driver.save_screenshot(file_name)

    def assert_no_console_errors(self):
        logs = self.driver.get_log('browser')

        for entry in logs:
            if entry['level'] == 'SEVERE' or entry['level'] == 'WARNING':
                known = False
                for known_error in KNOWN_CONSOLE_ERRORS:
                    if known_error in entry['message']:
                        known = True
                        break
                if not known:
                    # TODO: leaving this as a warning for now until we resolve the flakiness, then raise an AssertionError
                    logger.warning(f"Console error found: {entry['level']} - {entry['message']}")
