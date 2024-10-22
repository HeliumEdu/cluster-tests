FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y python3-virtualenv python3-pip wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CI_VENV="/venv"
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY src src
COPY requirements.txt .
COPY Makefile .

RUN python3 -m virtualenv /venv
RUN make install

ENTRYPOINT ["make", "test"]