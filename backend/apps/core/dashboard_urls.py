"""
Dashboard URL Configuration
"""
from django.urls import path
from . import dashboard_views

urlpatterns = [
    path('stats/', dashboard_views.dashboard_stats, name='dashboard-stats'),
]
