"""
Script para verificar que el dashboard filtra correctamente por roles.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.ml_predictions.models import FailurePrediction
from django.test import RequestFactory
from apps.core.dashboard_views import dashboard_stats
from rest_framework.test import force_authenticate

def test_dashboard_filtering():
    """Test que el dashboard filtra correctamente por roles."""
    
    print("\n" + "="*80)
    print("VERIFICACIÓN DE FILTRADO DE DASHBOARD POR ROLES")
    print("="*80 + "\n")
    
    # Get roles
    admin_role = Role.objects.get(name=Role.ADMIN)
    supervisor_role = Role.objects.get(name=Role.SUPERVISOR)
    operador_role = Role.objects.get(name=Role.OPERADOR)
    
    # Get users
    try:
        admin = User.objects.filter(role=admin_role).first()
        supervisor = User.objects.filter(role=supervisor_role).first()
        operador = User.objects.filter(role=operador_role).first()
        
        if not all([admin, supervisor, operador]):
            print("❌ No se encontraron usuarios de todos los roles")
            print(f"   Admin: {admin}")
            print(f"   Supervisor: {supervisor}")
            print(f"   Operador: {operador}")
            return
        
        print(f"✅ Usuarios encontrados:")
        print(f"   Admin: {admin.username}")
        print(f"   Supervisor: {supervisor.username}")
        print(f"   Operador: {operador.username}\n")
        
    except Exception as e:
        print(f"❌ Error al obtener usuarios: {e}")
        return
    
    # Get total counts
    total_assets = Asset.objects.count()
    total_work_orders = WorkOrder.objects.count()
    total_predictions = FailurePrediction.objects.count()
    
    print(f"📊 Datos totales en el sistema:")
    print(f"   Activos: {total_assets}")
    print(f"   Órdenes de Trabajo: {total_work_orders}")
    print(f"   Predicciones: {total_predictions}\n")
    
    # Get operador's assigned work orders
    operador_work_orders = WorkOrder.objects.filter(assigned_to=operador).count()
    operador_asset_ids = WorkOrder.objects.filter(assigned_to=operador).values_list('asset_id', flat=True).distinct()
    operador_assets = Asset.objects.filter(id__in=operador_asset_ids).count()
    operador_predictions = FailurePrediction.objects.filter(asset_id__in=operador_asset_ids).count()
    
    print(f"📋 Datos asignados al operador '{operador.username}':")
    print(f"   Órdenes de Trabajo: {operador_work_orders}")
    print(f"   Activos relacionados: {operador_assets}")
    print(f"   Predicciones relacionadas: {operador_predictions}\n")
    
    # Create request factory
    factory = RequestFactory()
    
    # Test ADMIN
    print("🔍 Probando dashboard como ADMIN...")
    request = factory.get('/api/v1/dashboard/stats/')
    force_authenticate(request, user=admin)
    response = dashboard_stats(request)
    
    admin_data = response.data
    print(f"   ✅ Admin ve:")
    print(f"      Activos: {admin_data['total_assets']}")
    print(f"      Órdenes de Trabajo: {admin_data['total_work_orders']}")
    print(f"      Predicciones: {admin_data['total_predictions']}")
    
    if admin_data['total_assets'] == total_assets:
        print(f"      ✅ Admin ve TODOS los activos")
    else:
        print(f"      ❌ Admin NO ve todos los activos")
    
    # Test SUPERVISOR
    print("\n🔍 Probando dashboard como SUPERVISOR...")
    request = factory.get('/api/v1/dashboard/stats/')
    force_authenticate(request, user=supervisor)
    response = dashboard_stats(request)
    
    supervisor_data = response.data
    print(f"   ✅ Supervisor ve:")
    print(f"      Activos: {supervisor_data['total_assets']}")
    print(f"      Órdenes de Trabajo: {supervisor_data['total_work_orders']}")
    print(f"      Predicciones: {supervisor_data['total_predictions']}")
    
    if supervisor_data['total_assets'] == total_assets:
        print(f"      ✅ Supervisor ve TODOS los activos (comportamiento actual)")
    else:
        print(f"      ⚠️  Supervisor ve datos filtrados")
    
    # Test OPERADOR
    print("\n🔍 Probando dashboard como OPERADOR...")
    request = factory.get('/api/v1/dashboard/stats/')
    force_authenticate(request, user=operador)
    response = dashboard_stats(request)
    
    operador_data = response.data
    print(f"   ✅ Operador ve:")
    print(f"      Activos: {operador_data['total_assets']}")
    print(f"      Órdenes de Trabajo: {operador_data['total_work_orders']}")
    print(f"      Predicciones: {operador_data['total_predictions']}")
    
    # Verify operador filtering
    print("\n📝 Verificación de filtrado del operador:")
    
    if operador_data['total_work_orders'] == operador_work_orders:
        print(f"   ✅ Órdenes de Trabajo: CORRECTO ({operador_work_orders})")
    else:
        print(f"   ❌ Órdenes de Trabajo: INCORRECTO")
        print(f"      Esperado: {operador_work_orders}")
        print(f"      Obtenido: {operador_data['total_work_orders']}")
    
    if operador_data['total_assets'] == operador_assets:
        print(f"   ✅ Activos: CORRECTO ({operador_assets})")
    else:
        print(f"   ❌ Activos: INCORRECTO")
        print(f"      Esperado: {operador_assets}")
        print(f"      Obtenido: {operador_data['total_assets']}")
    
    if operador_data['total_predictions'] == operador_predictions:
        print(f"   ✅ Predicciones: CORRECTO ({operador_predictions})")
    else:
        print(f"   ❌ Predicciones: INCORRECTO")
        print(f"      Esperado: {operador_predictions}")
        print(f"      Obtenido: {operador_data['total_predictions']}")
    
    # Summary
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    
    all_correct = (
        operador_data['total_work_orders'] == operador_work_orders and
        operador_data['total_assets'] == operador_assets and
        operador_data['total_predictions'] == operador_predictions
    )
    
    if all_correct:
        print("✅ El dashboard está filtrando correctamente por roles")
        print("✅ Los operadores solo ven sus datos asignados")
    else:
        print("❌ El dashboard NO está filtrando correctamente")
        print("❌ Los operadores están viendo datos que no deberían")
    
    print("="*80 + "\n")

if __name__ == '__main__':
    test_dashboard_filtering()
