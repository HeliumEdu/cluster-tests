<p align="center"><img src="https://www.heliumedu.com/assets/img/logo_full_blue.png" /></p>

![Python Versions](https://img.shields.io/badge/python-%203.10%20|%203.11%20|%203.12%20-blue)

# Helium CI Tests

## Getting Started

CI tests are developed using Python and [Tavern](https://taverntesting.github.io/).

The following environment variables must be set for the CI tests to run:

- `ENVIRONMENT` (optional; if not `prod`, same as allowed in [platform](https://github.com/HeliumEdu/platform?tab=readme-ov-file#project-information))
- `AWS_REGION` (optional; if not `prod`, set to AWS S3 region)
- `PROJECT_APP_HOST` (optional; if not `prod`, same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `frontend` environment)
- `PROJECT_API_HOST` (optional; if not `prod`, same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `platform` API environment)
- `PLATFORM_TWILIO_ACCOUNT_SID` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `PLATFORM_TWILIO_AUTH_TOKEN` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `CI_AWS_S3_ACCESS_KEY_ID` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `CI_AWS_S3_SECRET_ACCESS_KEY` (same as used in [platform](https://github.com/HeliumEdu/platform) web to upload attachments)
- `CI_TWILIO_RECIPIENT_PHONE_NUMBER` (a phone number to which test texts will be sent)

These CI tests require `heliumedu-ci-test@heliumedu.dev` to be setup to receive emails and store them in an S3
bucket, as documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html). If [the Terraform for `prod`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/prod#readme)
has already been applied, then this has been configured.

### Running Locally

These tests can also be run against Docker locally if provisioned by [the `deploy` repo](https://github.com/HeliumEdu/deploy).
An Internet connection is still necessary to validate end-to-end functionality for emails (AWS SES) and text messages
(Twilio), but [the minimal Terraform environment for `dev-local`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/dev-local#readme)
will provision this. When running these tests locally against Docker, ensure `PROJECT_APP_HOST` and `PROJECT_API_HOST`
are set to [their respective `local` values](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L33), and `AWS_REGION` is set to `us-east-2`, and
`PLATFORM_EMAIL_HOST_USER` and `PLATFORM_EMAIL_HOST_PASSWORD` are defined for the local `platform` Worker.

## Running Tests

To install the necessary packages, execute:

```sh
make install
```

To run CI tests, execute:

```sh
make test
```
