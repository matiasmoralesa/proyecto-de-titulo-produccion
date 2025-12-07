"""
Script para crear datos directamente en Railway usando Django shell
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.railway')

# Setup Django
import sys
sys.path.insert(0, 'backend')
django.setup()

from apps.assets.models import Asset, Location
from apps.authentication.models import User
from apps.machine_status.models import AssetStatus

print("=" * 60)
print("CREANDO DATOS EN RAILWAY")
print("=" * 60)

# Obtener usuario admin
try:
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No se encontró usuario admin")
        exit(1)
    print(f"✅ Usuario admin encontrado: {admin_user.username}")
except Exception as e:
    print(f"❌ Error obteniendo admin: {e}")
    exit(1)

# Crear ubicación
print("\n📍 Creando ubicación...")
try:
    location, created = Location.objects.get_or_create(
        name="Sede Principal",
        defaults={
            'address': 'Av. Principal 123',
            'city': 'Santiago',
            'country': 'Chile'
        }
    )
    if created:
        print(f"✅ Ubicación creada: {location.name}")
    else:
        print(f"ℹ️  Ubicación ya existe: {location.name}")
except Exception as e:
    print(f"❌ Error creando ubicación: {e}")
    exit(1)

# Crear activos
print("\n🚗 Creando activos...")
assets_data = [
    {
        'name': 'Camión Volvo 1',
        'vehicle_type': 'Camión',
        'model': 'Volvo FH16',
        'serial_number': 'CAM001',
        'license_plate': 'ABC-123'
    },
    {
        'name': 'Grúa Liebherr 1',
        'vehicle_type': 'Grúa',
        'model': 'Liebherr LTM 1100',
        'serial_number': 'GRU001',
        'license_plate': 'DEF-456'
    },
    {
        'name': 'Excavadora CAT 1',
        'vehicle_type': 'Excavadora',
        'model': 'CAT 320',
        'serial_number': 'EXC001',
        'license_plate': 'GHI-789'
    },
    {
        'name': 'Retroexcavadora JCB 1',
        'vehicle_type': 'Retroexcavadora',
        'model': 'JCB 3CX',
        'serial_number': 'RET001',
        'license_plate': 'JKL-012'
    },
    {
        'name': 'Montacargas Toyota 1',
        'vehicle_type': 'Montacargas',
        'model': 'Toyota 8FG25',
        'serial_number': 'MON001',
        'license_plate': 'MNO-345'
    }
]

created_count = 0
for asset_data in assets_data:
    try:
        asset, created = Asset.objects.get_or_create(
            serial_number=asset_data['serial_number'],
            defaults={
                **asset_data,
                'location': location,
                'status': 'ACTIVE',
                'purchase_date': '2023-01-01',
                'manufacturer': asset_data['model'].split()[0]
            }
        )
        
        if created:
            print(f"✅ Activo creado: {asset.name}")
            created_count += 1
            
            # Crear estado inicial
            try:
                status, status_created = AssetStatus.objects.get_or_create(
                    asset=asset,
                    defaults={
                        'status_type': 'OPERANDO',
                        'fuel_level': 100,
                        'odometer_reading': 0,
                        'condition_notes': 'Estado inicial del activo',
                        'last_updated_by': admin_user
                    }
                )
                if status_created:
                    print(f"   ✅ Estado creado: OPERANDO (100% combustible)")
            except Exception as e:
                print(f"   ⚠️  Error creando estado: {e}")
        else:
            print(f"ℹ️  Activo ya existe: {asset.name}")
            
            # Verificar si tiene estado
            if not hasattr(asset, 'current_status') or not AssetStatus.objects.filter(asset=asset).exists():
                try:
                    status, status_created = AssetStatus.objects.get_or_create(
                        asset=asset,
                        defaults={
                            'status_type': 'OPERANDO',
                            'fuel_level': 100,
                            'odometer_reading': 0,
                            'condition_notes': 'Estado inicial del activo',
                            'last_updated_by': admin_user
                        }
                    )
                    if status_created:
                        print(f"   ✅ Estado creado: OPERANDO (100% combustible)")
                except Exception as e:
                    print(f"   ⚠️  Error creando estado: {e}")
                    
    except Exception as e:
        print(f"❌ Error creando activo {asset_data['name']}: {e}")

print("\n" + "=" * 60)
print(f"✅ PROCESO COMPLETADO")
print(f"   Activos creados: {created_count}")
print(f"   Total activos: {Asset.objects.count()}")
print(f"   Total estados: {AssetStatus.objects.count()}")
print("=" * 60)

# Mostrar resumen
print("\n📊 RESUMEN DE ACTIVOS:")
for asset in Asset.objects.all():
    try:
        status = AssetStatus.objects.get(asset=asset)
        print(f"   {asset.name}: {status.status_type} ({status.fuel_level}% combustible)")
    except AssetStatus.DoesNotExist:
        print(f"   {asset.name}: SIN ESTADO")
