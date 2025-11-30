"""
URL configuration for inventory app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SparePartViewSet, StockMovementViewSet

app_name = 'inventory'

router = DefaultRouter()
router.register(r'spare-parts', SparePartViewSet, basename='spare-part')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')

urlpatterns = [
    path('', include(router.urls)),
]
