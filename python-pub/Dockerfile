# syntax=docker/dockerfile:1
FROM python:3.12-alpine3.19

WORKDIR /usr/src/app

RUN set -xe \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY nats_publisher.py .

ENTRYPOINT ["python", "./nats_publisher.py"]

