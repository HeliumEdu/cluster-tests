import os
import time
from email.parser import Parser

import boto
from dateutil import parser
from tavern.util.exceptions import TestFailError

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.18'


def get_verification_code(response, username, retry=0):
    conn = boto.connect_s3(os.environ.get('AWS_S3_ACCESS_KEY_ID'), os.environ.get('AWS_S3_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket(os.environ.get('AWS_S3_EMAIL_BUCKET', 'heliumedu'))

    latest_key = None
    for key in bucket.get_all_keys(prefix='ci.email/{}/'.format(username)):
        if not latest_key or parser.parse(key.last_modified) > parser.parse(latest_key.last_modified):
            latest_key = key
    email_str = latest_key.get_contents_as_string().decode('utf-8')
    email_body = None
    for part in Parser().parsestr(email_str).walk():
        if part.get_content_type() == 'text/plain':
            email_body = part.get_payload()
            break

    if not email_body or 'username={}&code'.format(username) not in email_body:
        if retry < 5:
            time.sleep(3)

            return get_verification_code(response, username, retry + 1)
        else:
            raise TestFailError("The verification email was not received after {} retries.".format(retry))

    verification_code = email_body.split('verify?username={}&code='.format(username))[1].split('\n')[0].strip()

    bucket.delete_key(latest_key)

    return {"email_verification_code": verification_code}
