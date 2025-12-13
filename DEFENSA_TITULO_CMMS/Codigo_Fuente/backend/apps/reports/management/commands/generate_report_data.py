from django.core.management.base import BaseCommand
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.authentication.models import User
from apps.inventory.models import SparePart, StockMovement
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Generate sample data for reports and analytics'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("🚀 Generando datos de ejemplo para reportes")
        self.stdout.write("=" * 60)
        self.stdout.write("")
        
        self.generate_work_orders()
        self.generate_stock_movements()
        
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("🎉 Datos generados exitosamente"))
        self.stdout.write("=" * 60)
        self.stdout.write("\n📊 Ahora puedes ver los gráficos en: http://localhost:5173/reports")
    
    def generate_work_orders(self):
        """Generate sample work orders with completion data."""
        self.stdout.write("🔧 Generando órdenes de trabajo...")
        
        assets = list(Asset.objects.all())
        users = list(User.objects.all())
        
        if not assets or not users:
            self.stdout.write(self.style.ERROR("❌ No hay activos o usuarios disponibles"))
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
                self.stdout.write(f"  ✅ Creadas {created_count} órdenes...")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Total: {created_count} órdenes de trabajo creadas"))
        
        # Show summary
        total = WorkOrder.objects.count()
        by_status = {}
        for status in ['Pendiente', 'En Progreso', 'Completada']:
            count = WorkOrder.objects.filter(status=status).count()
            by_status[status] = count
        
        self.stdout.write("\n📊 Resumen:")
        self.stdout.write(f"   Total: {total}")
        for status, count in by_status.items():
            self.stdout.write(f"   {status}: {count}")
    
    def generate_stock_movements(self):
        """Generate sample stock movements."""
        self.stdout.write("\n📦 Generando movimientos de inventario...")
        
        spare_parts = list(SparePart.objects.all())
        users = list(User.objects.all())
        
        if not spare_parts or not users:
            self.stdout.write(self.style.ERROR("❌ No hay repuestos o usuarios disponibles"))
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
            
            # Get current stock
            quantity_before = spare_part.quantity
            
            # Calculate new stock
            if movement_type == StockMovement.MOVEMENT_IN:
                quantity_after = quantity_before + quantity
            else:
                quantity_after = max(0, quantity_before - quantity)
            
            movement = StockMovement.objects.create(
                spare_part=spare_part,
                movement_type=movement_type,
                quantity=quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                unit_cost=spare_part.unit_cost,
            )
            
            # Update spare part stock
            spare_part.quantity = quantity_after
            spare_part.save()
            
            # Set created_at to past date
            movement.created_at = created_date
            movement.save()
            
            created_count += 1
            
            if created_count % 10 == 0:
                self.stdout.write(f"  ✅ Creados {created_count} movimientos...")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Total: {created_count} movimientos de inventario creados"))
