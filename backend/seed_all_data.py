"""
Script to seed all sample data for CMMS system
Run this to populate the database with test data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role
from apps.assets.models import Asset, Location
from apps.work_orders.models import WorkOrder
from apps.inventory.models import SparePart
from apps.maintenance.models import MaintenancePlan
from apps.ml_predictions.models import FailurePrediction
from datetime import datetime, timedelta
import random


def create_roles():
    """Create default roles"""
    print("\n📋 Creating roles...")
    roles = {
        'ADMIN': 'Administrator with full access',
        'SUPERVISOR': 'Supervisor with management access',
        'OPERADOR': 'Operator with basic access'
    }
    
    for name, description in roles.items():
        role, created = Role.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            print(f"  ✓ Created role: {name}")
        else:
            print(f"  - Role already exists: {name}")


def create_users():
    """Create sample users"""
    print("\n👥 Creating users...")
    
    admin_role = Role.objects.get(name='ADMIN')
    supervisor_role = Role.objects.get(name='SUPERVISOR')
    operator_role = Role.objects.get(name='OPERADOR')
    
    users_data = [
        ('admin', 'admin@cmms.com', 'admin123', admin_role, 'Admin', 'User'),
        ('supervisor', 'supervisor@cmms.com', 'super123', supervisor_role, 'Super', 'Visor'),
        ('operator1', 'operator1@cmms.com', 'oper123', operator_role, 'Operator', 'One'),
        ('operator2', 'operator2@cmms.com', 'oper123', operator_role, 'Operator', 'Two'),
    ]
    
    for username, email, password, role, first_name, last_name in users_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            print(f"  ✓ Created user: {username} ({role.name})")
        else:
            print(f"  - User already exists: {username}")


def create_locations():
    """Create sample locations"""
    print("\n📍 Creating locations...")
    
    locations_data = [
        ('Planta Principal', 'Av. Industrial 123, Lima', 'Planta de producción principal'),
        ('Almacén Central', 'Calle Logística 456, Lima', 'Almacén central de repuestos'),
        ('Taller de Mantenimiento', 'Jr. Mecánica 789, Lima', 'Taller de reparaciones'),
        ('Zona de Carga', 'Av. Transporte 321, Callao', 'Área de carga y descarga'),
    ]
    
    for name, address, description in locations_data:
        location, created = Location.objects.get_or_create(
            name=name,
            defaults={'address': address, 'description': description}
        )
        if created:
            print(f"  ✓ Created location: {name}")
        else:
            print(f"  - Location already exists: {name}")


def create_assets():
    """Create sample assets"""
    print("\n🚛 Creating assets...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create assets.")
        return
    
    locations = list(Location.objects.all())
    if not locations:
        print("  ⚠ No locations found. Creating default location...")
        location = Location.objects.create(
            name='Default Location',
            address='Default Address'
        )
        locations = [location]
    
    assets_data = [
        ('Camión Volquete 001', 'VOLQUETE', 'ABC-123', 'VOL-2023-001', 'OPERATIONAL'),
        ('Excavadora CAT 320', 'EXCAVADORA', 'DEF-456', 'EXC-2023-001', 'OPERATIONAL'),
        ('Cargador Frontal L200', 'CARGADOR_FRONTAL', 'GHI-789', 'CAR-2023-001', 'MAINTENANCE'),
        ('Retroexcavadora JCB', 'RETROEXCAVADORA', 'JKL-012', 'RET-2023-001', 'OPERATIONAL'),
        ('Minicargador Bobcat', 'MINICARGADOR', 'MNO-345', 'MIN-2023-001', 'OUT_OF_SERVICE'),
        ('Camión Volquete 002', 'VOLQUETE', 'PQR-678', 'VOL-2023-002', 'OPERATIONAL'),
        ('Excavadora Komatsu', 'EXCAVADORA', 'STU-901', 'EXC-2023-002', 'OPERATIONAL'),
        ('Cargador Frontal L300', 'CARGADOR_FRONTAL', 'VWX-234', 'CAR-2023-002', 'OPERATIONAL'),
    ]
    
    created_count = 0
    for name, vehicle_type, license_plate, serial_number, status in assets_data:
        if not Asset.objects.filter(serial_number=serial_number).exists() and \
           not Asset.objects.filter(license_plate=license_plate).exists():
            Asset.objects.create(
                name=name,
                vehicle_type=vehicle_type,
                license_plate=license_plate,
                serial_number=serial_number,
                status=status,
                location=random.choice(locations),
                installation_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
                created_by=admin_user
            )
            created_count += 1
            print(f"  ✓ Created asset: {name}")
        else:
            print(f"  - Asset already exists: {name}")
    
    print(f"  Total: {created_count} assets created")


def create_spare_parts():
    """Create sample spare parts"""
    print("\n🔧 Creating spare parts...")
    
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("  ⚠ No admin user found. Cannot create spare parts.")
        return
    
    parts_data = [
        ('Filtro de Aceite', 'FO-001', 50, 10, 150.00),
        ('Filtro de Aire', 'FA-001', 30, 10, 80.00),
        ('Pastillas de Freno', 'PF-001', 20, 5, 250.00),
        ('Aceite Hidráulico 20L', 'AH-001', 15, 5, 450.00),
        ('Correa de Distribución', 'CD-001', 10, 3, 180.00),
        ('Batería 12V', 'BAT-001', 8, 2, 350.00),
        ('Neumático 18"', 'NEU-001', 12, 4, 800.00),
        ('Bujías (Set 4)', 'BUJ-001', 25, 8, 120.00),
    ]
    
    created_count = 0
    for name, part_number, quantity, min_qty, unit_cost in parts_data:
        if not SparePart.objects.filter(part_number=part_number).exists():
            SparePart.objects.create(
                name=name,
                part_number=part_number,
                quantity=quantity,
                min_quantity=min_qty,
                unit_cost=unit_cost,
                description=f'Repuesto: {name}',
                created_by=admin_user
            )
            created_count += 1
            print(f"  ✓ Created spare part: {name}")
        else:
            print(f"  - Spare part already exists: {name}")
    
    print(f"  Total: {created_count} spare parts created")


def create_work_orders():
    """Create sample work orders"""
    print("\n📋 Creating work orders...")
    
    assets = list(Asset.objects.all())
    users = list(User.objects.filter(role__name__in=['SUPERVISOR', 'OPERADOR']))
    
    if not assets or not users:
        print("  ⚠ Need assets and users to create work orders")
        return
    
    statuses = ['Pendiente', 'En Progreso', 'Completada']
    priorities = ['Baja', 'Media', 'Alta', 'Urgente']
    
    created_count = 0
    for i in range(10):
        asset = random.choice(assets)
        assigned_to = random.choice(users)
        status = random.choice(statuses)
        priority = random.choice(priorities)
        
        wo = WorkOrder.objects.create(
            title=f'Mantenimiento {asset.vehicle_type} - {i+1}',
            description=f'Realizar mantenimiento preventivo en {asset.name}',
            priority=priority,
            status=status,
            asset=asset,
            assigned_to=assigned_to,
            created_by=assigned_to,
            scheduled_date=datetime.now() + timedelta(days=random.randint(1, 30))
        )
        
        if status == 'Completada':
            wo.completed_date = datetime.now() - timedelta(days=random.randint(1, 10))
            wo.actual_hours = random.uniform(2, 8)
            wo.save()
        
        created_count += 1
    
    print(f"  ✓ Created {created_count} work orders")


def create_maintenance_plans():
    """Create sample maintenance plans"""
    print("\n🔄 Creating maintenance plans...")
    
    assets = list(Asset.objects.all())
    users = list(User.objects.filter(role__name='SUPERVISOR'))
    
    if not assets or not users:
        print("  ⚠ Need assets and users to create maintenance plans")
        return
    
    created_count = 0
    for asset in assets[:5]:  # Create plans for first 5 assets
        user = random.choice(users)
        
        MaintenancePlan.objects.create(
            name=f'Plan Preventivo - {asset.name}',
            description=f'Mantenimiento preventivo programado para {asset.name}',
            asset=asset,
            recurrence_type='Mensual',
            recurrence_interval=1,
            start_date=datetime.now().date(),
            next_due_date=datetime.now().date() + timedelta(days=30),
            status='Activo',
            created_by=user
        )
        created_count += 1
    
    print(f"  ✓ Created {created_count} maintenance plans")


def create_predictions():
    """Create sample ML predictions"""
    print("\n🤖 Creating ML predictions...")
    
    assets = list(Asset.objects.all())
    
    if not assets:
        print("  ⚠ Need assets to create predictions")
        return
    
    risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    created_count = 0
    for asset in assets[:5]:  # Create predictions for first 5 assets
        risk_level = random.choice(risk_levels)
        probability = {
            'LOW': random.uniform(0.1, 0.3),
            'MEDIUM': random.uniform(0.3, 0.5),
            'HIGH': random.uniform(0.5, 0.7),
            'CRITICAL': random.uniform(0.7, 0.9),
        }[risk_level]
        
        FailurePrediction.objects.create(
            asset=asset,
            failure_probability=probability,
            risk_level=risk_level,
            model_version='1.0.0',
            confidence_score=random.uniform(0.7, 0.95),
            estimated_days_to_failure=random.randint(7, 90),
            recommended_action=f'Revisar {asset.vehicle_type} - Riesgo {risk_level}',
            features_snapshot={'hours': random.randint(100, 1000)}
        )
        created_count += 1
    
    print(f"  ✓ Created {created_count} predictions")


def seed_configuration():
    """Seed configuration data"""
    print("\n⚙️ Seeding configuration data...")
    import subprocess
    result = subprocess.run(['python', 'seed_configuration.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ Configuration data seeded successfully")
    else:
        print(f"  ⚠ Configuration seeding had issues: {result.stderr}")


def main():
    """Main function to seed all data"""
    print("\n" + "="*60)
    print("  SEEDING CMMS DATABASE WITH SAMPLE DATA")
    print("="*60)
    
    try:
        create_roles()
        create_users()
        seed_configuration()  # Seed configuration first
        create_locations()
        create_assets()
        create_spare_parts()
        create_work_orders()
        create_maintenance_plans()
        create_predictions()
        
        print("\n" + "="*60)
        print("  ✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  - Users: {User.objects.count()}")
        print(f"  - Locations: {Location.objects.count()}")
        print(f"  - Assets: {Asset.objects.count()}")
        print(f"  - Spare Parts: {SparePart.objects.count()}")
        print(f"  - Work Orders: {WorkOrder.objects.count()}")
        print(f"  - Maintenance Plans: {MaintenancePlan.objects.count()}")
        print(f"  - Predictions: {FailurePrediction.objects.count()}")
        print("\n🔐 Login Credentials:")
        print("  - Admin: admin / admin123")
        print("  - Supervisor: supervisor / super123")
        print("  - Operator: operator1 / oper123")
        print("\n🌐 Access the system at: http://localhost:5173")
        print()
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
