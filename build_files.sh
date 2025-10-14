#!/bin/sh

set -e
#!/bin/bash

echo "installing pip"
python3 -m pip install --upgrade pip

echo "installing requirements "
pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "loading fixture data"
python3 manage.py loaddata events.json