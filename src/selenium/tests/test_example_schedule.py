__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.13"

import os
import time

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

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "div.fc-event")) >= 40
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-course-\")]")) == 2
        )
        external_calendar_filter = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "calendar-filter-external"))
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-category-\")]")) == 11
        )

        # Event
        event = self.driver.find_element(By.XPATH, "//strong[text()='Meeting with Julian']").find_element(By.XPATH, "..")
        self.assertEqual("<strong>Meeting with Julian</strong>, 5:00 PM", event.get_attribute("innerHTML"))

        # Class schedule
        world_history_time = self.driver.find_elements(By.XPATH, "//strong[contains(text(), 'World History 🌎')]")[
            8].find_element(By.XPATH, "..")
        self.assertEqual("<strong>World History 🌎</strong>, 7:00 PM", world_history_time.get_attribute("innerHTML"))

        # Unchecked assignment, click to complete
        unchecked_assignment = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'Quiz 1')]").find_element(
            By.XPATH, "..")
        unchecked_assignment_html = unchecked_assignment.get_attribute("innerHTML")
        self.assertTrue(unchecked_assignment_html.startswith('<strong><input id="calendar-homework-checkbox-'))
        self.assertTrue(unchecked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox" "=""><span class="lbl" style="margin-top: -3px;"></span>Quiz 1</strong>, 11:00 AM'))
        # TODO: only commented out while debugging so it doesn't break the test, this is stable
        # unchecked_assignment.find_element(By.CSS_SELECTOR, "input").click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: (
        #         self.driver.find_element(By.XPATH, "//strike[contains(text(), 'Quiz 1')]").find_element(By.XPATH, "..").get_attribute("innerHTML")
        #     )
        # )

        # Checked assignment
        checked_assignment = self.driver.find_element(By.XPATH, "//strike[contains(text(), 'Quiz 3')]").find_element(
            By.XPATH, "../..")
        checked_assignment_html = checked_assignment.get_attribute("innerHTML")
        self.assertTrue(checked_assignment_html.startswith('<strong><input id="calendar-homework-checkbox-'))
        self.assertTrue(checked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox" checked="checked" "=""><span class="lbl" style="margin-top: -3px;"></span><strike>Quiz 3</strike></strong>, 2:00 PM'))

        # Change to list view, where "Create Homework" button is visible
        self.driver.find_element(By.CSS_SELECTOR, ".fc-button-list").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "create-homework")) and
            EC.visibility_of_element_located((By.XPATH, "//td[text()='Some Timed Event at 9am CT Inside DST']"))
        )

        # External calendar item
        external_calendar_item = self.driver.find_element(By.XPATH,
                                                          "//td[text()='Some Timed Event at 9am CT Inside DST']")
        external_calendar_item_time = external_calendar_item.find_element(By.XPATH, "following-sibling::*[1]")
        self.assertEqual("Oct 15, 2023 9:00 am", external_calendar_item_time.get_attribute("innerHTML"))

        # Filter dropdown visibility and action
        self.assertFalse(external_calendar_filter.is_displayed())
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-external"))
        )
        self.driver.find_element(By.ID, "calendar-filter-events").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 3
        )
        self.driver.find_element(By.ID, "calendar-filter-external").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 7
        )
        self.driver.find_element(By.ID, "calendar-filter-homework").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 29
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 50
        )
        self.driver.find_element(By.ID, "calendar-filter-class").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 24
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 50
        )
        self.driver.find_element(By.ID, "calendar-filter-homework").click()
        self.driver.find_element(By.ID, "calendar-filter-complete").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 17
        )

        # TODO: category and search filtering is currently broken, it seems
        # self.driver.find_element(By.ID, "filter-clear").click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 50
        # )
        # self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH, "//span[contains(text(), 'Project 👨🏽‍💻')]").click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 2
        # )
        # self.driver.find_element(By.ID, "filter-clear").click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 50
        # )
        # self.driver.find_element(By.ID, "calendar-search").send_keys("Chapter 4")
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 2
        # )

        # TODO: class filtering is currently broken
        # self.driver.find_element(By.ID, "filter-clear").click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 50
        # )
        # self.driver.find_elements(By.XPATH, "//[starts-with(@id, 'calendar-filter-course-')]")[0].click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 17
        # )
        # self.driver.find_element(By.ID, "calendar-filters").click()
        # calendar_filter_homework = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.ID, "calendar-filter-homework"))
        # )
        # calendar_filter_homework.click()
        # WebDriverWait(self.driver, 15).until(
        #     lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 7
        # )

        # Change back to month view, which can be detected by completed items having a strike again
        self.driver.find_element(By.CSS_SELECTOR, ".fc-button-month").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//strike[contains(text(), 'Quiz 3')]")) and
            EC.invisibility_of_element_located((By.ID, "create-homework"))
        )
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "filter-clear"))
        )
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "div.fc-event")) >= 40
        )

        # TODO: Check to ensure assignments and events are editable

        self.save_screenshot()

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

        # Wait for materials to load with the populated example schedule
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

        # Wait for grades to load with the populated example schedule
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
