"""
Search URL Configuration
"""
from django.urls import path
from . import search_views

urlpatterns = [
    path('global/', search_views.global_search, name='global-search'),
]
