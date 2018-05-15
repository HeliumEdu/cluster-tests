# Helium CI Tests

## Prerequisites

* Python (>= 3.6)
* Pip (>= 9.0)

## Getting Started
CI tests are developed using Python and [Tavern](https://taverntesting.github.io/).

The following environment variables must be set for the CI tests to run:

* ENV_API_HOST (ex. https://api.heliumedu.test)
* AWS_S3_ACCESS_KEY_ID
* AWS_S3_SECRET_ACCESS_KEY
* TWILIO_ACCOUNT_SID (same account used in `platform` worker to send text)
* TWILIO_AUTH_TOKEN (same token used in `platform` worker to send text)
* TWILIO_RECIPIENT_PHONE_NUMBER (a phone number to which test texts will be sent)

These CI tests also assume you have the ci.heliumedu.com setup to receive emails and store them in an S3 bucket, as
documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html).

To install necessary packages, execute:

```
make install
```

To run CI tests, execute:

```
make test
```
