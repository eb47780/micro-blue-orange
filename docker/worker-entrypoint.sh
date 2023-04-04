#!/bin/bash

cd /usr/src/app

dockerize -wait tcp://database:5432 -wait tcp://app:8000 -timeout 2700s -wait-retry-interval 10s

celery -A config.celery worker -B -l INFO -s /tmp/celerybeat-schedule