# Helium CI Tests

## Prerequisites

* Python (>= 3.6)
* Pip (>= 9.0)

## Getting Started
CI tests are developed using Python and [Tavern](https://taverntesting.github.io/).

The following environment variables must be set for the CI tests to run:

* ENV_API_HOST (ex. https://api.heliumedu.test)
* CI_TWILIO_RECIPIENT_PHONE_NUMBER (a phone number to which test texts will be sent)
* PLATFORM_AWS_S3_ACCESS_KEY_ID (same as used in `platform` web to upload attachments)
* PLATFORM_AWS_S3_SECRET_ACCESS_KEY (same as used in `platform` web to upload attachments)
* PLATFORM_TWILIO_ACCOUNT_SID (same as used in `platform` worker to send texts)
* PLATFORM_TWILIO_AUTH_TOKEN (same as used in `platform` worker to send texts)

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

To manually trigger these CI tests to run on Travis, execute the following (after substituting the proper `<token>`):

```
curl -s -X POST -H "Content-Type: application/json" -H "Accept: application/json" -H "Travis-API-Version: 3" -H "Authorization: token <token>" -d '{"request":{"branch":"master"}}' https://api.travis-ci.org/repo/HeliumEdu%2Fci-tests/requests
```
