#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create migrations if they don't exist, otherwise update
if [ ! -d "migrations" ]; then
    flask db init
    flask db migrate -m "Initial migration"
fi
flask db upgrade
