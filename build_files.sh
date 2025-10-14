#!/bin/sh

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "loading fixture data"
python manage.py loaddata events.json