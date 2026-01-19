__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.17.73"

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
    CLASS_INTRO_TO_PSYCH_BADGE = '<span class="label label-sm title-label" style="background-color: #3033cf !important">Intro to Psychology 🧠</span>'
    CLASS_CREATIVE_WRITING_BADGE = '<span class="label label-sm title-label" style="background-color: #bd42a4 !important">Creative Writing ✍️</span>'
    CLASS_FUNDAMENTALS_OF_PROGRAMMING_BADGE = '<span class="label label-sm title-label" style="background-color: #05cc90 !important"><a href="https://automatetheboringstuff.com" target="_blank" class="planner-title-with-link">Fundamentals of Programming 💻 <i class="icon-external-link"></i></a></span>'
    MATERIAL_BIRD_BY_BIRD_BADGE = '<span class="label label-sm title-label" style="background-color: #dc7d50 !important;"><a href="https://www.amazon.com/Bird-Some-Instructions-Writing-Life/dp/0385480016" target="_blank" class="planner-title-with-link">Bird by Bird: Some Instructions on Writing and Life <i class="icon-external-link"></i></a></span>'
    MATERIAL_AUTOMATE_BORING_STUFF_BADGE = '<span class="label label-sm title-label" style="background-color: #dc7d50 !important;"><a href="https://automatetheboringstuff.com" target="_blank" class="planner-title-with-link">Automate the Boring Stuff with Python <i class="icon-external-link"></i></a></span>'
    MATERIAL_NOTEBOOK_BADGE = '<span class="label label-sm title-label" style="background-color: #dc7d50 !important;">Notebook 📓</span>'
    MATERIAL_GOOGLE_WORKSPACE_BADGE = '<span class="label label-sm title-label" style="background-color: #dc7d50 !important"><a href="https://workspace.google.com/" target="_blank" class="planner-title-with-link">Google Workspace (Docs, Drive) <i class="icon-external-link"></i></a></span>'
    MATERIAL_PSYCH_14TH_EDITION_BADGE = '<span class="label label-sm title-label" style="background-color: #dc7d50 !important"><a href="https://www.pearson.com/en-us/subject-catalog/p/psychology/P200000009860" target="_blank" class="planner-title-with-link">Psychology, 14th Edition <i class="icon-external-link"></i></a></span>'
    CATEGORY_INTRO_TO_PSYCH_CATEGORY_QUIZ_BADGE = '<span class="label label-sm" style="background-color: #5658d7 !important">Quiz 💡</span>'
    TERM_GRADE_BADGE = '<span class="badge" style="background-color: #9d629d !important">87.79%  <span class="icon-x arrow-up-icon light-green"></span></span>'
    INTRO_TO_PSYCH_CLASS_GRADE_BADGE = '<span class="badge" style="background-color: #9d629d !important">84.97% <span class="icon-x arrow-up-icon light-green"></span></span>'
    INTRO_TO_PSYCH_CATEGORY_QUIZ_GRADE_BADGE = '<span class="badge" style="background-color: #9d629d !important">80.42% <span class="icon-x arrow-up-icon light-green"></span></span>'
    INTRO_TO_PSYCH_ASSIGNMENT_QUIZ3_GRADE_BADGE = '<span class="badge" style="background-color: #9d629d !important">85%</span>'

    def setUp(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
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
            '{}/planner/coursegroups/{}/courses/{}/homework/{}/?title=Short%20Stories%204'.format(self.api_host,
                                                                                                  course_group_id,
                                                                                                  course_id,
                                                                                                  homework_id),
            headers={'Authorization': "Bearer " + access_token},
            data={"completed": False},
            verify=False)

    def save_screenshot(self, suffix=''):
        timestamp = int(time.time() * 1000)
        test_name = inspect.stack()[1].function
        file_name = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{timestamp}{suffix}.png")
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
