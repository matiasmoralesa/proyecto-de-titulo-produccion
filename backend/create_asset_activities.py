"""
Script to create sample activities for all assets to test the monitoring system.
Creates work orders, status updates, and other activities.
"""
import os
import django
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder
from apps.machine_status.models import AssetStatus, AssetStatusHistory
from apps.authentication.models import User

def create_sample_activities():
    """Create sample activities for all assets."""
    
    print("🚀 Creating sample activities for all assets...")
    
    # Get all active assets
    assets = Asset.objects.filter(is_archived=False)
    print(f"Found {assets.count()} active assets")
    
    if assets.count() == 0:
        print("❌ No assets found. Please create assets first.")
        return
    
    # Get users
    try:
        admin = User.objects.get(username='admin')
        print(f"✅ Found admin user: {admin.username}")
    except User.DoesNotExist:
        print("❌ Admin user not found. Please create users first.")
        return
    
    # Get all users for assignment
    users = list(User.objects.filter(is_active=True))
    print(f"✅ Found {len(users)} active users")
    
    # Status types
    status_types = [
        AssetStatus.OPERANDO,
        AssetStatus.DETENIDA,
        AssetStatus.EN_MANTENIMIENTO,
        AssetStatus.FUERA_DE_SERVICIO
    ]
    
    # Work order priorities
    priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    # Work order statuses
    wo_statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
    
    total_work_orders = 0
    total_status_updates = 0
    
    for asset in assets:
        print(f"\n📦 Processing asset: {asset.name}")
        
        # Create or get asset status
        asset_status, created = AssetStatus.objects.get_or_create(
            asset=asset,
            defaults={
                'status_type': AssetStatus.OPERANDO,
                'odometer_reading': random.randint(1000, 50000),
                'fuel_level': random.randint(50, 100),
                'condition_notes': 'Vehículo en buenas condiciones',
                'last_updated_by': admin
            }
        )
        
        if created:
            print(f"  ✅ Created initial status for {asset.name}")
        
        # Create 3-7 work orders for each asset
        num_work_orders = random.randint(3, 7)
        print(f"  📝 Creating {num_work_orders} work orders...")
        
        for i in range(num_work_orders):
            # Random date in the last 6 months
            days_ago = random.randint(1, 180)
            created_date = timezone.now() - timedelta(days=days_ago)
            
            # Random status
            wo_status = random.choice(wo_statuses)
            
            # Generate work order number
            wo_number = f"WO-{asset.name[:3].upper()}-{random.randint(1000, 9999)}"
            
            # Check if work order already exists
            if WorkOrder.objects.filter(work_order_number=wo_number).exists():
                wo_number = f"WO-{asset.name[:3].upper()}-{random.randint(10000, 99999)}"
            
            # Random assigned user
            assigned_user = random.choice(users)
            
            # Work order titles
            titles = [
                "Mantenimiento preventivo programado",
                "Revisión de sistema eléctrico",
                "Cambio de aceite y filtros",
                "Reparación de sistema hidráulico",
                "Inspección general de seguridad",
                "Cambio de neumáticos",
                "Reparación de frenos",
                "Mantenimiento de motor"
            ]
            
            work_order = WorkOrder.objects.create(
                work_order_number=wo_number,
                title=random.choice(titles),
                description=f"Trabajo de mantenimiento para {asset.name}",
                priority=random.choice(priorities),
                status=wo_status,
                asset=asset,
                assigned_to=assigned_user,
                scheduled_date=created_date + timedelta(days=1),
                created_by=admin,
                created_at=created_date,
                updated_at=created_date
            )
            
            # If completed, add completion data
            if wo_status == 'COMPLETED':
                completion_date = created_date + timedelta(days=random.randint(1, 5))
                work_order.completed_date = completion_date
                work_order.actual_hours = Decimal(str(random.uniform(1.0, 8.0)))
                work_order.completion_notes = f"Trabajo completado satisfactoriamente. {random.choice(['Sin problemas adicionales.', 'Se encontraron desgastes menores.', 'Todo en orden.'])}"
                work_order.updated_at = completion_date
                work_order.save()
            
            total_work_orders += 1
        
        print(f"  ✅ Created {num_work_orders} work orders")
        
        # Create 5-10 status updates for each asset
        num_status_updates = random.randint(5, 10)
        print(f"  📊 Creating {num_status_updates} status updates...")
        
        for i in range(num_status_updates):
            # Random date in the last 6 months
            days_ago = random.randint(1, 180)
            update_date = timezone.now() - timedelta(days=days_ago)
            
            # Random status
            new_status = random.choice(status_types)
            
            # Random odometer (increasing over time)
            base_odometer = asset_status.odometer_reading or 1000
            odometer = base_odometer + random.randint(0, 1000)
            
            # Random fuel level
            fuel = random.randint(20, 100)
            
            # Condition notes based on status
            notes_by_status = {
                AssetStatus.OPERANDO: [
                    "Vehículo operando normalmente",
                    "Sin novedades",
                    "Todo en orden",
                    "Funcionamiento óptimo"
                ],
                AssetStatus.DETENIDA: [
                    "Vehículo detenido temporalmente",
                    "En espera de asignación",
                    "Pausa operacional"
                ],
                AssetStatus.EN_MANTENIMIENTO: [
                    "En mantenimiento preventivo",
                    "Revisión programada",
                    "Mantenimiento correctivo en curso"
                ],
                AssetStatus.FUERA_DE_SERVICIO: [
                    "Requiere reparación mayor",
                    "Fuera de servicio por falla",
                    "En espera de repuestos"
                ]
            }
            
            # Create status history entry
            AssetStatusHistory.objects.create(
                asset=asset,
                status_type=new_status,
                odometer_reading=odometer,
                fuel_level=fuel,
                condition_notes=random.choice(notes_by_status[new_status]),
                updated_by=random.choice(users),
                timestamp=update_date
            )
            
            total_status_updates += 1
        
        print(f"  ✅ Created {num_status_updates} status updates")
        
        # Update current asset status to most recent
        latest_history = AssetStatusHistory.objects.filter(asset=asset).order_by('-timestamp').first()
        if latest_history:
            asset_status.status_type = latest_history.status_type
            asset_status.odometer_reading = latest_history.odometer_reading
            asset_status.fuel_level = latest_history.fuel_level
            asset_status.condition_notes = latest_history.condition_notes
            asset_status.last_updated_by = latest_history.updated_by
            asset_status.updated_at = latest_history.timestamp
            asset_status.save()
    
    print(f"\n✅ Sample data creation completed!")
    print(f"📊 Summary:")
    print(f"   - Assets processed: {assets.count()}")
    print(f"   - Total work orders created: {total_work_orders}")
    print(f"   - Total status updates created: {total_status_updates}")
    print(f"\n🎉 You can now test the monitoring system with real data!")

if __name__ == '__main__':
    create_sample_activities()
