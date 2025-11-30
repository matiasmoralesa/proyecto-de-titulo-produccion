#!/bin/bash
set -e

echo "Starting deployment..."

# Run migrations
echo "Running migrations..."
python backend/manage.py migrate --settings=config.settings.railway --noinput

# Load production data if backup exists and database is empty
echo "Checking if data needs to be loaded..."
if [ -f "backend/data_backup.json" ]; then
    USER_COUNT=$(python backend/manage.py shell --settings=config.settings.railway -c "from django.contrib.auth.models import User; print(User.objects.count())")
    if [ "$USER_COUNT" = "0" ]; then
        echo "Database is empty. Loading production data..."
        python backend/manage.py load_production_data --settings=config.settings.railway || echo "Warning: Could not load data, continuing anyway..."
    else
        echo "Database already has data. Skipping data load."
    fi
else
    echo "No backup file found. Skipping data load."
fi

# Collect static files
echo "Collecting static files..."
python backend/manage.py collectstatic --settings=config.settings.railway --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --log-level info --access-logfile - --error-logfile -
