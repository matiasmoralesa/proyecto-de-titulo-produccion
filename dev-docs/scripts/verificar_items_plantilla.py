"""
Script para verificar items de una plantilla específica
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
        print("VERIFICANDO ITEMS DE PLANTILLAS")
        print("=" * 60)
        
        # Obtener plantillas
        templates_url = f'{BASE_URL}/api/v1/checklists/templates/'
        templates_response = requests.get(templates_url, headers=headers)
        
        if templates_response.status_code == 200:
            templates_data = templates_response.json()
            templates = templates_data.get('results', [])
            
            # Verificar items de cada plantilla
            for template in templates:
                template_id = template['id']
                template_name = template['name']
                
                # Obtener detalle de la plantilla
                detail_url = f'{BASE_URL}/api/v1/checklists/templates/{template_id}/'
                detail_response = requests.get(detail_url, headers=headers)
                
                if detail_response.status_code == 200:
                    detail = detail_response.json()
                    items = detail.get('items', [])
                    print(f"\n{template_name}:")
                    print(f"  Items: {len(items)}")
                    if items:
                        for item in items[:3]:  # Mostrar primeros 3
                            print(f"    • {item.get('text', 'N/A')}")
                else:
                    print(f"\n{template_name}: Error {detail_response.status_code}")
        
        print("\n" + "=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
