"""
Script to create sample inventory data for testing.
"""
import os
import sys
import django

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.inventory.models import SparePart, StockMovement
from apps.authentication.models import User
from django.db import models

def create_sample_inventory():
    """Create sample spare parts and stock movements."""
    
    # Get admin user
    admin_user = User.objects.filter(role__name='ADMIN').first()
    if not admin_user:
        print("No se encontró un usuario ADMIN. Ejecuta create_test_users.py primero.")
        return
    
    print("Creando repuestos de ejemplo...")
    
    # Sample spare parts data
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
            'unit_cost': 15.50,
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
            'unit_cost': 22.00,
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
            'unit_cost': 18.75,
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
            'unit_cost': 85.00,
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
            'unit_cost': 75.00,
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
            'unit_cost': 120.00,
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
            'unit_cost': 8.50,
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
            'unit_cost': 12.00,
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
            'unit_cost': 95.00,
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
            'unit_cost': 35.00,
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
            'unit_cost': 180.00,
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
            'unit_cost': 25.00,
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
            'unit_cost': 450.00,
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
            'unit_cost': 6.50,
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
            'unit_cost': 4.00,
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
            print(f"✓ Creado: {spare_part.part_number} - {spare_part.name}")
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
            print(f"  Ya existe: {spare_part.part_number} - {spare_part.name}")
    
    print(f"\n✓ Proceso completado. {len(created_parts)} repuestos creados.")
    
    # Show low stock alerts
    low_stock_parts = SparePart.objects.filter(quantity__lte=models.F('min_quantity'))
    if low_stock_parts.exists():
        print(f"\n⚠ Alertas de stock bajo ({low_stock_parts.count()}):")
        for part in low_stock_parts:
            print(f"  - {part.part_number}: {part.quantity} unidades (mínimo: {part.min_quantity})")

if __name__ == '__main__':
    create_sample_inventory()
