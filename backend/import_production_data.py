"""
Script para importar datos esenciales en la base de datos de producción.

Este script debe ejecutarse en Railway usando:
railway run python backend/import_production_data.py <archivo_json>
"""

import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.railway')
django.setup()

from apps.authentication.models import Role
from apps.checklists.models import ChecklistTemplate
from apps.configuration.models import Priority, WorkOrderType, AssetCategory
from apps.assets.models import Location
from django.db import transaction

def import_data(json_file):
    """Importa datos desde archivo JSON"""
    
    print(f"🔄 Cargando datos desde: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Archivo cargado. Versión: {data['metadata']['version']}")
    print(f"   Exportado el: {data['metadata']['exported_at']}")
    
    stats = {
        'roles': {'created': 0, 'updated': 0},
        'checklist_templates': {'created': 0, 'updated': 0},
        'priorities': {'created': 0, 'updated': 0},
        'work_order_types': {'created': 0, 'updated': 0},
        'asset_categories': {'created': 0, 'updated': 0},
        'locations': {'created': 0, 'updated': 0}
    }
    
    with transaction.atomic():
        # Importar Roles
        print("\n📋 Importando Roles...")
        for role_data in data['roles']:
            role, created = Role.objects.update_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'code': role_data.get('code', role_data['name'])
                }
            )
            if created:
                stats['roles']['created'] += 1
                print(f"   ✅ Creado: {role.name}")
            else:
                stats['roles']['updated'] += 1
                print(f"   🔄 Actualizado: {role.name}")
        
        # Importar Plantillas de Checklist
        print("\n📋 Importando Plantillas de Checklist...")
        for template_data in data['checklist_templates']:
            template, created = ChecklistTemplate.objects.update_or_create(
                code=template_data['code'],
                defaults={
                    'name': template_data['name'],
                    'description': template_data.get('description', ''),
                    'vehicle_type': template_data['vehicle_type'],
                    'is_system_template': template_data['is_system_template'],
                    'passing_score': template_data.get('passing_score', 80),
                    'items': template_data['items']
                }
            )
            if created:
                stats['checklist_templates']['created'] += 1
                print(f"   ✅ Creado: {template.name} ({template.code})")
            else:
                stats['checklist_templates']['updated'] += 1
                print(f"   🔄 Actualizado: {template.name} ({template.code})")
        
        # Importar Prioridades
        print("\n📋 Importando Prioridades...")
        for priority_data in data['priorities']:
            priority, created = Priority.objects.update_or_create(
                name=priority_data['name'],
                defaults={
                    'level': priority_data.get('level', 0),
                    'color': priority_data.get('color', '#000000')
                }
            )
            if created:
                stats['priorities']['created'] += 1
                print(f"   ✅ Creado: {priority.name}")
            else:
                stats['priorities']['updated'] += 1
                print(f"   🔄 Actualizado: {priority.name}")
        
        # Importar Tipos de Orden de Trabajo
        print("\n📋 Importando Tipos de Orden de Trabajo...")
        for wo_type_data in data['work_order_types']:
            wo_type, created = WorkOrderType.objects.update_or_create(
                name=wo_type_data['name'],
                defaults={
                    'description': wo_type_data.get('description', '')
                }
            )
            if created:
                stats['work_order_types']['created'] += 1
                print(f"   ✅ Creado: {wo_type.name}")
            else:
                stats['work_order_types']['updated'] += 1
                print(f"   🔄 Actualizado: {wo_type.name}")
        
        # Importar Categorías de Activos
        print("\n📋 Importando Categorías de Activos...")
        for category_data in data['asset_categories']:
            category, created = AssetCategory.objects.update_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data.get('description', '')
                }
            )
            if created:
                stats['asset_categories']['created'] += 1
                print(f"   ✅ Creado: {category.name}")
            else:
                stats['asset_categories']['updated'] += 1
                print(f"   🔄 Actualizado: {category.name}")
        
        # Importar Ubicaciones
        print("\n📋 Importando Ubicaciones...")
        for location_data in data['locations']:
            location, created = Location.objects.update_or_create(
                name=location_data['name'],
                defaults={
                    'address': location_data.get('address', ''),
                    'description': location_data.get('description', '')
                }
            )
            if created:
                stats['locations']['created'] += 1
                print(f"   ✅ Creado: {location.name}")
            else:
                stats['locations']['updated'] += 1
                print(f"   🔄 Actualizado: {location.name}")
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE IMPORTACIÓN")
    print("="*60)
    for key, value in stats.items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(f"   ✅ Creados: {value['created']}")
        print(f"   🔄 Actualizados: {value['updated']}")
        print(f"   📊 Total: {value['created'] + value['updated']}")
    
    print("\n✅ Importación completada exitosamente!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Error: Debes proporcionar el archivo JSON")
        print("   Uso: python import_production_data.py <archivo.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"❌ Error: El archivo {json_file} no existe")
        sys.exit(1)
    
    try:
        import_data(json_file)
    except Exception as e:
        print(f"\n❌ Error al importar datos: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
