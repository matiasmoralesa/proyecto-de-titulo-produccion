#!/usr/bin/env python
"""
Script para ejecutar el reset de datos en Railway.
Este script se puede ejecutar directamente en Railway.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar y ejecutar el comando
from django.core.management import call_command

print("=" * 60)
print("🚀 EJECUTANDO RESET DE DATOS EN RAILWAY")
print("=" * 60)
print()

try:
    call_command('reset_and_populate', '--no-input')
    print("\n✅ Proceso completado exitosamente")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
