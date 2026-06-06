#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

# Run database migrations before starting the server
# This runs at runtime when Render's internal network IS available
python manage.py migrate

# Start the production server
gunicorn dev_track.wsgi:application