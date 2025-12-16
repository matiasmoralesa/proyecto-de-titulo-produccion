"""
Signals para integración automática del sistema ML
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import FailurePrediction
from apps.work_orders.models import WorkOrder
from apps.notifications.models import Notification


@receiver(post_save, sender=FailurePrediction)
def handle_high_risk_prediction(sender, instance, created, **kwargs):
    """
    Cuando se crea una predicción de alto riesgo:
    1. Crear orden de trabajo automáticamente
    2. Asignar operador capacitado
    3. Enviar notificaciones
    """
    if not created:
        return
    
    # Solo actuar en predicciones de riesgo MEDIUM, HIGH o CRITICAL
    if instance.risk_level.upper() not in ['MEDIUM', 'HIGH', 'CRITICAL']:
        return
    
    # Verificar si ya existe una orden de trabajo reciente para este activo
    recent_wo = WorkOrder.objects.filter(
        asset=instance.asset,
        status__in=['pending', 'in_progress'],
        created_at__gte=timezone.now() - timedelta(days=7)
    ).exists()
    
    if recent_wo:
        print(f"Ya existe una orden de trabajo reciente para {instance.asset.name}")
        return
    
    # Buscar operador disponible
    try:
        from apps.authentication.models import User, Role
        
        # Buscar operadores con el rol OPERATOR que estén activos
        operator_role = Role.objects.filter(name='OPERATOR').first()
        if operator_role:
            best_operator = User.objects.filter(
                role=operator_role,
                is_active=True
            ).first()
        else:
            best_operator = None
        
        # Si no hay operador disponible, usar el primer admin/supervisor
        if not best_operator:
            admin_role = Role.objects.filter(name__in=['ADMIN', 'SUPERVISOR']).first()
            if admin_role:
                best_operator = User.objects.filter(role=admin_role, is_active=True).first()
        
        if not best_operator:
            print(f"No se encontró operador disponible para {instance.asset.name}")
            return
    
    except Exception as e:
        print(f"Error al buscar operador: {str(e)}")
        return
    
    # Crear orden de trabajo preventiva
    priority_map = {
        'MEDIUM': 'Media',
        'HIGH': 'Alta',
        'CRITICAL': 'Urgente'
    }
    
    work_order = WorkOrder.objects.create(
        asset=instance.asset,
        title=f'Mantenimiento Preventivo - Predicción ML',
        description=(
            f'🤖 Orden generada automáticamente por sistema de predicción ML\n\n'
            f'📊 Probabilidad de fallo: {instance.failure_probability:.1%}\n'
            f'⚠️ Nivel de riesgo: {instance.risk_level.upper()}\n'
            f'📅 Días estimados hasta fallo: {instance.estimated_days_to_failure}\n\n'
            f'💡 Acción recomendada:\n{instance.recommended_action}'
        ),
        priority=priority_map[instance.risk_level],
        status='Pendiente',
        scheduled_date=timezone.now() + timedelta(days=1),
        assigned_to=best_operator,
        created_by=best_operator  # Sistema automático usa el operador asignado
    )
    
    # Vincular predicción con orden de trabajo
    instance.work_order_created = work_order
    instance.save(update_fields=['work_order_created'])
    
    print(f"✓ Orden de trabajo {work_order.work_order_number} creada para {instance.asset.name}")
    print(f"✓ Operador {best_operator.get_full_name()} asignado automáticamente")
    
    # Crear notificación para el operador (sistema antiguo)
    try:
        Notification.objects.create(
            user=best_operator,
            title=f'Nueva OT Asignada: {work_order.work_order_number}',
            message=(
                f'Se te ha asignado una orden de trabajo de mantenimiento preventivo.\n\n'
                f'Activo: {instance.asset.name}\n'
                f'Prioridad: {work_order.priority}\n'
                f'Riesgo de fallo: {instance.failure_probability:.1%}'
            ),
            notification_type='work_order_assigned',
            related_object_type='work_order',
            related_object_id=str(work_order.id)
        )
        
        print(f"✓ Notificación in-app creada para {best_operator.get_full_name()}")
    
    except Exception as e:
        print(f"Error al crear notificación in-app: {str(e)}")
    
    # Enviar notificación por bot omnicanal
    try:
        from apps.omnichannel_bot.message_router import MessageRouter
        
        router = MessageRouter()
        priority_level = 'critical' if instance.risk_level.upper() == 'CRITICAL' else 'high' if instance.risk_level.upper() == 'HIGH' else 'normal'
        
        results = router.send_to_user(
            user=best_operator,
            title=f'📋 Nueva OT Asignada: {work_order.work_order_number}',
            message=(
                f'Se te ha asignado una orden de trabajo de mantenimiento preventivo.\n\n'
                f'🔧 Activo: {instance.asset.name}\n'
                f'⚠️ Prioridad: {work_order.priority}\n'
                f'📊 Riesgo de fallo: {instance.failure_probability:.1%}\n'
                f'📅 Programada: {work_order.scheduled_date.strftime("%d/%m/%Y")}\n\n'
                f'💡 {instance.recommended_action}'
            ),
            message_type='work_order_assigned',
            priority=priority_level,
            related_object_type='work_order',
            related_object_id=str(work_order.id)
        )
        
        if results:
            channels_sent = [ch for ch, success in results.items() if success]
            if channels_sent:
                print(f"✓ Notificación omnicanal enviada a {best_operator.get_full_name()} vía {', '.join(channels_sent)}")
    
    except Exception as e:
        print(f"Error al enviar notificación omnicanal: {str(e)}")
    
    # Notificar a supervisores si es crítico
    if instance.risk_level.upper() == 'CRITICAL':
        try:
            from apps.authentication.models import User, Role
            
            supervisor_role = Role.objects.get(name='SUPERVISOR')
            supervisors = User.objects.filter(role=supervisor_role, is_active=True)
            
            for supervisor in supervisors:
                Notification.objects.create(
                    user=supervisor,
                    title=f'🚨 ALERTA CRÍTICA: {instance.asset.name}',
                    message=(
                        f'El sistema ML ha detectado un riesgo CRÍTICO de fallo.\n\n'
                        f'Activo: {instance.asset.name}\n'
                        f'Probabilidad: {instance.failure_probability:.1%}\n'
                        f'Orden de trabajo: {work_order.work_order_number}\n'
                        f'Operador asignado: {work_order.assigned_to.get_full_name() if work_order.assigned_to else "Pendiente"}'
                    ),
                    notification_type='critical_alert',
                    related_object_type='work_order',
                    related_object_id=work_order.id
                )
            
            print(f"✓ Notificaciones críticas enviadas a {supervisors.count()} supervisores")
        
        except Exception as e:
            print(f"Error al notificar supervisores: {str(e)}")


@receiver(post_save, sender=WorkOrder)
def update_prediction_on_work_order_completion(sender, instance, created, **kwargs):
    """
    Cuando se completa una orden de trabajo generada por predicción,
    actualizar el registro de predicción
    """
    if created or instance.status != 'completed':
        return
    
    # Buscar predicción relacionada
    try:
        prediction = FailurePrediction.objects.get(work_order_created=instance)
        
        # Marcar como atendida
        if not hasattr(prediction, 'was_accurate'):
            # Aquí podrías agregar lógica para evaluar si la predicción fue correcta
            # basándote en los hallazgos de la orden de trabajo
            pass
        
        print(f"✓ Predicción actualizada para {instance.asset.name}")
    
    except FailurePrediction.DoesNotExist:
        pass
