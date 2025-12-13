"""
Serializers for notifications app.
"""
from rest_framework import serializers
from apps.notifications.models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'is_read',
            'read_at',
            'related_object_type',
            'related_object_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'read_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for NotificationPreference model."""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id',
            'work_order_created',
            'work_order_assigned',
            'work_order_updated',
            'work_order_completed',
            'asset_status_changed',
            'maintenance_due',
            'low_stock',
            'system',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
