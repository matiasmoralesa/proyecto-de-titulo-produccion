"""
URL configuration for checklists app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.checklists.views import (
    ChecklistTemplateViewSet,
    ChecklistResponseViewSet
)

router = DefaultRouter()
router.register(r'templates', ChecklistTemplateViewSet, basename='checklist-template')
router.register(r'responses', ChecklistResponseViewSet, basename='checklist-response')

urlpatterns = [
    path('', include(router.urls)),
]
