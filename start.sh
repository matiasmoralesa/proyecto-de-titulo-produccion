#!/bin/bash
# Script de inicio para Railway que ejecuta Django + Celery Worker + Celery Beat

cd backend

# Ejecutar migraciones
echo "Running migrations..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar Celery Worker en segundo plano
echo "Starting Celery Worker..."
celery -A config worker -l info --pool=solo &

# Iniciar Celery Beat en segundo plano
echo "Starting Celery Beat..."
celery -A config beat -l info &

# Iniciar Gunicorn (proceso principal)
echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3
