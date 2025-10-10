__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.12.2"

import os

import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase
from src.utils.common import get_user_access_token


class TestSeleniumExampleSchedule(SeleniumTestCase):
    def test_example_schedule_populated_calendar_page_month_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Computer%20Science%20%F0%9F%92%BB'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Getting started shouldn't show since we ticked box on last login
        WebDriverWait(self.driver, 5).until_not(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )

        # Wait for month view to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 40
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-course-\")]")) == 2
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//li[starts-with(@id, \"calendar-filter-category-\")]")) == 9
        )

        # Event
        event = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Meeting with John')]").find_element(
            By.XPATH, "..")
        self.assertEqual("Meeting with John, 12:00 PM", event.text)

        # Class schedule
        world_history_time = (self.driver.find_elements(By.XPATH, "//span[contains(text(), 'World History 🌎')]")[4]
                              .find_element(By.XPATH, ".."))
        self.assertEqual("World History 🌎, 7:00 PM", world_history_time.text)

        # Unchecked assignment, click to complete
        unchecked_assignment = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Quiz 1')]").find_element(
            By.XPATH, "..")
        unchecked_assignment_html = unchecked_assignment.get_attribute("innerHTML")
        self.assertTrue(unchecked_assignment_html.strip().startswith(
            '<span class="fc-title"><input id="calendar-homework-checkbox-'))
        self.assertTrue(unchecked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox"><span class="lbl" style="margin-top: -3px; margin-right: 3px;"></span>Quiz 1, 11:00 AM</span>'))
        unchecked_assignment.find_element(By.CSS_SELECTOR, "input").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: (
                self.driver.find_element(By.XPATH, "//s[contains(text(), 'Quiz 1')]")
                .find_element(By.XPATH, "..").get_attribute("innerHTML")
            )
        )

        checked_assignment = self.driver.find_element(By.XPATH, "//s[contains(text(), 'Quiz 3')]").find_element(
            By.XPATH, "../..")
        checked_assignment_html = checked_assignment.get_attribute("innerHTML")
        self.assertTrue(
            checked_assignment_html.strip().startswith('<span class="fc-title"><input id="calendar-homework-checkbox-'))
        self.assertTrue(checked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox" checked="checked"><span class="lbl" style="margin-top: -3px; margin-right: 3px;"></span><s>Quiz 3</s>, 2:00 PM</span>'))

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_month_view_external_calendar(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 40
        )

        found = False
        while not found:
            date = self.driver.find_element(By.CSS_SELECTOR, ".fc-left h2").text
            self.driver.find_element(By.CSS_SELECTOR, ".fc-prev-button").click()

            WebDriverWait(self.driver, 15).until(
                lambda wait: self.driver.find_element(By.CSS_SELECTOR, ".fc-left h2").text != date
            )

            if self.driver.find_element(By.CSS_SELECTOR, ".fc-left h2").text == "October 2023":
                found = True

        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) == 2
        )

        external_calendar_item = self.driver.find_element(By.XPATH,
                                                          "//span[contains(text(), 'Some Timed Event at 9am CT Inside DST')]")
        self.assertEqual("Some Timed Event at 9am CT Inside DST, 9:00 AM", external_calendar_item.text)

        # Filter to just homework, and the item should disappear
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-homework"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) == 0
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_assignments_list_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Computer%20Science%20%F0%9F%92%BB'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Change to assignments list view, where "Create Homework" button is visible
        self.driver.find_element(By.CSS_SELECTOR, ".fc-assignmentsList-button").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "create-homework")) and
            EC.visibility_of_element_located((By.XPATH, "//td[text()='Chapter 1 Reading']"))
        )

        # Ensure all homework shown
        self.assertEqual(22,
                         len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")))

        # No events are shown on assignments list view
        self.assertEqual(0, len(self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Meeting with John')]")))

        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-complete"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 17
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 22
        )

        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//span[starts-with(text(), 'Project')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 2
        )
        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//span[starts-with(text(), 'Quiz')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 9
        )
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 22
        )
        self.driver.find_element(By.ID, "calendar-search").send_keys("CHApTER 4")
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 2
        )

        # TODO: assert on the table columns for the two items shown

        self.driver.find_element(By.ID, "calendar-search").clear()
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 22
        )
        self.driver.find_element(By.ID, "calendar-classes").click()

        # All courses are shown by default, so click to disable one (thus filtering it out)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[starts-with(@id, \"calendar-filter-course-\")]"))
        )[0].click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 7
        )
        # Filter further to only show the non-excluded homework that is completed
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-complete"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 6
        )

        # Reset class filters
        self.driver.find_element(By.ID, "calendar-classes").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[starts-with(@id, \"calendar-filter-course-\")]"))
        )[0].click()

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_agenda_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Computer%20Science%20%F0%9F%92%BB'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Change to agenda (week) view
        self.driver.find_element(By.CSS_SELECTOR, ".fc-listWeek-button").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fc-list-heading"))
        )

        # TODO: make this robust to always find the third week in the month
        self.driver.find_element(By.CSS_SELECTOR, ".fc-next-button").click()

        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )

        # Filter dropdown visibility and action
        external_calendar_filter = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "calendar-filter-external"))
        )
        self.assertFalse(external_calendar_filter.is_displayed())
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-events"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 1
        )
        self.driver.find_element(By.ID, "calendar-filter-homework").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 8
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )
        self.driver.find_element(By.ID, "calendar-filter-class").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 5
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )
        self.driver.find_element(By.ID, "calendar-filter-homework").click()
        self.driver.find_element(By.ID, "calendar-filter-complete").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 2
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )
        self.driver.find_element(By.ID, "calendar-filter-homework").click()
        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//span[starts-with(text(), 'Quiz')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 2
        )
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )
        self.driver.find_element(By.ID, "calendar-search").send_keys("CHApTER 1")
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 2
        )

        self.driver.find_element(By.ID, "calendar-search").clear()
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 13
        )
        self.driver.find_element(By.ID, "calendar-classes").click()
        # All courses are shown by default, so click to disable one (thus filtering it out)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[starts-with(@id, \"calendar-filter-course-\")]"))
        )[0].click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 5
        )
        # Filter further to only show the non-excluded courses assignments
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calendar-filter-homework"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 2
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_calendar_assignment_tooltip(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 40
        )

        actions = ActionChains(self.driver)

        assignment_to_hover = self.driver.find_element(By.XPATH, "//s[contains(text(), 'Quiz 3')]").find_element(
            By.XPATH, "../..")
        actions.move_to_element(assignment_to_hover).perform()
        qtip = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtip-bootstrap"))
        )
        assignment_hover_html = qtip.get_attribute("innerHTML")
        self.assertIn("<strong>When:</strong>", assignment_hover_html)
        self.assertIn(" at ", assignment_hover_html)
        self.assertIn("<strong>Class Info:</strong>", assignment_hover_html)
        self.assertIn("World History 🌎", assignment_hover_html)
        self.assertIn("Quiz 📈", assignment_hover_html)
        self.assertIn(" HSC 405", assignment_hover_html)
        self.assertIn("<strong>Materials:</strong>", assignment_hover_html)
        self.assertIn("Sapiens: A Brief History of Humankind", assignment_hover_html)
        self.assertIn("<strong>Grade:</strong>", assignment_hover_html)
        self.assertIn("90%", assignment_hover_html)
        self.assertNotIn("Python", assignment_hover_html)
        self.assertNotIn("Civilizations", assignment_hover_html)

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_calendar_event_tooltip(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 40
        )

        actions = ActionChains(self.driver)

        event_to_hover = self.driver.find_element(By.XPATH,
                                                  "//span[contains(text(), 'Meeting with John')]").find_element(
            By.XPATH, "..")
        actions.move_to_element(event_to_hover).perform()
        qtip = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtip-bootstrap"))
        )
        event_hover_html = qtip.get_attribute("innerHTML")
        self.assertIn("<strong>When:</strong>", event_hover_html)
        self.assertIn(" to ", event_hover_html)
        self.assertNotIn("Class", event_hover_html)
        self.assertNotIn("Material", event_hover_html)
        self.assertNotIn("Grade", event_hover_html)

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_calendar_class_tooltip(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 40
        )

        actions = ActionChains(self.driver)

        class_to_hover = (self.driver.find_elements(By.XPATH, "//span[contains(text(), 'World History 🌎')]")[4]
                          .find_element(By.XPATH, ".."))
        actions.move_to_element(class_to_hover).perform()
        qtip = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtip-bootstrap"))
        )
        class_hover_html = qtip.get_attribute("innerHTML")
        self.assertIn("<strong>When:</strong>", class_hover_html)
        self.assertIn(" at ", class_hover_html)
        self.assertIn("<strong>Class Info:</strong>", class_hover_html)
        self.assertIn("World History 🌎", class_hover_html)
        self.assertIn(" HSC 405", class_hover_html)
        self.assertIn("<strong>Materials:</strong>", class_hover_html)
        self.assertIn("Sapiens: A Brief History of Humankind", class_hover_html)
        self.assertIn("Civilizations Past and Present, Combined Volume, 13th edition", class_hover_html)
        self.assertNotIn("Python", class_hover_html)
        self.assertNotIn("Grade", class_hover_html)

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
