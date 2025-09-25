__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.11.13"

import datetime
import logging
import os
import time

import pytz
import requests
from tavern._core.exceptions import TestFailError
from twilio.rest import Client

logger = logging.getLogger(__name__)

_RETRIES = 12 * 3

_RETRY_DELAY = 5


def get_verification_code(response, phone, retry=0):
    now = datetime.datetime.now(pytz.utc)

    client = Client(os.environ.get('PLATFORM_TWILIO_ACCOUNT_SID'), os.environ.get('PLATFORM_TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone, date_sent=now.date()):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    if latest_message is None:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, phone, retry + 1)
        else:
            raise TestFailError(
                "The verification SMS was not received after {} seconds.".format(_RETRY_DELAY * _RETRY_DELAY))

    logger.info('latest_message: {}'.format(latest_message))

    left_window = now - datetime.timedelta(seconds=30 + (retry * _RETRY_DELAY))
    right_window = now + datetime.timedelta(seconds=30 + (retry * _RETRY_DELAY))

    logger.info('left_window: {}'.format(left_window))
    logger.info('latest_message.date_created: {}'.format(latest_message.date_created))
    logger.info('right_window: {}'.format(right_window))

    in_test_window = left_window <= latest_message.date_created <= right_window
    if not latest_message or not in_test_window or 'Enter this verification code' not in latest_message.body:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, phone, retry + 1)
        else:
            raise TestFailError(
                "No matching verification SMS could be validated after {} seconds.".format(_RETRIES * _RETRY_DELAY))

    verification_code = int(latest_message.body.split('Helium\'s "Settings" page: ')[1])

    response = {"sms_verification_code": verification_code}
    logger.info(response)

    return response


def verify_reminder_marked_sent(response, env_api_host, access_token, reminder_id, retry=0):
    response = requests.get('{}/planner/reminders/{}/'.format(env_api_host, reminder_id),
                            headers={'Authorization': "Bearer " + access_token},
                            verify=False)

    if not (response.status_code == 200 and response.json()["sent"]):
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return verify_reminder_marked_sent(response, env_api_host, access_token, reminder_id, retry + 1)
        else:
            raise TestFailError(
                "The reminder was not marked as \"sent\" after {} seconds.".format(_RETRIES * _RETRY_DELAY))

    return {}


def verify_reminder_received(response, phone, retry=0):
    now = datetime.datetime.now(pytz.utc)

    if retry == 0:
        logger.info('/status/ response: {}'.format(response.json()))

    client = Client(os.environ.get('PLATFORM_TWILIO_ACCOUNT_SID'), os.environ.get('PLATFORM_TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone, date_sent=now.date()):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    left_window = now - datetime.timedelta(seconds=60 + (retry * _RETRY_DELAY))
    right_window = now + datetime.timedelta(seconds=60 + (retry * _RETRY_DELAY))

    logger.info('left_window: {}'.format(left_window))
    logger.info('latest_message.date_created: {}'.format(latest_message.date_created))
    logger.info('right_window: {}'.format(right_window))

    in_test_window = left_window <= latest_message.date_created <= right_window
    if not latest_message or not in_test_window or 'CI Test Homework in World History 🌎' not in latest_message.body:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return verify_reminder_received(response, phone, retry + 1)
        else:
            raise TestFailError("The reminder SMS was not received after {} seconds.".format(_RETRIES * _RETRY_DELAY))

    if latest_message.body != '(CI Test Homework in World History 🌎 on Tue, Apr 17 at 09:00 PM) CI test reminder message':
        raise AssertionError("latest_message.body: {}".format(latest_message.body))

    return {}
