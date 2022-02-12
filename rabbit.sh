#!/usr/bin/env sh

echo "Starting worker..."

celery -A rosrzhombnadzor worker -l INFO &

echo "Starting beat..." &

celery -A rosrzhombnadzor beat -l INFO