"""
Management command to create sample inventory data.
"""
from django.core.management.base import BaseCommand
from django.db import models
from apps.inventory.models import SparePart, StockMovement
from apps.authentication.models import User


class Command(BaseCommand):
    help = 'Create sample inventory data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creando repuestos de ejemplo...')
        
        # Get admin user
        admin_user = User.objects.filter(role__name='ADMIN').first()
        if not admin_user:
            self.stdout.write(self.style.ERROR(
                'No se encontró un usuario ADMIN. Ejecuta create_test_users.py primero.'
            ))
            return
        
        # Sample spare parts data (precios en CLP - Pesos Chilenos)
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
                'unit_cost': 12500,
                'storage_location': 'Estante A-1',
            },
            {
                'part_number': 'FLT-002',
                'name': 'Filtro de Aire',
                'description': 'Filtro de aire para motor diesel',
                'category': 'Filtros',
                'manufacturer': 'Mann Filter',
                'quantity': 8,
                'min_quantity': 10,
                'unit_of_measure': 'unidad',
                'unit_cost': 18500,
                'storage_location': 'Estante A-2',
            },
            {
                'part_number': 'FLT-003',
                'name': 'Filtro de Combustible',
                'description': 'Filtro de combustible diesel',
                'category': 'Filtros',
                'manufacturer': 'Bosch',
                'quantity': 15,
                'min_quantity': 8,
                'unit_of_measure': 'unidad',
                'unit_cost': 15800,
                'storage_location': 'Estante A-3',
            },
            {
                'part_number': 'BRK-001',
                'name': 'Pastillas de Freno Delanteras',
                'description': 'Juego de pastillas de freno delanteras',
                'category': 'Frenos',
                'manufacturer': 'Brembo',
                'quantity': 12,
                'min_quantity': 6,
                'unit_of_measure': 'juego',
                'unit_cost': 75000,
                'storage_location': 'Estante B-1',
            },
            {
                'part_number': 'BRK-002',
                'name': 'Pastillas de Freno Traseras',
                'description': 'Juego de pastillas de freno traseras',
                'category': 'Frenos',
                'manufacturer': 'Brembo',
                'quantity': 10,
                'min_quantity': 6,
                'unit_of_measure': 'juego',
                'unit_cost': 65000,
                'storage_location': 'Estante B-2',
            },
            {
                'part_number': 'BRK-003',
                'name': 'Disco de Freno',
                'description': 'Disco de freno ventilado',
                'category': 'Frenos',
                'manufacturer': 'Brembo',
                'quantity': 4,
                'min_quantity': 4,
                'unit_of_measure': 'unidad',
                'unit_cost': 95000,
                'storage_location': 'Estante B-3',
            },
            {
                'part_number': 'OIL-001',
                'name': 'Aceite de Motor 15W-40',
                'description': 'Aceite mineral para motor diesel',
                'category': 'Lubricantes',
                'manufacturer': 'Shell',
                'quantity': 50,
                'min_quantity': 20,
                'unit_of_measure': 'litro',
                'unit_cost': 7500,
                'storage_location': 'Bodega Principal',
            },
            {
                'part_number': 'OIL-002',
                'name': 'Aceite Hidráulico',
                'description': 'Aceite hidráulico ISO 68',
                'category': 'Lubricantes',
                'manufacturer': 'Mobil',
                'quantity': 30,
                'min_quantity': 15,
                'unit_of_measure': 'litro',
                'unit_cost': 9800,
                'storage_location': 'Bodega Principal',
            },
            {
                'part_number': 'BLT-001',
                'name': 'Correa de Distribución',
                'description': 'Correa de distribución reforzada',
                'category': 'Transmisión',
                'manufacturer': 'Gates',
                'quantity': 6,
                'min_quantity': 4,
                'unit_of_measure': 'unidad',
                'unit_cost': 85000,
                'storage_location': 'Estante C-1',
            },
            {
                'part_number': 'BLT-002',
                'name': 'Correa de Alternador',
                'description': 'Correa serpentina para alternador',
                'category': 'Transmisión',
                'manufacturer': 'Gates',
                'quantity': 8,
                'min_quantity': 5,
                'unit_of_measure': 'unidad',
                'unit_cost': 32000,
                'storage_location': 'Estante C-2',
            },
            {
                'part_number': 'BAT-001',
                'name': 'Batería 12V 100Ah',
                'description': 'Batería de arranque libre de mantenimiento',
                'category': 'Eléctrico',
                'manufacturer': 'Bosch',
                'quantity': 5,
                'min_quantity': 3,
                'unit_of_measure': 'unidad',
                'unit_cost': 165000,
                'storage_location': 'Bodega Eléctrica',
            },
            {
                'part_number': 'LMP-001',
                'name': 'Lámpara LED H7',
                'description': 'Lámpara LED para faros principales',
                'category': 'Eléctrico',
                'manufacturer': 'Philips',
                'quantity': 20,
                'min_quantity': 10,
                'unit_of_measure': 'unidad',
                'unit_cost': 22000,
                'storage_location': 'Bodega Eléctrica',
            },
            {
                'part_number': 'TIR-001',
                'name': 'Neumático 275/70R22.5',
                'description': 'Neumático para camión',
                'category': 'Neumáticos',
                'manufacturer': 'Michelin',
                'quantity': 8,
                'min_quantity': 6,
                'unit_of_measure': 'unidad',
                'unit_cost': 420000,
                'storage_location': 'Bodega de Neumáticos',
            },
            {
                'part_number': 'CLN-001',
                'name': 'Líquido Refrigerante',
                'description': 'Anticongelante concentrado',
                'category': 'Fluidos',
                'manufacturer': 'Prestone',
                'quantity': 25,
                'min_quantity': 15,
                'unit_of_measure': 'litro',
                'unit_cost': 5500,
                'storage_location': 'Bodega Principal',
            },
            {
                'part_number': 'WSH-001',
                'name': 'Líquido Limpiaparabrisas',
                'description': 'Líquido limpiaparabrisas concentrado',
                'category': 'Fluidos',
                'manufacturer': 'Rain-X',
                'quantity': 15,
                'min_quantity': 10,
                'unit_of_measure': 'litro',
                'unit_cost': 3500,
                'storage_location': 'Bodega Principal',
            },
        ]
        
        created_parts = []
        for part_data in spare_parts_data:
            spare_part, created = SparePart.objects.get_or_create(
                part_number=part_data['part_number'],
                defaults={**part_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"✓ Creado: {spare_part.part_number} - {spare_part.name}"
                ))
                created_parts.append(spare_part)
                
                # Create initial stock movement
                StockMovement.objects.create(
                    spare_part=spare_part,
                    movement_type=StockMovement.MOVEMENT_INITIAL,
                    quantity=spare_part.quantity,
                    quantity_before=0,
                    quantity_after=spare_part.quantity,
                    unit_cost=spare_part.unit_cost,
                    user=admin_user,
                    notes='Inventario inicial'
                )
            else:
                self.stdout.write(f"  Ya existe: {spare_part.part_number} - {spare_part.name}")
        
        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Proceso completado. {len(created_parts)} repuestos creados."
        ))
        
        # Show low stock alerts
        low_stock_parts = SparePart.objects.filter(quantity__lte=models.F('min_quantity'))
        if low_stock_parts.exists():
            self.stdout.write(self.style.WARNING(
                f"\n⚠ Alertas de stock bajo ({low_stock_parts.count()}):"
            ))
            for part in low_stock_parts:
                self.stdout.write(
                    f"  - {part.part_number}: {part.quantity} unidades (mínimo: {part.min_quantity})"
                )
