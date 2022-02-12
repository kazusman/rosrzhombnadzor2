FROM python:3.9.6-alpine

RUN apk update && apk add build-base libffi-dev postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
