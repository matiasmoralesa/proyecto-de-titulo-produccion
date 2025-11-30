"""
Serializers for inventory app.
"""
from rest_framework import serializers
from .models import SparePart, StockMovement
from apps.authentication.serializers import UserSerializer


class SparePartSerializer(serializers.ModelSerializer):
    """Serializer for SparePart model."""
    
    created_by = UserSerializer(read_only=True)
    stock_status = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()
    
    def get_stock_status(self, obj):
        return obj.stock_status()
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()
    
    def get_total_value(self, obj):
        return obj.total_value()
    
    class Meta:
        model = SparePart
        fields = [
            'id',
            'part_number',
            'name',
            'description',
            'category',
            'manufacturer',
            'quantity',
            'min_quantity',
            'unit_of_measure',
            'unit_cost',
            'storage_location',
            'is_active',
            'stock_status',
            'is_low_stock',
            'total_value',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_part_number(self, value):
        """Validate that part_number is unique."""
        instance = self.instance
        if instance and instance.part_number == value:
            return value
        
        if SparePart.objects.filter(part_number=value).exists():
            raise serializers.ValidationError(
                "Ya existe un repuesto con este número de parte."
            )
        return value
    
    def validate_quantity(self, value):
        """Validate that quantity is non-negative."""
        if value < 0:
            raise serializers.ValidationError(
                "La cantidad no puede ser negativa."
            )
        return value
    
    def validate_min_quantity(self, value):
        """Validate that min_quantity is non-negative."""
        if value < 0:
            raise serializers.ValidationError(
                "La cantidad mínima no puede ser negativa."
            )
        return value
    
    def validate_unit_cost(self, value):
        """Validate that unit_cost is non-negative."""
        if value < 0:
            raise serializers.ValidationError(
                "El costo unitario no puede ser negativo."
            )
        return value


class SparePartListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing spare parts."""
    
    stock_status = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()
    
    def get_stock_status(self, obj):
        return obj.stock_status()
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()
    
    def get_total_value(self, obj):
        return obj.total_value()
    
    class Meta:
        model = SparePart
        fields = [
            'id',
            'part_number',
            'name',
            'category',
            'quantity',
            'min_quantity',
            'unit_of_measure',
            'unit_cost',
            'stock_status',
            'is_low_stock',
            'total_value',
            'is_active',
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    """Serializer for StockMovement model."""
    
    spare_part = SparePartListSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    movement_type_display = serializers.CharField(
        source='get_movement_type_display',
        read_only=True
    )
    total_cost = serializers.SerializerMethodField()
    
    def get_total_cost(self, obj):
        return obj.total_cost()
    
    class Meta:
        model = StockMovement
        fields = [
            'id',
            'spare_part',
            'movement_type',
            'movement_type_display',
            'quantity',
            'quantity_before',
            'quantity_after',
            'unit_cost',
            'total_cost',
            'reference_type',
            'reference_id',
            'notes',
            'user',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'spare_part',
            'quantity_before',
            'quantity_after',
            'user',
            'created_at',
        ]


class StockAdjustmentSerializer(serializers.Serializer):
    """Serializer for stock adjustment operations."""
    
    quantity_change = serializers.IntegerField(
        help_text="Cantidad a ajustar (positivo para entrada, negativo para salida)"
    )
    movement_type = serializers.ChoiceField(
        choices=StockMovement.MOVEMENT_TYPES,
        help_text="Tipo de movimiento"
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Notas sobre el ajuste"
    )
    reference_type = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Tipo de referencia (ej: work_order, maintenance)"
    )
    reference_id = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="ID de la referencia"
    )
    
    def validate_quantity_change(self, value):
        """Validate that quantity_change is not zero."""
        if value == 0:
            raise serializers.ValidationError(
                "El cambio de cantidad no puede ser cero."
            )
        return value
    
    def validate(self, data):
        """Validate the adjustment data."""
        quantity_change = data.get('quantity_change')
        movement_type = data.get('movement_type')
        
        # Validate movement type matches quantity change direction
        if quantity_change > 0 and movement_type == StockMovement.MOVEMENT_OUT:
            raise serializers.ValidationError(
                "El tipo de movimiento 'Salida' requiere una cantidad negativa."
            )
        
        if quantity_change < 0 and movement_type in [
            StockMovement.MOVEMENT_IN,
            StockMovement.MOVEMENT_RETURN,
            StockMovement.MOVEMENT_INITIAL
        ]:
            raise serializers.ValidationError(
                f"El tipo de movimiento '{dict(StockMovement.MOVEMENT_TYPES)[movement_type]}' "
                "requiere una cantidad positiva."
            )
        
        return data


class LowStockAlertSerializer(serializers.ModelSerializer):
    """Serializer for low stock alerts."""
    
    stock_deficit = serializers.SerializerMethodField()
    
    class Meta:
        model = SparePart
        fields = [
            'id',
            'part_number',
            'name',
            'category',
            'quantity',
            'min_quantity',
            'stock_deficit',
            'unit_of_measure',
            'storage_location',
        ]
    
    def get_stock_deficit(self, obj):
        """Calculate how many units below minimum."""
        return max(0, obj.min_quantity - obj.quantity)
