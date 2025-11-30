"""
Views para monitoreo de Celery
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone
from datetime import timedelta


class CeleryTaskResultsView(APIView):
    """
    Vista para obtener resultados de tareas de Celery
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtener últimas 50 tareas
        tasks = TaskResult.objects.all().order_by('-date_done')[:50]
        
        data = []
        for task in tasks:
            data.append({
                'id': str(task.task_id),
                'task_name': task.task_name,
                'status': task.status,
                'result': task.result,
                'date_created': task.date_created,
                'date_done': task.date_done,
                'traceback': task.traceback,
            })
        
        return Response({'results': data})


class CeleryPeriodicTasksView(APIView):
    """
    Vista para obtener tareas programadas de Celery
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = PeriodicTask.objects.all().select_related('crontab')
        
        data = []
        for task in tasks:
            crontab_data = None
            if task.crontab:
                crontab_data = {
                    'minute': task.crontab.minute,
                    'hour': task.crontab.hour,
                    'day_of_week': task.crontab.day_of_week,
                    'day_of_month': task.crontab.day_of_month,
                    'month_of_year': task.crontab.month_of_year,
                }
            
            data.append({
                'id': task.id,
                'name': task.name,
                'task': task.task,
                'enabled': task.enabled,
                'last_run_at': task.last_run_at,
                'total_run_count': task.total_run_count,
                'crontab': crontab_data,
            })
        
        return Response({'results': data})


class CeleryStatsView(APIView):
    """
    Vista para obtener estadísticas de Celery
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Estadísticas de las últimas 24 horas
        last_24h = timezone.now() - timedelta(hours=24)
        
        recent_tasks = TaskResult.objects.filter(date_created__gte=last_24h)
        
        stats = {
            'total_tasks_24h': recent_tasks.count(),
            'success_24h': recent_tasks.filter(status='SUCCESS').count(),
            'failure_24h': recent_tasks.filter(status='FAILURE').count(),
            'pending_24h': recent_tasks.filter(status='PENDING').count(),
            'total_periodic_tasks': PeriodicTask.objects.count(),
            'active_periodic_tasks': PeriodicTask.objects.filter(enabled=True).count(),
        }
        
        return Response(stats)
