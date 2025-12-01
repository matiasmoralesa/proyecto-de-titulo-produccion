"""
Script para corregir los vehicle_types de los activos en producción.
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.railway')
django.setup()

from apps.assets.models import Asset

# Mapeo de valores incorrectos a correctos
VEHICLE_TYPE_MAPPING = {
    'EXCAVADORA': 'Retroexcavadora MDO',
    'RETROEXCAVADORA': 'Retroexcavadora MDO',
    'CARGADOR_FRONTAL': 'Cargador Frontal MDO',
    'CARGADOR FRONTAL': 'Cargador Frontal MDO',
    'MINICARGADOR': 'Minicargador MDO',
    'CAMION_SUPERSUCKER': 'Camión Supersucker',
    'CAMION SUPERSUCKER': 'Camión Supersucker',
    'CAMIONETA_MDO': 'Camioneta MDO',
    'CAMIONETA MDO': 'Camioneta MDO',
    'VOLQUETE': 'Camión Supersucker',  # Asumiendo que volquete es similar
}

def fix_vehicle_types():
    """Corrige los vehicle_types de todos los activos."""
    
    print("🔄 Corrigiendo vehicle_types de activos...")
    
    updated_count = 0
    skipped_count = 0
    
    for asset in Asset.objects.all():
        old_type = asset.vehicle_type
        
        # Si el tipo ya es correcto, skip
        if old_type in [
            'Camión Supersucker',
            'Camioneta MDO',
            'Retroexcavadora MDO',
            'Cargador Frontal MDO',
            'Minicargador MDO'
        ]:
            skipped_count += 1
            continue
        
        # Buscar el mapeo correcto
        new_type = VEHICLE_TYPE_MAPPING.get(old_type.upper().replace(' ', '_'))
        
        if not new_type:
            # Intentar match parcial
            if 'EXCAVADORA' in old_type.upper():
                new_type = 'Retroexcavadora MDO'
            elif 'CARGADOR' in old_type.upper() and 'FRONTAL' in old_type.upper():
                new_type = 'Cargador Frontal MDO'
            elif 'MINICARGADOR' in old_type.upper():
                new_type = 'Minicargador MDO'
            elif 'CAMION' in old_type.upper() or 'SUPERSUCKER' in old_type.upper():
                new_type = 'Camión Supersucker'
            elif 'CAMIONETA' in old_type.upper():
                new_type = 'Camioneta MDO'
            else:
                print(f"   ⚠️  No se pudo mapear: {asset.name} ({old_type})")
                continue
        
        # Actualizar
        asset.vehicle_type = new_type
        asset.save()
        updated_count += 1
        print(f"   ✅ {asset.name}: {old_type} → {new_type}")
    
    print(f"\n✅ Proceso completado!")
    print(f"   Actualizados: {updated_count}")
    print(f"   Sin cambios: {skipped_count}")
    print(f"   Total: {Asset.objects.count()}")

if __name__ == '__main__':
    try:
        fix_vehicle_types()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
