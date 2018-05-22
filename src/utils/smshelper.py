import datetime
import os
import time

import pytz
from tavern.util.exceptions import TestFailError
from twilio.rest import Client

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.18'


def get_verification_code(response, phone, retry=0):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    now = datetime.datetime.now(pytz.utc)
    in_test_window = now - datetime.timedelta(
        seconds=30 + (retry * 3)) <= latest_message.date_created <= now + datetime.timedelta(seconds=30 + (retry * 3))
    if not latest_message or not in_test_window or 'Enter this verification code' not in latest_message.body:
        if retry < 5:
            time.sleep(3)

            return get_verification_code(response, phone, retry + 1)
        else:
            raise TestFailError("The verification SMS was not received after {} retries.".format(retry))

    verification_code = int(latest_message.body.split('Helium\'s "Settings" page: ')[1])

    return {"sms_verification_code": verification_code}


def verify_reminder_received(response, phone, retry=0):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    now = datetime.datetime.now(pytz.utc)
    in_test_window = now - datetime.timedelta(
        seconds=30 + (retry * 3)) <= latest_message.date_created <= now + datetime.timedelta(seconds=30 + (retry * 3))
    if not latest_message or not in_test_window or 'CI Test Homework in American History' not in latest_message.body:
        if retry < 5:
            time.sleep(3)

            return verify_reminder_received(response, phone, retry + 1)
        else:
            raise TestFailError("The reminder SMS was not received after {} retries.".format(retry))

    assert latest_message.body == '(CI Test Homework in American History on Tue, Apr 17 at 09:00 PM) CI test reminder message'

    return {}
