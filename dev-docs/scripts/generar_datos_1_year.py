"""
Script para generar datos realistas de 1 año
"""
import requests
from decouple import config

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

url = f'{BASE_URL}/api/admin/seed-realistic-data/'

print("=" * 60)
print("GENERANDO DATOS REALISTAS - 1 AÑO")
print("=" * 60)
print(f"\n📡 URL: {url}")
print("⏳ Esto puede tomar varios minutos...")
print("\nGenerando:")
print("  - Activos adicionales (si es necesario)")
print("  - Órdenes de trabajo completadas (12-24 por activo)")
print("  - Actualizaciones de estado (24-48 por activo)")
print("  - Planes de mantenimiento")
print("  - Historial de 1 año completo")
print()

try:
    response = requests.post(url, timeout=600)  # 10 minutos timeout
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ ÉXITO")
        print(f"\n{data.get('message', 'Datos generados')}")
    else:
        print(f"\n❌ Error {response.status_code}")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print(f"\n⏱️  Timeout: La solicitud tomó más de 10 minutos")
    print(f"   Los datos pueden estar generándose en segundo plano")
    print(f"   Espera unos minutos y verifica en la aplicación")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
print("Para verificar los datos:")
print("  1. Accede a la aplicación web")
print("  2. Ve a 'Estado de Máquina'")
print("  3. Selecciona un activo")
print("  4. Revisa el historial de actividades")
print("=" * 60)
