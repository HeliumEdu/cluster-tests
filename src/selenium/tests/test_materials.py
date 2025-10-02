__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.37"

import os
import unittest
from urllib.parse import urlparse, parse_qs

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
        self.assertEqual('/planner/materials', query_params['next'][0])

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
