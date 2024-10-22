FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y python3-virtualenv python3-pip # python3-setuptools

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY src src
COPY requirements.txt .
COPY Makefile .

RUN python3 -m virtualenv /venv
RUN make install

ENTRYPOINT ["make", "test"]
