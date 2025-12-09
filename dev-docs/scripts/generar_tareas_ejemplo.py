"""
Script para generar tareas de ejemplo de Celery
"""
import requests
from decouple import config

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
        print("GENERANDO TAREAS DE EJEMPLO DE CELERY")
        print("=" * 60)
        
        # Generar tareas de ejemplo
        generate_url = f'{BASE_URL}/api/v1/celery/generate-sample-tasks/'
        generate_response = requests.post(generate_url, headers=headers)
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            print(f"\n✅ {result.get('message')}")
            print(f"\nTareas creadas:")
            for task in result.get('tasks', []):
                print(f"  • {task['task_name']}")
                print(f"    ID: {task['task_id'][:8]}...")
                print(f"    Estado: {task['status']}")
        else:
            print(f"❌ Error: {generate_response.status_code}")
            print(generate_response.text)
        
        # Verificar estadísticas
        print("\n📊 ESTADÍSTICAS")
        print("-" * 60)
        
        stats_url = f'{BASE_URL}/api/v1/celery/stats/'
        stats_response = requests.get(stats_url, headers=headers)
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"Total tareas (24h): {stats.get('total_tasks_24h', 0)}")
            print(f"Exitosas: {stats.get('success_24h', 0)}")
            print(f"Fallidas: {stats.get('failure_24h', 0)}")
            print(f"Pendientes: {stats.get('pending_24h', 0)}")
        
        print("\n" + "=" * 60)
        print("✅ COMPLETADO")
        print("=" * 60)
        print("\n💡 Ahora puedes ver las tareas en el Monitor de Celery")
        print("   Haz clic en 'Actualizar' para ver los resultados")
        
    else:
        print(f"❌ Error de login: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
