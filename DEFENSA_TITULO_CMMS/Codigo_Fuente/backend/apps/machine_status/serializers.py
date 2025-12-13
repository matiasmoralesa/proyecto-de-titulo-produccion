"""
Serializers for machine status app.
"""
from rest_framework import serializers
from .models import AssetStatus, AssetStatusHistory


class AssetStatusSerializer(serializers.ModelSerializer):
    """Serializer for AssetStatus model."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    status_type_display = serializers.CharField(source='get_status_type_display', read_only=True)
    last_updated_by_name = serializers.CharField(source='last_updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = AssetStatus
        fields = [
            'id',
            'asset',
            'asset_name',
            'status_type',
            'status_type_display',
            'odometer_reading',
            'fuel_level',
            'condition_notes',
            'last_updated_by',
            'last_updated_by_name',
            'updated_at',
            'created_at',
        ]
        read_only_fields = ['id', 'last_updated_by', 'updated_at', 'created_at']
    
    def validate_fuel_level(self, value):
        """Validate fuel level is between 0 and 100."""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('Fuel level must be between 0 and 100.')
        return value
    
    def create(self, validated_data):
        """Create status with last_updated_by from request."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['last_updated_by'] = request.user
        return super().create(validated_data)


class AssetStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating asset status."""
    
    class Meta:
        model = AssetStatus
        fields = [
            'status_type',
            'odometer_reading',
            'fuel_level',
            'condition_notes',
        ]
    
    def validate_fuel_level(self, value):
        """Validate fuel level is between 0 and 100."""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('Fuel level must be between 0 and 100.')
        return value


class AssetStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for AssetStatusHistory model."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = AssetStatusHistory
        fields = [
            'id',
            'asset',
            'asset_name',
            'status_type',
            'odometer_reading',
            'fuel_level',
            'condition_notes',
            'updated_by',
            'updated_by_name',
            'timestamp',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
