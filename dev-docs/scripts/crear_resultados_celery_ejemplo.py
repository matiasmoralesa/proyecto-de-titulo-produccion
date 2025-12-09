"""
Script para crear resultados de ejemplo de Celery en la base de datos
"""
import requests
from decouple import config
import json
from datetime import datetime, timedelta
import random

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

# Obtener token de admin
login_url = f'{BASE_URL}/api/v1/auth/login/'
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

print("=" * 60)
print("CREANDO RESULTADOS DE EJEMPLO DE CELERY")
print("=" * 60)

# Nota: Este script requiere acceso directo a la base de datos
# Como alternativa, voy a crear un endpoint en Django para generar datos de ejemplo

print("\n⚠️  Para crear resultados de Celery de ejemplo, necesitas:")
print("1. Tener Celery Worker ejecutándose")
print("2. O crear un endpoint en Django que inserte datos de ejemplo")
print("\n💡 Recomendación:")
print("   - Configura Celery Worker en Railway")
print("   - O usa el botón 'Actualizar' en el Monitor de Celery")
print("   - Las tareas se ejecutarán automáticamente cuando el worker esté activo")

print("\n" + "=" * 60)
