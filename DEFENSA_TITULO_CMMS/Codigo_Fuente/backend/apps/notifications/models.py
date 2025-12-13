"""
Notification models.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.authentication.models import User


class Notification(TimeStampedModel):
    """Notification model for user alerts."""
    
    # Notification Types
    TYPE_WORK_ORDER_CREATED = 'work_order_created'
    TYPE_WORK_ORDER_ASSIGNED = 'work_order_assigned'
    TYPE_WORK_ORDER_UPDATED = 'work_order_updated'
    TYPE_WORK_ORDER_COMPLETED = 'work_order_completed'
    TYPE_ASSET_STATUS_CHANGED = 'asset_status_changed'
    TYPE_MAINTENANCE_DUE = 'maintenance_due'
    TYPE_LOW_STOCK = 'low_stock'
    TYPE_SYSTEM = 'system'
    
    TYPE_CHOICES = [
        (TYPE_WORK_ORDER_CREATED, 'Orden de Trabajo Creada'),
        (TYPE_WORK_ORDER_ASSIGNED, 'Orden de Trabajo Asignada'),
        (TYPE_WORK_ORDER_UPDATED, 'Orden de Trabajo Actualizada'),
        (TYPE_WORK_ORDER_COMPLETED, 'Orden de Trabajo Completada'),
        (TYPE_ASSET_STATUS_CHANGED, 'Estado de Activo Cambiado'),
        (TYPE_MAINTENANCE_DUE, 'Mantenimiento Pendiente'),
        (TYPE_LOW_STOCK, 'Stock Bajo'),
        (TYPE_SYSTEM, 'Sistema'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related object tracking (generic)
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        from django.utils import timezone
        
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationPreference(TimeStampedModel):
    """User notification preferences."""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Notification type preferences
    work_order_created = models.BooleanField(default=True)
    work_order_assigned = models.BooleanField(default=True)
    work_order_updated = models.BooleanField(default=True)
    work_order_completed = models.BooleanField(default=True)
    asset_status_changed = models.BooleanField(default=True)
    maintenance_due = models.BooleanField(default=True)
    low_stock = models.BooleanField(default=True)
    system = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    def is_enabled(self, notification_type):
        """Check if notification type is enabled for user."""
        type_mapping = {
            Notification.TYPE_WORK_ORDER_CREATED: self.work_order_created,
            Notification.TYPE_WORK_ORDER_ASSIGNED: self.work_order_assigned,
            Notification.TYPE_WORK_ORDER_UPDATED: self.work_order_updated,
            Notification.TYPE_WORK_ORDER_COMPLETED: self.work_order_completed,
            Notification.TYPE_ASSET_STATUS_CHANGED: self.asset_status_changed,
            Notification.TYPE_MAINTENANCE_DUE: self.maintenance_due,
            Notification.TYPE_LOW_STOCK: self.low_stock,
            Notification.TYPE_SYSTEM: self.system,
        }
        return type_mapping.get(notification_type, True)
