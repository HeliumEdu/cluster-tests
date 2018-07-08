import os

import requests

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.26'


def create_attachment(response, env_api_host, token, course_id):
    response = requests.post('{}/planner/attachments/'.format(env_api_host),
                             headers={'Authorization': "Token " + token},
                             data={'course': course_id},
                             files={
                                 'file[]': (os.path.basename('requirements.txt'), open('requirements.txt', 'rb'),
                                            'application/octet-stream')
                             },
                             verify=False)

    assert response.status_code == 201

    return {"attachment_url": response.json()[0]['attachment']}
