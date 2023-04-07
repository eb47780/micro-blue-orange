#!/bin/bash

dockerize -wait tcp://database_schema:5432 -wait tcp://amqp:15672 -timeout 2700s -wait-retry-interval 10s 

cd checkout_service
celery -A checkout_service_config.celery worker -B -l INFO -s /tmp/celerybeat-schedule -n checkout_service