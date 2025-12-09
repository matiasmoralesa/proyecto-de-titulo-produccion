"""
Script para llamar al endpoint de seed de machine status
"""
import requests
from decouple import config

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

url = f'{BASE_URL}/api/admin/seed-machine-status/'

print("=" * 60)
print("LLAMANDO ENDPOINT DE SEED")
print("=" * 60)
print(f"\n📡 URL: {url}")
print("⏳ Ejecutando...")

try:
    response = requests.post(url, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ ÉXITO")
        print(f"\n{data.get('message', 'Datos creados')}")
    else:
        print(f"\n❌ Error {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
