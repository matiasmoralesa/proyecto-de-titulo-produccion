"""
Script para verificar historial de estados en producción
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
        
        # Verificar historial de estados
        history_url = f'{BASE_URL}/api/v1/machine-status/history/?page_size=1000'
        history_response = requests.get(history_url, headers=headers)
        
        if history_response.status_code == 200:
            history_data = history_response.json()
            history_count = history_data.get('count', len(history_data.get('results', [])))
            print("=" * 60)
            print("HISTORIAL DE ESTADOS")
            print("=" * 60)
            print(f"Total registros: {history_count}")
            
            # Agrupar por activo
            if 'results' in history_data:
                by_asset = {}
                for record in history_data['results']:
                    asset_id = record.get('asset')
                    if asset_id not in by_asset:
                        by_asset[asset_id] = 0
                    by_asset[asset_id] += 1
                
                print(f"\nRegistros por activo:")
                for asset_id, count in by_asset.items():
                    print(f"  Activo {asset_id}: {count} registros")
            
            print("=" * 60)
        else:
            print(f"Error: {history_response.status_code}")
            print(history_response.text)
    else:
        print(f"Error de login: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
