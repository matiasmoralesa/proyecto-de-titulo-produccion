"""
Script to seed configuration data (categories, priorities, work order types, etc.)
Run this to populate the configuration tables with sample data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.configuration.models import AssetCategory, Priority, WorkOrderType, SystemParameter
from apps.authentication.models import User


def create_asset_categories():
    """Create asset categories"""
    print("\n📋 Creating Asset Categories...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create categories.")
        return
    
    categories_data = [
        ('VEH-PES', 'Vehículos Pesados', 'Camiones, volquetes y vehículos de carga pesada'),
        ('MAQ-CON', 'Maquinaria de Construcción', 'Excavadoras, retroexcavadoras, cargadores frontales'),
        ('MAQ-AGR', 'Maquinaria Agrícola', 'Tractores, cosechadoras y equipos agrícolas'),
        ('EQP-IND', 'Equipos Industriales', 'Compresores, generadores, bombas industriales'),
        ('HER-MEN', 'Herramientas Menores', 'Herramientas eléctricas y manuales'),
        ('VEH-LIG', 'Vehículos Ligeros', 'Camionetas, autos y vehículos de transporte ligero'),
        ('EQP-OFI', 'Equipos de Oficina', 'Computadoras, impresoras y equipos de oficina'),
        ('SIS-INF', 'Sistemas de Información', 'Servidores, redes y sistemas IT'),
    ]
    
    created_count = 0
    for code, name, description in categories_data:
        if not AssetCategory.objects.filter(code=code).exists():
            AssetCategory.objects.create(
                code=code,
                name=name,
                description=description,
                is_active=True,
                created_by=admin_user
            )
            created_count += 1
            print(f"  ✓ Created category: {code} - {name}")
        else:
            print(f"  - Category already exists: {code}")
    
    print(f"  Total: {created_count} categories created")


def create_priorities():
    """Create priority levels"""
    print("\n🔴 Creating Priorities...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create priorities.")
        return
    
    priorities_data = [
        ('Crítica', 'Requiere atención inmediata, afecta operaciones críticas', 1, '#DC2626'),
        ('Alta', 'Importante, debe atenderse pronto', 2, '#EA580C'),
        ('Media', 'Prioridad normal, atender en tiempo regular', 3, '#F59E0B'),
        ('Baja', 'Puede esperar, no es urgente', 4, '#10B981'),
        ('Muy Baja', 'Mínima prioridad, atender cuando sea posible', 5, '#6B7280'),
    ]
    
    created_count = 0
    for name, description, level, color in priorities_data:
        if not Priority.objects.filter(level=level).exists():
            Priority.objects.create(
                name=name,
                description=description,
                level=level,
                color_code=color,
                is_active=True,
                created_by=admin_user
            )
            created_count += 1
            print(f"  ✓ Created priority: {name} (Nivel {level})")
        else:
            print(f"  - Priority level {level} already exists")
    
    print(f"  Total: {created_count} priorities created")


def create_work_order_types():
    """Create work order types"""
    print("\n🔧 Creating Work Order Types...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create work order types.")
        return
    
    types_data = [
        ('PREV', 'Mantenimiento Preventivo', 'Mantenimiento programado para prevenir fallas', False),
        ('CORR', 'Mantenimiento Correctivo', 'Reparación de fallas o averías', False),
        ('PRED', 'Mantenimiento Predictivo', 'Basado en predicciones de ML y análisis de datos', False),
        ('EMRG', 'Emergencia', 'Atención inmediata a fallas críticas', True),
        ('INSP', 'Inspección', 'Revisión y evaluación del estado del activo', False),
        ('MODI', 'Modificación', 'Cambios o mejoras en el activo', True),
        ('INST', 'Instalación', 'Instalación de nuevos equipos o componentes', True),
        ('CALI', 'Calibración', 'Ajuste y calibración de equipos', False),
    ]
    
    created_count = 0
    for code, name, description, requires_approval in types_data:
        if not WorkOrderType.objects.filter(code=code).exists():
            WorkOrderType.objects.create(
                code=code,
                name=name,
                description=description,
                requires_approval=requires_approval,
                is_active=True,
                created_by=admin_user
            )
            created_count += 1
            approval_text = " (Requiere aprobación)" if requires_approval else ""
            print(f"  ✓ Created type: {code} - {name}{approval_text}")
        else:
            print(f"  - Type already exists: {code}")
    
    print(f"  Total: {created_count} work order types created")


def create_system_parameters():
    """Create system parameters"""
    print("\n⚙️ Creating System Parameters...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create parameters.")
        return
    
    parameters_data = [
        ('system.name', 'CMMS - Sistema de Gestión de Mantenimiento', 'Nombre del sistema', 'string', True),
        ('system.version', '1.0.0', 'Versión del sistema', 'string', False),
        ('maintenance.default_duration', '4', 'Duración predeterminada de mantenimiento (horas)', 'integer', True),
        ('maintenance.advance_notice_days', '7', 'Días de anticipación para notificaciones de mantenimiento', 'integer', True),
        ('ml.prediction_threshold', '0.7', 'Umbral de probabilidad para predicciones ML', 'float', True),
        ('ml.auto_create_workorder', 'true', 'Crear automáticamente órdenes de trabajo desde predicciones', 'boolean', True),
        ('notifications.enabled', 'true', 'Habilitar notificaciones del sistema', 'boolean', True),
        ('notifications.email_enabled', 'false', 'Habilitar notificaciones por email', 'boolean', True),
        ('reports.retention_days', '365', 'Días de retención de reportes', 'integer', True),
        ('security.session_timeout', '3600', 'Tiempo de expiración de sesión (segundos)', 'integer', True),
    ]
    
    created_count = 0
    for key, value, description, data_type, is_editable in parameters_data:
        if not SystemParameter.objects.filter(key=key).exists():
            SystemParameter.objects.create(
                key=key,
                value=value,
                description=description,
                data_type=data_type,
                is_editable=is_editable,
                modified_by=admin_user
            )
            created_count += 1
            print(f"  ✓ Created parameter: {key}")
        else:
            print(f"  - Parameter already exists: {key}")
    
    print(f"  Total: {created_count} parameters created")


def main():
    """Main function to seed all configuration data"""
    print("\n" + "="*60)
    print("  SEEDING CONFIGURATION DATA")
    print("="*60)
    
    try:
        create_asset_categories()
        create_priorities()
        create_work_order_types()
        create_system_parameters()
        
        print("\n" + "="*60)
        print("  ✅ CONFIGURATION DATA SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  - Asset Categories: {AssetCategory.objects.count()}")
        print(f"  - Priorities: {Priority.objects.count()}")
        print(f"  - Work Order Types: {WorkOrderType.objects.count()}")
        print(f"  - System Parameters: {SystemParameter.objects.count()}")
        print("\n🌐 Access the configuration at: http://localhost:5173/configuration")
        print()
        
    except Exception as e:
        print(f"\n❌ Error seeding configuration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
