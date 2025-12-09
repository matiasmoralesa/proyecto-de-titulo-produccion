"""
Script para probar el endpoint de exportación de órdenes de trabajo
"""
import requests
from decouple import config

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

# Credenciales
USERNAME = 'admin'
PASSWORD = 'admin123'

def get_token():
    """Obtener token de autenticación"""
    url = f'{BASE_URL}/api/v1/auth/login/'
    data = {'username': USERNAME, 'password': PASSWORD}
    
    print("🔐 Obteniendo token...")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        token = response.json()['access']
        print("✅ Token obtenido")
        return token
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_export_work_orders(token):
    """Probar endpoint de exportación"""
    url = f'{BASE_URL}/api/v1/reports/export_work_orders/'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Parámetros de fecha (últimos 30 días)
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }
    
    print(f"\n📊 Probando exportación de órdenes de trabajo...")
    print(f"   URL: {url}")
    print(f"   Rango: {start_date.date()} a {end_date.date()}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Exportación exitosa")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Tamaño: {len(response.content)} bytes")
            
            # Guardar archivo
            filename = 'test_work_orders.csv'
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   Archivo guardado: {filename}")
            
            # Mostrar primeras líneas
            print(f"\n📄 Primeras líneas del CSV:")
            print(response.content.decode('utf-8')[:500])
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Excepción: {e}")

def main():
    print("=" * 60)
    print("PRUEBA DE EXPORTACIÓN DE ÓRDENES DE TRABAJO")
    print("=" * 60)
    
    token = get_token()
    if not token:
        return
    
    test_export_work_orders(token)
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == '__main__':
    main()
