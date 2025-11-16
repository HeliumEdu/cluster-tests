__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.17.21"

import os
import unittest
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumMaterials(SeleniumTestCase):
    def test_unauthenticated_materials_redirects(self):
        self.driver.get(os.path.join(self.app_host, 'planner', 'materials'))

        WebDriverWait(self.driver, 30).until(
            EC.url_matches(self.app_host)
        )
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('next', query_params)
        self.assertEqual('/planner/materials', query_params['next'][0].rstrip("/"))

        self.assert_no_console_errors()

    def test_example_schedule_populated_materials_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'materials'))

        # Wait for materials to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//span[starts-with(@id, \"material-group-title-\")]")) == 3
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                # Two group, one "create"
                self.driver.find_elements(By.CSS_SELECTOR, "ul#material-group-tabs > li")) == 4
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"material-\")]")) == 5
        )

        # TODO: assert that elements of material are displayed

        self.save_screenshot()

        self.assert_no_console_errors()


    @unittest.skip("TODO: implement")
    def test_materials_click_material_populates_dialog(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_material_groups_click_populates_dialog(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_material_groups_create(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_materials_create_material(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_material(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()

    @unittest.skip("TODO: implement")
    def test_delete_material_group(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        self.assert_no_console_errors()
