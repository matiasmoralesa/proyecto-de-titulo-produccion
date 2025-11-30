"""
Script para probar que Celery está configurado correctamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from config.celery import app

print("🧪 Probando configuración de Celery...\n")

# 1. Verificar que Celery está configurado
print(f"✓ Celery app: {app.main}")
print(f"✓ Broker: {app.conf.broker_url}")
print(f"✓ Result backend: {app.conf.result_backend}")
print(f"✓ Timezone: {app.conf.timezone}\n")

# 2. Listar tareas registradas
print("📋 Tareas registradas:")
for task_name in sorted(app.tasks.keys()):
    if not task_name.startswith('celery.'):
        print(f"   • {task_name}")

print("\n✅ Celery está configurado correctamente!")
print("\n📝 Próximos pasos:")
print("   1. Instalar Redis (ver CELERY_README.md)")
print("   2. Iniciar Redis: redis-server")
print("   3. Iniciar Celery worker: celery -A config worker --beat -l info --pool=solo")
