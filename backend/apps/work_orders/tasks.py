"""
Tareas de Celery para órdenes de trabajo
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import WorkOrder
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.work_orders.tasks.check_overdue_workorders')
def check_overdue_workorders():
    """
    Verifica órdenes de trabajo vencidas cada 30 minutos
    """
    logger.info("Verificando órdenes de trabajo vencidas...")
    
    try:
        # Órdenes vencidas (scheduled_date pasó y aún están pendientes)
        overdue_orders = WorkOrder.objects.filter(
            status__in=['Pendiente', 'En Progreso'],
            scheduled_date__lt=timezone.now()
        )
        
        overdue_count = overdue_orders.count()
        
        if overdue_count > 0:
            logger.warning(f"Se encontraron {overdue_count} órdenes vencidas")
            
            # Enviar notificación a cada operador asignado
            for wo in overdue_orders[:10]:  # Limitar a 10 para no saturar
                send_overdue_notification.delay(str(wo.id))
        
        return {
            'status': 'success',
            'overdue_count': overdue_count,
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error verificando órdenes vencidas: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task(name='apps.work_orders.tasks.send_overdue_notification')
def send_overdue_notification(workorder_id):
    """
    Envía notificación de orden vencida al operador
    """
    try:
        wo = WorkOrder.objects.get(id=workorder_id)
        
        from apps.omnichannel_bot.message_router import MessageRouter
        
        router = MessageRouter()
        
        days_overdue = (timezone.now().date() - wo.scheduled_date.date()).days
        
        router.send_to_user(
            user=wo.assigned_to,
            title=f'⏰ Orden Vencida: {wo.work_order_number}',
            message=(
                f'La siguiente orden de trabajo está vencida:\n\n'
                f'📋 {wo.work_order_number}\n'
                f'🔧 Activo: {wo.asset.name}\n'
                f'📅 Programada: {wo.scheduled_date.strftime("%d/%m/%Y")}\n'
                f'⏰ Vencida hace: {days_overdue} días\n\n'
                f'Por favor, actualiza el estado de esta orden.'
            ),
            message_type='overdue_reminder',
            priority='high',
            related_object_type='work_order',
            related_object_id=str(wo.id)
        )
        
        logger.info(f"Notificación de vencimiento enviada para {wo.work_order_number}")
        
        return {'status': 'success', 'workorder': wo.work_order_number}
    
    except WorkOrder.DoesNotExist:
        logger.error(f"Orden de trabajo {workorder_id} no encontrada")
        return {'status': 'error', 'error': 'WorkOrder not found'}
    except Exception as e:
        logger.error(f"Error enviando notificación: {str(e)}")
        return {'status': 'error', 'error': str(e)}
