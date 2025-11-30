"""
Script to fix vehicle types in assets to match template vehicle types
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.assets.models import Asset

# Mapping from old to new vehicle types
VEHICLE_TYPE_MAPPING = {
    'Camioneta MDO': 'CAMIONETA_MDO',
    'Camión Supersucker': 'CAMION_SUPERSUCKER',
    'Minicargador MDO': 'MINICARGADOR_MDO',
    'Cargador Frontal MDO': 'CARGADOR_FRONTAL_MDO',
    'Retroexcavadora MDO': 'RETROEXCAVADORA_MDO',
}

print("Actualizando tipos de vehículo...")
print("=" * 60)

updated_count = 0
for asset in Asset.objects.all():
    old_type = asset.vehicle_type
    if old_type in VEHICLE_TYPE_MAPPING:
        new_type = VEHICLE_TYPE_MAPPING[old_type]
        asset.vehicle_type = new_type
        asset.save()
        print(f"✓ {asset.name}: '{old_type}' → '{new_type}'")
        updated_count += 1
    else:
        print(f"⚠ {asset.name}: '{old_type}' (sin cambios)")

print("=" * 60)
print(f"Total actualizado: {updated_count} activos")
print("\nVerificando...")
print("\nActivos actualizados:")
for asset in Asset.objects.all():
    print(f"  - {asset.name}: {asset.vehicle_type}")
