"""
Admin views for data management
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.contrib.auth.decorators import user_passes_test
import os
import subprocess
import sys


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


@csrf_exempt
@require_http_methods(["POST", "GET"])
def seed_database(request):
    """
    Seed database with sample data using seed scripts.
    This endpoint is public for initial setup, but should be removed after use.
    """
    try:
        # Run seed_all_data.py script
        result = subprocess.run(
            [sys.executable, 'backend/seed_all_data.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            return JsonResponse({
                'success': True,
                'message': '✅ Database seeded successfully!',
                'output': result.stdout
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'Seed script failed: {result.stderr}',
                'output': result.stdout
            }, status=500)
    except subprocess.TimeoutExpired:
        return JsonResponse({
            'success': False,
            'error': 'Seed script timed out after 5 minutes'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error seeding database: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def seed_machine_status(request):
    """
    Seed machine status data for all assets.
    This endpoint is public for initial setup, but should be removed after use.
    """
    try:
        call_command('seed_machine_status', verbosity=2)
        return JsonResponse({
            'success': True,
            'message': '✅ Machine status data seeded successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error seeding machine status: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def generate_checklists(request):
    """
    Generate sample checklist templates and responses.
    This endpoint is public for initial setup, but should be removed after use.
    """
    try:
        # Run generate_sample_checklists.py script
        result = subprocess.run(
            [sys.executable, 'backend/generate_sample_checklists.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            return JsonResponse({
                'success': True,
                'message': '✅ Checklists generated successfully!',
                'output': result.stdout
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'Checklist generation failed: {result.stderr}',
                'output': result.stdout
            }, status=500)
    except subprocess.TimeoutExpired:
        return JsonResponse({
            'success': False,
            'error': 'Checklist generation timed out after 5 minutes'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error generating checklists: {str(e)}'
        }, status=500)
