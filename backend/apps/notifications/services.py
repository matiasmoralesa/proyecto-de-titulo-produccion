"""
Notification service for creating and managing notifications.
"""
from typing import List, Optional
from apps.notifications.models import Notification, NotificationPreference
from apps.authentication.models import User


class NotificationService:
    """Service for creating and managing notifications."""
    
    @staticmethod
    def create_notification(
        user: User,
        notification_type: str,
        title: str,
        message: str,
        related_object_type: str = '',
        related_object_id: Optional[int] = None
    ) -> Optional[Notification]:
        """
        Create a notification for a user.
        
        Args:
            user: User to receive the notification
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            related_object_type: Type of related object (e.g., 'work_order')
            related_object_id: ID of related object
            
        Returns:
            Created Notification or None if user has disabled this type
        """
        # Check user preferences
        try:
            preferences = NotificationPreference.objects.get(user=user)
            if not preferences.is_enabled(notification_type):
                return None
        except NotificationPreference.DoesNotExist:
            # Create default preferences if they don't exist
            NotificationPreference.objects.create(user=user)
        
        # Convert related_object_id to string if it's not None
        related_id_str = str(related_object_id) if related_object_id is not None else None
        
        # Create notification
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            related_object_type=related_object_type,
            related_object_id=related_id_str
        )
        
        return notification
    
    @staticmethod
    def create_bulk_notifications(
        users: List[User],
        notification_type: str,
        title: str,
        message: str,
        related_object_type: str = '',
        related_object_id: Optional[int] = None
    ) -> List[Notification]:
        """
        Create notifications for multiple users.
        
        Args:
            users: List of users to receive the notification
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            related_object_type: Type of related object
            related_object_id: ID of related object
            
        Returns:
            List of created Notifications
        """
        notifications = []
        for user in users:
            notification = NotificationService.create_notification(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                related_object_type=related_object_type,
                related_object_id=related_object_id
            )
            if notification:
                notifications.append(notification)
        
        return notifications
    
    @staticmethod
    def notify_work_order_created(work_order):
        """
        Create notifications when a work order is created.
        
        Args:
            work_order: WorkOrder instance
        """
        # Notify assigned user
        NotificationService.create_notification(
            user=work_order.assigned_to,
            notification_type=Notification.TYPE_WORK_ORDER_CREATED,
            title=f"Nueva Orden de Trabajo: {work_order.work_order_number}",
            message=f"Se ha creado una nueva orden de trabajo '{work_order.title}' asignada a ti.",
            related_object_type='work_order',
            related_object_id=work_order.id
        )
        
        # Notify supervisors and admins if high priority or urgent
        if work_order.priority in ['Alta', 'Urgente']:
            supervisors_and_admins = User.objects.filter(
                role__name__in=['ADMIN', 'SUPERVISOR']
            ).exclude(id=work_order.assigned_to.id)
            
            NotificationService.create_bulk_notifications(
                users=list(supervisors_and_admins),
                notification_type=Notification.TYPE_WORK_ORDER_CREATED,
                title=f"Orden de Trabajo Prioritaria: {work_order.work_order_number}",
                message=f"Se ha creado una orden de trabajo de prioridad {work_order.priority}: '{work_order.title}'",
                related_object_type='work_order',
                related_object_id=work_order.id
            )
    
    @staticmethod
    def notify_work_order_assigned(work_order, previous_assignee=None):
        """
        Create notifications when a work order is assigned or reassigned.
        
        Args:
            work_order: WorkOrder instance
            previous_assignee: Previous assigned user (if reassigned)
        """
        # Notify new assignee
        NotificationService.create_notification(
            user=work_order.assigned_to,
            notification_type=Notification.TYPE_WORK_ORDER_ASSIGNED,
            title=f"Orden de Trabajo Asignada: {work_order.work_order_number}",
            message=f"Se te ha asignado la orden de trabajo '{work_order.title}'.",
            related_object_type='work_order',
            related_object_id=work_order.id
        )
        
        # Notify previous assignee if reassigned
        if previous_assignee and previous_assignee != work_order.assigned_to:
            NotificationService.create_notification(
                user=previous_assignee,
                notification_type=Notification.TYPE_WORK_ORDER_UPDATED,
                title=f"Orden de Trabajo Reasignada: {work_order.work_order_number}",
                message=f"La orden de trabajo '{work_order.title}' ha sido reasignada a otro usuario.",
                related_object_type='work_order',
                related_object_id=work_order.id
            )
    
    @staticmethod
    def notify_work_order_updated(work_order, updated_by):
        """
        Create notifications when a work order is updated.
        
        Args:
            work_order: WorkOrder instance
            updated_by: User who updated the work order
        """
        # Notify assigned user if they didn't make the update
        if work_order.assigned_to != updated_by:
            NotificationService.create_notification(
                user=work_order.assigned_to,
                notification_type=Notification.TYPE_WORK_ORDER_UPDATED,
                title=f"Orden de Trabajo Actualizada: {work_order.work_order_number}",
                message=f"La orden de trabajo '{work_order.title}' ha sido actualizada.",
                related_object_type='work_order',
                related_object_id=work_order.id
            )
        
        # Notify creator if they didn't make the update
        if work_order.created_by != updated_by and work_order.created_by != work_order.assigned_to:
            NotificationService.create_notification(
                user=work_order.created_by,
                notification_type=Notification.TYPE_WORK_ORDER_UPDATED,
                title=f"Orden de Trabajo Actualizada: {work_order.work_order_number}",
                message=f"La orden de trabajo '{work_order.title}' ha sido actualizada.",
                related_object_type='work_order',
                related_object_id=work_order.id
            )
    
    @staticmethod
    def notify_work_order_completed(work_order):
        """
        Create notifications when a work order is completed.
        
        Args:
            work_order: WorkOrder instance
        """
        # Notify creator
        if work_order.created_by != work_order.assigned_to:
            NotificationService.create_notification(
                user=work_order.created_by,
                notification_type=Notification.TYPE_WORK_ORDER_COMPLETED,
                title=f"Orden de Trabajo Completada: {work_order.work_order_number}",
                message=f"La orden de trabajo '{work_order.title}' ha sido completada.",
                related_object_type='work_order',
                related_object_id=work_order.id
            )
        
        # Notify supervisors and admins
        supervisors_and_admins = User.objects.filter(
            role__name__in=['ADMIN', 'SUPERVISOR']
        ).exclude(id=work_order.assigned_to.id)
        
        NotificationService.create_bulk_notifications(
            users=list(supervisors_and_admins),
            notification_type=Notification.TYPE_WORK_ORDER_COMPLETED,
            title=f"Orden de Trabajo Completada: {work_order.work_order_number}",
            message=f"La orden de trabajo '{work_order.title}' ha sido completada por {work_order.assigned_to.get_full_name() or work_order.assigned_to.username}.",
            related_object_type='work_order',
            related_object_id=work_order.id
        )
