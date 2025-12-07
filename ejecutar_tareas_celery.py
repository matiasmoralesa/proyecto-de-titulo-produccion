"""
Script para ejecutar tareas de Celery manualmente y generar resultados
"""
import requests
from decouple import config
import time

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
        
        print("=" * 60)
        print("EJECUTANDO TAREAS DE CELERY")
        print("=" * 60)
        
        # Tareas a ejecutar
        tasks = [
            'check_overdue_workorders',
            'check_critical_assets',
            'cleanup_old_notifications',
        ]
        
        for task_name in tasks:
            print(f"\n🔄 Ejecutando: {task_name}")
            
            run_url = f'{BASE_URL}/api/v1/celery/run-task/'
            run_response = requests.post(
                run_url, 
                json={'task_name': task_name},
                headers=headers
            )
            
            if run_response.status_code == 200:
                result = run_response.json()
                print(f"   ✅ Tarea encolada: {result.get('task_id')}")
            else:
                print(f"   ❌ Error: {run_response.status_code}")
                print(f"   {run_response.text}")
            
            time.sleep(1)  # Esperar 1 segundo entre tareas
        
        # Esperar un poco para que las tareas se ejecuten
        print("\n⏳ Esperando 5 segundos para que las tareas se ejecuten...")
        time.sleep(5)
        
        # Verificar resultados
        print("\n📊 VERIFICANDO RESULTADOS")
        print("-" * 60)
        
        stats_url = f'{BASE_URL}/api/v1/celery/stats/'
        stats_response = requests.get(stats_url, headers=headers)
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"Total tareas (24h): {stats.get('total_tasks_24h', 0)}")
            print(f"Exitosas: {stats.get('success_24h', 0)}")
            print(f"Fallidas: {stats.get('failure_24h', 0)}")
            print(f"Pendientes: {stats.get('pending_24h', 0)}")
        
        # Ver últimas tareas
        results_url = f'{BASE_URL}/api/v1/celery/task-results/'
        results_response = requests.get(results_url, headers=headers)
        
        if results_response.status_code == 200:
            results = results_response.json().get('results', [])
            print(f"\n📋 Últimas {len(results)} tareas:")
            for i, task in enumerate(results[:5], 1):
                print(f"\n{i}. {task.get('task_name', 'N/A')}")
                print(f"   Estado: {task.get('status', 'N/A')}")
                print(f"   ID: {task.get('id', 'N/A')[:8]}...")
                if task.get('date_done'):
                    print(f"   Completada: {task.get('date_done', 'N/A')[:19]}")
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
