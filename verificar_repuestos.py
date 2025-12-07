"""
Script para verificar repuestos en producción
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
        print("VERIFICANDO REPUESTOS")
        print("=" * 60)
        
        # Verificar repuestos
        parts_url = f'{BASE_URL}/api/v1/inventory/spare-parts/'
        parts_response = requests.get(parts_url, headers=headers)
        
        if parts_response.status_code == 200:
            parts_data = parts_response.json()
            parts = parts_data.get('results', [])
            print(f"\n✅ Repuestos encontrados: {len(parts)}")
            
            if parts:
                print("\nPrimeros 5 repuestos:")
                for part in parts[:5]:
                    print(f"  • {part.get('name')} ({part.get('part_number')})")
                    print(f"    Stock: {part.get('quantity_in_stock', 0)}")
            else:
                print("\n⚠️  No hay repuestos creados")
        else:
            print(f"❌ Error: {parts_response.status_code}")
        
        # Verificar movimientos de stock
        movements_url = f'{BASE_URL}/api/v1/inventory/stock-movements/'
        movements_response = requests.get(movements_url, headers=headers)
        
        if movements_response.status_code == 200:
            movements_data = movements_response.json()
            movements = movements_data.get('results', [])
            print(f"\n✅ Movimientos de stock: {len(movements)}")
        else:
            print(f"\n❌ Error movimientos: {movements_response.status_code}")
        
        # Verificar endpoint de reportes
        reports_url = f'{BASE_URL}/api/v1/reports/spare-part-consumption/'
        reports_response = requests.get(reports_url, headers=headers)
        
        if reports_response.status_code == 200:
            consumption = reports_response.json()
            print(f"\n✅ Consumo de repuestos: {len(consumption)} registros")
            
            if consumption:
                print("\nTop 5 repuestos consumidos:")
                for item in consumption[:5]:
                    print(f"  • {item.get('spare_part__name', 'N/A')}")
                    print(f"    Cantidad: {item.get('total_quantity', 0)}")
            else:
                print("\n⚠️  No hay consumo de repuestos registrado")
        else:
            print(f"\n❌ Error reportes: {reports_response.status_code}")
        
        print("\n" + "=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
