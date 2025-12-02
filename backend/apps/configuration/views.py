"""
Views for configuration app.
"""
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.configuration.models import (
    AssetCategory,
    Priority,
    WorkOrderType,
    SystemParameter,
    AuditLog
)
from apps.configuration.serializers import (
    AssetCategorySerializer,
    PrioritySerializer,
    WorkOrderTypeSerializer,
    SystemParameterSerializer,
    AuditLogSerializer
)
from apps.authentication.permissions import IsAdmin


class AssetCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetCategory model.
    Only admins can create, update, or delete categories.
    """
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        # Log the creation
        self._log_action(AuditLog.ACTION_CREATE, serializer.instance)
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_data = AssetCategorySerializer(old_instance).data
        serializer.save()
        # Log the update
        self._log_action(AuditLog.ACTION_UPDATE, serializer.instance, old_data)
    
    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise serializers.ValidationError("No se puede eliminar esta categoría porque está en uso")
        # Log the deletion
        self._log_action(AuditLog.ACTION_DELETE, instance)
        instance.delete()
    
    def _log_action(self, action, instance, old_data=None):
        """Helper method to log actions."""
        changes = {}
        if action == AuditLog.ACTION_UPDATE and old_data:
            new_data = AssetCategorySerializer(instance).data
            changes = {k: {'old': old_data[k], 'new': new_data[k]} 
                      for k in old_data if old_data[k] != new_data[k]}
        
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            model_name='AssetCategory',
            object_id=str(instance.id),
            object_repr=str(instance),
            changes=changes,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )


class PriorityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Priority model.
    Only admins can create, update, or delete priorities.
    """
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'level', 'created_at']
    ordering = ['level']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        self._log_action(AuditLog.ACTION_CREATE, serializer.instance)
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_data = PrioritySerializer(old_instance).data
        serializer.save()
        self._log_action(AuditLog.ACTION_UPDATE, serializer.instance, old_data)
    
    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise serializers.ValidationError("No se puede eliminar esta prioridad porque está en uso")
        self._log_action(AuditLog.ACTION_DELETE, instance)
        instance.delete()
    
    def _log_action(self, action, instance, old_data=None):
        changes = {}
        if action == AuditLog.ACTION_UPDATE and old_data:
            new_data = PrioritySerializer(instance).data
            changes = {k: {'old': old_data[k], 'new': new_data[k]} 
                      for k in old_data if old_data[k] != new_data[k]}
        
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            model_name='Priority',
            object_id=str(instance.id),
            object_repr=str(instance),
            changes=changes,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )


class WorkOrderTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for WorkOrderType model.
    Only admins can create, update, or delete work order types.
    """
    queryset = WorkOrderType.objects.all()
    serializer_class = WorkOrderTypeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'requires_approval']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        self._log_action(AuditLog.ACTION_CREATE, serializer.instance)
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_data = WorkOrderTypeSerializer(old_instance).data
        serializer.save()
        self._log_action(AuditLog.ACTION_UPDATE, serializer.instance, old_data)
    
    def perform_destroy(self, instance):
        if not instance.can_delete():
            raise serializers.ValidationError("No se puede eliminar este tipo porque está en uso")
        self._log_action(AuditLog.ACTION_DELETE, instance)
        instance.delete()
    
    def _log_action(self, action, instance, old_data=None):
        changes = {}
        if action == AuditLog.ACTION_UPDATE and old_data:
            new_data = WorkOrderTypeSerializer(instance).data
            changes = {k: {'old': old_data[k], 'new': new_data[k]} 
                      for k in old_data if old_data[k] != new_data[k]}
        
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            model_name='WorkOrderType',
            object_id=str(instance.id),
            object_repr=str(instance),
            changes=changes,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )


class SystemParameterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SystemParameter model.
    Only admins can create, update, or delete system parameters.
    """
    queryset = SystemParameter.objects.all()
    serializer_class = SystemParameterSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['data_type', 'is_editable']
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']
    ordering = ['key']
    
    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)
        self._log_action(AuditLog.ACTION_CREATE, serializer.instance)
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_data = SystemParameterSerializer(old_instance).data
        serializer.save(modified_by=self.request.user)
        self._log_action(AuditLog.ACTION_UPDATE, serializer.instance, old_data)
    
    def perform_destroy(self, instance):
        self._log_action(AuditLog.ACTION_DELETE, instance)
        instance.delete()
    
    def _log_action(self, action, instance, old_data=None):
        changes = {}
        if action == AuditLog.ACTION_UPDATE and old_data:
            new_data = SystemParameterSerializer(instance).data
            changes = {k: {'old': old_data[k], 'new': new_data[k]} 
                      for k in old_data if old_data[k] != new_data[k]}
        
        AuditLog.objects.create(
            user=self.request.user,
            action=action,
            model_name='SystemParameter',
            object_id=str(instance.id),
            object_repr=str(instance),
            changes=changes,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for AuditLog model.
    Read-only access for admins to view audit logs.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['object_repr', 'user__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
