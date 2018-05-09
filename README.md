[![Build Status](https://travis-ci.org/HeliumEdu/ci-tests.svg?branch=master)](https://travis-ci.org/HeliumEdu/ci-tests)


# Helium CI Tests

## Prerequisites

* Python (>= 3.6)
* Pip (>= 9.0)

## Getting Started
The following environment variables must be set for the CI tests to run:

* ENV_API_HOST (ex. https://api.heliumedu.test)
* AWS_S3_ACCESS_KEY_ID
* AWS_S3_SECRET_ACCESS_KEY
* TWILIO_ACCOUNT_SID (TEST account is recommended)
* TWILIO_AUTH_TOKEN (TEST token is recommended)

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
