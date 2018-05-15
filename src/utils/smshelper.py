import os

from twilio.rest import Client

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.15'


def get_verification_code(response, phone):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    verification_code = int(latest_message.body.split('Helium\'s "Settings" page: ')[1])

    return {"sms_verification_code": verification_code}


def verify_reminder_received(response, phone):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    assert latest_message.body == '(CI Test Homework in American History on Tue, Apr 17 at 09:00 PM) CI test reminder message'

    return {}
