"""
Script para probar el endpoint de historial de estado de máquina
"""
import requests
import json
import os
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

def test_asset_statuses(token):
    """Probar endpoint de estados de activos"""
    url = f'{BASE_URL}/api/v1/machine-status/status/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"\n📊 Probando endpoint de estados de activos...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data)
        print(f"✅ Estados obtenidos: {len(results)} activos")
        
        if results:
            print(f"\n📋 Primer activo:")
            print(json.dumps(results[0], indent=2))
            return results[0]['asset']  # Retornar ID del primer activo
        return None
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_asset_history(token, asset_id):
    """Probar endpoint de historial de activo"""
    url = f'{BASE_URL}/api/v1/machine-status/asset-history/{asset_id}/complete-history/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"\n📜 Probando endpoint de historial completo para activo {asset_id}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        print(f"✅ Historial obtenido: {len(results)} actividades")
        print(f"   Total count: {data.get('count', 0)}")
        
        if results:
            print(f"\n📋 Primera actividad:")
            print(json.dumps(results[0], indent=2))
        else:
            print("⚠️  No hay actividades en el historial")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_asset_kpis(token, asset_id):
    """Probar endpoint de KPIs de activo"""
    url = f'{BASE_URL}/api/v1/machine-status/asset-history/{asset_id}/kpis/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"\n📈 Probando endpoint de KPIs para activo {asset_id}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ KPIs obtenidos exitosamente")
        print(f"\n📊 KPIs:")
        print(json.dumps(data['kpis'], indent=2))
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_status_history(token):
    """Probar endpoint de historial de estados"""
    url = f'{BASE_URL}/api/v1/machine-status/history/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"\n📜 Probando endpoint de historial de estados...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data)
        print(f"✅ Historial obtenido: {len(results)} registros")
        
        if results:
            print(f"\n📋 Primer registro:")
            print(json.dumps(results[0], indent=2))
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("PRUEBA DE ENDPOINTS DE ESTADO DE MÁQUINA")
    print("=" * 60)
    
    # 1. Obtener token
    token = get_token()
    if not token:
        print("\n❌ No se pudo obtener el token. Abortando pruebas.")
        return
    
    # 2. Probar estados de activos
    asset_id = test_asset_statuses(token)
    
    # 3. Probar historial de estados
    test_status_history(token)
    
    # 4. Si hay un activo, probar su historial completo
    if asset_id:
        test_asset_history(token, asset_id)
        test_asset_kpis(token, asset_id)
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == '__main__':
    main()
