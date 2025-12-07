"""
Script para verificar datos generados en producción
"""
import requests
from decouple import config

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

print("=" * 60)
print("VERIFICANDO DATOS EN PRODUCCIÓN")
print("=" * 60)

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
        
        # Verificar activos
        assets_url = f'{BASE_URL}/api/v1/assets/assets/'
        assets_response = requests.get(assets_url, headers=headers)
        if assets_response.status_code == 200:
            assets_data = assets_response.json()
            assets_count = assets_data.get('count', len(assets_data))
            print(f"\n✅ Activos: {assets_count}")
        
        # Verificar órdenes de trabajo
        wo_url = f'{BASE_URL}/api/v1/work-orders/?page_size=1000'
        wo_response = requests.get(wo_url, headers=headers)
        if wo_response.status_code == 200:
            wo_data = wo_response.json()
            wo_count = wo_data.get('count', len(wo_data))
            print(f"✅ Órdenes de trabajo: {wo_count}")
            
            # Contar por estado
            if 'results' in wo_data:
                completed = sum(1 for wo in wo_data['results'] if wo.get('status') == 'Completada')
                pending = sum(1 for wo in wo_data['results'] if wo.get('status') == 'Pendiente')
                in_progress = sum(1 for wo in wo_data['results'] if wo.get('status') == 'En Progreso')
                print(f"   - Completadas: {completed}")
                print(f"   - Pendientes: {pending}")
                print(f"   - En Progreso: {in_progress}")
        
        # Verificar dashboard
        dashboard_url = f'{BASE_URL}/api/v1/dashboard/'
        dashboard_response = requests.get(dashboard_url, headers=headers)
        if dashboard_response.status_code == 200:
            dashboard = dashboard_response.json()
            print(f"\n📊 DASHBOARD:")
            print(f"   Total OT: {dashboard.get('total_work_orders', 0)}")
            print(f"   OT Completadas: {dashboard.get('completed_work_orders', 0)}")
            print(f"   OT Pendientes: {dashboard.get('pending_work_orders', 0)}")
            print(f"   Total Activos: {dashboard.get('total_assets', 0)}")
            print(f"   Activos Activos: {dashboard.get('active_assets', 0)}")
        
        print("\n" + "=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
