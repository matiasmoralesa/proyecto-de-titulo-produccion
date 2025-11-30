"""
URLs for machine status app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetStatusViewSet, AssetStatusHistoryViewSet, AssetHistoryViewSet

app_name = 'machine_status'

router = DefaultRouter()
router.register(r'status', AssetStatusViewSet, basename='asset-status')
router.register(r'history', AssetStatusHistoryViewSet, basename='asset-status-history')
router.register(r'asset-history', AssetHistoryViewSet, basename='asset-complete-history')

urlpatterns = [
    path('', include(router.urls)),
]
