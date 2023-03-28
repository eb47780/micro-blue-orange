#!/bin/bash

cd /usr/src/app

if [ ! -f ".env" ]; then
  cp .env .env
fi

python manage.py runserver 0.0.0.0:8000