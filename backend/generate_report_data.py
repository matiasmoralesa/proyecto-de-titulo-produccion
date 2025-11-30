#!/usr/bin/env python
"""
Script to generate sample data for reports and analytics
"""
import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.authentication.models import User
from apps.inventory.models import SparePart, StockMovement
from django.utils import timezone


def generate_work_orders():
    """Generate sample work orders with completion data."""
    print("🔧 Generando órdenes de trabajo...")
    
    assets = list(Asset.objects.all())
    users = list(User.objects.all())
    
    if not assets or not users:
        print("❌ No hay activos o usuarios disponibles")
        return
    
    statuses = ['Pendiente', 'En Progreso', 'Completada']
    priorities = ['Baja', 'Media', 'Alta', 'Urgente']
    
    created_count = 0
    
    # Generate 30 work orders
    for i in range(30):
        asset = random.choice(assets)
        assigned_to = random.choice(users)
        created_by = random.choice(users)
        status = random.choice(statuses)
        priority = random.choice(priorities)
        
        # Random date in the last 60 days
        days_ago = random.randint(1, 60)
        created_date = timezone.now() - timedelta(days=days_ago)
        scheduled_date = created_date + timedelta(days=random.randint(1, 7))
        
        # Create work order
        wo = WorkOrder.objects.create(
            title=f"Mantenimiento {random.choice(['Preventivo', 'Correctivo', 'Predictivo'])} - {asset.name}",
            description=f"Trabajo de mantenimiento para {asset.name}",
            priority=priority,
            status=status,
            asset=asset,
            assigned_to=assigned_to,
            scheduled_date=scheduled_date,
            created_by=created_by,
        )
        
        # Set created_at to past date
        wo.created_at = created_date
        
        # If completed, add completion data
        if status == 'Completada':
            completion_days = random.randint(1, 5)
            wo.completed_date = scheduled_date + timedelta(days=completion_days)
            wo.actual_hours = Decimal(str(random.uniform(1, 8)))
            wo.completion_notes = random.choice([
                'Trabajo completado satisfactoriamente',
                'Reparación exitosa',
                'Mantenimiento preventivo realizado',
                'Problema resuelto',
                'Inspección completada'
            ])
        
        wo.save()
        created_count += 1
        
        if created_count % 10 == 0:
            print(f"  ✅ Creadas {created_count} órdenes...")
    
    print(f"✅ Total: {created_count} órdenes de trabajo creadas")
    
    # Show summary
    total = WorkOrder.objects.count()
    by_status = {}
    for status in ['Pendiente', 'En Progreso', 'Completada']:
        count = WorkOrder.objects.filter(status=status).count()
        by_status[status] = count
    
    print(f"\n📊 Resumen:")
    print(f"   Total: {total}")
    for status, count in by_status.items():
        print(f"   {status}: {count}")


def generate_stock_movements():
    """Generate sample stock movements."""
    print("\n📦 Generando movimientos de inventario...")
    
    spare_parts = list(SparePart.objects.all())
    users = list(User.objects.all())
    
    if not spare_parts or not users:
        print("❌ No hay repuestos o usuarios disponibles")
        return
    
    created_count = 0
    
    # Generate 50 stock movements
    for i in range(50):
        spare_part = random.choice(spare_parts)
        user = random.choice(users)
        
        # Random movement type (more OUT than IN)
        movement_type = random.choice([
            StockMovement.MOVEMENT_OUT,
            StockMovement.MOVEMENT_OUT,
            StockMovement.MOVEMENT_OUT,
            StockMovement.MOVEMENT_IN,
        ])
        
        quantity = random.randint(1, 10)
        
        # Random date in the last 60 days
        days_ago = random.randint(1, 60)
        created_date = timezone.now() - timedelta(days=days_ago)
        
        movement = StockMovement.objects.create(
            spare_part=spare_part,
            movement_type=movement_type,
            quantity=quantity,
            reason=random.choice([
                'Mantenimiento preventivo',
                'Reparación',
                'Reposición de stock',
                'Uso en orden de trabajo',
                'Ajuste de inventario'
            ]),
            performed_by=user,
        )
        
        # Update spare part stock
        if movement_type == StockMovement.MOVEMENT_IN:
            spare_part.current_stock += quantity
        else:
            spare_part.current_stock = max(0, spare_part.current_stock - quantity)
        
        spare_part.save()
        
        # Set created_at to past date
        movement.created_at = created_date
        movement.save()
        
        created_count += 1
        
        if created_count % 10 == 0:
            print(f"  ✅ Creados {created_count} movimientos...")
    
    print(f"✅ Total: {created_count} movimientos de inventario creados")


def main():
    print("=" * 60)
    print("🚀 Generando datos de ejemplo para reportes")
    print("=" * 60)
    print()
    
    generate_work_orders()
    generate_stock_movements()
    
    print()
    print("=" * 60)
    print("🎉 Datos generados exitosamente")
    print("=" * 60)
    print("\n📊 Ahora puedes ver los gráficos en: http://localhost:5173/reports")


if __name__ == '__main__':
    main()
