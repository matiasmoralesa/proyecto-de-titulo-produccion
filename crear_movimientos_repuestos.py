"""
Script para crear movimientos de repuestos de ejemplo
"""
import requests
from decouple import config
import random
from datetime import datetime, timedelta

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
        print("CREANDO MOVIMIENTOS DE REPUESTOS")
        print("=" * 60)
        
        # Obtener repuestos
        parts_url = f'{BASE_URL}/api/v1/inventory/spare-parts/'
        parts_response = requests.get(parts_url, headers=headers)
        
        if parts_response.status_code != 200:
            print("❌ Error obteniendo repuestos")
            exit(1)
        
        parts = parts_response.json().get('results', [])
        print(f"\n✅ Repuestos encontrados: {len(parts)}")
        
        # Obtener órdenes de trabajo
        wo_url = f'{BASE_URL}/api/v1/work-orders/?page_size=50'
        wo_response = requests.get(wo_url, headers=headers)
        
        if wo_response.status_code != 200:
            print("❌ Error obteniendo órdenes de trabajo")
            exit(1)
        
        work_orders = wo_response.json().get('results', [])
        print(f"✅ Órdenes de trabajo encontradas: {len(work_orders)}")
        
        if not parts or not work_orders:
            print("\n⚠️  No hay suficientes datos para crear movimientos")
            exit(1)
        
        # Crear movimientos de entrada primero (para tener stock)
        print("\n📦 Creando movimientos de ENTRADA...")
        for part in parts:
            movement_data = {
                'spare_part': part['id'],
                'movement_type': 'IN',
                'quantity': random.randint(50, 200),
                'unit_cost': random.uniform(10, 500),
                'notes': 'Stock inicial - Compra de repuestos'
            }
            
            movement_url = f'{BASE_URL}/api/v1/inventory/stock-movements/'
            movement_response = requests.post(movement_url, json=movement_data, headers=headers)
            
            if movement_response.status_code in [200, 201]:
                print(f"  ✅ Entrada: {part['name']} - {movement_data['quantity']} unidades")
            else:
                print(f"  ❌ Error: {movement_response.status_code}")
        
        # Crear movimientos de salida (consumo en órdenes de trabajo)
        print("\n📤 Creando movimientos de SALIDA...")
        movements_created = 0
        
        for i in range(30):  # Crear 30 movimientos de salida
            part = random.choice(parts)
            wo = random.choice(work_orders)
            
            movement_data = {
                'spare_part': part['id'],
                'movement_type': 'OUT',
                'quantity': random.randint(1, 10),
                'unit_cost': random.uniform(10, 500),
                'reference_type': 'work_order',
                'reference_id': wo['id'],
                'notes': f'Usado en OT {wo["work_order_number"]}'
            }
            
            movement_url = f'{BASE_URL}/api/v1/inventory/stock-movements/'
            movement_response = requests.post(movement_url, json=movement_data, headers=headers)
            
            if movement_response.status_code in [200, 201]:
                movements_created += 1
                if movements_created % 10 == 0:
                    print(f"  Creados: {movements_created}/30")
            else:
                print(f"  ❌ Error: {movement_response.status_code} - {movement_response.text[:100]}")
        
        print(f"\n✅ Total movimientos de salida creados: {movements_created}")
        
        # Verificar consumo
        print("\n📊 Verificando consumo de repuestos...")
        reports_url = f'{BASE_URL}/api/v1/reports/spare-part-consumption/'
        reports_response = requests.get(reports_url, headers=headers)
        
        if reports_response.status_code == 200:
            consumption = reports_response.json()
            print(f"✅ Registros de consumo: {len(consumption)}")
            
            if consumption:
                print("\nTop 5 repuestos consumidos:")
                for item in consumption[:5]:
                    print(f"  • {item.get('spare_part__name', 'N/A')}: {item.get('total_quantity', 0)} unidades")
        else:
            print(f"❌ Error en reportes: {reports_response.status_code}")
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
