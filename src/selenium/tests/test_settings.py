__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import os
import unittest
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumSettings(SeleniumTestCase):
    def test_unauthenticated_settings_redirects(self):
        self.driver.get(os.path.join(self.app_host, 'settings'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(self.app_host)
        )
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('next', query_params)
        self.assertEqual('/settings', query_params['next'][0].rstrip("/"))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_change_preferences(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_change_phone_number(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_change_username(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_change_email(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_change_password(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_disable_enable_private_feeds(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        # TODO: assert that the feed no longer works once disabled

        # TODO: assert that the feed URIs are accessible and return valid data again

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_import_schedule(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_export_schedule(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_add_external_calendar(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_external_calendar(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'settings'))

        self.assert_no_console_errors()
