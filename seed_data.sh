#!/bin/bash

rm -rf nuffleapi/migrations
rm db.sqlite3
python manage.py makemigrations nuffleapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata coach
python manage.py loaddata leagues
python manage.py loaddata teams
python manage.py loaddata players
python manage.py loaddata events
python manage.py loaddata eventteams
python manage.py loaddata eventnotes