__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.41"

import os
import unittest
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumCalendar(SeleniumTestCase):
    def test_unauthenticated_calendar_redirects(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(self.app_host)
        )
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('next', query_params)
        self.assertEqual('/planner/calendar', query_params['next'][0].rstrip("/"))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_change_view_backend_responds(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # TODO: include changing the month / week

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_check_completed(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_click_event_populates_dialog(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_create_homework_with_reminder_and_attachment_dismiss_reminder(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_search_box(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_toggle_classes(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_calendar_toggle_filters(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_external_calendar_events_are_displayed(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_dismiss_popup_reminder(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_homework(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_event(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_hidden_course_group_not_shown(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_hidden_material_group_not_shown(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        self.assert_no_console_errors()
