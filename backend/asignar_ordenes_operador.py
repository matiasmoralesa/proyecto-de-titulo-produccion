"""
Script para asignar órdenes de trabajo a un operador.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role
from apps.work_orders.models import WorkOrder

def asignar_ordenes():
    """Asignar órdenes de trabajo a operadores."""
    
    print("\n" + "="*80)
    print("ASIGNACIÓN DE ÓRDENES DE TRABAJO A OPERADORES")
    print("="*80 + "\n")
    
    # Get operador role
    operador_role = Role.objects.get(name=Role.OPERADOR)
    
    # Get all operadores
    operadores = User.objects.filter(role=operador_role)
    
    if not operadores.exists():
        print("❌ No se encontraron operadores en el sistema")
        return
    
    print(f"✅ Operadores encontrados: {operadores.count()}\n")
    
    for operador in operadores:
        print(f"📋 Operador: {operador.username}")
        
        # Count current assignments
        current_assignments = WorkOrder.objects.filter(assigned_to=operador).count()
        print(f"   Órdenes actuales: {current_assignments}")
        
        if current_assignments == 0:
            # Get unassigned work orders
            unassigned_orders = WorkOrder.objects.filter(assigned_to__isnull=True)[:3]
            
            if unassigned_orders.exists():
                print(f"   Asignando {unassigned_orders.count()} órdenes...")
                
                for order in unassigned_orders:
                    order.assigned_to = operador
                    order.save()
                    print(f"      ✅ {order.work_order_number} - {order.title}")
                
                print(f"   ✅ Total asignadas: {unassigned_orders.count()}\n")
            else:
                print(f"   ⚠️  No hay órdenes sin asignar\n")
        else:
            print(f"   ✅ Ya tiene órdenes asignadas\n")
    
    # Summary
    print("="*80)
    print("RESUMEN")
    print("="*80 + "\n")
    
    for operador in operadores:
        total = WorkOrder.objects.filter(assigned_to=operador).count()
        print(f"✅ {operador.username}: {total} órdenes asignadas")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    asignar_ordenes()
