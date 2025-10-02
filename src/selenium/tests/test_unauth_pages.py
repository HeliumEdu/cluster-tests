__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumUnauthPages(SeleniumTestCase):
    def test_index(self):
        self.driver.get(self.app_host)
        self.assertEqual("{} | {}".format(self.info['name'], self.info['tagline']), self.driver.title)

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tour-carousel > div > div:nth-child(1) > img"))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_about(self):
        self.driver.get(os.path.join(self.app_host, 'about'))
        self.assertEqual("{} | {}".format(self.info['name'], 'About'), self.driver.title)

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a[href=\"https://www.patreon.com/alexdlaird\"] img"))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_press(self):
        self.driver.get(os.path.join(self.app_host, 'press'))
        self.assertEqual("{} | {}".format(self.info['name'], 'Press'), self.driver.title)

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a[href=\"https://www.patreon.com/alexdlaird\"] img"))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_privacy(self):
        self.driver.get(os.path.join(self.app_host, 'privacy'))

        self.assertEqual("{} | {}".format(self.info['name'], 'Privacy Policy'), self.driver.title)

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a[href=\"https://www.patreon.com/alexdlaird\"] img"))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_terms(self):
        self.driver.get(os.path.join(self.app_host, 'terms'))

        self.assertEqual("{} | {}".format(self.info['name'], 'Terms of Service'), self.driver.title)

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "a[href=\"https://www.patreon.com/alexdlaird\"] img"))
        )

        self.save_screenshot()

        # TODO: investigate the jQuery UI exception on this page (which shouldn't even be being used here)
        self.assert_no_console_errors()
