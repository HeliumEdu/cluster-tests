__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.7.14"

import os

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumPages(SeleniumTestCase):
    def test_tour(self):
        info = self.get_info().json()

        self.driver.get(self.app_host)
        self.assertEqual("{} | {}".format(info['name'], info['tagline']), self.driver.title)

        # Assert carousel is rendering, data shown (ie. static resources are rendering)
        carousel_img = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tour-carousel > div > div:nth-child(1) > img"))
        )
        response = requests.get(carousel_img.get_attribute('src'),
                                verify=False)
        self.assertEqual(200, response.status_code)

    def test_docs(self):
        self.driver.get(os.path.join(self.api_host, 'docs'))
        self.assertEqual("Helium API Documentation", self.driver.title)

        # Assert static resources are rendering (ie. collectstatic has run, static resources can be rendered)
        head_resource_link = self.driver.find_element(By.CSS_SELECTOR, "head > link:nth-child(5)")
        response = requests.get(head_resource_link.get_attribute('href'),
                                verify=False)
        self.assertEqual(200, response.status_code)
