#!/bin/sh

# Run your Django management command
while true; do python manage.py command 10000; sleep 60 * 60 * 12; done

# Start your Django project
python manage.py runserver 0.0.0.0:8000