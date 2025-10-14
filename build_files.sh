#!/bin/sh

set -e

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "loading fixture data"
python3 manage.py loaddata events.json