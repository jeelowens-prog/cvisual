#!/usr/bin/env bash
# exit on error
set -o errexit

#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run intelligent migration handling
python manage_db.py
