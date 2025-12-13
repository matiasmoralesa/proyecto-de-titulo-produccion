"""
Admin configuration for Notifications app.
"""
from django.contrib import admin
from apps.notifications.models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    
    list_display = [
        'id',
        'user',
        'notification_type',
        'title',
        'is_read',
        'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'notification_type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Related Object', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """Admin interface for NotificationPreference model."""
    
    list_display = [
        'user',
        'work_order_created',
        'work_order_assigned',
        'work_order_completed',
        'maintenance_due'
    ]
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Work Order Notifications', {
            'fields': (
                'work_order_created',
                'work_order_assigned',
                'work_order_updated',
                'work_order_completed'
            )
        }),
        ('Other Notifications', {
            'fields': (
                'asset_status_changed',
                'maintenance_due',
                'low_stock',
                'system'
            )
        }),
    )
