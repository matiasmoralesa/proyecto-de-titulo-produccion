"""
Script to create sample maintenance plans.
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.maintenance.models import MaintenancePlan
from apps.assets.models import Asset
from apps.authentication.models import User

# Get users
admin_user = User.objects.filter(role__name='ADMIN').first()
operator_user = User.objects.filter(role__name='OPERADOR').first()

if not admin_user:
    print("❌ Error: No se encontró usuario ADMIN")
    exit(1)

# Get assets
assets = Asset.objects.all()[:5]

if not assets:
    print("❌ Error: No se encontraron activos")
    exit(1)

print(f"✓ Encontrados {len(assets)} activos")

# Sample maintenance plans
maintenance_plans = [
    {
        'name': 'Cambio de Aceite',
        'description': 'Cambio de aceite de motor y filtro',
        'asset': assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_MONTHLY,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'estimated_duration_hours': 1.5,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Revisión de Frenos',
        'description': 'Inspección y ajuste del sistema de frenos',
        'asset': assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_QUARTERLY,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'estimated_duration_hours': 2.0,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Mantenimiento por Horas',
        'description': 'Mantenimiento preventivo cada 100 horas de uso',
        'asset': assets[1] if len(assets) > 1 else assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_HOURS,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'usage_threshold': 100,
        'last_usage_value': 45,
        'estimated_duration_hours': 3.0,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Inspección Anual',
        'description': 'Inspección técnica vehicular anual',
        'asset': assets[2] if len(assets) > 2 else assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_YEARLY,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'estimated_duration_hours': 4.0,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Revisión Semanal',
        'description': 'Revisión general semanal de niveles y estado',
        'asset': assets[3] if len(assets) > 3 else assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_WEEKLY,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'estimated_duration_hours': 0.5,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Mantenimiento por Kilómetros',
        'description': 'Mantenimiento cada 5000 km',
        'asset': assets[4] if len(assets) > 4 else assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_KILOMETERS,
        'recurrence_interval': 1,
        'start_date': date.today(),
        'usage_threshold': 5000,
        'last_usage_value': 3200,
        'estimated_duration_hours': 2.5,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_ACTIVE,
        'created_by': admin_user,
    },
    {
        'name': 'Plan Pausado',
        'description': 'Este plan está temporalmente pausado',
        'asset': assets[0],
        'recurrence_type': MaintenancePlan.RECURRENCE_MONTHLY,
        'recurrence_interval': 2,
        'start_date': date.today() - timedelta(days=30),
        'estimated_duration_hours': 1.0,
        'assigned_to': operator_user,
        'status': MaintenancePlan.STATUS_PAUSED,
        'is_paused': True,
        'created_by': admin_user,
    },
]

# Create maintenance plans
created_count = 0
for plan_data in maintenance_plans:
    # Check if plan already exists
    existing = MaintenancePlan.objects.filter(
        name=plan_data['name'],
        asset=plan_data['asset']
    ).first()
    
    if existing:
        print(f"⚠ Plan ya existe: {plan_data['name']} - {plan_data['asset'].name}")
        continue
    
    try:
        plan = MaintenancePlan.objects.create(**plan_data)
        created_count += 1
        
        status_emoji = "⏸" if plan.is_paused else "✓"
        print(f"{status_emoji} Creado: {plan.name} - {plan.asset.name} ({plan.recurrence_type})")
        
        if plan.next_due_date:
            print(f"  Próximo mantenimiento: {plan.next_due_date}")
        elif plan.usage_until_due():
            unit = 'hrs' if plan.recurrence_type == MaintenancePlan.RECURRENCE_HOURS else 'km'
            print(f"  Uso restante: {plan.usage_until_due()} {unit}")
            
    except Exception as e:
        print(f"❌ Error creando {plan_data['name']}: {str(e)}")

print(f"\n✅ Proceso completado!")
print(f"📊 Planes creados: {created_count}")
print(f"📊 Total de planes: {MaintenancePlan.objects.count()}")
