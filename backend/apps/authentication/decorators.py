"""
Decorators for role-based access control.
"""
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Role


def role_required(*roles):
    """
    Decorator to check if user has one of the required roles.
    
    Usage:
        @role_required(Role.ADMIN, Role.SUPERVISOR)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Autenticación requerida.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if request.user.role.name not in roles:
                return Response(
                    {'detail': 'No tiene permisos para realizar esta acción.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to check if user is admin.
    
    Usage:
        @admin_required
        def my_view(request):
            ...
    """
    return role_required(Role.ADMIN)(view_func)


def supervisor_or_admin_required(view_func):
    """
    Decorator to check if user is supervisor or admin.
    
    Usage:
        @supervisor_or_admin_required
        def my_view(request):
            ...
    """
    return role_required(Role.ADMIN, Role.SUPERVISOR)(view_func)
