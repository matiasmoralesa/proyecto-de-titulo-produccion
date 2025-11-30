"""
Serializers for checklists app.
"""
from rest_framework import serializers
from apps.checklists.models import (
    ChecklistTemplate,
    ChecklistTemplateItem,
    ChecklistResponse,
    ChecklistItemResponse
)
from apps.assets.serializers import AssetListSerializer
from apps.authentication.serializers import UserSerializer


class ChecklistTemplateItemSerializer(serializers.ModelSerializer):
    """Serializer for ChecklistTemplateItem model."""
    
    class Meta:
        model = ChecklistTemplateItem
        fields = [
            'id',
            'section',
            'order',
            'question',
            'response_type',
            'required',
            'observations_allowed',
        ]
        read_only_fields = ['id']


class ChecklistTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ChecklistTemplate model."""
    items = ChecklistTemplateItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    required_items_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(
        source='created_by.get_full_name',
        read_only=True,
        allow_null=True
    )
    
    def get_total_items(self, obj):
        return obj.total_items()
    
    def get_required_items_count(self, obj):
        return obj.required_items_count()
    
    class Meta:
        model = ChecklistTemplate
        fields = [
            'id',
            'code',
            'name',
            'description',
            'vehicle_type',
            'is_system_template',
            'passing_score',
            'is_active',
            'items',
            'total_items',
            'required_items_count',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'is_system_template',
        ]
    
    def validate(self, data):
        """Validate that system templates cannot be modified."""
        if self.instance and self.instance.is_system_template:
            raise serializers.ValidationError(
                "Las plantillas del sistema no pueden ser modificadas."
            )
        return data


class ChecklistItemResponseSerializer(serializers.ModelSerializer):
    """Serializer for ChecklistItemResponse model."""
    template_item = ChecklistTemplateItemSerializer(read_only=True)
    template_item_id = serializers.IntegerField(write_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ChecklistItemResponse
        fields = [
            'id',
            'template_item',
            'template_item_id',
            'response_value',
            'observations',
            'photo',
            'photo_url',
            'answered_at',
        ]
        read_only_fields = ['id', 'answered_at']
    
    def get_photo_url(self, obj):
        """Get the full URL for the photo."""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None
    
    def validate(self, data):
        """Validate response based on template item type."""
        template_item_id = data.get('template_item_id')
        response_value = data.get('response_value', '')
        
        if template_item_id:
            try:
                template_item = ChecklistTemplateItem.objects.get(id=template_item_id)
                
                # Validate response type
                if template_item.response_type == ChecklistTemplateItem.RESPONSE_YES_NO_NA:
                    if response_value and response_value not in ['yes', 'no', 'na']:
                        raise serializers.ValidationError({
                            'response_value': 'Debe ser "yes", "no" o "na".'
                        })
                
                # Validate required fields
                if template_item.required and not response_value:
                    raise serializers.ValidationError({
                        'response_value': 'Este campo es requerido.'
                    })
                
            except ChecklistTemplateItem.DoesNotExist:
                raise serializers.ValidationError({
                    'template_item_id': 'Item de plantilla no encontrado.'
                })
        
        return data


class ChecklistResponseSerializer(serializers.ModelSerializer):
    """Serializer for ChecklistResponse model."""
    template = ChecklistTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True)
    asset = AssetListSerializer(read_only=True)
    asset_id = serializers.CharField(write_only=True)  # Changed to CharField to support UUID
    work_order_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_responses = ChecklistItemResponseSerializer(many=True, read_only=True)
    completed_by_name = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    
    def get_completed_by_name(self, obj):
        """Get the name of the user who completed the checklist."""
        if not obj.completed_by:
            return None
        full_name = obj.completed_by.get_full_name()
        if full_name and full_name.strip():
            return full_name
        return obj.completed_by.username
    
    class Meta:
        model = ChecklistResponse
        fields = [
            'id',
            'template',
            'template_id',
            'asset',
            'asset_id',
            'work_order',
            'work_order_id',
            'completed_by',
            'completed_by_name',
            'completed_at',
            'score',
            'status',
            'signature_data',
            'pdf_file',
            'pdf_url',
            'item_responses',
            'completion_percentage',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'completed_by',
            'completed_at',
            'score',
            'status',
            'pdf_file',
            'created_at',
            'updated_at',
        ]
    
    def get_completion_percentage(self, obj):
        """Get completion percentage."""
        return obj.completion_percentage()
    
    def get_pdf_url(self, obj):
        """Get the full URL for the PDF."""
        if obj.pdf_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.pdf_file.url)
        return None
    
    def validate(self, data):
        """Validate checklist response data."""
        template_id = data.get('template_id')
        asset_id = data.get('asset_id')
        
        # Validate template exists and is active
        try:
            template = ChecklistTemplate.objects.get(id=template_id, is_active=True)
        except ChecklistTemplate.DoesNotExist:
            raise serializers.ValidationError({
                'template_id': 'Plantilla no encontrada o inactiva.'
            })
        
        # Validate asset exists
        from apps.assets.models import Asset
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            raise serializers.ValidationError({
                'asset_id': 'Activo no encontrado.'
            })
        
        # Validate vehicle type matches
        if asset.vehicle_type != template.vehicle_type:
            raise serializers.ValidationError({
                'template_id': f'Esta plantilla es para {template.get_vehicle_type_display()}, '
                              f'pero el activo es {asset.get_vehicle_type_display()}.'
            })
        
        return data
    
    def create(self, validated_data):
        """Create checklist response and set completed_by from request user."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['completed_by'] = request.user
        
        return super().create(validated_data)


class ChecklistResponseDetailSerializer(ChecklistResponseSerializer):
    """Detailed serializer for ChecklistResponse with all item responses."""
    item_responses = ChecklistItemResponseSerializer(many=True, read_only=True)


class ChecklistCompletionSerializer(serializers.Serializer):
    """Serializer for completing a checklist with all responses."""
    template_id = serializers.IntegerField()
    asset_id = serializers.CharField()  # Changed to CharField to support UUID
    work_order_id = serializers.IntegerField(required=False, allow_null=True)
    signature_data = serializers.CharField(required=False, allow_blank=True)
    item_responses = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )
    
    def validate(self, data):
        """Validate completion data."""
        template_id = data.get('template_id')
        asset_id = data.get('asset_id')
        item_responses = data.get('item_responses', [])
        
        # Validate template exists and is active
        try:
            template = ChecklistTemplate.objects.get(id=template_id, is_active=True)
        except ChecklistTemplate.DoesNotExist:
            raise serializers.ValidationError({
                'template_id': 'Plantilla no encontrada o inactiva.'
            })
        
        # Validate asset exists
        from apps.assets.models import Asset
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            raise serializers.ValidationError({
                'asset_id': 'Activo no encontrado.'
            })
        
        # Validate vehicle type matches
        if asset.vehicle_type != template.vehicle_type:
            raise serializers.ValidationError({
                'template_id': f'Esta plantilla es para {template.get_vehicle_type_display()}, '
                              f'pero el activo es {asset.get_vehicle_type_display()}.'
            })
        
        # Validate all required items are present
        required_items = template.items.filter(required=True).values_list('id', flat=True)
        provided_item_ids = [item.get('template_item_id') for item in item_responses]
        
        missing_items = set(required_items) - set(provided_item_ids)
        if missing_items:
            raise serializers.ValidationError({
                'item_responses': f'Faltan respuestas para items requeridos: {list(missing_items)}'
            })
        
        # Validate each item response
        for item_response in item_responses:
            template_item_id = item_response.get('template_item_id')
            response_value = item_response.get('response_value', '')
            
            try:
                template_item = ChecklistTemplateItem.objects.get(
                    id=template_item_id,
                    template=template
                )
                
                # Validate response type
                if template_item.response_type == ChecklistTemplateItem.RESPONSE_YES_NO_NA:
                    if response_value and response_value not in ['yes', 'no', 'na']:
                        raise serializers.ValidationError({
                            'item_responses': f'Item {template_item_id}: Debe ser "yes", "no" o "na".'
                        })
                
                # Validate required fields
                if template_item.required and not response_value:
                    raise serializers.ValidationError({
                        'item_responses': f'Item {template_item_id}: Este campo es requerido.'
                    })
                
            except ChecklistTemplateItem.DoesNotExist:
                raise serializers.ValidationError({
                    'item_responses': f'Item de plantilla {template_item_id} no encontrado.'
                })
        
        data['template'] = template
        data['asset'] = asset
        return data
