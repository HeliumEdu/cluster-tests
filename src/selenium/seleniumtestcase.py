__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.7.21"

import inspect
import os
import time
import unittest

import boto3
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.variablehelper import get_common_variables


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

        self.app_host = os.environ.get('PROJECT_APP_HOST')
        self.api_host = os.environ.get('PROJECT_API_HOST')

        self.test_username = "heliumedu-ci-test"
        self.test_email = get_common_variables(self.get_info())['test_email']
        self.test_password = "test_pass_1!"

    def tearDown(self):
        self.driver.close()

    def get_info(self):
        return requests.get(os.path.join(self.api_host, 'info'), headers={'Content-Type': 'application/json'},
                            verify=False)

    def given_user_is_authenticated(self):
        self.driver.get(os.path.join(self.app_host, 'login'))

        self.driver.find_element(By.ID, "id_username").send_keys(self.test_username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.test_password)

        self.driver.find_element(By.CSS_SELECTOR, "#login-form > fieldset > div.clearfix > button").click()

        # Login will redirect us to the planner
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Calendar")
        )

    def save_screenshot_to_s3(self):
        timestamp = int(time.time() * 1000)
        test_name = inspect.stack()[1].function
        file_name = f"{test_name}_{timestamp}.png"
        self.driver.save_screenshot(file_name)

        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.environ.get('CI_AWS_S3_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.environ.get('CI_AWS_S3_SECRET_ACCESS_KEY'),
                                 region_name=os.environ.get('AWS_REGION'))
        environment = os.environ.get('ENVIRONMENT')
        bucket_name = f'heliumedu.{environment}'
        s3_client.upload_file(file_name, bucket_name, file_name)
