"""
Script to create sample assets for testing.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.assets.models import Asset, Location
from apps.authentication.models import User

# Get admin user
admin = User.objects.get(username='admin')

# Get locations
locations = list(Location.objects.all())

# Sample assets data
assets_data = [
    {
        'name': 'Camión Supersucker 001',
        'vehicle_type': Asset.CAMION_SUPERSUCKER,
        'model': 'Volvo FH16',
        'serial_number': 'SS-2024-001',
        'license_plate': 'ABC-123',
        'location': locations[0],
        'installation_date': '2024-01-15',
        'status': Asset.STATUS_OPERANDO,
    },
    {
        'name': 'Camioneta MDO 001',
        'vehicle_type': Asset.CAMIONETA_MDO,
        'model': 'Toyota Hilux',
        'serial_number': 'CM-2024-001',
        'license_plate': 'DEF-456',
        'location': locations[1],
        'installation_date': '2024-02-10',
        'status': Asset.STATUS_OPERANDO,
    },
    {
        'name': 'Retroexcavadora MDO 001',
        'vehicle_type': Asset.RETROEXCAVADORA_MDO,
        'model': 'Caterpillar 420F',
        'serial_number': 'RE-2024-001',
        'license_plate': 'GHI-789',
        'location': locations[2],
        'installation_date': '2024-03-05',
        'status': Asset.STATUS_EN_MANTENIMIENTO,
    },
    {
        'name': 'Cargador Frontal MDO 001',
        'vehicle_type': Asset.CARGADOR_FRONTAL_MDO,
        'model': 'Komatsu WA320',
        'serial_number': 'CF-2024-001',
        'license_plate': 'JKL-012',
        'location': locations[3],
        'installation_date': '2024-04-20',
        'status': Asset.STATUS_OPERANDO,
    },
    {
        'name': 'Minicargador MDO 001',
        'vehicle_type': Asset.MINICARGADOR_MDO,
        'model': 'Bobcat S650',
        'serial_number': 'MC-2024-001',
        'license_plate': 'MNO-345',
        'location': locations[4],
        'installation_date': '2024-05-12',
        'status': Asset.STATUS_DETENIDA,
    },
    {
        'name': 'Camión Supersucker 002',
        'vehicle_type': Asset.CAMION_SUPERSUCKER,
        'model': 'Volvo FH16',
        'serial_number': 'SS-2024-002',
        'license_plate': 'PQR-678',
        'location': locations[0],
        'installation_date': '2024-06-01',
        'status': Asset.STATUS_OPERANDO,
    },
    {
        'name': 'Camioneta MDO 002',
        'vehicle_type': Asset.CAMIONETA_MDO,
        'model': 'Ford Ranger',
        'serial_number': 'CM-2024-002',
        'license_plate': 'STU-901',
        'location': locations[1],
        'installation_date': '2024-07-15',
        'status': Asset.STATUS_OPERANDO,
    },
]

print('Creating sample assets...\n')

created_count = 0
for asset_data in assets_data:
    serial = asset_data['serial_number']
    
    if Asset.objects.filter(serial_number=serial).exists():
        print(f'- Asset already exists: {asset_data["name"]}')
    else:
        asset = Asset.objects.create(
            **asset_data,
            created_by=admin
        )
        created_count += 1
        print(f'✓ Created asset: {asset.name} ({asset.vehicle_type})')

print(f'\n✓ Successfully created {created_count} asset(s)')
print(f'Total assets in system: {Asset.objects.count()}')
