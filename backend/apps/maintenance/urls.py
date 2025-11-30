"""
Maintenance URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenancePlanViewSet

app_name = 'maintenance'

router = DefaultRouter()
router.register(r'plans', MaintenancePlanViewSet, basename='maintenance-plan')

urlpatterns = [
    path('', include(router.urls)),
]
