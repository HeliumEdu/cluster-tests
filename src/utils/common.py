__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import time

import requests

# POST /auth/token/ is unauthenticated; 7s keeps retries under the 10/min anon rate limit
_ANON_RETRY_DELAY = 7


def get_user_access_token(env_api_host, username, password):
    for attempt in range(3):
        response = requests.post(f"{env_api_host}/auth/token/",
                                 data={"username": username, "password": password},
                                 verify=False)
        if response.status_code != 429:
            return response

        print(f"get_user_access_token attempt {attempt + 1} throttled ({response.status_code}): {response.json()}")
        time.sleep(_ANON_RETRY_DELAY)

    return response


def assert_response_length(response, expected_length):
    length = len(response.json())
    assert length == expected_length, \
        f"Response length mismatch: Expected {expected_length}, got {length}"
