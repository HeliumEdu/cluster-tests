__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.7.13"

import logging
import os

logger = logging.getLogger(__name__)

ENVIRONMENT = os.environ.get('ENVIRONMENT')
ENVIRONMENT_PREFIX = f'{ENVIRONMENT}.' if 'prod' not in ENVIRONMENT else ''


def get_common_variables(response):
    response = {'test_username': 'heliumedu-ci-test',
                'test_email': f'heliumedu-ci-test@{ENVIRONMENT_PREFIX}heliumedu.dev',
                'test_password': 'test_pass_1!',
                'contact_email': f'contact@{ENVIRONMENT_PREFIX}heliumedu.com'}
    logger.info(response)

    return response
