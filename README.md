[![CI/CD](https://github.com/heliumedu/ci-tests/workflows/CI/CD/badge.svg)](https://github.com/heliumedu/ci-tests/actions?query=workflow%3ACI%2FCD)
![GitHub License](https://img.shields.io/github/license/heliumedu/ci-tests)

# Helium CI Tests

<p align="center"><img src="https://www.heliumedu.com/assets/img/logo_full_blue.png" /></p>

## Prerequisites

- Python (>= 3.6)
- Pip (>= 9.0)

## Getting Started
CI tests are developed using Python and [Tavern](https://taverntesting.github.io/).

The following environment variables must be set for the CI tests to run:

- `PROJECT_APP_HOST` (same as used in [deploy](https://github.com/HeliumEdu/deploy) for frontend host)
- `PROJECT_API_HOST` (same as used in [deploy](https://github.com/HeliumEdu/deploy) for API host)
- `PLATFORM_AWS_S3_ACCESS_KEY_ID` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `PLATFORM_AWS_S3_SECRET_ACCESS_KEY` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `PLATFORM_TWILIO_ACCOUNT_SID` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `PLATFORM_TWILIO_AUTH_TOKEN` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `CI_TWILIO_RECIPIENT_PHONE_NUMBER` (a phone number to which test texts will be sent)

These CI tests also assume you have the ci.heliumedu.com setup to receive emails and store them in an S3 bucket, as
documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html).

To install necessary packages, execute:

```sh
make install
```

To run CI tests, execute:

```sh
make test
```

To manually trigger these CI tests to run on Travis, execute the following (after substituting the proper `<token>`):

```sh
curl -s -X POST -H "Content-Type: application/json" -H "Accept: application/json" -H "Travis-API-Version: 3" -H "Authorization: token <token>" -d '{"request":{"branch":"master"}}' https://api.travis-ci.org/repo/HeliumEdu%2Fci-tests/requests
```
