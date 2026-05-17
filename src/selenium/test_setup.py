__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.17.85"

import os

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase
from src.utils.workspacehelper import init_workspace, wait_for_example_schedule, get_user_access_token


class TestSeleniumSetup(SeleniumTestCase):
    def test_1_provision_user(self):
        # Registration is no longer driven through the legacy frontend; provision the test
        # user directly through the API and verify the seeded example schedule is in place.
        token_response = init_workspace(self.info_response, self.api_host,
                                        self.test_username, self.test_email, self.test_password)

        self.assertEqual(200, token_response.status_code,
                         f"Login failed after provisioning user: {token_response.status_code} {token_response.text}")

        wait_for_example_schedule(token_response, self.api_host, token_response.json()["access"])

    def test_2_login_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'login'))

        username_field = self.driver.find_element(By.ID, "id_username")
        password_field = self.driver.find_element(By.ID, "id_password")

        username_field.send_keys(self.test_username)
        password_field.send_keys(self.test_password)

        login_button = self.driver.find_element(By.CSS_SELECTOR, "#login-form > fieldset > div.clearfix > button")
        login_button.click()

        # Login will redirect us to the planner
        WebDriverWait(self.driver, 30).until(
            EC.title_contains("Calendar")
        )

        self.save_screenshot()

        self.assertEqual(os.path.join(self.app_host, 'planner', 'calendar'), self.driver.current_url.strip('/'))

        # Wait for calendar to load
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

    def test_3_settings_disable_calendar_event_limit(self):
        response = get_user_access_token(self.api_host, self.test_username, self.test_password)

        response = requests.put('{}/auth/user/settings/'.format(self.api_host),
                                headers={'Authorization': "Bearer " + response.json()['access']},
                                data={'calendar_event_limit': False,
                                      'default_view': 0},  # Month view (tests expect this)
                                verify=False)

        self.assertEqual(200, response.status_code)

    def test_4_create_external_calendar(self):
        response = get_user_access_token(self.api_host, self.test_username, self.test_password)

        response = requests.post('{}/feed/externalcalendars/'.format(self.api_host),
                                 headers={'Authorization': "Bearer " + response.json()['access']},
                                 data={'title': 'Helium Test Calendar',
                                       'url': 'https://calendar.google.com/calendar/ical/86c55b7d91f8d4c22ca722fe22ee19779774863c6e31b6b23346e475c44a23ad%40group.calendar.google.com/public/basic.ics',
                                       'shown_on_calendar': True},
                                 verify=False)

        self.assertEqual(201, response.status_code)
