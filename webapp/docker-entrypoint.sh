#!/bin/bash

python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py crontab add

service cron start

gunicorn config.wsgi:application --bind 0.0.0.0:8888
