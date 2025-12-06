"""
Script para limpiar el caché del dashboard después del deployment
Ejecutar después de actualizar dashboard_views.py
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.core.cache import cache

def clear_dashboard_cache():
    """
    Limpia el caché del dashboard para forzar recarga de datos
    """
    print("=" * 60)
    print("  LIMPIEZA DE CACHÉ DEL DASHBOARD")
    print("=" * 60)
    print()
    
    try:
        # Limpiar todo el caché
        cache.clear()
        print("✅ Caché limpiado exitosamente")
        print()
        print("Los usuarios verán datos actualizados en su próxima visita")
        print()
        
    except Exception as e:
        print("❌ Error al limpiar caché:")
        print(f"   {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    clear_dashboard_cache()
