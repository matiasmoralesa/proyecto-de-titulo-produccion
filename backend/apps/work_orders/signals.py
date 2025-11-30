"""
Signals for Work Order notifications.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.work_orders.models import WorkOrder
from apps.notifications.services import NotificationService


@receiver(pre_save, sender=WorkOrder)
def track_work_order_changes(sender, instance, **kwargs):
    """Track changes to work order for notifications."""
    if instance.pk:
        try:
            # Get the previous state
            previous = WorkOrder.objects.get(pk=instance.pk)
            instance._previous_assigned_to = previous.assigned_to
            instance._previous_status = previous.status
        except WorkOrder.DoesNotExist:
            instance._previous_assigned_to = None
            instance._previous_status = None
    else:
        instance._previous_assigned_to = None
        instance._previous_status = None


@receiver(post_save, sender=WorkOrder)
def work_order_notification_handler(sender, instance, created, **kwargs):
    """
    Handle work order notifications on create and update.
    
    Args:
        sender: WorkOrder model
        instance: WorkOrder instance
        created: Boolean indicating if this is a new instance
        kwargs: Additional keyword arguments
    """
    if created:
        # New work order created
        NotificationService.notify_work_order_created(instance)
    else:
        # Work order updated
        # Check if assigned user changed
        previous_assignee = getattr(instance, '_previous_assigned_to', None)
        if previous_assignee and previous_assignee != instance.assigned_to:
            NotificationService.notify_work_order_assigned(instance, previous_assignee)
        
        # Check if status changed to completed
        previous_status = getattr(instance, '_previous_status', None)
        if previous_status and previous_status != instance.status:
            if instance.status == WorkOrder.STATUS_COMPLETED:
                NotificationService.notify_work_order_completed(instance)
            else:
                # General update notification
                # Get the user who made the update from the request context
                # For now, we'll skip this as we need request context
                pass
