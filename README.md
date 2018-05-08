[![Build Status](https://travis-ci.org/HeliumEdu/ci-tests.svg?branch=master)](https://travis-ci.org/HeliumEdu/ci-tests)


# Helium CI Tests

## Prerequisites

* Python (>= 3.6)
* Pip (>= 9.0)

## Getting Started
The following environment variables must be set for the CI tests to run:

* ENV_API_HOST (ex. https://api.heliumedu.com)
* TWILIO_ACCOUNT_SID (TEST account is recommended)
* TWILIO_AUTH_TOKEN (TEST token is recommended)

Then, to run CI tests, execute:

```
make install test
```
