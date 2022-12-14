FROM python:3.8-slim-buster

WORKDIR /bot

COPY ./bot /bot

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
