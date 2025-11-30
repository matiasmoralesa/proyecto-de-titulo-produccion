"""
Serializers for configuration app.
"""
from rest_framework import serializers
from apps.configuration.models import (
    AssetCategory,
    Priority,
    WorkOrderType,
    SystemParameter,
    AuditLog
)


class AssetCategorySerializer(serializers.ModelSerializer):
    """Serializer for AssetCategory model."""
    created_by_name = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    
    class Meta:
        model = AssetCategory
        fields = [
            'id',
            'name',
            'description',
            'code',
            'is_active',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
            'can_delete',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_can_delete(self, obj):
        return obj.can_delete()


class PrioritySerializer(serializers.ModelSerializer):
    """Serializer for Priority model."""
    created_by_name = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    
    class Meta:
        model = Priority
        fields = [
            'id',
            'name',
            'description',
            'level',
            'color_code',
            'is_active',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
            'can_delete',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_can_delete(self, obj):
        return obj.can_delete()


class WorkOrderTypeSerializer(serializers.ModelSerializer):
    """Serializer for WorkOrderType model."""
    created_by_name = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkOrderType
        fields = [
            'id',
            'name',
            'description',
            'code',
            'requires_approval',
            'is_active',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
            'can_delete',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_can_delete(self, obj):
        return obj.can_delete()


class SystemParameterSerializer(serializers.ModelSerializer):
    """Serializer for SystemParameter model."""
    modified_by_name = serializers.SerializerMethodField()
    typed_value = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemParameter
        fields = [
            'id',
            'key',
            'value',
            'description',
            'data_type',
            'is_editable',
            'modified_by',
            'modified_by_name',
            'created_at',
            'updated_at',
            'typed_value',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'modified_by']
    
    def get_modified_by_name(self, obj):
        return obj.modified_by.get_full_name() if obj.modified_by else None
    
    def get_typed_value(self, obj):
        return obj.get_typed_value()
    
    def validate(self, data):
        """Validate that non-editable parameters cannot be modified."""
        if self.instance and not self.instance.is_editable:
            raise serializers.ValidationError("Este parámetro no es editable")
        return data


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""
    user_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'timestamp',
            'user',
            'user_name',
            'action',
            'action_display',
            'model_name',
            'object_id',
            'object_repr',
            'changes',
            'ip_address',
        ]
        read_only_fields = ['id', 'timestamp', 'user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else 'Sistema'
