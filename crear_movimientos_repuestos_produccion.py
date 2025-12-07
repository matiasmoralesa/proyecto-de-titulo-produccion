"""
Script para crear movimientos de repuestos en producción vía endpoint
"""
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.production.template')

# URL del backend en Railway
BACKEND_URL = os.getenv('VITE_API_URL', 'https://proyecto-de-titulo-produccion-production.up.railway.app')

# Token de admin (obtener del sistema)
# Necesitarás iniciar sesión primero para obtener el token
def get_admin_token():
    """Obtener token de admin"""
    login_url = f"{BACKEND_URL}/api/v1/auth/login/"
    
    # Credenciales de admin
    credentials = {
        "username": "admin",
        "password": "admin123"  # Cambiar por la contraseña real
    }
    
    print(f"🔐 Iniciando sesión en {login_url}...")
    response = requests.post(login_url, json=credentials)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Sesión iniciada correctamente")
        return data.get('access')
    else:
        print(f"❌ Error al iniciar sesión: {response.status_code}")
        print(response.text)
        return None

def create_spare_parts_movements(token):
    """Crear movimientos de repuestos"""
    url = f"{BACKEND_URL}/api/v1/inventory/seed-spare-parts-usage/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n📦 Creando movimientos de repuestos en {url}...")
    response = requests.post(url, headers=headers)
    
    if response.status_code in [200, 201]:
        print("✅ Movimientos de repuestos creados exitosamente")
        print(response.json())
        return True
    else:
        print(f"❌ Error al crear movimientos: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("CREAR MOVIMIENTOS DE REPUESTOS EN PRODUCCIÓN")
    print("=" * 60)
    
    # Obtener token
    token = get_admin_token()
    if not token:
        print("\n❌ No se pudo obtener el token de autenticación")
        return
    
    # Crear movimientos
    success = create_spare_parts_movements(token)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ PROCESO FALLIDO")
        print("=" * 60)

if __name__ == "__main__":
    main()
