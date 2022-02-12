#!/usr/bin/env sh

./manage.py migrate

./manage.py collectstatic
