"""
Custom permission classes for authentication.
"""
from rest_framework import permissions
from .models import Role


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user has ADMIN role.
    """
    message = 'Solo los administradores pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role.name == Role.ADMIN
        )


class IsSupervisorOrAdmin(permissions.BasePermission):
    """
    Permission class to check if user has SUPERVISOR or ADMIN role.
    """
    message = 'Solo supervisores y administradores pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role.name in [Role.ADMIN, Role.SUPERVISOR]
        )


class IsOperadorOrAbove(permissions.BasePermission):
    """
    Permission class to check if user has any valid role.
    """
    message = 'Debe estar autenticado para realizar esta acción.'
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role.name in [Role.ADMIN, Role.SUPERVISOR, Role.OPERADOR]
        )


class IsOwnerOrSupervisor(permissions.BasePermission):
    """
    Permission class to check if user is the owner of the object or has supervisor/admin role.
    """
    message = 'Solo puede acceder a sus propios recursos o ser supervisor/administrador.'
    
    def has_object_permission(self, request, view, obj):
        # Admins and supervisors can access everything
        if request.user.role.name in [Role.ADMIN, Role.SUPERVISOR]:
            return True
        
        # Check if object has a user field and if it matches the request user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has an assigned_to field
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == request.user
        
        # Check if object has a created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False
