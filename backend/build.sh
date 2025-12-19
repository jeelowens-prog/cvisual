#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run robust migration handler
python manage_db.py
