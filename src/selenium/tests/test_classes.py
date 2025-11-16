__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.57"

import os
import unittest
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumClasses(SeleniumTestCase):
    def test_unauthenticated_classes_redirects(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(self.app_host)
        )
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('next', query_params)
        self.assertEqual('/planner/classes', query_params['next'][0].rstrip("/"))

        self.assert_no_console_errors()

    def test_example_schedule_populated_classes_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        # Wait for classes to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//span[starts-with(@id, \"course-group-title-\")]")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                # One group, one "create"
                self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li")) == 2
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"course-\")]")) == 3
        )

        # TODO: assert that elements of class are displayed

        self.save_screenshot()

        self.assert_no_console_errors()


    @unittest.skip("TODO: implement")
    def test_classes_click_class_populates_dialog(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_course_groups_click_populates_dialog(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_course_groups_create(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_classes_create_course_with_schedule_and_categories_and_attachment(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_course(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_course_group(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()
