"""
Core permission classes for role-based access control.
"""
from rest_framework import permissions
from apps.authentication.models import Role
import logging

logger = logging.getLogger(__name__)


class IsAdminOnly(permissions.BasePermission):
    """
    Permission class that only allows ADMIN role.
    """
    message = 'Solo los administradores pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        has_perm = request.user.role.name == Role.ADMIN
        
        if not has_perm:
            logger.warning(
                f"Permission denied: User {request.user.username} "
                f"(role: {request.user.role.name}) attempted admin action"
            )
        
        return has_perm


class IsSupervisorOrAbove(permissions.BasePermission):
    """
    Permission class that allows SUPERVISOR and ADMIN roles.
    """
    message = 'Solo supervisores y administradores pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role.name in [Role.ADMIN, Role.SUPERVISOR]


class IsOperadorOrAbove(permissions.BasePermission):
    """
    Permission class that allows any authenticated user with a valid role.
    """
    message = 'Debe estar autenticado con un rol válido.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role.name in [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR]


class IsOwnerOrSupervisor(permissions.BasePermission):
    """
    Permission class for object-level permissions.
    Allows access if:
    - User is ADMIN or SUPERVISOR
    - User is the owner of the object (assigned_to, user, created_by)
    """
    message = 'Solo puede acceder a sus propios recursos o ser supervisor/administrador.'
    
    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins and supervisors can access everything
        if request.user.role.name in [Role.ADMIN, Role.SUPERVISOR]:
            return True
        
        # Check various ownership fields
        ownership_fields = ['assigned_to', 'user', 'created_by', 'owner']
        
        for field in ownership_fields:
            if hasattr(obj, field):
                owner = getattr(obj, field)
                if owner == request.user:
                    return True
        
        # Log unauthorized access attempt
        logger.warning(
            f"Object permission denied: User {request.user.username} "
            f"attempted to access {obj.__class__.__name__} {obj.id}"
        )
        
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for object-level permissions (stricter).
    Allows access if:
    - User is ADMIN
    - User is the owner of the object
    
    Note: Supervisors do NOT have automatic access with this permission.
    """
    message = 'Solo puede acceder a sus propios recursos o ser administrador.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if request.user.role.name == Role.ADMIN:
            return True
        
        # Check ownership
        ownership_fields = ['assigned_to', 'user', 'created_by', 'owner']
        
        for field in ownership_fields:
            if hasattr(obj, field):
                owner = getattr(obj, field)
                if owner == request.user:
                    return True
        
        return False


class ReadOnlyForOperador(permissions.BasePermission):
    """
    Permission class that allows:
    - ADMIN and SUPERVISOR: Full access (read/write)
    - OPERADOR: Read-only access
    """
    message = 'Los operadores solo tienen acceso de lectura.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins and supervisors: full access
        if request.user.role.name in [Role.ADMIN, Role.SUPERVISOR]:
            return True
        
        # Operadores: only safe methods (GET, HEAD, OPTIONS)
        if request.user.role.name == Role.OPERADOR:
            return request.method in permissions.SAFE_METHODS
        
        return False
