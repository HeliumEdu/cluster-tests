import time

import requests
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


def get_example_schedule_info(response, env_api_host, retry=0):
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
    course_group_id = coursegroups[0]['id']

    courses_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/'.format(course_group_id),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert courses_response.status_code == 200
    courses = courses_response.json()

    if len(events) != 3 or len(courses) != 2:
        if retry < 10:
            time.sleep(2)

            return get_example_schedule_info(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was not populated with events and courses after {} retries.".format(retry))

    course_id = None
    for course in courses:
        if course['title'] == 'American History':
            course_id = course['id']
            break
    assert course_id is not None

    categories_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/categories/'.format(course_group_id, course_id),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert categories_response.status_code == 200
    categories = categories_response.json()

    homework_response = requests.get(
        env_api_host + '/planner/coursegroups/{}/courses/{}/homework/'.format(course_group_id, course_id),
        headers={'Authorization': "Token " + token},
        verify=False)
    assert homework_response.status_code == 200
    homework = homework_response.json()

    if len(categories) != 5 or len(homework) != 15:
        if retry < 10:
            time.sleep(2)

            return get_example_schedule_info(response, env_api_host, retry + 1)
        else:
            raise TestFailError(
                "The example schedule was not populated with categories and homework after {} retries.".format(retry))

    category_id = None
    for category in categories:
        if category['title'] == 'Writing Assignment':
            category_id = category['id']
            break
    assert category_id is not None

    homework_id = None
    for h in homework:
        if h['title'] == 'Chapter 2 Prompts' and h['category'] == category_id:
            homework_id = h['id']
            break
    assert homework_id is not None

    return {}
