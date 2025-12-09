"""
Script para verificar checklists generados
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
        print("VERIFICANDO CHECKLISTS")
        print("=" * 60)
        
        # 1. Verificar plantillas
        templates_url = f'{BASE_URL}/api/v1/checklists/templates/'
        templates_response = requests.get(templates_url, headers=headers)
        
        if templates_response.status_code == 200:
            templates_data = templates_response.json()
            templates = templates_data.get('results', [])
            print(f"\n✅ Plantillas de checklist: {len(templates)}")
            for template in templates:
                print(f"   • {template['name']} ({template['code']})")
                print(f"     Items: {template.get('item_count', 0)}")
        else:
            print(f"❌ Error plantillas: {templates_response.status_code}")
        
        # 2. Verificar respuestas completadas
        responses_url = f'{BASE_URL}/api/v1/checklists/responses/?page_size=1000'
        responses_response = requests.get(responses_url, headers=headers)
        
        if responses_response.status_code == 200:
            responses_data = responses_response.json()
            
            # Contar todas las páginas
            all_responses = []
            page = 1
            
            while True:
                page_url = f'{BASE_URL}/api/v1/checklists/responses/?page={page}&page_size=100'
                page_response = requests.get(page_url, headers=headers)
                
                if page_response.status_code == 200:
                    page_data = page_response.json()
                    results = page_data.get('results', [])
                    
                    if not results:
                        break
                    
                    all_responses.extend(results)
                    
                    if not page_data.get('next'):
                        break
                    
                    page += 1
                else:
                    break
            
            print(f"\n✅ Checklists completados: {len(all_responses)}")
            
            # Agrupar por plantilla
            by_template = {}
            for resp in all_responses:
                template_name = resp.get('template_name', 'Unknown')
                if template_name not in by_template:
                    by_template[template_name] = 0
                by_template[template_name] += 1
            
            print(f"\nPor plantilla:")
            for template_name, count in by_template.items():
                print(f"   • {template_name}: {count}")
            
            # Mostrar últimos 5
            print(f"\nÚltimos 5 checklists:")
            for resp in all_responses[:5]:
                print(f"   • {resp.get('template_name')} - {resp.get('asset_name')}")
                print(f"     Completado: {resp.get('completed_at', 'N/A')[:10]}")
        else:
            print(f"❌ Error respuestas: {responses_response.status_code}")
        
        print("\n" + "=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
