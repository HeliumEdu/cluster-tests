__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.1"

import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumUnauthRedirects(SeleniumTestCase):
    def test_tour_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'tour'))
        # The /tour URL redirects to the index
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(self.app_host)
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_support_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'support'))
        # The /support URL redirects to an external portal
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(self.info['support_url'])
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_contact_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'contact'))
        # The /support URL redirects to an external portal
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(self.info['support_url'])
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_docs_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'docs'))
        # The /docs URL redirects to the API /docs page
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(os.path.join(self.api_host, 'docs'))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_status_redirect(self):
        start_url = os.path.join(self.app_host, 'status')
        self.driver.get(start_url)
        # The /status URL redirects to the API /status page
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(os.path.join(self.api_host, 'status'))
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_admin_redirect(self):
        start_url = os.path.join(self.app_host, 'admin')
        self.driver.get(start_url)
        # The /admin URL redirects to the API /admin page
        WebDriverWait(self.driver, 10).until(
            EC.url_matches(os.path.join(self.api_host, 'admin'))
        )

        self.save_screenshot()

        self.assert_no_console_errors()
