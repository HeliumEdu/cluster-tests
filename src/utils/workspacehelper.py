import datetime
import time

import pytz
import requests
from dateutil import parser
from tavern.util.exceptions import TestFailError

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.18'


def init_workspace(response, env_api_host, username, email, password):
    # If the test user already exists, cleanup from a previous test
    response = requests.delete(env_api_host + '/auth/user/delete/',
                               data={'username': username, 'email': email, 'password': password},
                               verify=False)

    # If the user existed and was deleted, wait to ensure their data is fully deleted
    if response.status_code == 204:
        time.sleep(3)

    return {}


def wait_for_example_schedule(response, env_api_host, retry=0):
    token = response.json()['token']

    # It can take a few seconds for the example schedule to finish populating, so wait before wasting retries
    time.sleep(10)

    events_response = requests.get(env_api_host + '/planner/events/',
                                   headers={'Authorization': "Token " + token},
                                   verify=False)
    assert events_response.status_code == 200
    events = events_response.json()

    coursegroups_response = requests.get(env_api_host + '/planner/coursegroups/',
                                         headers={'Authorization': "Token " + token},
                                         verify=False)
    assert coursegroups_response.status_code == 200
    coursegroups = coursegroups_response.json()
    course_group = coursegroups[0]

    courses_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/'.format(course_group['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert courses_response.status_code == 200
    courses = courses_response.json()

    if len(events) != 3 or len(courses) != 2:
        if retry < 10:
            time.sleep(2)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was only populated with {} events and {} courses "
                "after {} retries.".format(retry, len(events), len(courses)))

    course = None
    for course in courses:
        if course['title'] == 'American History':
            course = course
            break
    assert course is not None

    categories_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/categories/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert categories_response.status_code == 200
    categories = categories_response.json()

    homework_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/homework/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert homework_response.status_code == 200
    homework = homework_response.json()

    if len(categories) != 5 or len(homework) != 15:
        if retry < 10:
            time.sleep(2)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was only populated with {} categories and {} homework "
                "after {} retries.".format(retry, len(categories), len(homework)))

    category = None
    for category in categories:
        if category['title'] == 'Writing Assignment':
            category = category
            break
    assert category is not None

    # Await grade accuracy if worker processing is slow
    if course_group['average_grade'] != '86.2108' or course_group['trend'] != -0.00092027674442886:
        if retry < 10:
            time.sleep(2)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's course group {} grades were not properly calculated "
                "after {} retries.".format(course_group, retry))

    if category['average_grade'] != '92.6667' or category['grade_by_weight'] != '18.5333' \
            or category['trend'] != 0.0383333333333334:
        if retry < 10:
            time.sleep(2)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's category {} grades were not properly calculated "
                "after {} retries.".format(category, retry))

    # Assert on a sampling to ensure the example schedule was "moved" into the current month
    now = datetime.datetime.now(pytz.utc)
    assert parser.parse(events[0]['start']).month == now.month
    assert parser.parse(course_group['start_date']).month == now.month
    assert parser.parse(courses[0]['start_date']).month == now.month
    assert parser.parse(courses[1]['start_date']).month == now.month
    assert parser.parse(homework[0]['start']).month == now.month

    return {}
