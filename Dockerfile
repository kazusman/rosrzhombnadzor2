FROM python:3.9.6-slim

RUN apt-get update && apt-get -y install libpq-dev gcc ffmpeg libsm6 libxext6 -y

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . .
