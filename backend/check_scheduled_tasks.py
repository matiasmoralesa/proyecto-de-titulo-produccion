import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django_celery_beat.models import PeriodicTask

print("\n📅 Tareas Programadas en Celery Beat:\n")

tasks = PeriodicTask.objects.all()

if not tasks.exists():
    print("⚠️  No hay tareas programadas aún.")
    print("   Las tareas se crearán automáticamente cuando Celery Beat las detecte.")
else:
    for task in tasks:
        status = "✅ Activa" if task.enabled else "❌ Inactiva"
        print(f"{status} - {task.name}")
        print(f"   Tarea: {task.task}")
        if task.crontab:
            print(f"   Horario: {task.crontab}")
        print()

print(f"\nTotal: {tasks.count()} tareas")
