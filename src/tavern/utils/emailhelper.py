import datetime
import logging
import os
import time
from email.parser import Parser

import boto3
import pytz
from dateutil import parser
from tavern.util.exceptions import TestFailError

__author__ = "Alex Laird"
__copyright__ = "Copyright 2019, Helium Edu"
__version__ = "1.4.38"

logger = logging.getLogger(__name__)

_RETRIES = 24

_RETRY_DELAY = 5


def get_verification_code(response, username, retry=0):
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.environ.get('PLATFORM_AWS_S3_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('PLATFORM_AWS_S3_SECRET_ACCESS_KEY'))
    bucket = s3.Bucket(os.environ.get('PLATFORM_AWS_S3_EMAIL_BUCKET', 'heliumedu'))

    latest_key = None
    for key in bucket.objects.filter(Prefix='ci.email/{}/'.format(username)):
        if not latest_key or key.last_modified > latest_key.last_modified:
            latest_key = key

    if latest_key is None:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, username, retry + 1)
        else:
            raise TestFailError("The verification email was not received after {} retries.".format(retry))

    logger.info('latest_key: {}'.format(latest_key))

    email_str = latest_key.get()["Body"].read().decode('utf-8')

    email_date = datetime.datetime(1, 1, 1, 0, 0)
    email_body = None
    for part in Parser().parsestr(email_str).walk():
        payload = part.get_payload()

        if part.get_content_type() == 'text/plain':
            email_body = payload
        elif part.get_content_type() == 'multipart/alternative' and 'Date' in part.keys():
            email_date = parser.parse(part.get('Date'))

        if email_date and email_body:
            break

    now = datetime.datetime.now(pytz.utc)
    left_window = now - datetime.timedelta(seconds=15 + (retry * _RETRY_DELAY))
    right_window = now + datetime.timedelta(seconds=15 + (retry * _RETRY_DELAY))

    logger.info('left_window: {}'.format(left_window))
    logger.info('email_date: {}'.format(email_date))
    logger.info('right_window: {}'.format(right_window))

    in_test_window = left_window <= email_date <= right_window
    if not email_date or not email_body or not in_test_window or 'username={}&code'.format(username) not in email_body:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, username, retry + 1)
        else:
            raise TestFailError("No matching verification email could be validated after {} retries.".format(retry))

    verification_code = email_body.split('verify?username={}&code='.format(username))[1].split('\n')[0].strip()

    latest_key.delete()

    response = {"email_verification_code": verification_code}
    logger.info(response)

    return response
