# Procfile para Railway/Render
# Este archivo define los procesos que se ejecutarán

# Proceso principal: Django con Gunicorn + Celery Worker + Celery Beat
web: bash start.sh

# Procesos separados (comentados, usar solo si se crean servicios separados en Railway)
# worker: cd backend && celery -A config worker -l info --pool=solo
# beat: cd backend && celery -A config beat -l info
