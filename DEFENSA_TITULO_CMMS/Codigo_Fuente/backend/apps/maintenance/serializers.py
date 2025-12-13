"""
Serializers for maintenance app.
"""
from rest_framework import serializers
from .models import MaintenancePlan
from apps.assets.serializers import AssetListSerializer
from apps.authentication.serializers import UserSerializer


class MaintenancePlanListSerializer(serializers.ModelSerializer):
    """Serializer for MaintenancePlan list view."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    is_due = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()
    usage_until_due = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenancePlan
        fields = [
            'id', 'name', 'asset', 'asset_name', 'recurrence_type',
            'recurrence_interval', 'next_due_date', 'status', 'is_paused',
            'assigned_to', 'assigned_to_name', 'created_by_name',
            'is_due', 'is_overdue', 'days_until_due', 'usage_until_due',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_assigned_to_name(self, obj):
        """Get assigned user name."""
        if obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip() or obj.assigned_to.username
        return None
    
    def get_is_due(self, obj):
        """Check if maintenance is due."""
        return obj.is_due()
    
    def get_is_overdue(self, obj):
        """Check if maintenance is overdue."""
        return obj.is_overdue()
    
    def get_days_until_due(self, obj):
        """Get days until due."""
        return obj.days_until_due()
    
    def get_usage_until_due(self, obj):
        """Get usage until due."""
        return obj.usage_until_due()


class MaintenancePlanDetailSerializer(serializers.ModelSerializer):
    """Serializer for MaintenancePlan detail view."""
    asset_data = AssetListSerializer(source='asset', read_only=True)
    assigned_to_data = UserSerializer(source='assigned_to', read_only=True)
    created_by_data = UserSerializer(source='created_by', read_only=True)
    paused_by_data = UserSerializer(source='paused_by', read_only=True)
    is_due = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()
    usage_until_due = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenancePlan
        fields = [
            'id', 'name', 'description', 'asset', 'asset_data',
            'recurrence_type', 'recurrence_interval', 'start_date',
            'next_due_date', 'last_completed_date', 'usage_threshold',
            'last_usage_value', 'estimated_duration_hours', 'assigned_to',
            'assigned_to_data', 'status', 'is_paused', 'paused_at',
            'paused_by', 'paused_by_data', 'created_by', 'created_by_data',
            'is_due', 'is_overdue', 'days_until_due', 'usage_until_due',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'paused_at', 'paused_by',
            'created_at', 'updated_at'
        ]
    
    def get_is_due(self, obj):
        """Check if maintenance is due."""
        return obj.is_due()
    
    def get_is_overdue(self, obj):
        """Check if maintenance is overdue."""
        return obj.is_overdue()
    
    def get_days_until_due(self, obj):
        """Get days until due."""
        return obj.days_until_due()
    
    def get_usage_until_due(self, obj):
        """Get usage until due."""
        return obj.usage_until_due()


class MaintenancePlanCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating maintenance plans."""
    
    class Meta:
        model = MaintenancePlan
        fields = [
            'name', 'description', 'asset', 'recurrence_type',
            'recurrence_interval', 'start_date', 'usage_threshold',
            'estimated_duration_hours', 'assigned_to', 'status'
        ]
    
    def validate(self, attrs):
        """Validate maintenance plan data."""
        recurrence_type = attrs.get('recurrence_type')
        usage_threshold = attrs.get('usage_threshold')
        
        # Validate usage-based plans have usage_threshold
        if recurrence_type in [MaintenancePlan.RECURRENCE_HOURS, MaintenancePlan.RECURRENCE_KILOMETERS]:
            if not usage_threshold:
                raise serializers.ValidationError({
                    'usage_threshold': 'Usage threshold is required for usage-based maintenance plans.'
                })
        
        # Validate recurrence_interval is positive
        recurrence_interval = attrs.get('recurrence_interval', 1)
        if recurrence_interval < 1:
            raise serializers.ValidationError({
                'recurrence_interval': 'Recurrence interval must be at least 1.'
            })
        
        return attrs


class MaintenancePlanPauseSerializer(serializers.Serializer):
    """Serializer for pausing/resuming maintenance plans."""
    action = serializers.ChoiceField(choices=['pause', 'resume'])


class MaintenancePlanCompleteSerializer(serializers.Serializer):
    """Serializer for completing maintenance."""
    completion_date = serializers.DateField(required=False)
    usage_value = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_usage_value(self, value):
        """
        Validate that usage value is not negative.
        """
        if value is not None and value < 0:
            raise serializers.ValidationError(
                'El valor de uso no puede ser negativo.'
            )
        return value


class MaintenancePlanUsageUpdateSerializer(serializers.Serializer):
    """Serializer for updating usage value."""
    current_usage = serializers.IntegerField(required=True, min_value=0)
    
    def validate_current_usage(self, value):
        """
        Validate that current usage is not negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                'El uso actual no puede ser negativo.'
            )
        return value
