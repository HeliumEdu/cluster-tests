<p align="center"><img src="https://www.heliumedu.com/assets/img/logo_full_blue.png" /></p>

![Python Versions](https://img.shields.io/badge/python-%203.10%20|%203.11%20-blue)

# Helium CI Tests

## Getting Started

CI tests are developed using Python and [Tavern](https://taverntesting.github.io/).

The following environment variables must be set for the CI tests to run:

- `PROJECT_APP_HOST` (same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `frontend` environment)
- `PROJECT_API_HOST` (same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `platform` API environment)
- `PLATFORM_AWS_S3_ACCESS_KEY_ID` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `PLATFORM_AWS_S3_SECRET_ACCESS_KEY` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `PLATFORM_TWILIO_ACCOUNT_SID` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `PLATFORM_TWILIO_AUTH_TOKEN` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `CI_TWILIO_RECIPIENT_PHONE_NUMBER` (a phone number to which test texts will be sent)

These CI tests require `heliumedu-ci-test@heliumedu.dev` to be setup to receive emails and store them in an S3
bucket, as documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html).
If [the Terraform for `prod`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/prod#readme) has
already been applied, then this has been configured.

These tests can also be run against the local Docker container(s) provisioned by [the `deploy` repo](https://github.com/HeliumEdu/deploy).
An Internet connection is still necessary to validate end-to-end functionality for emails (AWS SES) and text messages
(Twilio), but [the minimal Terraform for `dev-local`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/dev-local#readme) can be applied for this.

## Running Tests

To install the necessary packages, execute:

```sh
make install
```

To run CI tests, execute:

```sh
make test
```
