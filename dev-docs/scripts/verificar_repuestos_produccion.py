"""
Script para verificar datos de repuestos en producción
"""
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.production.template')

# URL del backend en Railway
BACKEND_URL = os.getenv('VITE_API_URL', 'https://proyecto-de-titulo-produccion-production.up.railway.app')

def get_admin_token():
    """Obtener token de admin"""
    login_url = f"{BACKEND_URL}/api/v1/auth/login/"
    
    credentials = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(login_url, json=credentials)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access')
    return None

def verify_spare_parts(token):
    """Verificar repuestos"""
    url = f"{BACKEND_URL}/api/v1/inventory/spare-parts/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📦 REPUESTOS:")
    print("=" * 60)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        print(f"Total de repuestos: {len(results)}\n")
        
        for part in results:
            print(f"  • {part['name']}")
            print(f"    - Número de parte: {part['part_number']}")
            print(f"    - Stock actual: {part['quantity']}")
            print(f"    - Stock mínimo: {part['min_quantity']}")
            print()
    else:
        print(f"❌ Error: {response.status_code}")

def verify_stock_movements(token):
    """Verificar movimientos de stock"""
    url = f"{BACKEND_URL}/api/v1/inventory/stock-movements/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📊 MOVIMIENTOS DE STOCK:")
    print("=" * 60)
    response = requests.get(url, headers=headers, params={'page_size': 10})
    
    if response.status_code == 200:
        data = response.json()
        total = data.get('count', 0)
        results = data.get('results', [])
        
        print(f"Total de movimientos: {total}")
        print(f"Mostrando últimos 10:\n")
        
        for movement in results[:10]:
            spare_part = movement.get('spare_part', {})
            spare_part_name = spare_part.get('name', 'N/A') if isinstance(spare_part, dict) else 'N/A'
            print(f"  • {spare_part_name}")
            print(f"    - Tipo: {movement['movement_type']}")
            print(f"    - Cantidad: {movement['quantity']}")
            print(f"    - Antes: {movement['quantity_before']} → Después: {movement['quantity_after']}")
            print(f"    - Notas: {movement.get('notes', 'N/A')}")
            print()
    else:
        print(f"❌ Error: {response.status_code}")

def verify_consumption_report(token):
    """Verificar reporte de consumo"""
    url = f"{BACKEND_URL}/api/v1/reports/spare_part_consumption/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📈 REPORTE DE CONSUMO DE REPUESTOS:")
    print("=" * 60)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total de repuestos con consumo: {len(data)}\n")
        
        for item in data[:10]:
            print(f"  • {item['spare_part__name']}")
            print(f"    - Número de parte: {item['spare_part__part_number']}")
            print(f"    - Cantidad consumida: {item['total_quantity']}")
            print(f"    - Número de movimientos: {item['movement_count']}")
            print()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def main():
    print("=" * 60)
    print("VERIFICACIÓN DE REPUESTOS EN PRODUCCIÓN")
    print("=" * 60)
    
    token = get_admin_token()
    if not token:
        print("\n❌ No se pudo obtener el token de autenticación")
        return
    
    verify_spare_parts(token)
    verify_stock_movements(token)
    verify_consumption_report(token)
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    main()
