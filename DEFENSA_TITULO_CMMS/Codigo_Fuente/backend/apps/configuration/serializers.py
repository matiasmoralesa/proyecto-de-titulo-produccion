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
    
    def validate_code(self, value):
        """Validate that code is unique."""
        if self.instance:
            # Updating existing instance
            if AssetCategory.objects.exclude(pk=self.instance.pk).filter(code=value).exists():
                raise serializers.ValidationError("Ya existe una categoría con este código")
        else:
            # Creating new instance
            if AssetCategory.objects.filter(code=value).exists():
                raise serializers.ValidationError("Ya existe una categoría con este código")
        return value
    
    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido")
        return value.strip()


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
    
    def validate_color_code(self, value):
        """Validate that color code is in hex format."""
        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise serializers.ValidationError("El código de color debe estar en formato hexadecimal (#RRGGBB)")
        return value.upper()
    
    def validate_level(self, value):
        """Validate that level is unique."""
        if self.instance:
            # Updating existing instance
            if Priority.objects.exclude(pk=self.instance.pk).filter(level=value).exists():
                raise serializers.ValidationError("Ya existe una prioridad con este nivel")
        else:
            # Creating new instance
            if Priority.objects.filter(level=value).exists():
                raise serializers.ValidationError("Ya existe una prioridad con este nivel")
        return value
    
    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido")
        return value.strip()


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
    
    def validate_code(self, value):
        """Validate that code is unique."""
        if self.instance:
            # Updating existing instance
            if WorkOrderType.objects.exclude(pk=self.instance.pk).filter(code=value).exists():
                raise serializers.ValidationError("Ya existe un tipo de orden con este código")
        else:
            # Creating new instance
            if WorkOrderType.objects.filter(code=value).exists():
                raise serializers.ValidationError("Ya existe un tipo de orden con este código")
        return value
    
    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido")
        return value.strip()


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
        
        # Validate value matches data_type
        if 'value' in data and 'data_type' in data:
            self._validate_value_type(data['value'], data['data_type'])
        elif 'value' in data and self.instance:
            self._validate_value_type(data['value'], self.instance.data_type)
        
        return data
    
    def _validate_value_type(self, value, data_type):
        """Validate that value matches the specified data type."""
        try:
            if data_type == 'integer':
                int(value)
            elif data_type == 'float':
                float(value)
            elif data_type == 'boolean':
                if value.lower() not in ('true', 'false', '1', '0', 'yes', 'no'):
                    raise ValueError()
            elif data_type == 'json':
                import json
                json.loads(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                f"El valor no coincide con el tipo de dato {data_type}"
            )


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
