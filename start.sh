#!/bin/bash
set -e

echo "Starting deployment..."

# Run migrations
echo "Running migrations..."
python backend/manage.py migrate --settings=config.settings.railway --noinput

# Collect static files
echo "Collecting static files..."
python backend/manage.py collectstatic --settings=config.settings.railway --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --log-level info --access-logfile - --error-logfile -
