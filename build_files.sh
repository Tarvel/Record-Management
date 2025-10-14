#!/bin/sh

set -e

echo "Collecting static files..."
python3.10 manage.py collectstatic --noinput

echo "loading fixture data"
python manage.py loaddata events.json