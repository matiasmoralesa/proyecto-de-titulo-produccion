"""
URLs para monitoreo de Celery
"""
from django.urls import path
from .celery_views import (
    CeleryTaskResultsView, 
    CeleryPeriodicTasksView, 
    CeleryStatsView,
    RunTaskManuallyView
)

urlpatterns = [
    path('task-results/', CeleryTaskResultsView.as_view(), name='celery-task-results'),
    path('periodic-tasks/', CeleryPeriodicTasksView.as_view(), name='celery-periodic-tasks'),
    path('stats/', CeleryStatsView.as_view(), name='celery-stats'),
    path('run-task/', RunTaskManuallyView.as_view(), name='celery-run-task'),
]
