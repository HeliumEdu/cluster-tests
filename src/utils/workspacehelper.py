import requests

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.17'


def init_workspace(response, env_api_host, username, email, password):
    response = requests.post('{}/auth/token/'.format(env_api_host), data={'username': username, 'password': password},
                             verify=False)

    # If the test user already exists, cleanup from a previous test
    json_response = response.json()
    if response.status_code == 200:
        requests.delete(env_api_host + '/auth/user/',
                        headers={'Authorization': "Token " + response.json()['token']},
                        data={'username': username, 'email': email, 'password': password},
                        verify=False)
    elif response.status_code == 400 and 'non_field_errors' in json_response and \
                    'account is not active' in json_response['non_field_errors'][0]:
        requests.get("{}/auth/user/delete-inactive".format(env_api_host),
                     data={'username': username, 'email': email, 'password': password},
                     verify=False)

    return {}
