from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.configuration.views import (
    AssetCategoryViewSet,
    PriorityViewSet,
    WorkOrderTypeViewSet,
    SystemParameterViewSet,
    AuditLogViewSet
)

router = DefaultRouter()
router.register(r'asset-categories', AssetCategoryViewSet, basename='asset-category')
router.register(r'priorities', PriorityViewSet, basename='priority')
router.register(r'work-order-types', WorkOrderTypeViewSet, basename='work-order-type')
router.register(r'system-parameters', SystemParameterViewSet, basename='system-parameter')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
