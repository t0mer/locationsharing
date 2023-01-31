FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

ENV EMAIL_ADDRESS ""
ENV COOKIES_FILE_NAME ""
ENV MQTT_HOST ""
ENV MQTT_PORT 1883
ENV MQTT_USERNAME ""
ENV MQTT_PASSWORD ""
ENV UPDATE_INTERVAL 1

RUN apt update -yqq

RUN apt install -yqq python3-pip && \
    apt install -yqq libffi-dev && \
    apt install -yqq libssl-dev

RUN  pip3 install --upgrade pip --no-cache-dir && \
     pip3 install --upgrade setuptools --no-cache-dir

RUN mkdir -p /app/cookies

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

COPY app /app

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/python3", "/app/app.py"]