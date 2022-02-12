#!/usr/bin/env sh

echo "Starting worker..."

celery -A app worker -l INFO &

echo "Starting beat..." &

celery -A app beat -l INFO