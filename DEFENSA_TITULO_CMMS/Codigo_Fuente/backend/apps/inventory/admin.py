"""
Admin configuration for inventory app.
"""
from django.contrib import admin
from .models import SparePart, StockMovement


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    """Admin interface for SparePart model."""
    
    list_display = [
        'part_number',
        'name',
        'category',
        'quantity',
        'min_quantity',
        'stock_status',
        'unit_cost',
        'is_active',
    ]
    list_filter = ['category', 'is_active', 'manufacturer']
    search_fields = ['part_number', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('part_number', 'name', 'description', 'category', 'manufacturer')
        }),
        ('Stock', {
            'fields': ('quantity', 'min_quantity', 'unit_of_measure', 'storage_location')
        }),
        ('Costos', {
            'fields': ('unit_cost',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating a spare part."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """Admin interface for StockMovement model."""
    
    list_display = [
        'spare_part',
        'movement_type',
        'quantity',
        'quantity_before',
        'quantity_after',
        'user',
        'created_at',
    ]
    list_filter = ['movement_type', 'created_at']
    search_fields = ['spare_part__name', 'spare_part__part_number', 'notes']
    readonly_fields = [
        'spare_part',
        'movement_type',
        'quantity',
        'quantity_before',
        'quantity_after',
        'unit_cost',
        'user',
        'created_at',
    ]
    
    fieldsets = (
        ('Movimiento', {
            'fields': (
                'spare_part',
                'movement_type',
                'quantity',
                'quantity_before',
                'quantity_after',
            )
        }),
        ('Costos', {
            'fields': ('unit_cost',)
        }),
        ('Referencia', {
            'fields': ('reference_type', 'reference_id')
        }),
        ('Información Adicional', {
            'fields': ('notes', 'user', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual creation of stock movements."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing of stock movements."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disable deletion of stock movements."""
        return False
