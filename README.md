<p align="center"><img src="https://www.heliumedu.com/assets/img/logo_full_blue.png" /></p>

![Python Versions](https://img.shields.io/badge/python-%203.10%20|%203.11%20|%203.12%20-blue)

# Helium Cluster Tests

The `cluster-tests` validate integration and end-to-end functionality of the [Helium Edu](https://www.heliumedu.com/) APIs and UI.

## Prerequisites

- Python (>= 3.12)

## Getting Started

Cluster tests are developed using Python and [Tavern](https://taverntesting.github.io/) and [Selenium](https://www.selenium.dev/documentation/).

The following environment variables must be set for the tests to run:

- `ENVIRONMENT` (optional; if not `prod`, same as allowed in [platform](https://github.com/HeliumEdu/platform?tab=readme-ov-file#project-information))
- `AWS_REGION` (optional; if not `prod`, set to AWS S3 region)
- `PROJECT_APP_HOST` (optional; if not `prod`, same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `frontend` environment)
- `PROJECT_API_HOST` (optional; if not `prod`, same as chosen in [platform](https://github.com/HeliumEdu/platform/blob/main/conf/configs/common.py#L32) for a `platform` API environment)
- `PLATFORM_TWILIO_ACCOUNT_SID` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `PLATFORM_TWILIO_AUTH_TOKEN` (same as used in [platform](https://github.com/HeliumEdu/platform) worker to send texts)
- `CI_TWILIO_RECIPIENT_PHONE_NUMBER` (a Twilio phone number to which test texts will be sent)
- `CI_AWS_S3_ACCESS_KEY_ID` ([credentials with access](https://github.com/HeliumEdu/deploy/blob/main/terraform/modules/secretsmanager/ci_creds/main.tf#L5) to the inbound email S3 bucket)
- `CI_AWS_S3_SECRET_ACCESS_KEY` ([credentials with access](https://github.com/HeliumEdu/deploy/blob/main/terraform/modules/secretsmanager/ci_creds/main.tf#L5) to the inbound email S3 bucket)

These cluster tests require `heliumedu-cluster1@heliumedu.dev` and `heliumedu-cluster2@heliumedu.dev` to be provisioned
to store inbound emails in an S3 bucket, as documented [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html).
[The Terraform for `prod`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/prod#readme) can be
applied to configure this (or `dev-local` to run fully contained within Docker, as described below).

Once `prod` is provisioned, all cluster test suites can be run with:

```sh
make test
```

The cluster tests are broken in to two suites: `make test-smoke` and `make test-selenium`. The `smoke` tests are
written using Tavern and intended to quickly provide a high-level assurance of basic end-to-end functionality,
primarily around the APIs and responses (as well as external dependencies)—these should catch significant regressions
in the cluster. The `selenium` suite is intended to be more thorough, with a particular focus on validating
interactions between the UI and the backend.

### Running Locally in Docker

These cluster tests can be run locally against Docker to make development easier. The easiest way to achieve this is
to use [the `deploy` project](https://github.com/HeliumEdu/deploy?tab=readme-ov-file#docker-setup) to setup the
entire Helium stack locally. An Internet connection is still necessary to validate all end-to-end functionality
(emails use AWS SES, text messages use Twilio). [The minimal Terraform for `dev-local`](https://github.com/HeliumEdu/deploy/tree/main/terraform/environments/dev-local#readme)
can be applied to configure these services automatically.

Once the above is done, the cluster tests can be run locally with:

```sh
make test-local
```

#### Image Architecture

Due to the nature of its dependencies, this project will only build an `linux/amd64` image, even when Docker is running
on another architecture.
