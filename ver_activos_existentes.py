"""
Script para ver activos existentes en producción
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
        
        # Obtener activos
        assets_url = f'{BASE_URL}/api/v1/assets/assets/'
        assets_response = requests.get(assets_url, headers=headers)
        
        if assets_response.status_code == 200:
            data = assets_response.json()
            print(f"DEBUG - Tipo de respuesta: {type(data)}")
            print(f"DEBUG - Keys: {data.keys() if isinstance(data, dict) else 'Es una lista'}")
            print(f"DEBUG - Respuesta completa: {data}")
            
            # Puede ser una lista o un objeto con 'results'
            assets = data if isinstance(data, list) else data.get('results', [])
            print("\n" + "=" * 60)
            print("ACTIVOS EXISTENTES EN PRODUCCIÓN")
            print("=" * 60)
            for i, asset in enumerate(assets, 1):
                print(f"\n{i}. {asset['name']}")
                print(f"   ID: {asset['id']}")
                print(f"   Serial: {asset['serial_number']}")
                print(f"   Tipo: {asset['vehicle_type']}")
                print(f"   Modelo: {asset.get('model', 'N/A')}")
                print(f"   Placa: {asset.get('license_plate', 'N/A')}")
            print("\n" + "=" * 60)
            print(f"Total: {len(assets)} activos")
            print("=" * 60)
        else:
            print(f"Error: {assets_response.status_code}")
            print(assets_response.text)
    else:
        print(f"Error de login: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
