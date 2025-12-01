"""
URLs para carga de datos de producción.
"""
from django.urls import path
from .data_loader_views import load_production_data, check_production_data

urlpatterns = [
    path('load-production-data/', load_production_data, name='load-production-data'),
    path('check-production-data/', check_production_data, name='check-production-data'),
]
