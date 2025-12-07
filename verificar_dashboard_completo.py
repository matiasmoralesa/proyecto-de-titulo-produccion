"""
Script para verificar todos los datos del dashboard
"""
import requests
from decouple import config
import json

BASE_URL = config('BACKEND_URL', default='https://proyecto-de-titulo-produccion-production.up.railway.app')

# Obtener token de admin
login_url = f'{BASE_URL}/api/v1/auth/login/'
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        token = response.json()['access']
        headers = {'Authorization': f'Bearer {token}'}
        
        print("=" * 80)
        print("VERIFICACIÓN COMPLETA DEL DASHBOARD")
        print("=" * 80)
        
        # 1. Dashboard principal
        print("\n1️⃣  DASHBOARD PRINCIPAL")
        print("-" * 80)
        dashboard_url = f'{BASE_URL}/api/v1/dashboard/stats/'
        dashboard_response = requests.get(dashboard_url, headers=headers)
        
        if dashboard_response.status_code == 200:
            dashboard = dashboard_response.json()
            print(f"✅ Status: OK")
            print(f"\nKPIs:")
            print(f"  - Total Activos: {dashboard.get('total_assets', 0)}")
            print(f"  - Activos Activos: {dashboard.get('active_assets', 0)}")
            print(f"  - Total OT: {dashboard.get('total_work_orders', 0)}")
            print(f"  - OT Completadas: {dashboard.get('completed_work_orders', 0)}")
            print(f"  - OT Pendientes: {dashboard.get('pending_work_orders', 0)}")
            print(f"  - OT En Progreso: {dashboard.get('in_progress_work_orders', 0)}")
            
            # Verificar gráficos
            print(f"\nGráficos:")
            
            # Tipos de mantenimiento
            maint_types = dashboard.get('maintenance_by_type', {})
            print(f"  - Tipos de Mantenimiento: {len(maint_types)} tipos")
            for mtype, count in maint_types.items():
                print(f"    • {mtype}: {count}")
            
            # Predicciones
            predictions = dashboard.get('failure_predictions_timeline', [])
            print(f"  - Línea de Predicciones: {len(predictions)} puntos de datos")
            
            # Actividad mensual
            monthly = dashboard.get('monthly_activity', [])
            print(f"  - Actividad Mensual: {len(monthly)} meses")
            if monthly:
                total_ordenes = sum(m.get('total_ordenes', 0) for m in monthly)
                total_completadas = sum(m.get('completadas', 0) for m in monthly)
                print(f"    Total órdenes en gráfico: {total_ordenes}")
                print(f"    Total completadas en gráfico: {total_completadas}")
            
            # Tiempo de resolución
            resolution = dashboard.get('resolution_time_by_priority', {})
            print(f"  - Tiempo de Resolución: {len(resolution)} prioridades")
            for priority, time in resolution.items():
                print(f"    • {priority}: {time}h")
            
            # Utilización de activos
            utilization = dashboard.get('asset_utilization', [])
            print(f"  - Utilización de Activos: {len(utilization)} activos")
            for asset in utilization[:5]:  # Mostrar top 5
                print(f"    • {asset.get('name')}: {asset.get('utilization', 0):.1f}%")
        else:
            print(f"❌ Error: {dashboard_response.status_code}")
            print(dashboard_response.text[:500])
        
        # 2. Reportes
        print("\n2️⃣  REPORTES")
        print("-" * 80)
        reports_url = f'{BASE_URL}/api/v1/reports/dashboard/'
        reports_response = requests.get(reports_url, headers=headers)
        
        if reports_response.status_code == 200:
            reports = reports_response.json()
            print(f"✅ Status: OK")
            print(f"\nKPIs de Reportes:")
            print(f"  - MTBF: {reports.get('mtbf', 'N/A')}")
            print(f"  - MTTR: {reports.get('mttr', 'N/A')}")
            print(f"  - OEE: {reports.get('oee', 'N/A')}%")
            
            # Work order summary
            wo_summary = reports.get('work_order_summary', {})
            print(f"\nResumen de OT:")
            print(f"  - Total: {wo_summary.get('total', 0)}")
            print(f"  - Horas trabajadas: {wo_summary.get('total_hours_worked', 0)}")
            print(f"  - Tiempo promedio: {wo_summary.get('avg_completion_time', 0)}h")
            
            # Por estado
            by_status = wo_summary.get('by_status', {})
            print(f"\n  Por Estado:")
            for status, data in by_status.items():
                print(f"    • {data.get('label', status)}: {data.get('count', 0)}")
            
            # Por prioridad
            by_priority = wo_summary.get('by_priority', {})
            print(f"\n  Por Prioridad:")
            for priority, data in by_priority.items():
                print(f"    • {data.get('label', priority)}: {data.get('count', 0)}")
            
            # Por tipo
            by_type = wo_summary.get('by_type', {})
            print(f"\n  Por Tipo:")
            for wtype, data in by_type.items():
                print(f"    • {data.get('label', wtype)}: {data.get('count', 0)}")
        else:
            print(f"❌ Error: {reports_response.status_code}")
            print(reports_response.text[:500])
        
        # 3. Verificar órdenes de trabajo
        print("\n3️⃣  ÓRDENES DE TRABAJO")
        print("-" * 80)
        wo_url = f'{BASE_URL}/api/v1/work-orders/?page_size=5'
        wo_response = requests.get(wo_url, headers=headers)
        
        if wo_response.status_code == 200:
            wo_data = wo_response.json()
            print(f"✅ Total: {wo_data.get('count', 0)} órdenes")
            print(f"\nÚltimas 5 órdenes:")
            for wo in wo_data.get('results', [])[:5]:
                print(f"  • {wo.get('work_order_number')} - {wo.get('title')}")
                print(f"    Estado: {wo.get('status')} | Prioridad: {wo.get('priority')}")
                print(f"    Activo: {wo.get('asset_name', 'N/A')}")
        else:
            print(f"❌ Error: {wo_response.status_code}")
        
        print("\n" + "=" * 80)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("=" * 80)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
