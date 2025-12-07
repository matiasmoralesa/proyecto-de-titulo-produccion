"""
Script automático para cargar datos en producción
"""
import requests
from decouple import config

# URL base de la API
BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

def seed_data():
    """Generar datos de prueba"""
    url = f'{BASE_URL}/api/admin/seed-data/'
    
    print("=" * 60)
    print("GENERANDO DATOS DE PRUEBA EN PRODUCCIÓN")
    print("=" * 60)
    print(f"\n📡 URL: {url}")
    print("⏳ Cargando datos...")
    
    try:
        response = requests.post(url, timeout=300)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ ÉXITO")
            print(f"\n{data.get('message', 'Datos cargados')}")
            
            if 'details' in data:
                print(f"\n📋 Detalles:")
                for key, value in data['details'].items():
                    print(f"   {key}: {value}")
            
            return True
        else:
            print(f"\n❌ Error {response.status_code}")
            print(response.text[:500])
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    if seed_data():
        print("\n✅ Datos cargados. Ejecuta: python test_machine_status_endpoint.py")
    else:
        print("\n❌ Error al cargar datos")
