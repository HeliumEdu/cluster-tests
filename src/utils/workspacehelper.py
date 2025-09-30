__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.38"

import datetime
import logging
import time

import pytz
import requests
from dateutil import parser
from tavern._core.exceptions import TestFailError

logger = logging.getLogger(__name__)

_RETRIES = 10

_RETRY_DELAY = 3


def init_workspace(response, env_api_host, username, password):
    response = get_user_access_token(env_api_host, username, password)

    if response.status_code == 200:
        access_token = response.json()['access']

        logger.info(f"Token obtained, so user {username} exists from a previous run and will be cleaned up")

        requests.delete(env_api_host + '/auth/user/delete/',
                        headers={'Authorization': "Bearer " + access_token},
                        data={'password': password},
                        verify=False)
    else:
        logger.info("Attempting to delete inactive user, if exists from a previous failed run")

        requests.delete(env_api_host + '/auth/user/delete/inactive/',
                        data={'username': username, 'password': password},
                        verify=False)

    retries = 0
    while retries < _RETRIES and response.status_code != 401:
        logger.info(f"Response {response.status_code}, waiting for user deletion to complete ...")

        time.sleep(_RETRY_DELAY)
        retries += 1

        response = get_user_access_token(env_api_host, username, password)

    if response.status_code != 401:
        raise TestFailError("Workspaces could not be initialized, user from previous run was never deleted")

    return {}


def wait_for_example_schedule(response, env_api_host, access_token, retry=0):
    events_response = requests.get(env_api_host + '/planner/events/',
                                   headers={'Authorization': "Bearer " + access_token},
                                   verify=False)
    if events_response.status_code != 200:
        raise AssertionError("events_response.status_code: {}".format(events_response.status_code))
    events = events_response.json()

    coursegroups_response = requests.get(env_api_host + '/planner/coursegroups/',
                                         headers={'Authorization': "Bearer " + access_token},
                                         verify=False)
    if coursegroups_response.status_code != 200:
        raise AssertionError("coursegroups_response.status_code: {}".format(coursegroups_response.status_code))
    coursegroups = coursegroups_response.json()
    course_group = coursegroups[0]

    courses_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/'.format(course_group['id']),
        headers={'Authorization': "Bearer " + access_token},
        verify=False)
    if courses_response.status_code != 200:
        raise AssertionError("courses_response.status_code: {}".format(courses_response.status_code))
    courses = courses_response.json()

    if len(events) != 3 or len(courses) != 2:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, access_token, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was only populated with {} events and {} courses "
                "after {} seconds.".format(len(events), len(courses), _RETRIES * _RETRY_DELAY))

    course = None
    for course in courses:
        if course['title'] == 'World History 🌎':
            course = course
            break
    if course is None:
        raise AssertionError("course is None")

    categories_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/categories/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Bearer " + access_token},
        verify=False)
    if categories_response.status_code != 200:
        raise AssertionError("categories_response.status_code: {}".format(categories_response.status_code))
    categories = categories_response.json()

    homework_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/homework/'.format(course_group['id'], course['id']),
        headers={'Authorization': "Bearer " + access_token},
        verify=False)
    if homework_response.status_code != 200:
        raise AssertionError("homework_response.status_code: {}".format(homework_response.status_code))
    homework = homework_response.json()

    if len(categories) != 5 or len(homework) != 15:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, access_token, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was only populated with {} categories and {} homework "
                "after {} seconds.".format(len(categories), len(homework), _RETRIES * _RETRY_DELAY))

    category = None
    for category in categories:
        if category['title'] == 'Writing Assignment 📝':
            category = category
            break
    if category is None:
        raise AssertionError("category is None")

    # Await grade accuracy if worker processing is slow
    if course_group['average_grade'] != '86.2108' or course_group['trend'] != -0.0009202767444288602:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, access_token, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's course group {} grades were not properly calculated "
                "after {} seconds.".format(course_group, _RETRIES * _RETRY_DELAY))

    if category['average_grade'] != '92.6667' or category['grade_by_weight'] != '18.5333' \
            or category['trend'] != 0.03833333333333341:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return wait_for_example_schedule(response, env_api_host, access_token, retry + 1)
        else:
            raise TestFailError(
                "The example schedule's category {} grades were not properly calculated "
                "after {} seconds.".format(category, _RETRIES * _RETRY_DELAY))

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


def get_user_access_token(env_api_host, username, password):
    return requests.post(f"{env_api_host}/auth/token/",
                         data={"username": username, "password": password},
                         verify=False)
