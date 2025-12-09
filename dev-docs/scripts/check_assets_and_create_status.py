"""
Script para verificar activos y crear estados iniciales
"""
import requests
import json
from decouple import config

# URL base de la API
BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

# Credenciales de admin
USERNAME = 'admin'
PASSWORD = 'admin123'

def get_token():
    """Obtener token de autenticación"""
    url = f'{BASE_URL}/api/v1/auth/login/'
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    print(f"🔐 Obteniendo token de autenticación...")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        token = response.json()['access']
        print(f"✅ Token obtenido exitosamente")
        return token
    else:
        print(f"❌ Error obteniendo token: {response.status_code}")
        print(response.text)
        return None

def get_assets(token):
    """Obtener lista de activos"""
    url = f'{BASE_URL}/api/v1/assets/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"\n📦 Obteniendo lista de activos...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if not results and isinstance(data, list):
            results = data
        
        print(f"✅ Activos encontrados: {len(results)}")
        
        if results:
            for i, asset in enumerate(results):
                if i >= 5:
                    break
                print(f"   - {asset['name']} ({asset['vehicle_type']}) - ID: {asset['id']}")
        
        return results
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return []

def create_asset_status(token, asset_id, asset_name):
    """Crear estado inicial para un activo"""
    url = f'{BASE_URL}/api/v1/machine-status/status/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'asset': asset_id,
        'status_type': 'OPERANDO',
        'odometer_reading': 0,
        'fuel_level': 100,
        'condition_notes': 'Estado inicial del activo'
    }
    
    print(f"\n📝 Creando estado para {asset_name}...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ Estado creado exitosamente")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("VERIFICACIÓN Y CREACIÓN DE ESTADOS DE ACTIVOS")
    print("=" * 60)
    
    # 1. Obtener token
    token = get_token()
    if not token:
        print("\n❌ No se pudo obtener el token. Abortando.")
        return
    
    # 2. Obtener activos
    assets = get_assets(token)
    
    if not assets:
        print("\n⚠️  No hay activos en la base de datos.")
        print("   Primero debes cargar datos de activos.")
        return
    
    # 3. Crear estados para todos los activos
    print(f"\n🔄 Creando estados para {len(assets)} activos...")
    success_count = 0
    
    for asset in assets:
        if create_asset_status(token, asset['id'], asset['name']):
            success_count += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ Estados creados: {success_count}/{len(assets)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
