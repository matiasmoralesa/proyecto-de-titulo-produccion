"""
Script para cargar datos en producción usando el endpoint de admin
"""
import requests
from decouple import config

# URL base de la API
BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

def load_data_via_endpoint():
    """Cargar datos usando el endpoint de admin"""
    url = f'{BASE_URL}/api/admin/load-data/'
    
    print("=" * 60)
    print("CARGANDO DATOS EN PRODUCCIÓN")
    print("=" * 60)
    print(f"\n📡 Enviando solicitud a: {url}")
    print("⏳ Esto puede tomar varios minutos...")
    
    try:
        response = requests.post(url, timeout=300)  # 5 minutos de timeout
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ DATOS CARGADOS EXITOSAMENTE")
            print(f"\n📊 Resumen:")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
            
            if 'details' in data:
                print(f"\n📋 Detalles:")
                for key, value in data['details'].items():
                    print(f"   - {key}: {value}")
            
            return True
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️  Timeout: La solicitud tomó más de 5 minutos")
        print(f"   Los datos pueden estar cargándose en segundo plano")
        print(f"   Espera unos minutos y verifica con el script de prueba")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def seed_data_via_endpoint():
    """Generar datos de prueba usando el endpoint de seed"""
    url = f'{BASE_URL}/api/admin/seed-data/'
    
    print("\n" + "=" * 60)
    print("GENERANDO DATOS DE PRUEBA")
    print("=" * 60)
    print(f"\n📡 Enviando solicitud a: {url}")
    print("⏳ Esto puede tomar varios minutos...")
    
    try:
        response = requests.post(url, timeout=300)  # 5 minutos de timeout
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ DATOS GENERADOS EXITOSAMENTE")
            print(f"\n📊 Resumen:")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
            
            if 'details' in data:
                print(f"\n📋 Detalles:")
                for key, value in data['details'].items():
                    print(f"   - {key}: {value}")
            
            return True
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️  Timeout: La solicitud tomó más de 5 minutos")
        print(f"   Los datos pueden estar generándose en segundo plano")
        print(f"   Espera unos minutos y verifica con el script de prueba")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    print("\n🚀 CARGA DE DATOS EN PRODUCCIÓN")
    print("\nOpciones:")
    print("1. Cargar desde backup (load-data)")
    print("2. Generar datos de prueba (seed-data)")
    
    choice = input("\nSelecciona una opción (1 o 2): ").strip()
    
    if choice == '1':
        success = load_data_via_endpoint()
    elif choice == '2':
        success = seed_data_via_endpoint()
    else:
        print("❌ Opción inválida")
        return
    
    if success:
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python test_machine_status_endpoint.py")
        print("2. Ejecuta: python check_assets_and_create_status.py")
        print("3. Accede a la aplicación y verifica los datos")
    else:
        print("\n" + "=" * 60)
        print("⚠️  PROCESO CON ERRORES")
        print("=" * 60)
        print("\n📝 Alternativas:")
        print("1. Intenta nuevamente en unos minutos")
        print("2. Usa Railway Shell: railway shell")
        print("3. Contacta al administrador del sistema")

if __name__ == '__main__':
    main()
