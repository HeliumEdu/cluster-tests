__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.4.26"

import os

import requests


def create_attachment(response, env_api_host, token, course_id):
    response = requests.post('{}/planner/attachments/'.format(env_api_host),
                             headers={'Authorization': "Token " + token},
                             data={'course': course_id},
                             files={
                                 'file[]': (os.path.basename('requirements.txt'), open('requirements.txt', 'rb'),
                                            'application/octet-stream')
                             },
                             verify=False)

    if response.status_code != 201:
        raise AssertionError("response.status_code: {}".format(response.status_code))

    return {"attachment_url": response.json()[0]['attachment']}
