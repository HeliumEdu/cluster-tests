__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.12.29"

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
    "cdnjs.cloudflare.com/",
    "www.googletagmanager.com",
    "www.google-analytics.com/",
]

logger = logging.getLogger(__name__)


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        options = Options()
        # options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
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

        self.test_username = "heliumedu-cluster-2"
        self.test_email = f'heliumedu-cluster+2@{self.env_prefix}heliumedu.dev'
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

    def given_homework_incomplete(self, access_token, course_group_id, course_id, homework_id):
        requests.patch(
            '{}/planner/coursegroups/{}/courses/{}/homework/{}/?title=Quiz%201'.format(self.api_host,
                                                                                       course_group_id,
                                                                                       course_id,
                                                                                       homework_id),
            headers={'Authorization': "Bearer " + access_token},
            data={"completed": False},
            verify=False)

    def save_screenshot(self):
        timestamp = int(time.time() * 1000)
        test_name = inspect.stack()[1].function
        file_name = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{timestamp}.png")
        self.driver.save_screenshot(file_name)

    def assert_no_console_errors(self, test_ignore_errors=None):
        if not test_ignore_errors:
            test_ignore_errors = []
        test_ignore_errors += KNOWN_CONSOLE_ERRORS

        logs = self.driver.get_log('browser')

        for entry in logs:
            if entry['level'] == 'SEVERE' or entry['level'] == 'WARNING':
                known = False
                for known_error in test_ignore_errors:
                    if known_error in entry['message']:
                        known = True
                        break
                if not known:
                    raise AssertionError(f"Console error found: {entry['level']} - {entry['message']}")
                else:
                    logger.warning(f"Known console issue found: {entry['level']} - {entry['message']}")
