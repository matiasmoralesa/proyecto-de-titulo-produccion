"""
Configuración de Celery para el proyecto CMMS
"""
import os
from celery import Celery
from celery.schedules import crontab

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Crear instancia de Celery
app = Celery('cmms')

# Configuración desde Django settings con prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrir tareas en todas las apps
app.autodiscover_tasks()

# Configurar tareas programadas (Celery Beat)
app.conf.beat_schedule = {
    # Predicciones ML diarias a las 6:00 AM
    'run-daily-predictions': {
        'task': 'apps.ml_predictions.tasks.run_daily_predictions',
        'schedule': crontab(hour=6, minute=0),
        'options': {'expires': 3600}  # Expira en 1 hora si no se ejecuta
    },
    
    # Verificar activos críticos cada 4 horas
    'check-critical-assets': {
        'task': 'apps.assets.tasks.check_critical_assets',
        'schedule': crontab(minute=0, hour='*/4'),  # Cada 4 horas (0, 4, 8, 12, 16, 20)
    },
    
    # Limpiar notificaciones antiguas cada día a medianoche
    'cleanup-old-notifications': {
        'task': 'apps.notifications.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=0, minute=0),
    },
    
    # Generar reporte semanal los lunes a las 8:00 AM
    'generate-weekly-report': {
        'task': 'apps.reports.tasks.generate_weekly_report',
        'schedule': crontab(day_of_week=1, hour=8, minute=0),
    },
    
    # Verificar órdenes de trabajo vencidas cada 30 minutos
    'check-overdue-workorders': {
        'task': 'apps.work_orders.tasks.check_overdue_workorders',
        'schedule': crontab(minute='*/30'),
    },
}

# Configuración de zona horaria
app.conf.timezone = 'America/Santiago'  # Ajusta según tu zona horaria

# Configuración de resultados
app.conf.result_backend = 'django-db'
app.conf.result_extended = True

# Configuración de serialización
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Configuración de logging
app.conf.worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
app.conf.worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarea de debug para probar Celery"""
    print(f'Request: {self.request!r}')
