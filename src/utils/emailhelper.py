__copyright__ = "Copyright (c) 2025 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.54"

import datetime
import logging
import os
import time
from email.parser import Parser

import boto3
from tavern._core.exceptions import TestFailError

logger = logging.getLogger(__name__)

_RETRIES = 12 * 5

_RETRY_DELAY = 5

_EMAIL_MAX_AGE_MINUTES = 5


def get_verification_code(response, username, email=None, retry=0, _cutoff=None):
    if _cutoff is None:
        _cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=_EMAIL_MAX_AGE_MINUTES)

    environment = os.environ.get('ENVIRONMENT')
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.environ.get('AWS_INTEGRATION_S3_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_INTEGRATION_S3_SECRET_ACCESS_KEY'),
                        region_name=os.environ.get('AWS_REGION'))
    bucket = s3.Bucket('heliumedu-integration')
    prefix = f'{environment}/inbound.email/heliumedu-cluster/'

    try:
        all_keys = sorted(
            [k for k in bucket.objects.filter(Prefix=prefix) if k.last_modified >= _cutoff],
            key=lambda k: k.last_modified,
            reverse=True
        )

        matched_key = None
        email_body = None
        for key in all_keys:
            email_str = key.get()["Body"].read().decode('utf-8')

            body = None
            for part in Parser().parsestr(email_str).walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload()
                    break

            if body and (
                f'username={username}&code' in body or
                (email and f'email={email}&code' in body)
            ):
                matched_key = key
                email_body = body
                break

        if not matched_key:
            if retry < _RETRIES:
                time.sleep(_RETRY_DELAY)

                return get_verification_code(response, username, email, retry + 1, _cutoff)
            else:
                raise TestFailError(
                    "The verification email was not received after {} seconds.".format(_RETRIES * _RETRY_DELAY))

        if email and f'email={email}&code=' in email_body:
            verification_code = email_body.split(f'verify?email={email}&code=')[1].split('\n')[0].strip()
        else:
            verification_code = email_body.split(f'verify?username={username}&code=')[1].split('\n')[0].strip()

        matched_key.delete()

        response = {"email_verification_code": verification_code}
        logger.info(response)

        return response
    except TestFailError:
        raise
    except Exception as e:
        logger.warning('Error during email fetch: {}'.format(e))
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, username, email, retry + 1, _cutoff)
        else:
            raise TestFailError("Failed to retrieve verification email after {} seconds: {}".format(_RETRIES * _RETRY_DELAY, e))
