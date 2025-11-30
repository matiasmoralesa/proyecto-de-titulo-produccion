# Celery - Sistema de Tareas Automáticas

## 🎯 ¿Qué hace Celery en este proyecto?

Celery ejecuta tareas automáticamente en segundo plano, sin que tengas que estar presente:

### Tareas Programadas Automáticas

1. **Predicciones ML Diarias** (6:00 AM)
   - Analiza todos los activos
   - Genera predicciones de fallos
   - Crea órdenes de trabajo automáticamente
   - Envía notificaciones

2. **Verificación de Activos Críticos** (Cada hora)
   - Revisa activos fuera de servicio
   - Detecta predicciones de alto riesgo
   - Envía alertas si hay situaciones críticas

3. **Órdenes Vencidas** (Cada 30 minutos)
   - Detecta órdenes de trabajo vencidas
   - Envía recordatorios a operadores

4. **Reporte Semanal** (Lunes 8:00 AM)
   - Genera estadísticas de la semana
   - Envía a supervisores y admins

5. **Limpieza de Notificaciones** (Medianoche)
   - Elimina notificaciones antiguas (>30 días)
   - Mantiene la base de datos limpia

## 🚀 Instalación y Configuración

### 1. Instalar Redis (Requerido)

Redis es el "mensajero" que Celery usa para gestionar tareas.

**Windows:**
```bash
# Opción A: Usar WSL (recomendado)
wsl --install
# Luego en WSL:
sudo apt-get update
sudo apt-get install redis-server
redis-server

# Opción B: Usar Memurai (Redis para Windows)
# Descargar de: https://www.memurai.com/
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
redis-server

# Mac
brew install redis
redis-server
```

**Docker (más fácil):**
```bash
docker run -d -p 6379:6379 redis:latest
```

### 2. Verificar que Redis esté corriendo

```bash
redis-cli ping
# Debe responder: PONG
```

## 🎮 Comandos para Usar Celery

### Iniciar Celery Worker (Ejecutor de Tareas)

```bash
# En una terminal (dejar corriendo)
cd backend
celery -A config worker -l info

# En Windows, agregar --pool=solo
celery -A config worker -l info --pool=solo
```

### Iniciar Celery Beat (Programador de Tareas)

```bash
# En OTRA terminal (dejar corriendo)
cd backend
celery -A config beat -l info
```

### Iniciar Ambos a la Vez (Desarrollo)

```bash
# Solo para desarrollo
celery -A config worker --beat -l info --pool=solo
```

## 📊 Monitorear Celery

### Ver Tareas Programadas

```bash
# En Django shell
python manage.py shell

>>> from django_celery_beat.models import PeriodicTask
>>> for task in PeriodicTask.objects.all():
...     print(f"{task.name}: {task.enabled}")
```

### Ver Resultados de Tareas

```bash
# Django Admin
http://localhost:8000/admin/django_celery_results/taskresult/

# O en shell
>>> from django_celery_results.models import TaskResult
>>> TaskResult.objects.all().order_by('-date_done')[:5]
```

### Flower (UI Web para Celery) - Opcional

```bash
pip install flower
celery -A config flower

# Abrir: http://localhost:5555
```

## 🧪 Probar Tareas Manualmente

### Ejecutar Predicciones Ahora

```python
# En Django shell
python manage.py shell

>>> from apps.ml_predictions.tasks import run_daily_predictions
>>> result = run_daily_predictions.delay()
>>> result.get()  # Esperar resultado
```

### Ejecutar Cualquier Tarea

```python
>>> from apps.assets.tasks import check_critical_assets
>>> result = check_critical_assets.delay()
>>> result.get()

>>> from apps.reports.tasks import generate_weekly_report
>>> result = generate_weekly_report.delay()
>>> result.get()
```

## 📝 Tareas Disponibles

### ML Predictions
- `run_daily_predictions` - Predicciones diarias (automático 6 AM)
- `predict_single_asset(asset_id)` - Predecir un activo específico
- `train_model(samples=1000)` - Entrenar modelo ML

### Assets
- `check_critical_assets` - Verificar activos críticos (automático cada hora)
- `send_critical_alert` - Enviar alerta crítica

### Work Orders
- `check_overdue_workorders` - Verificar órdenes vencidas (automático cada 30 min)
- `send_overdue_notification(wo_id)` - Notificar orden vencida

### Reports
- `generate_weekly_report` - Reporte semanal (automático lunes 8 AM)
- `generate_monthly_report` - Reporte mensual

### Notifications
- `cleanup_old_notifications` - Limpiar notificaciones (automático medianoche)
- `send_daily_summary` - Resumen diario

## ⚙️ Configuración Avanzada

### Cambiar Horarios de Tareas

Editar `backend/config/celery.py`:

```python
app.conf.beat_schedule = {
    'run-daily-predictions': {
        'task': 'apps.ml_predictions.tasks.run_daily_predictions',
        'schedule': crontab(hour=6, minute=0),  # Cambiar hora aquí
    },
}
```

### Ejemplos de Crontab

```python
crontab(hour=6, minute=0)           # 6:00 AM diario
crontab(hour='*/2')                 # Cada 2 horas
crontab(minute='*/30')              # Cada 30 minutos
crontab(day_of_week=1, hour=8)     # Lunes 8 AM
crontab(day_of_month=1, hour=0)    # Día 1 de cada mes a medianoche
```

### Cambiar Zona Horaria

En `backend/config/settings/base.py`:

```python
CELERY_TIMEZONE = 'America/Santiago'  # Cambiar según tu zona
```

## 🐛 Troubleshooting

### Error: "Cannot connect to Redis"

```bash
# Verificar que Redis esté corriendo
redis-cli ping

# Si no responde, iniciar Redis
redis-server
```

### Error: "Task not registered"

```bash
# Reiniciar Celery worker
# Ctrl+C para detener
celery -A config worker -l info --pool=solo
```

### Ver Logs Detallados

```bash
# Worker con logs debug
celery -A config worker -l debug --pool=solo

# Beat con logs debug
celery -A config beat -l debug
```

### Limpiar Tareas Pendientes

```python
# En Django shell
>>> from config.celery import app
>>> app.control.purge()
```

## 📈 Producción

### Usar Supervisor (Linux)

```ini
# /etc/supervisor/conf.d/celery.conf
[program:celery-worker]
command=/path/to/venv/bin/celery -A config worker -l info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true

[program:celery-beat]
command=/path/to/venv/bin/celery -A config beat -l info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true
```

### Usar Systemd (Linux)

```ini
# /etc/systemd/system/celery.service
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
ExecStart=/path/to/venv/bin/celery -A config worker -l info

[Install]
WantedBy=multi-user.target
```

## ✅ Verificar que Todo Funciona

```bash
# 1. Redis corriendo
redis-cli ping
# Debe responder: PONG

# 2. Celery worker corriendo
celery -A config inspect active
# Debe mostrar workers activos

# 3. Celery beat corriendo
celery -A config inspect scheduled
# Debe mostrar tareas programadas

# 4. Ejecutar tarea de prueba
python manage.py shell
>>> from config.celery import debug_task
>>> result = debug_task.delay()
>>> result.get()
```

## 🎯 Resumen

**Para desarrollo:**
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Django
python manage.py runserver

# Terminal 3: Celery (worker + beat)
celery -A config worker --beat -l info --pool=solo
```

**Para producción:**
- Usar Supervisor o Systemd
- Múltiples workers para escalabilidad
- Monitoreo con Flower
- Logs centralizados

## 📞 Comandos Rápidos

```bash
# Iniciar todo (desarrollo)
redis-server &
python manage.py runserver &
celery -A config worker --beat -l info --pool=solo

# Ver tareas programadas
python manage.py shell -c "from django_celery_beat.models import PeriodicTask; [print(t.name) for t in PeriodicTask.objects.all()]"

# Ejecutar predicciones manualmente
python manage.py shell -c "from apps.ml_predictions.tasks import run_daily_predictions; run_daily_predictions.delay()"

# Ver últimos resultados
python manage.py shell -c "from django_celery_results.models import TaskResult; [print(f'{t.task_name}: {t.status}') for t in TaskResult.objects.all()[:5]]"
```

¡Celery está listo para automatizar tu CMMS! 🚀
