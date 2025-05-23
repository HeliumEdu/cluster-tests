<p align="center"><img src="https://www.heliumedu.com/assets/img/logo_full_blue.png" /></p>

![Python Versions](https://img.shields.io/badge/python-%203.10%20|%203.11%20|%203.12%20-blue)

# Helium CI Tests

The `ci-tests` that validate end-to-end functionality of [Helium Edu](https://www.heliumedu.com/).

## Prerequisites

- Python (>= 3.12)

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
- `CI_TWILIO_RECIPIENT_PHONE_NUMBER` (a Twilio phone number to which test texts will be sent)

These CI tests require `heliumedu-ci-test@heliumedu.dev` to be setup to receive emails and store them in an S3
bucket, as documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html).
[The Terraform for `prod`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/prod#readme) can be
applied to configure this.

Once the above is done, the CI tests can be run with:

```sh
make test
```

## Development

### Running Locally

These tests can be run locally against Docker to make development easier. The easiest way to achieve this is to use
[the `deploy` project](https://github.com/HeliumEdu/deploy?tab=readme-ov-file#docker-setup) to setup the entire Helium
stack locally. An Internet connection is still necessary to validate all end-to-end functionality (emails use
AWS SES, text messages use Twilio). [The minimal Terraform for `dev-local`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/dev-local#readme)
can be applied to configure these services.

Once the above is done, the CI tests can be run locally with:

```sh
make test-local
```