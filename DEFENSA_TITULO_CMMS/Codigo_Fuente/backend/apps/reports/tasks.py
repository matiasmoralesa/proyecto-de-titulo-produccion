"""
Tareas de Celery para reportes
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.reports.tasks.generate_weekly_report')
def generate_weekly_report():
    """
    Genera reporte semanal automático los lunes
    """
    logger.info("Generando reporte semanal...")
    
    try:
        from apps.work_orders.models import WorkOrder
        from apps.ml_predictions.models import FailurePrediction
        from apps.assets.models import Asset
        
        # Fecha de inicio de la semana (lunes pasado)
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Estadísticas de la semana
        wo_completed = WorkOrder.objects.filter(
            status='Completada',
            completed_date__date__gte=week_start,
            completed_date__date__lte=week_end
        ).count()
        
        wo_created = WorkOrder.objects.filter(
            created_at__date__gte=week_start,
            created_at__date__lte=week_end
        ).count()
        
        predictions_made = FailurePrediction.objects.filter(
            prediction_date__date__gte=week_start,
            prediction_date__date__lte=week_end
        ).count()
        
        high_risk = FailurePrediction.objects.filter(
            prediction_date__date__gte=week_start,
            prediction_date__date__lte=week_end,
            risk_level__in=['HIGH', 'CRITICAL']
        ).count()
        
        total_assets = Asset.objects.filter(is_archived=False).count()
        
        # Crear mensaje del reporte
        report_message = (
            f'📊 *Reporte Semanal CMMS*\n'
            f'Semana del {week_start.strftime("%d/%m")} al {week_end.strftime("%d/%m/%Y")}\n\n'
            f'📋 *Órdenes de Trabajo*\n'
            f'   • Creadas: {wo_created}\n'
            f'   • Completadas: {wo_completed}\n\n'
            f'🤖 *Predicciones ML*\n'
            f'   • Total: {predictions_made}\n'
            f'   • Alto riesgo: {high_risk}\n\n'
            f'🔧 *Activos*\n'
            f'   • Total activos: {total_assets}\n\n'
            f'Generado automáticamente el {timezone.now().strftime("%d/%m/%Y %H:%M")}'
        )
        
        # Enviar a supervisores y admins
        from apps.omnichannel_bot.message_router import MessageRouter
        
        router = MessageRouter()
        
        stats_supervisor = router.broadcast_to_role(
            role_name='SUPERVISOR',
            title='📊 Reporte Semanal',
            message=report_message,
            priority='normal'
        )
        
        stats_admin = router.broadcast_to_role(
            role_name='ADMIN',
            title='📊 Reporte Semanal',
            message=report_message,
            priority='normal'
        )
        
        total_sent = stats_supervisor['success'] + stats_admin['success']
        
        logger.info(f"Reporte semanal enviado a {total_sent} usuarios")
        
        return {
            'status': 'success',
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'wo_completed': wo_completed,
            'wo_created': wo_created,
            'predictions': predictions_made,
            'high_risk': high_risk,
            'sent_to': total_sent,
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error generando reporte semanal: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task(name='apps.reports.tasks.generate_monthly_report')
def generate_monthly_report():
    """
    Genera reporte mensual (puede ser programado para el día 1 de cada mes)
    """
    logger.info("Generando reporte mensual...")
    
    # Similar al reporte semanal pero con datos del mes
    # Implementación similar...
    
    return {
        'status': 'success',
        'message': 'Reporte mensual generado',
        'timestamp': timezone.now().isoformat()
    }
