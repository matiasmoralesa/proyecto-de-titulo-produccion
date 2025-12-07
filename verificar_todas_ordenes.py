"""
Script para verificar TODAS las órdenes de trabajo (sin paginación)
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
        print("VERIFICANDO TODAS LAS ÓRDENES DE TRABAJO")
        print("=" * 60)
        
        # Obtener todas las órdenes (sin límite de paginación)
        all_work_orders = []
        page = 1
        
        while True:
            wo_url = f'{BASE_URL}/api/v1/work-orders/?page={page}&page_size=100'
            wo_response = requests.get(wo_url, headers=headers)
            
            if wo_response.status_code == 200:
                wo_data = wo_response.json()
                results = wo_data.get('results', [])
                
                if not results:
                    break
                
                all_work_orders.extend(results)
                print(f"Página {page}: {len(results)} órdenes")
                
                if not wo_data.get('next'):
                    break
                
                page += 1
            else:
                print(f"Error: {wo_response.status_code}")
                break
        
        # Contar por estado
        completed = sum(1 for wo in all_work_orders if wo.get('status') == 'Completada')
        pending = sum(1 for wo in all_work_orders if wo.get('status') == 'Pendiente')
        in_progress = sum(1 for wo in all_work_orders if wo.get('status') == 'En Progreso')
        cancelled = sum(1 for wo in all_work_orders if wo.get('status') == 'Cancelada')
        
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"Total órdenes: {len(all_work_orders)}")
        print(f"  - Completadas: {completed} ({completed/len(all_work_orders)*100:.1f}%)")
        print(f"  - Pendientes: {pending}")
        print(f"  - En Progreso: {in_progress}")
        print(f"  - Canceladas: {cancelled}")
        print("=" * 60)
        
    else:
        print(f"Error de login: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
