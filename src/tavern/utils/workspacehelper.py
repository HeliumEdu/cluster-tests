__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.7.13"

import datetime
import logging
import os
import pytz
import requests
import time
from dateutil import parser
from tavern._core.exceptions import TestFailError

# These are imported as a smoke test validation of dependencies

logger = logging.getLogger(__name__)

_RETRIES = 10

_RETRY_DELAY = 2

ENVIRONMENT = os.environ.get('ENVIRONMENT')
ENVIRONMENT_PREFIX = f'{ENVIRONMENT}.' if 'prod' not in ENVIRONMENT else ''


def get_contact_email(response):
    response = {'contact_email': f'contact@{ENVIRONMENT_PREFIX}heliumedu.com'}
    logger.info(response)

    return response


def get_ci_email(response):
    response = {'test_email': f'heliumedu-ci-test@{ENVIRONMENT_PREFIX}heliumedu.dev'}
    logger.info(response)

    return response


def init_workspace(response, env_api_host, username, email, password):
    logger.info('/info/ response: {}'.format(response.json()))

    # If the test user already exists, cleanup from a previous test
    response = requests.delete(env_api_host + '/auth/user/delete/',
                               data={'username': username, 'email': email, 'password': password},
                               verify=False)

    # If the user existed and was deleted, wait to ensure their data is fully deleted
    if response.status_code == 204:
        time.sleep(3)

    return {}


def wait_for_example_schedule(response, env_api_host, retry=0):
    logger.info('/auth/token/ response: {}'.format(response.json()))

    token = response.json()['token']

    # It can take a few seconds for the example schedule to finish populating, so wait before wasting retries
    time.sleep(10)

    events_response = requests.get(env_api_host + '/planner/events/',
                                   headers={'Authorization': "Token " + token},
                                   verify=False)
    if events_response.status_code != 200:
        raise AssertionError("events_response.status_code: {}".format(events_response.status_code))
    events = events_response.json()

    coursegroups_response = requests.get(env_api_host + '/planner/coursegroups/',
                                         headers={'Authorization': "Token " + token},
                                         verify=False)
    if coursegroups_response.status_code != 200:
        raise AssertionError("coursegroups_response.status_code: {}".format(coursegroups_response.status_code))
    coursegroups = coursegroups_response.json()
    course_group = coursegroups[0]

    courses_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/'.format(course_group['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    if courses_response.status_code != 200:
        raise AssertionError("courses_response.status_code: {}".format(courses_response.status_code))
    courses = courses_response.json()

    if len(events) != 3 or len(courses) != 2:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

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
    if course is None:
        raise AssertionError("course is None")

    categories_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/categories/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    if categories_response.status_code != 200:
        raise AssertionError("categories_response.status_code: {}".format(categories_response.status_code))
    categories = categories_response.json()

    homework_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/homework/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Token " + token},
        verify=False)
    if homework_response.status_code != 200:
        raise AssertionError("homework_response.status_code: {}".format(homework_response.status_code))
    homework = homework_response.json()

    if len(categories) != 5 or len(homework) != 15:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

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
    if category is None:
        raise AssertionError("category is None")

    # Await grade accuracy if worker processing is slow
    if course_group['average_grade'] != '86.2108' or course_group['trend'] != -0.0009202767444288602:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's course group {} grades were not properly calculated "
                "after {} retries.".format(course_group, retry))

    if category['average_grade'] != '92.6667' or category['grade_by_weight'] != '18.5333' \
            or category['trend'] != 0.03833333333333341:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's category {} grades were not properly calculated "
                "after {} retries.".format(category, retry))

    # Assert on a sampling to ensure the example schedule was "moved" into the current month
    now = datetime.datetime.now(pytz.utc)
    if parser.parse(events[0]['start']).month != now.month:
        raise AssertionError("events[0] month: {}".format(events[0]['start'].month))
    if parser.parse(course_group['start_date']).month != now.month:
        raise AssertionError("course_group month: {}".format(course_group['start_date'].month))
    if parser.parse(courses[0]['start_date']).month != now.month:
        raise AssertionError("courses[0] month: {}".format(courses[0]['start_date'].month))
    if parser.parse(courses[1]['start_date']).month != now.month:
        raise AssertionError("courses[1] month: {}".format(courses[1]['start_date'].month))
    if parser.parse(homework[0]['start']).month != now.month:
        raise AssertionError("homework[0] month: {}".format(homework[0]['start'].month))

    return {}
