"""
Management command to seed spare parts usage data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from apps.inventory.models import SparePart, StockMovement
from apps.work_orders.models import WorkOrder
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Seed spare parts usage data for work orders'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("GENERANDO DATOS DE USO DE REPUESTOS")
        self.stdout.write("=" * 60)

        # Obtener datos necesarios
        spare_parts = list(SparePart.objects.all())
        work_orders = list(WorkOrder.objects.filter(status='Completada')[:50])
        admin_user = User.objects.filter(role__name='ADMIN').first()

        if not spare_parts:
            self.stdout.write(self.style.ERROR("❌ No hay repuestos en el sistema"))
            return

        if not work_orders:
            self.stdout.write(self.style.ERROR("❌ No hay órdenes de trabajo completadas"))
            return

        self.stdout.write(f"\n✅ Repuestos: {len(spare_parts)}")
        self.stdout.write(f"✅ Órdenes completadas: {len(work_orders)}")

        # Primero, agregar stock inicial a todos los repuestos
        self.stdout.write("\n📦 Agregando stock inicial...")
        for part in spare_parts:
            initial_stock = random.randint(50, 200)
            old_quantity = part.quantity
            part.quantity = initial_stock
            part.save()
            
            StockMovement.objects.create(
                spare_part=part,
                movement_type='IN',
                quantity=initial_stock,
                quantity_before=old_quantity,
                quantity_after=initial_stock,
                unit_cost=Decimal(str(random.uniform(10, 500))),
                user=admin_user,
                notes='Stock inicial - Compra de repuestos'
            )
            
            self.stdout.write(f"   ✅ {part.name}: {initial_stock} unidades")

        # Crear movimientos de salida (uso en órdenes de trabajo)
        self.stdout.write("\n📤 Creando movimientos de salida...")
        movements_created = 0

        for wo in work_orders:
            # Cada orden usa entre 1 y 4 repuestos diferentes
            num_parts = random.randint(1, 4)
            used_parts = random.sample(spare_parts, min(num_parts, len(spare_parts)))

            for part in used_parts:
                quantity = random.randint(1, 5)
                
                try:
                    # Refrescar el repuesto para obtener la cantidad actual
                    part.refresh_from_db()
                    old_quantity = part.quantity
                    new_quantity = max(0, old_quantity - quantity)
                    part.quantity = new_quantity
                    part.save()
                    
                    StockMovement.objects.create(
                        spare_part=part,
                        movement_type='OUT',
                        quantity=quantity,
                        quantity_before=old_quantity,
                        quantity_after=new_quantity,
                        unit_cost=Decimal(str(random.uniform(10, 500))),
                        user=admin_user,
                        reference_type='work_order',
                        reference_id=str(wo.id),
                        notes=f'Usado en OT {wo.work_order_number}'
                    )
                    movements_created += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   ⚠️  Error: {e}"))

        self.stdout.write(f"\n✅ Movimientos de salida creados: {movements_created}")

        # Resumen
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ GENERACIÓN COMPLETADA"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\nResumen:")
        self.stdout.write(f"  - Repuestos con stock: {len(spare_parts)}")
        self.stdout.write(f"  - Movimientos de salida: {movements_created}")
        self.stdout.write(f"  - Órdenes con repuestos: {len(work_orders)}")
