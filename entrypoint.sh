#!/bin/bash
sudo source /teak_env/bin/activate
sudo pip install -r requirements.txt
# RUN pip install django gunicorn


sudo python3 manage.py makemigrations
# Apply database migrations
sudo python3 manage.py migrate

# Collect static files (if needed)
# python3 manage.py collectstatic 

# Start Gunicorn server
sudo python manage.py runserver 0.0.0.0:8000
# exec gunicorn core.wsgi:application --bind 0.0.0.0:8009
