__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.61"

import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumUnauthRedirects(SeleniumTestCase):
    def test_support_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'support'))
        # The /support URL redirects to support
        WebDriverWait(self.driver, 30).until(
            EC.url_matches("https://heliumedu.freshdesk.com/support/home")
        )

        self.save_screenshot()

    def test_contact_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'contact'))
        # The /contact URL redirects to support
        WebDriverWait(self.driver, 30).until(
            EC.url_matches("https://heliumedu.freshdesk.com/support/home")
        )

        self.save_screenshot()

    def test_docs_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'docs'))
        # The /docs URL redirects to the API /docs page
        WebDriverWait(self.driver, 30).until(
            EC.url_matches(os.path.join(self.api_host, 'docs'))
        )

        self.save_screenshot()

    def test_status_redirect(self):
        start_url = os.path.join(self.app_host, 'status')
        self.driver.get(start_url)
        # The /status URL redirects to the status page
        WebDriverWait(self.driver, 30).until(
            EC.url_matches("https://status.heliumedu.com")
        )

        self.save_screenshot()
