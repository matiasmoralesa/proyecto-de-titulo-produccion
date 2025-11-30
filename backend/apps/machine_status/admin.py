"""
Admin configuration for machine status app.
"""
from django.contrib import admin
from .models import AssetStatus, AssetStatusHistory


@admin.register(AssetStatus)
class AssetStatusAdmin(admin.ModelAdmin):
    """Admin for AssetStatus model."""
    list_display = [
        'asset',
        'status_type',
        'odometer_reading',
        'fuel_level',
        'last_updated_by',
        'updated_at',
    ]
    list_filter = ['status_type', 'updated_at']
    search_fields = ['asset__name', 'condition_notes']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Asset Information', {
            'fields': ('asset', 'status_type')
        }),
        ('Status Details', {
            'fields': ('odometer_reading', 'fuel_level', 'condition_notes')
        }),
        ('Metadata', {
            'fields': ('last_updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AssetStatusHistory)
class AssetStatusHistoryAdmin(admin.ModelAdmin):
    """Admin for AssetStatusHistory model."""
    list_display = [
        'asset',
        'status_type',
        'odometer_reading',
        'fuel_level',
        'updated_by',
        'timestamp',
    ]
    list_filter = ['status_type', 'timestamp']
    search_fields = ['asset__name', 'condition_notes']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        """Disable adding history records manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing history records."""
        return False
