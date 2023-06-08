#!/bin/bash

cd /usr/src/payment

dockerize -wait tcp://database_schema:5432 -wait tcp://amqp:15672 -timeout 2700s -wait-retry-interval 10s 
celery -A config.celery worker -B -l INFO -s /tmp/celerybeat-schedule -n payment_service