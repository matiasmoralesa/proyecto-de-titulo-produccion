"""
Tareas de Celery para notificaciones
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Notification
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.notifications.tasks.cleanup_old_notifications')
def cleanup_old_notifications(days=30):
    """
    Limpia notificaciones antiguas (más de 30 días)
    """
    logger.info(f"Limpiando notificaciones de más de {days} días...")
    
    try:
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Eliminar notificaciones leídas antiguas
        deleted_count, _ = Notification.objects.filter(
            is_read=True,
            created_at__lt=cutoff_date
        ).delete()
        
        logger.info(f"Se eliminaron {deleted_count} notificaciones antiguas")
        
        return {
            'status': 'success',
            'deleted_count': deleted_count,
            'cutoff_date': cutoff_date.isoformat(),
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error limpiando notificaciones: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task(name='apps.notifications.tasks.send_daily_summary')
def send_daily_summary():
    """
    Envía resumen diario de notificaciones no leídas
    """
    logger.info("Enviando resumen diario de notificaciones...")
    
    try:
        from apps.authentication.models import User
        from apps.omnichannel_bot.message_router import MessageRouter
        
        router = MessageRouter()
        sent_count = 0
        
        # Para cada usuario activo
        for user in User.objects.filter(is_active=True):
            unread_count = Notification.objects.filter(
                user=user,
                is_read=False
            ).count()
            
            if unread_count > 0:
                router.send_to_user(
                    user=user,
                    title='📊 Resumen Diario',
                    message=(
                        f'Tienes {unread_count} notificaciones sin leer.\n\n'
                        'Revisa el sistema para mantenerte al día.'
                    ),
                    message_type='daily_summary',
                    priority='normal'
                )
                sent_count += 1
        
        logger.info(f"Resumen enviado a {sent_count} usuarios")
        
        return {
            'status': 'success',
            'sent_to': sent_count,
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error enviando resumen diario: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
