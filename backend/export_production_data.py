"""
Script para exportar datos esenciales de la base de datos local
para cargarlos en producción.

Exporta:
- Roles de usuario
- Plantillas de checklist
- Configuración del sistema
- Datos maestros (prioridades, categorías, etc.)
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import Role
from apps.checklists.models import ChecklistTemplate
from apps.configuration.models import Priority, WorkOrderType, AssetCategory
from apps.assets.models import Location

def export_data():
    """Exporta datos esenciales a JSON"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'production_data_{timestamp}.json'
    
    data = {
        'metadata': {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0'
        },
        'roles': [],
        'checklist_templates': [],
        'priorities': [],
        'work_order_types': [],
        'asset_categories': [],
        'locations': []
    }
    
    print("🔄 Exportando datos...")
    
    # Exportar Roles
    print("\n📋 Exportando Roles...")
    for role in Role.objects.all():
        data['roles'].append({
            'name': role.name,
            'description': role.description
        })
    print(f"   ✅ {len(data['roles'])} roles exportados")
    
    # Exportar Plantillas de Checklist
    print("\n📋 Exportando Plantillas de Checklist...")
    for template in ChecklistTemplate.objects.all():
        data['checklist_templates'].append({
            'code': template.code,
            'name': template.name,
            'description': template.description if hasattr(template, 'description') else '',
            'vehicle_type': template.vehicle_type,
            'is_system_template': template.is_system_template,
            'passing_score': template.passing_score if hasattr(template, 'passing_score') else 80,
            'items': template.items
        })
    print(f"   ✅ {len(data['checklist_templates'])} plantillas exportadas")
    
    # Exportar Prioridades
    print("\n📋 Exportando Prioridades...")
    for priority in Priority.objects.all():
        data['priorities'].append({
            'name': priority.name,
            'level': priority.level if hasattr(priority, 'level') else 0,
            'color': priority.color if hasattr(priority, 'color') else '#000000'
        })
    print(f"   ✅ {len(data['priorities'])} prioridades exportadas")
    
    # Exportar Tipos de Orden de Trabajo
    print("\n📋 Exportando Tipos de Orden de Trabajo...")
    for wo_type in WorkOrderType.objects.all():
        data['work_order_types'].append({
            'name': wo_type.name,
            'description': wo_type.description if hasattr(wo_type, 'description') else ''
        })
    print(f"   ✅ {len(data['work_order_types'])} tipos exportados")
    
    # Exportar Categorías de Activos
    print("\n📋 Exportando Categorías de Activos...")
    for category in AssetCategory.objects.all():
        data['asset_categories'].append({
            'name': category.name,
            'description': category.description if hasattr(category, 'description') else ''
        })
    print(f"   ✅ {len(data['asset_categories'])} categorías exportadas")
    
    # Exportar Ubicaciones
    print("\n📋 Exportando Ubicaciones...")
    for location in Location.objects.all():
        data['locations'].append({
            'name': location.name,
            'address': location.address if hasattr(location, 'address') else '',
            'description': location.description if hasattr(location, 'description') else ''
        })
    print(f"   ✅ {len(data['locations'])} ubicaciones exportadas")
    
    # Guardar archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Datos exportados exitosamente a: {output_file}")
    print(f"\n📊 Resumen:")
    print(f"   - Roles: {len(data['roles'])}")
    print(f"   - Plantillas de Checklist: {len(data['checklist_templates'])}")
    print(f"   - Prioridades: {len(data['priorities'])}")
    print(f"   - Tipos de Orden de Trabajo: {len(data['work_order_types'])}")
    print(f"   - Categorías de Activos: {len(data['asset_categories'])}")
    print(f"   - Ubicaciones: {len(data['locations'])}")
    
    return output_file

if __name__ == '__main__':
    try:
        output_file = export_data()
        print(f"\n🚀 Siguiente paso: Cargar este archivo en producción")
        print(f"   Comando: railway run python backend/import_production_data.py {output_file}")
    except Exception as e:
        print(f"\n❌ Error al exportar datos: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
