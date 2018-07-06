import boto
import datetime
import os
import pytz
import time
from dateutil import parser
from email.parser import Parser
from tavern.util.exceptions import TestFailError

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.24'


def get_verification_code(response, username, retry=0):
    conn = boto.connect_s3(os.environ.get('PLATFORM_AWS_S3_ACCESS_KEY_ID'),
                           os.environ.get('PLATFORM_AWS_S3_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket(os.environ.get('PLATFORM_AWS_S3_EMAIL_BUCKET', 'heliumedu'))

    latest_key = None
    for key in bucket.get_all_keys(prefix='ci.email/{}/'.format(username)):
        if not latest_key or parser.parse(key.last_modified) > parser.parse(latest_key.last_modified):
            latest_key = key

    if latest_key is None:
        return get_verification_code(response, username, retry + 1)

    email_str = latest_key.get_contents_as_string().decode('utf-8')

    now = datetime.datetime.now(pytz.utc)
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

    in_test_window = now - datetime.timedelta(seconds=15 + (retry * 5)) <= email_date <= now + datetime.timedelta(
        seconds=15 + (retry * 5))
    if not email_date or not email_body or not in_test_window or 'username={}&code'.format(username) not in email_body:
        if retry < 24:
            time.sleep(5)

            return get_verification_code(response, username, retry + 1)
        else:
            raise TestFailError("The verification email was not received after {} retries.".format(retry))

    verification_code = email_body.split('verify?username={}&code='.format(username))[1].split('\n')[0].strip()

    bucket.delete_key(latest_key)

    return {"email_verification_code": verification_code}
