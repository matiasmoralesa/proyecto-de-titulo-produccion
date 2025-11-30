"""
Script to create sample work orders.
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.authentication.models import User

# Get users
admin = User.objects.get(username='admin')
users = list(User.objects.all())

# Get assets
assets = list(Asset.objects.all()[:5])

# Sample work orders
work_orders_data = [
    {
        'title': 'Mantenimiento preventivo 1000 horas',
        'description': 'Cambio de aceite, filtros y revisión general del motor',
        'priority': WorkOrder.PRIORITY_HIGH,
        'status': WorkOrder.STATUS_PENDING,
        'asset': assets[0],
        'assigned_to': users[0],
        'scheduled_date': datetime.now() + timedelta(days=2),
    },
    {
        'title': 'Reparación de sistema hidráulico',
        'description': 'Fuga detectada en cilindro principal, requiere reemplazo de sellos',
        'priority': WorkOrder.PRIORITY_URGENT,
        'status': WorkOrder.STATUS_IN_PROGRESS,
        'asset': assets[1],
        'assigned_to': users[0],
        'scheduled_date': datetime.now(),
    },
    {
        'title': 'Inspección de frenos',
        'description': 'Revisión completa del sistema de frenos y pastillas',
        'priority': WorkOrder.PRIORITY_MEDIUM,
        'status': WorkOrder.STATUS_PENDING,
        'asset': assets[2],
        'assigned_to': users[0],
        'scheduled_date': datetime.now() + timedelta(days=5),
    },
    {
        'title': 'Cambio de neumáticos',
        'description': 'Reemplazo de neumáticos delanteros por desgaste',
        'priority': WorkOrder.PRIORITY_LOW,
        'status': WorkOrder.STATUS_COMPLETED,
        'asset': assets[3],
        'assigned_to': users[0],
        'scheduled_date': datetime.now() - timedelta(days=3),
        'completed_date': datetime.now() - timedelta(days=1),
        'completion_notes': 'Neumáticos reemplazados exitosamente. Sin problemas.',
        'actual_hours': 2.5,
    },
    {
        'title': 'Revisión eléctrica',
        'description': 'Diagnóstico de sistema eléctrico por falla intermitente',
        'priority': WorkOrder.PRIORITY_HIGH,
        'status': WorkOrder.STATUS_IN_PROGRESS,
        'asset': assets[4],
        'assigned_to': users[0],
        'scheduled_date': datetime.now() - timedelta(days=1),
    },
]

print('Creating sample work orders...\n')

created_count = 0
for wo_data in work_orders_data:
    wo = WorkOrder.objects.create(
        **wo_data,
        created_by=admin
    )
    created_count += 1
    print(f'✓ Created: {wo.work_order_number} - {wo.title} ({wo.status})')

print(f'\n✓ Successfully created {created_count} work order(s)')
print(f'Total work orders: {WorkOrder.objects.count()}')
