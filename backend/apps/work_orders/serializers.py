"""
Serializers for work orders app.
"""
from rest_framework import serializers
from .models import WorkOrder
from apps.assets.serializers import AssetListSerializer
from apps.authentication.serializers import UserSerializer


class WorkOrderListSerializer(serializers.ModelSerializer):
    """Serializer for WorkOrder list view."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = [
            'id', 'work_order_number', 'title', 'priority', 'status',
            'asset', 'asset_name', 'assigned_to', 'assigned_to_name',
            'scheduled_date', 'completed_date', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'work_order_number', 'created_at']


class WorkOrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for WorkOrder detail view."""
    asset_data = AssetListSerializer(source='asset', read_only=True)
    assigned_to_data = UserSerializer(source='assigned_to', read_only=True)
    created_by_data = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = [
            'id', 'work_order_number', 'title', 'description', 'priority', 'status',
            'asset', 'asset_data', 'assigned_to', 'assigned_to_data',
            'scheduled_date', 'completed_date', 'completion_notes', 'actual_hours',
            'created_by', 'created_by_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'work_order_number', 'created_by', 'created_at', 'updated_at']


class WorkOrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating work orders."""
    
    class Meta:
        model = WorkOrder
        fields = [
            'title', 'description', 'priority', 'asset', 'assigned_to', 'scheduled_date'
        ]


class WorkOrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating work orders."""
    
    class Meta:
        model = WorkOrder
        fields = ['title', 'description', 'priority', 'assigned_to', 'scheduled_date', 'status']
    
    def validate_status(self, value):
        """Validate status transition."""
        instance = self.instance
        if instance and not instance.can_transition_to(value):
            raise serializers.ValidationError(
                f"Cannot transition from {instance.status} to {value}"
            )
        return value


class WorkOrderCompleteSerializer(serializers.Serializer):
    """Serializer for completing work orders."""
    completion_notes = serializers.CharField(required=True)
    actual_hours = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
