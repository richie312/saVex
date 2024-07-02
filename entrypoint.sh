#!/bin/sh

# Run your Django management command
while true; do python manage.py command 12000; sleep 60; done

# Start your Django project
python manage.py runserver 0.0.0.0:8000