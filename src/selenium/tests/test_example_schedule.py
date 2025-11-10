__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.16.8"

import calendar
import datetime
import os

import pytz
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.selenium.seleniumtestcase import SeleniumTestCase
from src.utils.common import get_user_access_token


class TestSeleniumExampleSchedule(SeleniumTestCase):
    def test_example_schedule_populated_calendar_page_month_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Creative%20Writing%20%E2%9C%8D%EF%B8%8F'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        # Wait for month view to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 75
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//input[starts-with(@id, \"calendar-filter-course-\")]")) == 3
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//input[starts-with(@id, \"calendar-filter-category-\")]")) == 11
        )

        # Event
        event = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Study Session (Final, Programming)')]").find_element(
            By.XPATH, "..")
        self.assertEqual("Study Session (Final, Programming), 12:00 PM", event.text)

        # Class schedule
        intro_to_psych = (self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Intro to Psychology 🧠')]")[4]
                              .find_element(By.XPATH, ".."))
        self.assertEqual("Intro to Psychology 🧠, 1:00 PM", intro_to_psych.text)

        # Unchecked assignment, click to complete
        unchecked_assignment = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Short Stories 4')]").find_element(
            By.XPATH, "../..")
        unchecked_assignment_html = unchecked_assignment.get_attribute("innerHTML")
        self.assertTrue(unchecked_assignment_html.strip().startswith(
            '<span class="fc-title"><input id="calendar-homework-checkbox-'))
        self.assertTrue(unchecked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox"><span class="lbl" style="margin-top: -3px; margin-right: 3px;"></span><span class="fc-has-url">Short Stories 4</span>, 11:00 AM</span>'))
        unchecked_assignment.find_element(By.CSS_SELECTOR, "input").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: (
                self.driver.find_element(By.XPATH, "//s[contains(text(), 'Short Stories 4')]")
                .find_element(By.XPATH, "..").get_attribute("innerHTML")
            )
        )

        checked_assignment = self.driver.find_element(By.XPATH, "//s[contains(text(), 'Essay 5')]").find_element(
            By.XPATH, "../../..")
        checked_assignment_html = checked_assignment.get_attribute("innerHTML")
        self.assertTrue(
            checked_assignment_html.strip().startswith('<span class="fc-title"><input id="calendar-homework-checkbox-'))
        self.assertTrue(checked_assignment_html.endswith(
            'type="checkbox" class="ace calendar-homework-checkbox" checked="checked"><span class="lbl" style="margin-top: -3px; margin-right: 3px;"></span><span class="fc-has-url"><s>Essay 5</s></span>, 11:00 AM</span>'))

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_month_view_external_calendar(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 75
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
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[for='calendar-filter-homework']"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) == 0
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_assignments_list_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Creative%20Writing%20%E2%9C%8D%EF%B8%8F'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fc-assignmentsList-button"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="assignments-list-table_length"]'))
        )
        select = Select(self.driver.find_element(By.CSS_SELECTOR, 'select[name="assignments-list-table_length"]'))
        select.select_by_value("100")

        WebDriverWait(self.driver, 10).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 53
        )

        # No events are shown on assignments list view
        self.assertEqual(0, len(self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Study Session (Final, Programming)')]")))

        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[for='calendar-filter-complete']"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 35
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 53
        )

        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//label[starts-with(text(), ' Project')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 3
        )
        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//label[starts-with(text(), ' Quiz')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 16
        )
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 53
        )
        self.driver.find_element(By.ID, "calendar-search").send_keys("sTudy")
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 4
        )

        # TODO: assert on the table columns for the two items shown

        self.driver.find_element(By.ID, "calendar-search").clear()
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 53
        )
        self.driver.find_element(By.ID, "calendar-classes").click()

        # All courses are shown by default, so click to disable one (thus filtering it out)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//label[starts-with(@for, \"calendar-filter-course-\")]"))
        )[0].click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 16
        )
        # Filter further to only show the non-excluded homework that is completed
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[for='calendar-filter-complete']"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"homework-table-row-\")]")) == 11
        )

        # Reset class filters
        self.driver.find_element(By.ID, "calendar-classes").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//label[starts-with(@for, \"calendar-filter-course-\")]"))
        )[0].click()

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_populated_calendar_page_agenda_view(self):
        self.given_user_is_authenticated()
        access_token = get_user_access_token(self.api_host, self.test_username, self.test_password).json()['access']
        course = requests.get('{}/planner/courses/?title=Creative%20Writing%20%E2%9C%8D%EF%B8%8F'.format(self.api_host),
                              headers={'Authorization': "Bearer " + access_token},
                              verify=False).json()[0]
        homework = requests.get('{}/planner/homework/?title=Quiz%201'.format(self.api_host),
                                headers={'Authorization': "Bearer " + access_token},
                                verify=False).json()[0]
        self.given_homework_incomplete(access_token, course["course_group"], course["id"], homework["id"])

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        # Change to agenda (week) view
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fc-listWeek-button"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fc-list-heading"))
        )

        target_timezone = pytz.timezone('America/Chicago')
        utc_now = pytz.utc.localize(datetime.datetime.now())
        local_today = utc_now.astimezone(target_timezone).date()

        calendar.setfirstweekday(calendar.SUNDAY)
        month_calendar = calendar.monthcalendar(local_today.year, local_today.month)

        desired_week = month_calendar[1]

        day = local_today.day

        while day < desired_week[0]:
            self.driver.find_element(By.CSS_SELECTOR, ".fc-next-button").click()
            day += 7
        while day > desired_week[-1]:
            self.driver.find_element(By.CSS_SELECTOR, ".fc-prev-button").click()
            day -= 7

        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )

        # Filter dropdown visibility and action
        external_calendar_filter = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "calendar-filter-external"))
        )
        self.assertFalse(external_calendar_filter.is_displayed())
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[for='calendar-filter-events']"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 3
        )
        self.driver.find_element(By.CSS_SELECTOR, "[for='calendar-filter-homework']").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 10
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )
        self.driver.find_element(By.CSS_SELECTOR, "[for='calendar-filter-class']").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 8
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )
        self.driver.find_element(By.CSS_SELECTOR, "[for='calendar-filter-homework']").click()
        self.driver.find_element(By.CSS_SELECTOR, "[for='calendar-filter-complete']").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 6
        )

        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )
        self.driver.find_element(By.CSS_SELECTOR, "[for='calendar-filter-homework']").click()
        self.driver.find_element(By.ID, "calendar-filter-list").find_element(By.XPATH,
                                                                             "//label[starts-with(text(), ' Quiz')]").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 2
        )
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )
        self.driver.find_element(By.ID, "calendar-search").send_keys("sTudy")
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 1
        )

        self.driver.find_element(By.ID, "calendar-search").clear()
        self.driver.find_element(By.ID, "filter-clear").click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 18
        )
        self.driver.find_element(By.ID, "calendar-classes").click()
        # All courses are shown by default, so click to disable one (thus filtering it out)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[starts-with(@for, \"calendar-filter-course-\")]"))
        )[0].click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 8
        )
        # Filter further to only show the non-excluded courses assignments
        self.driver.find_element(By.ID, "calendar-filters").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[for='calendar-filter-homework']"))
        ).click()
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(
                self.driver.find_elements(By.XPATH,
                                          "//table[contains(@class, 'fc-list-table')]//tr[contains(@class, 'fc-list-item')]")) == 3
        )

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_calendar_assignment_tooltip(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) > 75
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
        self.assertIn("<strong>Info:</strong>", assignment_hover_html)
        self.assertIn("Intro to Psychology 🧠", assignment_hover_html)
        self.assertIn("Quiz 💡", assignment_hover_html)
        self.assertIn(" SOC 110", assignment_hover_html)
        self.assertIn("<strong>Materials:</strong>", assignment_hover_html)
        self.assertIn("Psychology, 14th Edition", assignment_hover_html)
        self.assertIn("<strong>Grade:</strong>", assignment_hover_html)
        self.assertIn("85%", assignment_hover_html)
        self.assertNotIn("Python", assignment_hover_html)
        self.assertNotIn("Bird", assignment_hover_html)

        self.save_screenshot()

        self.assert_no_console_errors()

    def test_example_schedule_calendar_event_tooltip(self):
        self.given_user_is_authenticated()

        self.driver.get(os.path.join(self.app_host, 'planner', 'calendar'))

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 75
        )

        actions = ActionChains(self.driver)

        event_to_hover = self.driver.find_element(By.XPATH,
                                                  "//span[contains(text(), 'Final Portfolio Writing Workshop')]").find_element(
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

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "getting-started-modal"))
        )
        self.driver.find_element(By.ID, "close-getting-started").click()

        # Wait for calendar to load with the populated example schedule
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.CSS_SELECTOR, "a.fc-event")) >= 75
        )

        actions = ActionChains(self.driver)

        class_to_hover = (self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Intro to Psychology 🧠')]")[4]
                          .find_element(By.XPATH, ".."))
        actions.move_to_element(class_to_hover).perform()
        qtip = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtip-bootstrap"))
        )
        class_hover_html = qtip.get_attribute("innerHTML")
        self.assertIn("<strong>When:</strong>", class_hover_html)
        self.assertIn(" at ", class_hover_html)
        self.assertIn("<strong>Info:</strong>", class_hover_html)
        self.assertIn(" SOC 110", class_hover_html)
        self.assertNotIn("Materials:", class_hover_html)
        self.assertNotIn("14th Edition", class_hover_html)
        self.assertNotIn("Bird", class_hover_html)
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
                # One group, one "create"
                self.driver.find_elements(By.CSS_SELECTOR, "ul#course-group-tabs > li")) == 2
        )
        WebDriverWait(self.driver, 15).until(
            lambda wait: len(self.driver.find_elements(By.XPATH, "//tr[starts-with(@id, \"course-\")]")) == 3
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
            lambda wait: len(self.driver.find_elements(By.XPATH, "//div[starts-with(@id, \"course-body-\")]")) == 3
        )

        self.save_screenshot()

        self.assert_no_console_errors()