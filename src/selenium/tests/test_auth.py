__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.12.4"

import os
import unittest
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumAuth(SeleniumTestCase):
    @unittest.skip("TODO: implement")
    def test_logout(self):
        self.driver.get(os.path.join(self.app_host, 'logout'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_forgot(self):
        self.driver.get(os.path.join(self.app_host, 'forgot'))

        self.assert_no_console_errors()

    def test_authenticated_login_redirects_calendar(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'login'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(os.path.join(self.app_host, 'planner', 'calendar'))
        )

        self.assert_no_console_errors()

    def test_authenticated_planner_base_redirects_to_calendar(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(os.path.join(self.app_host, 'planner', 'calendar'))
        )

        # TODO: this should be cleaned up to prevent the warning
        self.assert_no_console_errors(["Attempting to call a FullCalendar method on an element with no calendar."])

    def test_unauthenticated_planner_base_redirects(self):
        self.driver.get(os.path.join(self.app_host, 'planner'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(self.app_host)
        )
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('next', query_params)
        self.assertEqual('/planner/calendar', query_params['next'][0].rstrip("/"))

        self.assert_no_console_errors()
