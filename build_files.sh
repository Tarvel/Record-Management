#!/bin/sh
set -e

echo "Installing pip..."
python3 -m pip install --upgrade pip

export PATH=$PATH:/python312/bin

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# echo "Loading fixture data..."
# python3 manage.py loaddata events.json
