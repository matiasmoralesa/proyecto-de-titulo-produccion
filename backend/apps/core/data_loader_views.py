"""
Views para cargar datos de producción sin necesidad de shell.
"""
from django.core.management import call_command
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from apps.authentication.permissions import IsAdmin
import os


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def load_production_data(request):
    """
    Endpoint para cargar datos de producción.
    Solo accesible por administradores.
    """
    
    results = {
        'success': True,
        'loaded': [],
        'errors': [],
        'summary': {}
    }
    
    # Lista de fixtures a cargar en orden
    fixtures = [
        ('roles_export.json', 'Roles'),
        ('checklist_templates_export.json', 'Plantillas de Checklist'),
        ('priorities_export.json', 'Prioridades'),
        ('workorder_types_export.json', 'Tipos de Orden de Trabajo'),
        ('asset_categories_export.json', 'Categorías de Activos'),
        ('locations_export.json', 'Ubicaciones'),
    ]
    
    for fixture_file, description in fixtures:
        try:
            fixture_path = f'backend/{fixture_file}'
            
            # Verificar que el archivo existe
            if not os.path.exists(fixture_path):
                results['errors'].append(f'{description}: Archivo no encontrado ({fixture_path})')
                results['success'] = False
                continue
            
            # Cargar el fixture
            call_command('loaddata', fixture_path, verbosity=0)
            results['loaded'].append(description)
            
        except Exception as e:
            results['errors'].append(f'{description}: {str(e)}')
            results['success'] = False
    
    # Generar resumen
    from apps.authentication.models import Role
    from apps.checklists.models import ChecklistTemplate
    from apps.configuration.models import Priority, WorkOrderType, AssetCategory
    from apps.assets.models import Location
    
    try:
        results['summary'] = {
            'roles': Role.objects.count(),
            'checklist_templates': ChecklistTemplate.objects.count(),
            'priorities': Priority.objects.count(),
            'workorder_types': WorkOrderType.objects.count(),
            'asset_categories': AssetCategory.objects.count(),
            'locations': Location.objects.count(),
        }
    except Exception as e:
        results['errors'].append(f'Error al generar resumen: {str(e)}')
    
    return Response(results)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def activate_admin_user(request):
    """
    Endpoint temporal para activar el usuario admin.
    DEBE SER REMOVIDO DESPUÉS DE USAR.
    """
    from apps.authentication.models import User, Role
    
    try:
        # Obtener o crear el rol ADMIN
        admin_role, _ = Role.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Administrador del sistema'}
        )
        
        # Obtener el usuario admin
        admin = User.objects.get(username='admin')
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.role = admin_role
        admin.save()
        
        return Response({
            'success': True,
            'message': 'Usuario admin activado correctamente',
            'user': {
                'username': admin.username,
                'email': admin.email,
                'is_active': admin.is_active,
                'is_staff': admin.is_staff,
                'is_superuser': admin.is_superuser,
                'role': admin.role.name
            }
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Usuario admin no existe'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def check_production_data(request):
    """
    Endpoint para verificar qué datos están cargados.
    Solo accesible por administradores.
    """
    
    from apps.authentication.models import Role
    from apps.checklists.models import ChecklistTemplate
    from apps.configuration.models import Priority, WorkOrderType, AssetCategory
    from apps.assets.models import Location
    
    data = {
        'roles': {
            'count': Role.objects.count(),
            'items': list(Role.objects.values('name', 'description'))
        },
        'checklist_templates': {
            'count': ChecklistTemplate.objects.count(),
            'items': list(ChecklistTemplate.objects.values('code', 'name', 'vehicle_type'))
        },
        'priorities': {
            'count': Priority.objects.count(),
            'items': list(Priority.objects.values('name'))
        },
        'workorder_types': {
            'count': WorkOrderType.objects.count(),
            'items': list(WorkOrderType.objects.values('name'))
        },
        'asset_categories': {
            'count': AssetCategory.objects.count(),
            'items': list(AssetCategory.objects.values('name'))
        },
        'locations': {
            'count': Location.objects.count(),
            'items': list(Location.objects.values('name'))
        }
    }
    
    # Verificar si faltan datos esenciales
    missing = []
    if data['roles']['count'] < 3:
        missing.append('roles')
    if data['checklist_templates']['count'] < 5:
        missing.append('checklist_templates')
    
    data['status'] = 'complete' if not missing else 'incomplete'
    data['missing'] = missing
    
    return Response(data)
