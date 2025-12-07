"""
Script para limpiar datos antiguos y regenerar datos realistas
"""
import requests
from decouple import config
import time

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

print("=" * 60)
print("LIMPIEZA Y REGENERACIÓN DE DATOS")
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
        
        print("\n1️⃣  Eliminando TODAS las órdenes de trabajo antiguas...")
        
        # Obtener todas las órdenes de trabajo (paginado)
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
                print(f"   Página {page}: {len(results)} órdenes encontradas")
                
                if not wo_data.get('next'):
                    break
                
                page += 1
            else:
                print(f"   Error: {wo_response.status_code}")
                break
        
        print(f"\n   Total encontradas: {len(all_work_orders)} órdenes")
        print(f"   Eliminando...")
        
        deleted_count = 0
        for wo in all_work_orders:
            delete_url = f"{BASE_URL}/api/v1/work-orders/{wo['id']}/"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code in [204, 200]:
                deleted_count += 1
                if deleted_count % 50 == 0:
                    print(f"   Progreso: {deleted_count}/{len(all_work_orders)}")
        
        print(f"   ✅ Eliminadas: {deleted_count} órdenes")
        
        print("\n2️⃣  Eliminando historial de estados antiguo...")
        
        # Eliminar historial de estados
        history_url = f'{BASE_URL}/api/v1/machine-status/history/?page_size=1000'
        history_response = requests.get(history_url, headers=headers)
        
        if history_response.status_code == 200:
            history_data = history_response.json()
            history_records = history_data.get('results', [])
            
            print(f"   Encontrados: {len(history_records)} registros")
            print(f"   ⚠️  No se pueden eliminar vía API - se mantendrán")
        
        print("\n3️⃣  Generando nuevos datos realistas...")
        print("   ⏳ Esto puede tomar varios minutos...")
        
        # Llamar al endpoint de seed
        seed_url = f'{BASE_URL}/api/admin/seed-realistic-data/'
        seed_response = requests.post(seed_url, headers=headers, timeout=300)
        
        if seed_response.status_code == 200:
            print("   ✅ Datos generados exitosamente")
        else:
            print(f"   ❌ Error: {seed_response.status_code}")
            print(f"   {seed_response.text}")
        
        print("\n4️⃣  Verificando datos generados...")
        
        # Verificar órdenes de trabajo
        wo_response = requests.get(wo_url, headers=headers)
        if wo_response.status_code == 200:
            wo_data = wo_response.json()
            wo_count = wo_data.get('count', 0)
            completed = sum(1 for wo in wo_data.get('results', []) if wo.get('status') == 'Completada')
            pending = sum(1 for wo in wo_data.get('results', []) if wo.get('status') == 'Pendiente')
            in_progress = sum(1 for wo in wo_data.get('results', []) if wo.get('status') == 'En Progreso')
            print(f"   ✅ Órdenes de trabajo: {wo_count}")
            print(f"      - Completadas: {completed}")
            print(f"      - Pendientes: {pending}")
            print(f"      - En Progreso: {in_progress}")
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
