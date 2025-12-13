"""
Admin configuration for Maintenance app.
"""
from django.contrib import admin
from .models import MaintenancePlan


@admin.register(MaintenancePlan)
class MaintenancePlanAdmin(admin.ModelAdmin):
    """Admin interface for MaintenancePlan model."""
    
    list_display = [
        'name',
        'asset',
        'recurrence_type',
        'next_due_date',
        'status',
        'is_paused',
        'created_at'
    ]
    list_filter = ['status', 'recurrence_type', 'is_paused', 'created_at']
    search_fields = ['name', 'description', 'asset__name']
    readonly_fields = ['created_at', 'updated_at', 'paused_at']
    date_hierarchy = 'next_due_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'asset', 'assigned_to')
        }),
        ('Configuración de Recurrencia', {
            'fields': (
                'recurrence_type',
                'recurrence_interval',
                'start_date',
                'next_due_date',
                'last_completed_date'
            )
        }),
        ('Mantenimiento Basado en Uso', {
            'fields': ('usage_threshold', 'last_usage_value'),
            'classes': ('collapse',)
        }),
        ('Detalles Adicionales', {
            'fields': ('estimated_duration_hours', 'status')
        }),
        ('Estado de Pausa', {
            'fields': ('is_paused', 'paused_at', 'paused_by'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
