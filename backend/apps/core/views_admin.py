"""
Admin views for data management
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.contrib.auth.decorators import user_passes_test
import os


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@csrf_exempt
@require_http_methods(["POST", "GET"])
def load_backup_data(request):
    """
    Load data from backup file.
    This endpoint is public for initial setup, but should be removed after use.
    """
    backup_file = 'backend/data_backup.json'
    
    if not os.path.exists(backup_file):
        return JsonResponse({
            'success': False,
            'error': f'Backup file not found: {backup_file}'
        }, status=404)
    
    try:
        call_command('loaddata', backup_file, verbosity=2)
        return JsonResponse({
            'success': True,
            'message': '✅ Data loaded successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error loading data: {str(e)}'
        }, status=500)
