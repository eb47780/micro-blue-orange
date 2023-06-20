#!/bin/bash

cd /usr/src/checkout

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

dockerize -wait tcp://database_schema:5432 -wait tcp://amqp:15672 -timeout 2700s -wait-retry-interval 10s

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata initial_data 
DJANGO_SUPERUSER_EMAIL=endritberisha@microblueorange.com
export DJANGO_SUPERUSER_EMAIL

DJANGO_SUPERUSER_USERNAME=endritberisha
export DJANGO_SUPERUSER_USERNAME

DJANGO_SUPERUSER_PASSWORD=123456
export DJANGO_SUPERUSER_PASSWORD

python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
python3 manage.py runserver 0.0.0.0:8000