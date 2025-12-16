"""
Assets URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, AssetViewSet  # AssetDocumentViewSet comentado

app_name = 'assets'

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'assets', AssetViewSet, basename='asset')
# router.register(r'documents', AssetDocumentViewSet, basename='document')  # Comentado - funcionalidad removida

urlpatterns = [
    path('', include(router.urls)),
]
