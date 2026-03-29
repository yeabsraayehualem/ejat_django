#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e
echo "Making migrations"
python manage.py makemigrations
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate



# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
