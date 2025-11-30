"""
Serializers for assets app.
"""
from rest_framework import serializers
from .models import Location, Asset, AssetDocument


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""
    asset_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'address', 'coordinates', 'description',
            'asset_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_asset_count(self, obj):
        """Get count of active assets in this location."""
        return obj.assets.filter(is_archived=False).count()


class AssetDocumentSerializer(serializers.ModelSerializer):
    """Serializer for AssetDocument model."""
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = AssetDocument
        fields = [
            'id', 'asset', 'title', 'document_type', 'file', 'file_url',
            'file_size', 'description', 'uploaded_by', 'uploaded_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at']
    
    def get_file_url(self, obj):
        """Get full URL for the file."""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size(self, obj):
        """Get file size in bytes."""
        if obj.file:
            return obj.file.size
        return None


class AssetListSerializer(serializers.ModelSerializer):
    """Serializer for Asset list view."""
    location_name = serializers.CharField(source='location.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'vehicle_type', 'model', 'serial_number',
            'license_plate', 'location', 'location_name', 'installation_date',
            'status', 'is_archived', 'document_count', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_document_count(self, obj):
        """Get count of documents for this asset."""
        return obj.documents.count()


class AssetDetailSerializer(serializers.ModelSerializer):
    """Serializer for Asset detail view."""
    location_name = serializers.CharField(source='location.name', read_only=True)
    location_data = LocationSerializer(source='location', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    documents = AssetDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'vehicle_type', 'model', 'serial_number',
            'license_plate', 'location', 'location_name', 'location_data',
            'installation_date', 'status', 'is_archived',
            'created_by', 'created_by_name', 'created_by_email',
            'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class AssetCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating assets."""
    
    class Meta:
        model = Asset
        fields = [
            'name', 'vehicle_type', 'model', 'serial_number',
            'license_plate', 'location', 'installation_date', 'status'
        ]
    
    def validate_serial_number(self, value):
        """Validate serial number is uppercase."""
        return value.upper()
    
    def validate_license_plate(self, value):
        """Validate license plate is uppercase."""
        if value:
            return value.upper()
        return value
    
    def validate(self, attrs):
        """Additional validation."""
        # Check for duplicate serial number (excluding current instance on update)
        serial_number = attrs.get('serial_number')
        if serial_number:
            queryset = Asset.objects.filter(serial_number=serial_number)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    'serial_number': 'Asset with this serial number already exists.'
                })
        
        # Check for duplicate license plate (excluding current instance on update)
        license_plate = attrs.get('license_plate')
        if license_plate:
            queryset = Asset.objects.filter(license_plate=license_plate)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    'license_plate': 'Asset with this license plate already exists.'
                })
        
        return attrs
