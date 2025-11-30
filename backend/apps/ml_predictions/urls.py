"""
ML Predictions URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FailurePredictionViewSet

router = DefaultRouter()
router.register(r'predictions', FailurePredictionViewSet, basename='prediction')

urlpatterns = [
    path('', include(router.urls)),
]
