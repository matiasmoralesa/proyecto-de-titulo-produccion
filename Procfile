# Procfile para Railway/Render
# Este archivo define los procesos que se ejecutarán

# Proceso principal: Django con Gunicorn
web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3

# Proceso para Celery Worker (crear servicio separado en Railway)
worker: cd backend && celery -A config worker -l info --pool=solo

# Proceso para Celery Beat (crear servicio separado en Railway)
beat: cd backend && celery -A config beat -l info
