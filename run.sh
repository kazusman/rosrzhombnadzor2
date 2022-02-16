#!/usr/bin/env sh

echo "STARTING SERVICES"

docker-compose up -d --force-recreate --build

echo "SERVICES ARE UP, MIGRATING AND COLLECTING STATIC"

docker-compose exec web ./prestart.sh

echo "MIGRATED AND COLLECTED. RUNNING CELERY BEAT AND WORKER"

docker-compose exec web ./rabbit.sh

