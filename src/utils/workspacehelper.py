import json

import requests

from . import emailhelper

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.13'


def init_workspace(response, env_api_host, username, email, password):
    response = requests.post('{}/auth/token/'.format(env_api_host), data={'username': username, 'password': password},
                             verify=False)

    # The test user already exists, which means a previous tests didn't clean up
    if response.status_code == 400 and 'account is not active' in response.content:
        verification_code = emailhelper.get_verification_code(response, username)['verification_code']

        requests.get("{}/auth/user/verify/?username={}&code={}&welcome-email=false".format(env_api_host,
                                                                                           username,
                                                                                           verification_code),
                     verify=False)

        response = requests.post('{}/auth/token/'.format(env_api_host),
                                 data={'username': username, 'password': password},
                                 verify=False)

    if response.status_code == 200:
        token = json.loads(response.content)['token']

        requests.delete(env_api_host + '/auth/user/',
                        headers={'Authorization': "Token " + token},
                        data={'username': username, 'email': email, 'password': password},
                        verify=False)

    return {}
