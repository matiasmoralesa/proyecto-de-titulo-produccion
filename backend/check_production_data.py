"""
Script para verificar que todos los datos esenciales están cargados en producción.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.railway')
django.setup()

from apps.authentication.models import Role
from apps.checklists.models import ChecklistTemplate
from apps.configuration.models import Priority, WorkOrderType, AssetCategory
from apps.assets.models import Location

def check_data():
    """Verifica que todos los datos esenciales estén presentes"""
    
    print("="*60)
    print("🔍 VERIFICACIÓN DE DATOS DE PRODUCCIÓN")
    print("="*60)
    
    all_ok = True
    
    # Verificar Roles
    print("\n📋 Roles de Usuario:")
    roles = Role.objects.all()
    print(f"   Total: {roles.count()}")
    
    expected_roles = ['ADMIN', 'SUPERVISOR', 'OPERADOR']
    for role_name in expected_roles:
        exists = Role.objects.filter(name=role_name).exists()
        if exists:
            print(f"   ✅ {role_name}")
        else:
            print(f"   ❌ {role_name} - FALTANTE")
            all_ok = False
    
    # Verificar Plantillas de Checklist
    print("\n📋 Plantillas de Checklist:")
    templates = ChecklistTemplate.objects.all()
    print(f"   Total: {templates.count()}")
    
    expected_templates = [
        'SUPERSUCKER-CH01',
        'F-PR-020-CH01',
        'F-PR-034-CH01',
        'F-PR-037-CH01',
        'F-PR-040-CH01'
    ]
    
    for code in expected_templates:
        template = ChecklistTemplate.objects.filter(code=code).first()
        if template:
            items_count = len(template.items) if template.items else 0
            print(f"   ✅ {code}: {template.name} ({items_count} items)")
        else:
            print(f"   ❌ {code} - FALTANTE")
            all_ok = False
    
    # Verificar Prioridades
    print("\n📋 Prioridades:")
    priorities = Priority.objects.all()
    print(f"   Total: {priorities.count()}")
    if priorities.count() > 0:
        for priority in priorities:
            print(f"   ✅ {priority.name}")
    else:
        print(f"   ⚠️  No hay prioridades configuradas")
    
    # Verificar Tipos de Orden de Trabajo
    print("\n📋 Tipos de Orden de Trabajo:")
    wo_types = WorkOrderType.objects.all()
    print(f"   Total: {wo_types.count()}")
    if wo_types.count() > 0:
        for wo_type in wo_types:
            print(f"   ✅ {wo_type.name}")
    else:
        print(f"   ⚠️  No hay tipos de orden de trabajo configurados")
    
    # Verificar Categorías de Activos
    print("\n📋 Categorías de Activos:")
    categories = AssetCategory.objects.all()
    print(f"   Total: {categories.count()}")
    if categories.count() > 0:
        for category in categories:
            print(f"   ✅ {category.name}")
    else:
        print(f"   ⚠️  No hay categorías de activos configuradas")
    
    # Verificar Ubicaciones
    print("\n📋 Ubicaciones:")
    locations = Location.objects.all()
    print(f"   Total: {locations.count()}")
    if locations.count() > 0:
        for location in locations:
            print(f"   ✅ {location.name}")
    else:
        print(f"   ⚠️  No hay ubicaciones configuradas")
    
    # Resumen final
    print("\n" + "="*60)
    if all_ok:
        print("✅ VERIFICACIÓN EXITOSA")
        print("   Todos los datos esenciales están presentes")
        return 0
    else:
        print("❌ VERIFICACIÓN FALLIDA")
        print("   Faltan datos esenciales (ver arriba)")
        return 1

if __name__ == '__main__':
    try:
        exit_code = check_data()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
