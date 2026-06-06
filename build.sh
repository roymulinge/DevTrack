#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

# Install all Python dependencies
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input