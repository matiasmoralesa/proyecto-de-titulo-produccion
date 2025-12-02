"""
Script para limpiar datos de producción y crear datos de muestra nuevos.
Mantiene solo las plantillas de checklist.
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Cambiar al directorio backend antes de setup
original_dir = os.getcwd()
os.chdir(backend_dir)

django.setup()

# Volver al directorio original
os.chdir(original_dir)

from django.contrib.auth import get_user_model
from apps.assets.models import Location, Asset, AssetDocument
from apps.work_orders.models import WorkOrder
from apps.inventory.models import SparePart, StockMovement
from apps.maintenance.models import MaintenancePlan
from apps.configuration.models import (
    AssetCategory, Priority, WorkOrderType, SystemParameter, AuditLog, AccessLog
)
from apps.authentication.models import Role
from apps.notifications.models import Notification
from apps.omnichannel_bot.models import MessageLog
from apps.ml_predictions.models import FailurePrediction, OperatorPerformance
from apps.machine_status.models import AssetStatus, AssetStatusHistory
from apps.checklists.models import ChecklistResponse, ChecklistItemResponse

User = get_user_model()


def clear_all_data():
    """Elimina todos los datos excepto plantillas de checklist."""
    print("🗑️  Limpiando datos existentes...")
    
    # Eliminar en orden para respetar foreign keys
    print("  - Eliminando respuestas de checklist...")
    ChecklistItemResponse.objects.all().delete()
    ChecklistResponse.objects.all().delete()
    
    print("  - Eliminando notificaciones...")
    Notification.objects.all().delete()
    
    print("  - Eliminando logs de mensajes...")
    MessageLog.objects.all().delete()
    
    print("  - Eliminando predicciones y performance...")
    FailurePrediction.objects.all().delete()
    OperatorPerformance.objects.all().delete()
    
    print("  - Eliminando historial de estado de activos...")
    AssetStatusHistory.objects.all().delete()
    AssetStatus.objects.all().delete()
    
    print("  - Eliminando logs de acceso...")
    AccessLog.objects.all().delete()
    
    print("  - Eliminando logs de auditoría...")
    AuditLog.objects.all().delete()
    
    print("  - Eliminando movimientos de stock...")
    StockMovement.objects.all().delete()
    
    print("  - Eliminando repuestos...")
    SparePart.objects.all().delete()
    
    print("  - Eliminando planes de mantenimiento...")
    MaintenancePlan.objects.all().delete()
    
    print("  - Eliminando órdenes de trabajo...")
    WorkOrder.objects.all().delete()
    
    print("  - Eliminando documentos de activos...")
    AssetDocument.objects.all().delete()
    
    print("  - Eliminando activos...")
    Asset.objects.all().delete()
    
    print("  - Eliminando ubicaciones...")
    Location.objects.all().delete()
    
    print("  - Eliminando usuarios (excepto superusuarios)...")
    User.objects.filter(is_superuser=False).delete()
    
    print("  - Eliminando configuraciones...")
    AssetCategory.objects.all().delete()
    Priority.objects.all().delete()
    WorkOrderType.objects.all().delete()
    SystemParameter.objects.all().delete()
    
    print("✅ Datos limpiados exitosamente\n")


def create_users():
    """Crea usuarios de muestra para cada rol."""
    print("👥 Creando usuarios...")
    
    # Crear o obtener roles
    admin_role, _ = Role.objects.get_or_create(
        name=Role.ADMIN,
        defaults={'description': 'Administrador del sistema'}
    )
    supervisor_role, _ = Role.objects.get_or_create(
        name=Role.SUPERVISOR,
        defaults={'description': 'Supervisor de operaciones'}
    )
    operador_role, _ = Role.objects.get_or_create(
        name=Role.OPERADOR,
        defaults={'description': 'Operador de campo'}
    )
    
    users = {}
    
    # Admin
    if not User.objects.filter(username='admin').exists():
        users['admin'] = User.objects.create_user(
            username='admin',
            email='admin@cmms.com',
            password='admin123',
            first_name='Carlos',
            last_name='Administrador',
            role=admin_role,
            is_staff=True,
            is_superuser=True,
            must_change_password=False
        )
        print("  ✓ Admin creado: admin / admin123")
    else:
        users['admin'] = User.objects.get(username='admin')
        print("  ✓ Admin ya existe")
    
    # Supervisores
    users['supervisor1'] = User.objects.create_user(
        username='supervisor1',
        email='supervisor1@cmms.com',
        password='super123',
        first_name='María',
        last_name='Supervisor',
        role=supervisor_role,
        must_change_password=False
    )
    
    users['supervisor2'] = User.objects.create_user(
        username='supervisor2',
        email='supervisor2@cmms.com',
        password='super123',
        first_name='Juan',
        last_name='Coordinador',
        role=supervisor_role,
        must_change_password=False
    )
    print("  ✓ 2 Supervisores creados")
    
    # Operadores
    users['operador1'] = User.objects.create_user(
        username='operador1',
        email='operador1@cmms.com',
        password='oper123',
        first_name='Pedro',
        last_name='Técnico',
        role=operador_role,
        must_change_password=False
    )
    
    users['operador2'] = User.objects.create_user(
        username='operador2',
        email='operador2@cmms.com',
        password='oper123',
        first_name='Ana',
        last_name='Mecánica',
        role=operador_role,
        must_change_password=False
    )
    
    users['operador3'] = User.objects.create_user(
        username='operador3',
        email='operador3@cmms.com',
        password='oper123',
        first_name='Luis',
        last_name='Operador',
        role=operador_role,
        must_change_password=False
    )
    print("  ✓ 3 Operadores creados")
    
    return users


def create_configuration(users):
    """Crea datos de configuración."""
    print("\n⚙️  Creando configuración...")
    
    # Categorías de Activos
    categories = [
        {'name': 'Vehículos Pesados', 'code': 'VH', 'description': 'Camiones y vehículos de gran tonelaje'},
        {'name': 'Vehículos Livianos', 'code': 'VL', 'description': 'Camionetas y vehículos pequeños'},
        {'name': 'Maquinaria Pesada', 'code': 'MP', 'description': 'Excavadoras, cargadores, etc.'},
        {'name': 'Equipos Especializados', 'code': 'EE', 'description': 'Equipos de succión y limpieza'},
    ]
    
    created_categories = {}
    for cat_data in categories:
        cat = AssetCategory.objects.create(
            name=cat_data['name'],
            code=cat_data['code'],
            description=cat_data['description'],
            created_by=users['admin']
        )
        created_categories[cat_data['code']] = cat
    print(f"  ✓ {len(categories)} categorías creadas")
    
    # Prioridades
    priorities = [
        {'name': 'Urgente', 'level': 1, 'color_code': '#FF0000'},
        {'name': 'Alta', 'level': 2, 'color_code': '#FF6600'},
        {'name': 'Media', 'level': 3, 'color_code': '#FFCC00'},
        {'name': 'Baja', 'level': 4, 'color_code': '#00CC00'},
    ]
    
    created_priorities = {}
    for pri_data in priorities:
        pri = Priority.objects.create(
            name=pri_data['name'],
            level=pri_data['level'],
            color_code=pri_data['color_code'],
            created_by=users['admin']
        )
        created_priorities[pri_data['name']] = pri
    print(f"  ✓ {len(priorities)} prioridades creadas")
    
    # Tipos de Orden de Trabajo
    wo_types = [
        {'name': 'Mantenimiento Preventivo', 'code': 'MP', 'requires_approval': False},
        {'name': 'Mantenimiento Correctivo', 'code': 'MC', 'requires_approval': False},
        {'name': 'Reparación de Emergencia', 'code': 'RE', 'requires_approval': True},
        {'name': 'Inspección', 'code': 'INS', 'requires_approval': False},
        {'name': 'Modificación', 'code': 'MOD', 'requires_approval': True},
    ]
    
    created_wo_types = {}
    for wo_data in wo_types:
        wo_type = WorkOrderType.objects.create(
            name=wo_data['name'],
            code=wo_data['code'],
            requires_approval=wo_data['requires_approval'],
            created_by=users['admin']
        )
        created_wo_types[wo_data['code']] = wo_type
    print(f"  ✓ {len(wo_types)} tipos de orden creados")
    
    # Parámetros del Sistema
    params = [
        {'key': 'maintenance_notification_days', 'value': '7', 'data_type': 'integer', 
         'description': 'Días de anticipación para notificaciones de mantenimiento'},
        {'key': 'low_stock_threshold', 'value': '10', 'data_type': 'integer',
         'description': 'Umbral de stock bajo para repuestos'},
        {'key': 'enable_rbac', 'value': 'true', 'data_type': 'boolean',
         'description': 'Habilitar control de acceso basado en roles'},
    ]
    
    for param_data in params:
        SystemParameter.objects.create(
            key=param_data['key'],
            value=param_data['value'],
            data_type=param_data['data_type'],
            description=param_data['description'],
            modified_by=users['admin']
        )
    print(f"  ✓ {len(params)} parámetros del sistema creados")
    
    return created_categories, created_priorities, created_wo_types



def create_locations():
    """Crea ubicaciones de muestra."""
    print("\n📍 Creando ubicaciones...")
    
    locations_data = [
        {
            'name': 'Planta Central',
            'address': 'Av. Industrial 1234, Lima',
            'coordinates': '-12.0464,-77.0428',
            'description': 'Planta principal de operaciones'
        },
        {
            'name': 'Almacén Norte',
            'address': 'Jr. Los Pinos 567, Lima',
            'coordinates': '-12.0264,-77.0528',
            'description': 'Almacén de repuestos y equipos'
        },
        {
            'name': 'Taller de Mantenimiento',
            'address': 'Av. Los Talleres 890, Lima',
            'coordinates': '-12.0564,-77.0328',
            'description': 'Taller especializado en mantenimiento'
        },
        {
            'name': 'Base Operativa Sur',
            'address': 'Calle Las Flores 345, Lima',
            'coordinates': '-12.0764,-77.0228',
            'description': 'Base de operaciones zona sur'
        },
    ]
    
    locations = {}
    for loc_data in locations_data:
        loc = Location.objects.create(**loc_data)
        locations[loc_data['name']] = loc
    
    print(f"  ✓ {len(locations)} ubicaciones creadas")
    return locations


def create_assets(locations, users):
    """Crea activos de muestra."""
    print("\n🚛 Creando activos...")
    
    assets_data = [
        {
            'name': 'Camión Supersucker SS-001',
            'vehicle_type': 'Camión Supersucker',
            'model': 'Vactor 2100',
            'serial_number': 'SS-2024-001',
            'license_plate': 'ABC-123',
            'location': locations['Planta Central'],
            'installation_date': (datetime.now() - timedelta(days=365)).date(),
            'status': 'Operando',
        },
        {
            'name': 'Camión Supersucker SS-002',
            'vehicle_type': 'Camión Supersucker',
            'model': 'Vactor 2100',
            'serial_number': 'SS-2024-002',
            'license_plate': 'ABC-124',
            'location': locations['Planta Central'],
            'installation_date': (datetime.now() - timedelta(days=300)).date(),
            'status': 'Operando',
        },
        {
            'name': 'Camioneta MDO-001',
            'vehicle_type': 'Camioneta MDO',
            'model': 'Toyota Hilux 4x4',
            'serial_number': 'MDO-2024-001',
            'license_plate': 'DEF-456',
            'location': locations['Base Operativa Sur'],
            'installation_date': (datetime.now() - timedelta(days=200)).date(),
            'status': 'Operando',
        },
        {
            'name': 'Retroexcavadora RE-001',
            'vehicle_type': 'Retroexcavadora MDO',
            'model': 'Caterpillar 420F',
            'serial_number': 'RE-2024-001',
            'license_plate': 'GHI-789',
            'location': locations['Taller de Mantenimiento'],
            'installation_date': (datetime.now() - timedelta(days=500)).date(),
            'status': 'En Mantenimiento',
        },
        {
            'name': 'Cargador Frontal CF-001',
            'vehicle_type': 'Cargador Frontal MDO',
            'model': 'Caterpillar 950M',
            'serial_number': 'CF-2024-001',
            'license_plate': 'JKL-012',
            'location': locations['Almacén Norte'],
            'installation_date': (datetime.now() - timedelta(days=450)).date(),
            'status': 'Operando',
        },
        {
            'name': 'Minicargador MC-001',
            'vehicle_type': 'Minicargador MDO',
            'model': 'Bobcat S650',
            'serial_number': 'MC-2024-001',
            'license_plate': 'MNO-345',
            'location': locations['Base Operativa Sur'],
            'installation_date': (datetime.now() - timedelta(days=180)).date(),
            'status': 'Operando',
        },
        {
            'name': 'Camioneta MDO-002',
            'vehicle_type': 'Camioneta MDO',
            'model': 'Ford Ranger XLT',
            'serial_number': 'MDO-2024-002',
            'license_plate': 'PQR-678',
            'location': locations['Planta Central'],
            'installation_date': (datetime.now() - timedelta(days=150)).date(),
            'status': 'Detenida',
        },
    ]
    
    assets = []
    for asset_data in assets_data:
        asset = Asset.objects.create(
            **asset_data,
            created_by=users['admin']
        )
        assets.append(asset)
    
    print(f"  ✓ {len(assets)} activos creados")
    return assets



def create_spare_parts(users):
    """Crea repuestos de muestra."""
    print("\n🔧 Creando repuestos...")
    
    spare_parts_data = [
        {
            'part_number': 'FLT-001',
            'name': 'Filtro de Aceite',
            'description': 'Filtro de aceite para motor diesel',
            'category': 'Filtros',
            'manufacturer': 'Mann Filter',
            'quantity': 25,
            'min_quantity': 10,
            'unit_of_measure': 'unidad',
            'unit_cost': Decimal('45.50'),
            'storage_location': 'Almacén Norte - Estante A1',
        },
        {
            'part_number': 'FLT-002',
            'name': 'Filtro de Aire',
            'description': 'Filtro de aire para motor diesel',
            'category': 'Filtros',
            'manufacturer': 'Mann Filter',
            'quantity': 30,
            'min_quantity': 15,
            'unit_of_measure': 'unidad',
            'unit_cost': Decimal('38.00'),
            'storage_location': 'Almacén Norte - Estante A1',
        },
        {
            'part_number': 'FLT-003',
            'name': 'Filtro de Combustible',
            'description': 'Filtro de combustible diesel',
            'category': 'Filtros',
            'manufacturer': 'Bosch',
            'quantity': 20,
            'min_quantity': 10,
            'unit_of_measure': 'unidad',
            'unit_cost': Decimal('52.00'),
            'storage_location': 'Almacén Norte - Estante A2',
        },
        {
            'part_number': 'ACE-001',
            'name': 'Aceite Motor 15W-40',
            'description': 'Aceite mineral para motor diesel',
            'category': 'Lubricantes',
            'manufacturer': 'Shell',
            'quantity': 100,
            'min_quantity': 30,
            'unit_of_measure': 'litro',
            'unit_cost': Decimal('18.50'),
            'storage_location': 'Almacén Norte - Zona B',
        },
        {
            'part_number': 'ACE-002',
            'name': 'Aceite Hidráulico ISO 68',
            'description': 'Aceite hidráulico para sistemas',
            'category': 'Lubricantes',
            'manufacturer': 'Mobil',
            'quantity': 80,
            'min_quantity': 25,
            'unit_of_measure': 'litro',
            'unit_cost': Decimal('22.00'),
            'storage_location': 'Almacén Norte - Zona B',
        },
        {
            'part_number': 'FRE-001',
            'name': 'Pastillas de Freno Delanteras',
            'description': 'Juego de pastillas de freno delanteras',
            'category': 'Sistema de Frenos',
            'manufacturer': 'Brembo',
            'quantity': 12,
            'min_quantity': 6,
            'unit_of_measure': 'juego',
            'unit_cost': Decimal('185.00'),
            'storage_location': 'Almacén Norte - Estante C1',
        },
        {
            'part_number': 'FRE-002',
            'name': 'Pastillas de Freno Traseras',
            'description': 'Juego de pastillas de freno traseras',
            'category': 'Sistema de Frenos',
            'manufacturer': 'Brembo',
            'quantity': 10,
            'min_quantity': 6,
            'unit_of_measure': 'juego',
            'unit_cost': Decimal('165.00'),
            'storage_location': 'Almacén Norte - Estante C1',
        },
        {
            'part_number': 'BAT-001',
            'name': 'Batería 12V 100Ah',
            'description': 'Batería de arranque para vehículos pesados',
            'category': 'Sistema Eléctrico',
            'manufacturer': 'Bosch',
            'quantity': 8,
            'min_quantity': 4,
            'unit_of_measure': 'unidad',
            'unit_cost': Decimal('320.00'),
            'storage_location': 'Almacén Norte - Estante D1',
        },
        {
            'part_number': 'NEU-001',
            'name': 'Neumático 295/80R22.5',
            'description': 'Neumático para camión',
            'category': 'Neumáticos',
            'manufacturer': 'Michelin',
            'quantity': 16,
            'min_quantity': 8,
            'unit_of_measure': 'unidad',
            'unit_cost': Decimal('850.00'),
            'storage_location': 'Almacén Norte - Zona E',
        },
        {
            'part_number': 'MAN-001',
            'name': 'Manguera Hidráulica 1/2"',
            'description': 'Manguera hidráulica alta presión',
            'category': 'Sistema Hidráulico',
            'manufacturer': 'Parker',
            'quantity': 5,
            'min_quantity': 3,
            'unit_of_measure': 'metro',
            'unit_cost': Decimal('45.00'),
            'storage_location': 'Almacén Norte - Estante F1',
        },
    ]
    
    spare_parts = []
    for part_data in spare_parts_data:
        part = SparePart.objects.create(
            **part_data,
            created_by=users['admin']
        )
        spare_parts.append(part)
    
    print(f"  ✓ {len(spare_parts)} repuestos creados")
    return spare_parts



def create_work_orders(assets, users):
    """Crea órdenes de trabajo de muestra."""
    print("\n📋 Creando órdenes de trabajo...")
    
    now = timezone.now()
    
    work_orders_data = [
        {
            'title': 'Mantenimiento Preventivo 5000 km',
            'description': 'Cambio de aceite, filtros y revisión general del motor',
            'priority': 'Media',
            'status': 'Completada',
            'asset': assets[0],
            'assigned_to': users['operador1'],
            'scheduled_date': now - timedelta(days=10),
            'completed_date': now - timedelta(days=8),
            'completion_notes': 'Mantenimiento completado sin novedades. Se cambiaron todos los filtros y aceite.',
            'actual_hours': Decimal('3.5'),
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Reparación Sistema Hidráulico',
            'description': 'Fuga detectada en manguera hidráulica principal',
            'priority': 'Alta',
            'status': 'En Progreso',
            'asset': assets[3],
            'assigned_to': users['operador2'],
            'scheduled_date': now - timedelta(days=2),
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Inspección Mensual',
            'description': 'Inspección rutinaria mensual de todos los sistemas',
            'priority': 'Media',
            'status': 'Pendiente',
            'asset': assets[1],
            'assigned_to': users['operador1'],
            'scheduled_date': now + timedelta(days=3),
            'created_by': users['supervisor2'],
        },
        {
            'title': 'Cambio de Neumáticos',
            'description': 'Reemplazo de neumáticos delanteros por desgaste',
            'priority': 'Media',
            'status': 'Completada',
            'asset': assets[2],
            'assigned_to': users['operador3'],
            'scheduled_date': now - timedelta(days=15),
            'completed_date': now - timedelta(days=14),
            'completion_notes': 'Se reemplazaron ambos neumáticos delanteros. Alineación y balanceo realizados.',
            'actual_hours': Decimal('2.0'),
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Reparación Sistema de Frenos',
            'description': 'Cambio de pastillas de freno delanteras y revisión de discos',
            'priority': 'Alta',
            'status': 'En Progreso',
            'asset': assets[6],
            'assigned_to': users['operador2'],
            'scheduled_date': now - timedelta(days=1),
            'created_by': users['supervisor2'],
        },
        {
            'title': 'Mantenimiento Preventivo 10000 km',
            'description': 'Mantenimiento mayor: cambio de aceite, filtros, revisión de frenos y suspensión',
            'priority': 'Media',
            'status': 'Pendiente',
            'asset': assets[4],
            'assigned_to': users['operador1'],
            'scheduled_date': now + timedelta(days=7),
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Revisión Sistema Eléctrico',
            'description': 'Diagnóstico de falla en sistema de luces',
            'priority': 'Baja',
            'status': 'Pendiente',
            'asset': assets[5],
            'assigned_to': users['operador3'],
            'scheduled_date': now + timedelta(days=5),
            'created_by': users['supervisor2'],
        },
        {
            'title': 'Cambio de Batería',
            'description': 'Reemplazo de batería por bajo rendimiento',
            'priority': 'Media',
            'status': 'Completada',
            'asset': assets[0],
            'assigned_to': users['operador1'],
            'scheduled_date': now - timedelta(days=20),
            'completed_date': now - timedelta(days=19),
            'completion_notes': 'Batería reemplazada. Sistema eléctrico funcionando correctamente.',
            'actual_hours': Decimal('1.5'),
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Reparación Urgente Motor',
            'description': 'Sobrecalentamiento del motor - requiere atención inmediata',
            'priority': 'Urgente',
            'status': 'En Progreso',
            'asset': assets[1],
            'assigned_to': users['operador2'],
            'scheduled_date': now,
            'created_by': users['supervisor1'],
        },
        {
            'title': 'Inspección Pre-Operacional',
            'description': 'Inspección antes de iniciar operaciones',
            'priority': 'Media',
            'status': 'Completada',
            'asset': assets[5],
            'assigned_to': users['operador3'],
            'scheduled_date': now - timedelta(days=5),
            'completed_date': now - timedelta(days=5),
            'completion_notes': 'Inspección completada. Vehículo en condiciones óptimas.',
            'actual_hours': Decimal('0.5'),
            'created_by': users['supervisor2'],
        },
    ]
    
    work_orders = []
    for wo_data in work_orders_data:
        wo = WorkOrder.objects.create(**wo_data)
        work_orders.append(wo)
    
    print(f"  ✓ {len(work_orders)} órdenes de trabajo creadas")
    return work_orders



def create_maintenance_plans(assets, users):
    """Crea planes de mantenimiento de muestra."""
    print("\n🔄 Creando planes de mantenimiento...")
    
    now = timezone.now()
    
    plans_data = [
        {
            'name': 'Mantenimiento Preventivo Mensual - SS-001',
            'description': 'Revisión mensual de sistemas críticos y cambio de filtros',
            'asset': assets[0],
            'recurrence_type': 'Mensual',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=30)).date(),
            'estimated_duration_hours': Decimal('4.0'),
            'assigned_to': users['operador1'],
            'status': 'Activo',
            'created_by': users['supervisor1'],
        },
        {
            'name': 'Mantenimiento Preventivo Mensual - SS-002',
            'description': 'Revisión mensual de sistemas críticos y cambio de filtros',
            'asset': assets[1],
            'recurrence_type': 'Mensual',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=30)).date(),
            'estimated_duration_hours': Decimal('4.0'),
            'assigned_to': users['operador1'],
            'status': 'Activo',
            'created_by': users['supervisor1'],
        },
        {
            'name': 'Inspección Semanal - Camioneta MDO-001',
            'description': 'Inspección semanal de niveles y sistemas básicos',
            'asset': assets[2],
            'recurrence_type': 'Semanal',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=7)).date(),
            'estimated_duration_hours': Decimal('1.0'),
            'assigned_to': users['operador3'],
            'status': 'Activo',
            'created_by': users['supervisor2'],
        },
        {
            'name': 'Mantenimiento Trimestral - Retroexcavadora',
            'description': 'Mantenimiento mayor trimestral de sistemas hidráulicos y mecánicos',
            'asset': assets[3],
            'recurrence_type': 'Trimestral',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=90)).date(),
            'estimated_duration_hours': Decimal('8.0'),
            'assigned_to': users['operador2'],
            'status': 'Activo',
            'created_by': users['supervisor1'],
        },
        {
            'name': 'Mantenimiento por Horas - Cargador Frontal',
            'description': 'Mantenimiento cada 250 horas de operación',
            'asset': assets[4],
            'recurrence_type': 'Por Horas',
            'recurrence_interval': 250,
            'start_date': now.date(),
            'usage_threshold': 250,
            'last_usage_value': 180,
            'estimated_duration_hours': Decimal('6.0'),
            'assigned_to': users['operador2'],
            'status': 'Activo',
            'created_by': users['supervisor1'],
        },
        {
            'name': 'Inspección Diaria - Minicargador',
            'description': 'Inspección diaria pre-operacional',
            'asset': assets[5],
            'recurrence_type': 'Diario',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=1)).date(),
            'estimated_duration_hours': Decimal('0.5'),
            'assigned_to': users['operador3'],
            'status': 'Activo',
            'created_by': users['supervisor2'],
        },
        {
            'name': 'Mantenimiento Anual - Camioneta MDO-002',
            'description': 'Mantenimiento mayor anual completo',
            'asset': assets[6],
            'recurrence_type': 'Anual',
            'recurrence_interval': 1,
            'start_date': now.date(),
            'next_due_date': (now + timedelta(days=365)).date(),
            'estimated_duration_hours': Decimal('12.0'),
            'assigned_to': users['operador1'],
            'status': 'Activo',
            'created_by': users['supervisor1'],
        },
    ]
    
    plans = []
    for plan_data in plans_data:
        plan = MaintenancePlan.objects.create(**plan_data)
        plans.append(plan)
    
    print(f"  ✓ {len(plans)} planes de mantenimiento creados")
    return plans


def create_stock_movements(spare_parts, users):
    """Crea movimientos de stock de muestra."""
    print("\n📦 Creando movimientos de stock...")
    
    movements_count = 0
    
    # Crear movimientos iniciales para cada repuesto
    for part in spare_parts:
        StockMovement.objects.create(
            spare_part=part,
            movement_type='INITIAL',
            quantity=part.quantity,
            quantity_before=0,
            quantity_after=part.quantity,
            unit_cost=part.unit_cost,
            user=users['admin'],
            notes='Inventario inicial'
        )
        movements_count += 1
    
    print(f"  ✓ {movements_count} movimientos de stock creados")



def main():
    """Función principal."""
    print("=" * 60)
    print("🚀 SCRIPT DE LIMPIEZA Y POBLACIÓN DE DATOS")
    print("=" * 60)
    print()
    
    # Confirmar con el usuario
    response = input("⚠️  ADVERTENCIA: Este script eliminará TODOS los datos existentes.\n¿Desea continuar? (escriba 'SI' para confirmar): ")
    
    if response.upper() != 'SI':
        print("\n❌ Operación cancelada por el usuario.")
        return
    
    print("\n" + "=" * 60)
    
    try:
        # Paso 1: Limpiar datos
        clear_all_data()
        
        # Paso 2: Crear usuarios
        users = create_users()
        
        # Paso 3: Crear configuración
        categories, priorities, wo_types = create_configuration(users)
        
        # Paso 4: Crear ubicaciones
        locations = create_locations()
        
        # Paso 5: Crear activos
        assets = create_assets(locations, users)
        
        # Paso 6: Crear repuestos
        spare_parts = create_spare_parts(users)
        
        # Paso 7: Crear órdenes de trabajo
        work_orders = create_work_orders(assets, users)
        
        # Paso 8: Crear planes de mantenimiento
        maintenance_plans = create_maintenance_plans(assets, users)
        
        # Paso 9: Crear movimientos de stock
        create_stock_movements(spare_parts, users)
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📊 RESUMEN DE DATOS CREADOS:")
        print(f"  • Usuarios: {User.objects.count()}")
        print(f"  • Ubicaciones: {Location.objects.count()}")
        print(f"  • Activos: {Asset.objects.count()}")
        print(f"  • Órdenes de Trabajo: {WorkOrder.objects.count()}")
        print(f"  • Planes de Mantenimiento: {MaintenancePlan.objects.count()}")
        print(f"  • Repuestos: {SparePart.objects.count()}")
        print(f"  • Movimientos de Stock: {StockMovement.objects.count()}")
        print(f"  • Categorías: {AssetCategory.objects.count()}")
        print(f"  • Prioridades: {Priority.objects.count()}")
        print(f"  • Tipos de Orden: {WorkOrderType.objects.count()}")
        
        print("\n👥 CREDENCIALES DE ACCESO:")
        print("  Admin:")
        print("    Usuario: admin")
        print("    Password: admin123")
        print("\n  Supervisores:")
        print("    Usuario: supervisor1 / Password: super123")
        print("    Usuario: supervisor2 / Password: super123")
        print("\n  Operadores:")
        print("    Usuario: operador1 / Password: oper123")
        print("    Usuario: operador2 / Password: oper123")
        print("    Usuario: operador3 / Password: oper123")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
