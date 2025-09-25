__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.13"

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase


class TestSeleniumExampleSchedule(SeleniumTestCase):
    def test_example_schedule_populated_calendar_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Getting started shouldn't show since we ticked box on last login
        WebDriverWait(self.driver, 5).until_not(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        # Wait for calendar to load, awaiting example schedule display
        WebDriverWait(self.driver, 30).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "div.fc-event")) >= 40
        )
        WebDriverWait(self.driver, 30).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-course-\")]")) == 2
        )
        WebDriverWait(self.driver, 30).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-category-\")]")) == 9
        )

        # TODO: assert that elements of class schedule are displayed
        # TODO: assert that a homework is displayed
        # TODO: assert that an event is displayed

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_classes_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        # Wait for classes to load, awaiting example schedule display
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//span[starts-with(@id, \"course-group-title-\")]")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li:not(.hidden-xs)")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"course-\")]")) == 2
        )

        # TODO: assert that elements of class are displayed

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_materials_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'materials'))

        # Wait for materials to load, awaiting example schedule display
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//span[starts-with(@id, \"material-group-title-\")]")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.CSS_SELECTOR, "ul#material-group-tabs > li:not(.hidden-xs)")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"material-\")]")) == 4
        )

        # TODO: assert that elements of material are displayed

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_grades_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'grades'))

        # Wait for grades to load, awaiting example schedule display
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//div[starts-with(@id, \"course-group-container-\")]")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li")) == 1
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//div[starts-with(@id, \"course-body-\")]")) == 2
        )

        self.save_screenshot()

        self.assert_no_console_errors()
