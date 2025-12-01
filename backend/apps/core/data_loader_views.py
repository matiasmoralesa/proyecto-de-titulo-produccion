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
    
    # Cargar plantillas de checklist directamente
    try:
        call_command('create_checklist_templates')
        results['loaded'].append('Plantillas de Checklist')
    except Exception as e:
        import traceback
        results['errors'].append(f'Plantillas de Checklist: {str(e)} - {traceback.format_exc()}')
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
@permission_classes([IsAuthenticated, IsAdmin])
def fix_vehicle_types(request):
    """
    Endpoint para corregir los vehicle_types de los activos.
    """
    from apps.assets.models import Asset
    
    # Mapeo de valores incorrectos a correctos
    VEHICLE_TYPE_MAPPING = {
        'EXCAVADORA': 'Retroexcavadora MDO',
        'RETROEXCAVADORA': 'Retroexcavadora MDO',
        'CARGADOR_FRONTAL': 'Cargador Frontal MDO',
        'CARGADOR FRONTAL': 'Cargador Frontal MDO',
        'MINICARGADOR': 'Minicargador MDO',
        'CAMION_SUPERSUCKER': 'Camión Supersucker',
        'CAMION SUPERSUCKER': 'Camión Supersucker',
        'CAMIONETA_MDO': 'Camioneta MDO',
        'CAMIONETA MDO': 'Camioneta MDO',
        'VOLQUETE': 'Camión Supersucker',
    }
    
    updated = []
    skipped = []
    errors = []
    
    for asset in Asset.objects.all():
        old_type = asset.vehicle_type
        
        # Si el tipo ya es correcto, skip
        if old_type in [
            'Camión Supersucker',
            'Camioneta MDO',
            'Retroexcavadora MDO',
            'Cargador Frontal MDO',
            'Minicargador MDO'
        ]:
            skipped.append(f"{asset.name} ({old_type})")
            continue
        
        # Buscar el mapeo correcto
        new_type = VEHICLE_TYPE_MAPPING.get(old_type.upper().replace(' ', '_'))
        
        if not new_type:
            # Intentar match parcial
            if 'EXCAVADORA' in old_type.upper():
                new_type = 'Retroexcavadora MDO'
            elif 'CARGADOR' in old_type.upper() and 'FRONTAL' in old_type.upper():
                new_type = 'Cargador Frontal MDO'
            elif 'MINICARGADOR' in old_type.upper():
                new_type = 'Minicargador MDO'
            elif 'CAMION' in old_type.upper() or 'SUPERSUCKER' in old_type.upper():
                new_type = 'Camión Supersucker'
            elif 'CAMIONETA' in old_type.upper():
                new_type = 'Camioneta MDO'
            else:
                errors.append(f"{asset.name} ({old_type}) - No se pudo mapear")
                continue
        
        # Actualizar
        try:
            asset.vehicle_type = new_type
            asset.save()
            updated.append(f"{asset.name}: {old_type} → {new_type}")
        except Exception as e:
            errors.append(f"{asset.name}: {str(e)}")
    
    return Response({
        'success': len(errors) == 0,
        'updated': updated,
        'skipped': skipped,
        'errors': errors,
        'summary': {
            'updated_count': len(updated),
            'skipped_count': len(skipped),
            'error_count': len(errors),
            'total_assets': Asset.objects.count()
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def debug_admin_user(request):
    """
    Endpoint para debug del usuario admin.
    """
    from apps.authentication.models import User
    
    try:
        admin = User.objects.get(username='admin')
        return Response({
            'username': admin.username,
            'email': admin.email,
            'is_active': admin.is_active,
            'is_staff': admin.is_staff,
            'is_superuser': admin.is_superuser,
            'role': admin.role.name if admin.role else None,
            'password_set': bool(admin.password)
        })
    except User.DoesNotExist:
        return Response({'error': 'Usuario no existe'}, status=404)


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
        # Resetear password para asegurar que está hasheado correctamente
        admin.set_password('admin123')
        admin.save()
        
        return Response({
            'success': True,
            'message': 'Usuario admin activado correctamente con password reseteado',
            'user': {
                'username': admin.username,
                'email': admin.email,
                'is_active': admin.is_active,
                'is_staff': admin.is_staff,
                'is_superuser': admin.is_superuser,
                'role': admin.role.name
            },
            'credentials': {
                'username': 'admin',
                'password': 'admin123'
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
