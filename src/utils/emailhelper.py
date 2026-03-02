__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import logging
import os
import time
from email.parser import Parser

import boto3
from tavern._core.exceptions import TestFailError

logger = logging.getLogger(__name__)

_RETRIES = 12 * 5

_RETRY_DELAY = 5


def get_verification_code(response, username, retry=0):
    environment = os.environ.get('ENVIRONMENT')
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.environ.get('AWS_INTEGRATION_S3_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_INTEGRATION_S3_SECRET_ACCESS_KEY'),
                        region_name=os.environ.get('AWS_REGION'))
    bucket = s3.Bucket('heliumedu-integration')
    prefix = f'{environment}/inbound.email/heliumedu-cluster/'

    try:
        latest_key = None
        for key in bucket.objects.filter(Prefix=prefix):
            if not latest_key or key.last_modified > latest_key.last_modified:
                latest_key = key

        if latest_key is None:
            if retry < _RETRIES:
                time.sleep(_RETRY_DELAY)

                return get_verification_code(response, username, retry + 1)
            else:
                raise TestFailError(
                    "The verification email was not received after {} seconds.".format(_RETRIES * _RETRY_DELAY))

        logger.info('latest_key: {}'.format(latest_key))

        email_str = latest_key.get()["Body"].read().decode('utf-8')

        email_body = None
        for part in Parser().parsestr(email_str).walk():
            if part.get_content_type() == 'text/plain':
                email_body = part.get_payload()
                break

        logger.info('email_date: {}'.format(latest_key.last_modified))
        logger.info('email_body (truncated): {}'.format((email_body or '')[:300]))

        if not email_body or 'username={}&code'.format(username) not in email_body:
            if retry < _RETRIES:
                time.sleep(_RETRY_DELAY)

                return get_verification_code(response, username, retry + 1)
            else:
                raise TestFailError("No matching verification email could be validated after {} seconds.".format(_RETRIES * _RETRY_DELAY))

        verification_code = email_body.split('verify?username={}&code='.format(username))[1].split('\n')[0].strip()

        latest_key.delete()

        response = {"email_verification_code": verification_code}
        logger.info(response)

        return response
    except TestFailError:
        raise
    except Exception as e:
        logger.warning('Error during email fetch: {}'.format(e))
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, username, retry + 1)
        else:
            raise TestFailError("Failed to retrieve verification email after {} seconds: {}".format(_RETRIES * _RETRY_DELAY, e))
