"""
Admin configuration for work orders app.
"""
from django.contrib import admin
from .models import WorkOrder


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    """Admin for WorkOrder model."""
    list_display = [
        'work_order_number', 'title', 'asset', 'priority', 'status',
        'assigned_to', 'scheduled_date', 'created_at'
    ]
    list_filter = ['status', 'priority', 'scheduled_date', 'created_at']
    search_fields = ['work_order_number', 'title', 'description', 'asset__name']
    readonly_fields = ['work_order_number', 'id', 'created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('work_order_number', 'title', 'description', 'asset')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'priority', 'status', 'scheduled_date')
        }),
        ('Completion', {
            'fields': ('completed_date', 'completion_notes', 'actual_hours'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
