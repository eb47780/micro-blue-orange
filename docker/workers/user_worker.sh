#!/bin/bash

dockerize -wait tcp://database_schema:5432 -wait tcp://amqp:15672 -timeout 2700s -wait-retry-interval 10s 

cd user_service
celery -A user_service_config.celery worker -B -l INFO -s /tmp/celerybeat-schedule -n user_service
