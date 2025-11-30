"""
Prueba de ejecución de tarea de Celery
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.ml_predictions.tasks import run_daily_predictions
import time

print("🧪 Probando ejecución de tarea de Celery...\n")
print("📤 Enviando tarea: run_daily_predictions")

# Enviar tarea a Celery
result = run_daily_predictions.delay()

print(f"✓ Tarea enviada con ID: {result.id}")
print(f"📊 Estado: {result.state}")
print("\n⏳ Esperando resultado (esto puede tardar un momento)...\n")

# Esperar resultado (máximo 60 segundos)
try:
    output = result.get(timeout=60)
    print("✅ Tarea completada exitosamente!")
    print(f"\n📋 Resultado:")
    for key, value in output.items():
        print(f"   {key}: {value}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
