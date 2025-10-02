__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import requests


def get_user_access_token(env_api_host, username, password):
    return requests.post(f"{env_api_host}/auth/token/",
                         data={"username": username, "password": password},
                         verify=False)


def assert_response_length(response, expected_length):
    length = len(response.json())
    assert length == expected_length, \
        f"Response length mismatch: Expected {expected_length}, got {length}"
