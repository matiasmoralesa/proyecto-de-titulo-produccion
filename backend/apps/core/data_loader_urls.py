"""
URLs para carga de datos de producción.
"""
from django.urls import path
from .data_loader_views import load_production_data, check_production_data, activate_admin_user, debug_admin_user

urlpatterns = [
    path('debug-admin/', debug_admin_user, name='debug-admin'),
    path('activate-admin/', activate_admin_user, name='activate-admin'),
    path('load-production-data/', load_production_data, name='load-production-data'),
    path('check-production-data/', check_production_data, name='check-production-data'),
]
