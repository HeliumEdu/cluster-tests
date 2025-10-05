__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.57"

import datetime
import os

import pytz
import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase
from src.utils.emailhelper import get_verification_code
from src.utils.workspacehelper import init_workspace, wait_for_example_schedule, get_user_access_token


class TestSeleniumSetup(SeleniumTestCase):
    def test_1_register_new_user(self):
        init_workspace(self.info_response, self.api_host, self.test_username, self.test_password)

        self.driver.get(os.path.join(self.app_host, 'register'))

        time_zone_chosen = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_time_zone_chosen"))
        )

        username_field = self.driver.find_element(By.ID, "id_username")
        email_field = self.driver.find_element(By.ID, "id_email")
        password_field = self.driver.find_element(By.ID, "id_password1")
        confirm_password_field = self.driver.find_element(By.ID, "id_password2")
        terms_checkbox = self.driver.find_element(By.CSS_SELECTOR,
                                                  "#register-form > div:nth-child(1) > div > fieldset > label:nth-child(6) > input")

        username_field.send_keys(self.test_username)
        email_field.send_keys(self.test_email)
        password_field.send_keys(self.test_password)
        confirm_password_field.send_keys(self.test_password)

        time_zone_chosen.click()
        time_zone_chosen_search = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-search input"))
        )
        time_zone_chosen_search.send_keys("Chicago")
        time_zone_chosen_search.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="id_time_zone_chosen"]/a/span[text()="Chicago"]'))
        )

        terms_checkbox.click()

        login_button = self.driver.find_element(By.CSS_SELECTOR, "#register-form > div:nth-child(2) > div > button")
        login_button.click()

        # Registration will redirect us to the login page and await verification
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Login")
        )

        self.save_screenshot()

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))

        success_status = self.driver.find_element(By.CSS_SELECTOR, "#status")
        self.assertTrue(success_status.is_displayed())
        self.assertIn("The last step is to verify your email address.", success_status.text)

        email_verification_code = get_verification_code(self.info, self.test_username)[
            'email_verification_code']

        self.driver.get(os.path.join(self.app_host, "verify") +
                        f"?username={self.test_username}&code={email_verification_code}&welcome-email=false")

        # Verification will redirect us to the login page
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Login")
        )

        self.save_screenshot()

        self.assertEqual(os.path.join(self.app_host, 'login'), self.driver.current_url.strip('/'))
        success_status = self.driver.find_element(By.CSS_SELECTOR, "#status")
        self.assertTrue(success_status.is_displayed())
        self.assertIn("Your email address has been verified.", success_status.text)

        token_response = requests.post(f"{self.api_host}/auth/token/",
                                       data={"username": self.test_username, "password": self.test_password},
                                       verify=False)
        wait_for_example_schedule(token_response, self.api_host, token_response.json()["access"])

    def test_3_login_new_user(self):
        self.driver.get(os.path.join(self.app_host, 'login'))

        username_field = self.driver.find_element(By.ID, "id_username")
        password_field = self.driver.find_element(By.ID, "id_password")

        username_field.send_keys(self.test_username)
        password_field.send_keys(self.test_password)

        login_button = self.driver.find_element(By.CSS_SELECTOR, "#login-form > fieldset > div.clearfix > button")
        login_button.click()

        # Login will redirect us to the planner
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Calendar")
        )

        self.save_screenshot()

        self.assertEqual(os.path.join(self.app_host, 'planner', 'calendar'), self.driver.current_url.strip('/'))

        # Wait for calendar to load
        getting_started_modal = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        # Click this to fire request to not show it on next login
        show_getting_started_checkbox = self.driver.find_element(By.ID, "show-getting-started")
        show_getting_started_checkbox.click()

        close_getting_started_button = self.driver.find_element(By.ID, "close-getting-started")
        close_getting_started_button.click()

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element(getting_started_modal)
        )

    def test_4_create_external_calendar(self):
        response = get_user_access_token(self.api_host, self.test_username, self.test_password)

        response = requests.post('{}/feed/externalcalendars/'.format(self.api_host),
                                 headers={'Authorization': "Bearer " + response.json()['access']},
                                 data={'title': 'Helium Test Calendar',
                                       'url': 'https://calendar.google.com/calendar/ical/86c55b7d91f8d4c22ca722fe22ee19779774863c6e31b6b23346e475c44a23ad%40group.calendar.google.com/public/basic.ics',
                                       'shown_on_calendar': True},
                                 verify=False)

        self.assertEqual(201, response.status_code)

    def test_5_create_event(self):
        response = get_user_access_token(self.api_host, self.test_username, self.test_password)

        start = datetime.datetime.now(pytz.utc).replace(day=17, hour=18, minute=0, second=0)
        end = start + datetime.timedelta(hours=1)

        response = requests.post('{}/planner/events/'.format(self.api_host),
                                 headers={'Authorization': "Bearer " + response.json()['access']},
                                 data={'title': 'Meeting with John',
                                       'all_day': False,
                                       'show_end_time': True,
                                       'start': start.isoformat(),
                                       'end': end.isoformat(),
                                       'priority': 75,
                                       'comments': 'some comment',
                                       'owner_id': '12345'},
                                 verify=False)

        self.assertEqual(201, response.status_code)