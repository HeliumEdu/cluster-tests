import time

import requests

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.17'


def init_workspace(response, env_api_host, username, email, password):
    # If the test user already exists, cleanup from a previous test
    response = requests.delete(env_api_host + '/auth/user/delete/',
                               data={'username': username, 'email': email, 'password': password},
                               verify=False)

    # If the user existed and was deleted, wait to ensure their data is fully deleted
    if response.status_code == 204:
        time.sleep(3)

    return {}
