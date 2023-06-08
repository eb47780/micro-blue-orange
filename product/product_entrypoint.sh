#!/bin/bash

cd /usr/src/product

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

dockerize -wait tcp://database_schema:5432 -wait tcp://amqp:15672 -timeout 2700s -wait-retry-interval 10s

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata initial_data 
python3 manage.py runserver 0.0.0.0:8000