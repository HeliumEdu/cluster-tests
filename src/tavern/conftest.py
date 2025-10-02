import os

import pytest
import requests


@pytest.fixture
def access_token():
    api_host = os.environ.get('PROJECT_API_HOST')

    response = requests.post(f"{api_host}/auth/token/",
                             data={"username": "heliumedu-cluster-1", "password": "test_pass_1!"},
                             verify=False)

    return response.json()["access"]


@pytest.fixture
def project_info():
    api_host = os.environ.get('PROJECT_API_HOST')

    response = requests.get(f"{api_host}/info/",
                            verify=False)

    return {"min_ext": "" if os.environ.get("ENVIRONMENT", "local") else ".min"} | response.json()
