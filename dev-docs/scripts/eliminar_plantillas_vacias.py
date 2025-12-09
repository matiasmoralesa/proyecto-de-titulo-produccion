"""
Script para eliminar plantillas de checklist sin items
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
        print("ELIMINANDO PLANTILLAS VACÍAS")
        print("=" * 60)
        
        # Obtener plantillas
        templates_url = f'{BASE_URL}/api/v1/checklists/templates/'
        templates_response = requests.get(templates_url, headers=headers)
        
        if templates_response.status_code == 200:
            templates_data = templates_response.json()
            templates = templates_data.get('results', [])
            
            print(f"\nEncontradas: {len(templates)} plantillas")
            
            # Eliminar solo las 3 nuevas que no tienen items
            codes_to_delete = ['INSP-DIARIA', 'MANT-MENSUAL', 'INSP-SEGURIDAD']
            
            deleted = 0
            for template in templates:
                if template['code'] in codes_to_delete and template.get('item_count', 0) == 0:
                    delete_url = f"{BASE_URL}/api/v1/checklists/templates/{template['id']}/"
                    delete_response = requests.delete(delete_url, headers=headers)
                    if delete_response.status_code in [204, 200]:
                        deleted += 1
                        print(f"   ✅ Eliminada: {template['name']}")
                    else:
                        print(f"   ❌ Error eliminando {template['name']}: {delete_response.status_code}")
            
            print(f"\n✅ Total eliminadas: {deleted}")
        else:
            print(f"❌ Error: {templates_response.status_code}")
        
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
