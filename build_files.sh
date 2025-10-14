#!/bin/sh
set -e

echo "Installing pip..."
python3 -m pip install --upgrade pip

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# echo "Loading fixture data..."
# python3 manage.py loaddata events.json
