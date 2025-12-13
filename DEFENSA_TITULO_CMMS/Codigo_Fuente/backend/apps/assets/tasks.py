"""
Tareas de Celery para gestión de activos
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Asset
from apps.ml_predictions.models import FailurePrediction
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.assets.tasks.check_critical_assets')
def check_critical_assets():
    """
    Verifica activos en estado crítico cada hora
    """
    logger.info("Verificando activos críticos...")
    
    try:
        # Activos fuera de servicio
        out_of_service = Asset.objects.filter(
            is_archived=False,
            status='Fuera de Servicio'
        ).count()
        
        # Activos con predicciones de alto riesgo recientes
        high_risk_predictions = FailurePrediction.objects.filter(
            risk_level__in=['HIGH', 'CRITICAL'],
            prediction_date__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        # Activos sin mantenimiento reciente (más de 90 días)
        from apps.maintenance.models import MaintenanceRecord
        assets_needing_maintenance = 0
        
        for asset in Asset.objects.filter(is_archived=False):
            last_maintenance = MaintenanceRecord.objects.filter(
                asset=asset
            ).order_by('-maintenance_date').first()
            
            if not last_maintenance or \
               (timezone.now().date() - last_maintenance.maintenance_date).days > 90:
                assets_needing_maintenance += 1
        
        logger.info(
            f"Verificación completada: {out_of_service} fuera de servicio, "
            f"{high_risk_predictions} alto riesgo, "
            f"{assets_needing_maintenance} necesitan mantenimiento"
        )
        
        # Si hay situaciones críticas, enviar alerta
        if out_of_service > 5 or high_risk_predictions > 10:
            send_critical_alert.delay(
                out_of_service=out_of_service,
                high_risk=high_risk_predictions
            )
        
        return {
            'status': 'success',
            'out_of_service': out_of_service,
            'high_risk_predictions': high_risk_predictions,
            'needing_maintenance': assets_needing_maintenance,
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error verificando activos críticos: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }


@shared_task(name='apps.assets.tasks.send_critical_alert')
def send_critical_alert(out_of_service=0, high_risk=0):
    """
    Envía alerta crítica a supervisores
    """
    logger.info("Enviando alerta crítica...")
    
    try:
        from apps.omnichannel_bot.message_router import MessageRouter
        
        router = MessageRouter()
        
        message = (
            f'🚨 *ALERTA CRÍTICA DEL SISTEMA*\n\n'
            f'Se ha detectado una situación que requiere atención:\n\n'
            f'❌ Activos fuera de servicio: {out_of_service}\n'
            f'⚠️ Predicciones de alto riesgo: {high_risk}\n\n'
            f'Por favor, revisa el sistema inmediatamente.'
        )
        
        # Enviar a supervisores
        stats = router.broadcast_to_role(
            role_name='SUPERVISOR',
            title='🚨 Alerta Crítica',
            message=message,
            priority='critical'
        )
        
        logger.info(f"Alerta enviada a {stats['success']} supervisores")
        
        return {
            'status': 'success',
            'sent_to': stats['success'],
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error enviando alerta crítica: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
