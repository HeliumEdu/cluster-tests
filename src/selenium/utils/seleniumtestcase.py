__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import os
import unittest

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

        self.app_host = os.environ.get('PROJECT_APP_HOST')
        self.api_host = os.environ.get('PROJECT_API_HOST')

    def tearDown(self):
        self.driver.close()

    def get_info(self):
        return requests.get(os.path.join(self.api_host, 'info'), headers={'Content-Type': 'application/json'},
                            verify=False).json()
