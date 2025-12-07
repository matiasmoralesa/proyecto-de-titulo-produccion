"""
Script para limpiar el caché del dashboard
"""
import requests
from decouple import config

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

# Obtener token de admin
login_url = f'{BASE_URL}/api/v1/auth/login/'
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        token = response.json()['access']
        headers = {'Authorization': f'Bearer {token}'}
        
        print("=" * 60)
        print("LIMPIANDO CACHÉ DEL DASHBOARD")
        print("=" * 60)
        
        # Llamar al endpoint de limpiar caché
        cache_url = f'{BASE_URL}/api/v1/celery/clear-dashboard-cache/'
        cache_response = requests.post(cache_url, headers=headers)
        
        if cache_response.status_code == 200:
            print("✅ Caché limpiado exitosamente")
        else:
            print(f"❌ Error: {cache_response.status_code}")
            print(cache_response.text)
        
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
