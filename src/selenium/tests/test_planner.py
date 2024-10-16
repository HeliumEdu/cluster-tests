__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.seleniumtestcase import SeleniumTestCase


class TestSeleniumAuth(SeleniumTestCase):
    def test_example_schedule_populated_calendar_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Getting started shouldn't show since we ticked box on last login
        WebDriverWait(self.driver, 5).until_not(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        # Wait for calendar to load
        event_selector = "div.fc-event"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, event_selector))
        )

        # Expect the example schedule on the page
        self.assertEqual(45, len(self.driver.find_elements(By.CSS_SELECTOR, event_selector)))
        classes_filter_button = self.driver.find_element(By.ID, "calendar-classes")
        classes_filter_button.click()
        self.assertEqual(2, len(self.driver.find_elements(By.XPATH,
                                                          "//li[starts-with(@id, \"calendar-filter-course-\")]")))
        filter_button = self.driver.find_element(By.ID, "calendar-filters")
        filter_button.click()
        self.assertEqual(8, len(self.driver.find_elements(By.XPATH,
                                                          "//li[starts-with(@id, \"calendar-filter-category-\")]")))

    def test_example_schedule_populated_classes_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'classes'))

        # Wait for classes to load
        course_group_title_starts_with_selector = "//span[starts-with(@id, \"course-group-title-\")]"
        course_group_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, course_group_title_starts_with_selector))
        )

        # Expect the example schedule on the page
        self.assertEqual(course_group_title.text, "Example Semester")
        self.assertEqual(1, len(self.driver.find_elements(By.XPATH, course_group_title_starts_with_selector)))
        self.assertEqual(1,
                         len(self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li:not(.hidden-xs)")))
        self.assertEqual(2, len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"course-\")]")))

    def test_example_schedule_populated_materials_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'materials'))

        # Wait for materials to load
        material_group_title_starts_with_selector = "//span[starts-with(@id, \"material-group-title-\")]"
        material_group_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, material_group_title_starts_with_selector))
        )

        # Expect the example schedule on the page
        self.assertEqual(material_group_title.text, "Example Textbooks")
        self.assertEqual(2, len(self.driver.find_elements(By.XPATH, material_group_title_starts_with_selector)))
        self.assertEqual(2,
                         len(self.driver.find_elements(By.CSS_SELECTOR, "ul#material-group-tabs > li:not(.hidden-xs)")))
        self.assertEqual(4, len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"material-\")]")))

    def test_example_schedule_populated_grades_page(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'grades'))

        # Wait for grades to load
        course_group_container_starts_with_selector = "//div[starts-with(@id, \"course-group-container-\")]"
        course_group_container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, course_group_container_starts_with_selector))
        )

        course_body_div_starts_with_selector = "//div[starts-with(@id, \"course-body-\")]"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, course_body_div_starts_with_selector))
        )

        # Expect the example schedule on the page
        self.assertEqual(course_group_container.find_element(By.CSS_SELECTOR, "h4").text, "Grades for Example Semester")
        self.assertEqual(1, len(self.driver.find_elements(By.XPATH, course_group_container_starts_with_selector)))
        self.assertEqual(1, len(self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li")))
        self.assertEqual(2, len(self.driver.find_elements(By.XPATH, course_body_div_starts_with_selector)))
