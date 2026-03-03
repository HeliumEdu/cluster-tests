import os
import time

import pytest
import requests

_ANON_RETRY_DELAY = 7


@pytest.fixture(scope="session")
def access_token():
    api_host = os.environ.get('PROJECT_API_HOST')

    for attempt in range(3):
        response = requests.post(f"{api_host}/auth/token/",
                                 data={"username": "heliumedu-cluster-1", "password": "test_pass_1!"},
                                 verify=False)

        token_data = response.json()
        if "access" in token_data:
            return token_data["access"]

        # Rate limited or transient error — wait and retry
        print(f"access_token fixture attempt {attempt + 1} failed ({response.status_code}): {token_data}")
        time.sleep(_ANON_RETRY_DELAY)

    raise Exception(f"Could not obtain access token after 3 attempts: {response.json()}")
