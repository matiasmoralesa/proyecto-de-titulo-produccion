"""
Comandos interactivos del bot de Telegram
"""
from typing import Dict, Optional
from apps.authentication.models import User
from apps.work_orders.models import WorkOrder
from apps.ml_predictions.models import FailurePrediction
from apps.assets.models import Asset
from django.utils import timezone
from datetime import timedelta


class BotCommandHandler:
    """
    Maneja los comandos del bot de Telegram
    """
    
    def __init__(self):
        self.commands = {
            '/start': self.cmd_start,
            '/help': self.cmd_help,
            '/status': self.cmd_status,
            '/workorders': self.cmd_workorders,
            '/predictions': self.cmd_predictions,
            '/assets': self.cmd_assets,
            '/myinfo': self.cmd_myinfo,
        }
    
    def handle_command(self, command: str, user: Optional[User] = None) -> Dict:
        """
        Procesa un comando y retorna la respuesta
        
        Returns:
            Dict con 'text' y opcionalmente 'buttons'
        """
        command = command.lower().split()[0]  # Solo el comando, sin parámetros
        
        handler = self.commands.get(command)
        if handler:
            return handler(user)
        else:
            return {
                'text': (
                    f'❌ Comando "{command}" no reconocido.\n\n'
                    'Usa /help para ver los comandos disponibles.'
                )
            }
    
    def cmd_start(self, user: Optional[User] = None) -> Dict:
        """Comando /start"""
        return {
            'text': (
                '👋 ¡Bienvenido al Bot CMMS!\n\n'
                'Soy tu asistente para el sistema de gestión de mantenimiento.\n\n'
                '📋 Puedo ayudarte con:\n'
                '• Ver tus órdenes de trabajo\n'
                '• Consultar predicciones de fallos\n'
                '• Revisar estado de activos\n'
                '• Recibir notificaciones en tiempo real\n\n'
                'Usa /help para ver todos los comandos disponibles.'
            ),
            'buttons': [
                [{'text': '📋 Mis Órdenes', 'callback_data': 'cmd_workorders'}],
                [{'text': '⚠️ Predicciones', 'callback_data': 'cmd_predictions'}],
                [{'text': '❓ Ayuda', 'callback_data': 'cmd_help'}]
            ]
        }
    
    def cmd_help(self, user: Optional[User] = None) -> Dict:
        """Comando /help"""
        return {
            'text': (
                '📚 *Comandos Disponibles*\n\n'
                '/start - Iniciar el bot\n'
                '/help - Ver esta ayuda\n'
                '/status - Estado general del sistema\n'
                '/workorders - Ver tus órdenes de trabajo\n'
                '/predictions - Ver predicciones de alto riesgo\n'
                '/assets - Ver estado de activos\n'
                '/myinfo - Ver tu información\n\n'
                '💡 También puedes usar los botones interactivos para navegar.'
            )
        }
    
    def cmd_status(self, user: Optional[User] = None) -> Dict:
        """Comando /status - Estado general del sistema"""
        # Estadísticas generales
        total_assets = Asset.objects.filter(is_archived=False).count()
        active_wo = WorkOrder.objects.filter(status__in=['Pendiente', 'En Progreso']).count()
        high_risk = FailurePrediction.objects.filter(
            risk_level__in=['HIGH', 'CRITICAL'],
            prediction_date__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return {
            'text': (
                '📊 *Estado del Sistema CMMS*\n\n'
                f'🔧 Activos activos: {total_assets}\n'
                f'📋 Órdenes de trabajo activas: {active_wo}\n'
                f'⚠️ Predicciones de alto riesgo: {high_risk}\n\n'
                f'🕐 Última actualización: {timezone.now().strftime("%d/%m/%Y %H:%M")}'
            ),
            'buttons': [
                [{'text': '📋 Ver OT Activas', 'callback_data': 'cmd_workorders'}],
                [{'text': '⚠️ Ver Predicciones', 'callback_data': 'cmd_predictions'}]
            ]
        }
    
    def cmd_workorders(self, user: Optional[User] = None) -> Dict:
        """Comando /workorders - Ver órdenes de trabajo"""
        if not user:
            return {'text': '❌ Usuario no identificado. Contacta al administrador.'}
        
        # Órdenes asignadas al usuario
        my_workorders = WorkOrder.objects.filter(
            assigned_to=user,
            status__in=['Pendiente', 'En Progreso']
        ).order_by('-created_at')[:5]
        
        if not my_workorders.exists():
            return {
                'text': (
                    '✅ *Mis Órdenes de Trabajo*\n\n'
                    'No tienes órdenes de trabajo pendientes.\n\n'
                    '¡Buen trabajo! 🎉'
                )
            }
        
        text = '📋 *Mis Órdenes de Trabajo*\n\n'
        
        for wo in my_workorders:
            priority_emoji = {
                'Baja': '🟢',
                'Media': '🟡',
                'Alta': '🟠',
                'Urgente': '🔴'
            }.get(wo.priority, '⚪')
            
            status_emoji = {
                'Pendiente': '⏳',
                'En Progreso': '🔄',
                'Completada': '✅',
                'Cancelada': '❌'
            }.get(wo.status, '⚪')
            
            text += (
                f'{priority_emoji} *{wo.work_order_number}*\n'
                f'   {wo.title}\n'
                f'   Activo: {wo.asset.name}\n'
                f'   Estado: {status_emoji} {wo.status}\n'
                f'   Programada: {wo.scheduled_date.strftime("%d/%m/%Y")}\n\n'
            )
        
        # Crear botones para cada OT
        buttons = []
        for wo in my_workorders[:3]:  # Máximo 3 botones
            buttons.append([{
                'text': f'Ver {wo.work_order_number}',
                'callback_data': f'wo_detail_{wo.id}'
            }])
        
        return {'text': text, 'buttons': buttons}
    
    def cmd_predictions(self, user: Optional[User] = None) -> Dict:
        """Comando /predictions - Ver predicciones de alto riesgo"""
        # Predicciones recientes de alto riesgo
        predictions = FailurePrediction.objects.filter(
            risk_level__in=['HIGH', 'CRITICAL'],
            prediction_date__gte=timezone.now() - timedelta(days=7)
        ).order_by('-failure_probability')[:5]
        
        if not predictions.exists():
            return {
                'text': (
                    '✅ *Predicciones de Fallos*\n\n'
                    'No hay predicciones de alto riesgo en los últimos 7 días.\n\n'
                    '¡Todo bajo control! 🎉'
                )
            }
        
        text = '⚠️ *Predicciones de Alto Riesgo*\n\n'
        
        for pred in predictions:
            risk_emoji = {
                'LOW': '🟢',
                'MEDIUM': '🟡',
                'HIGH': '🟠',
                'CRITICAL': '🔴'
            }.get(pred.risk_level, '⚪')
            
            text += (
                f'{risk_emoji} *{pred.asset.name}*\n'
                f'   Probabilidad: {pred.failure_probability:.1%}\n'
                f'   Riesgo: {pred.risk_level}\n'
                f'   Días estimados: {pred.estimated_days_to_failure}\n'
                f'   Fecha: {pred.prediction_date.strftime("%d/%m/%Y")}\n\n'
            )
        
        return {'text': text}
    
    def cmd_assets(self, user: Optional[User] = None) -> Dict:
        """Comando /assets - Ver estado de activos"""
        # Activos por estado
        assets_by_status = {}
        for asset in Asset.objects.filter(is_archived=False):
            status = asset.status
            assets_by_status[status] = assets_by_status.get(status, 0) + 1
        
        text = '🔧 *Estado de Activos*\n\n'
        
        status_emoji = {
            'Operando': '✅',
            'En Mantenimiento': '🔧',
            'Fuera de Servicio': '❌',
            'En Reparación': '🔨'
        }
        
        for status, count in assets_by_status.items():
            emoji = status_emoji.get(status, '⚪')
            text += f'{emoji} {status}: {count}\n'
        
        total = sum(assets_by_status.values())
        text += f'\n📊 Total: {total} activos'
        
        return {'text': text}
    
    def cmd_myinfo(self, user: Optional[User] = None) -> Dict:
        """Comando /myinfo - Ver información del usuario"""
        if not user:
            return {'text': '❌ Usuario no identificado. Contacta al administrador.'}
        
        # Estadísticas del usuario
        my_wo_pending = WorkOrder.objects.filter(
            assigned_to=user,
            status='Pendiente'
        ).count()
        
        my_wo_in_progress = WorkOrder.objects.filter(
            assigned_to=user,
            status='En Progreso'
        ).count()
        
        my_wo_completed = WorkOrder.objects.filter(
            assigned_to=user,
            status='Completada'
        ).count()
        
        text = (
            f'👤 *Mi Información*\n\n'
            f'Nombre: {user.get_full_name() or user.username}\n'
            f'Usuario: @{user.username}\n'
            f'Rol: {user.role.name if user.role else "Sin rol"}\n\n'
            f'📊 *Mis Estadísticas*\n\n'
            f'⏳ Pendientes: {my_wo_pending}\n'
            f'🔄 En progreso: {my_wo_in_progress}\n'
            f'✅ Completadas: {my_wo_completed}\n'
        )
        
        return {'text': text}
    
    def handle_callback(self, callback_data: str, user: Optional[User] = None) -> Dict:
        """
        Maneja callbacks de botones
        """
        # Comandos simples
        if callback_data.startswith('cmd_'):
            command = '/' + callback_data[4:]
            return self.handle_command(command, user)
        
        # Detalle de orden de trabajo
        if callback_data.startswith('wo_detail_'):
            wo_id = callback_data.split('_')[2]
            return self.get_workorder_detail(wo_id, user)
        
        # Acciones sobre órdenes de trabajo
        if callback_data.startswith('wo_accept_'):
            wo_id = callback_data.split('_')[2]
            return self.accept_workorder(wo_id, user)
        
        if callback_data.startswith('wo_start_'):
            wo_id = callback_data.split('_')[2]
            return self.start_workorder(wo_id, user)
        
        return {'text': '❌ Acción no reconocida'}
    
    def get_workorder_detail(self, wo_id: str, user: Optional[User] = None) -> Dict:
        """Obtiene el detalle de una orden de trabajo"""
        try:
            wo = WorkOrder.objects.get(id=wo_id)
            
            priority_emoji = {
                'Baja': '🟢',
                'Media': '🟡',
                'Alta': '🟠',
                'Urgente': '🔴'
            }.get(wo.priority, '⚪')
            
            text = (
                f'📋 *Detalle de Orden de Trabajo*\n\n'
                f'*{wo.work_order_number}*\n'
                f'{wo.title}\n\n'
                f'🔧 Activo: {wo.asset.name}\n'
                f'{priority_emoji} Prioridad: {wo.priority}\n'
                f'📅 Programada: {wo.scheduled_date.strftime("%d/%m/%Y %H:%M")}\n'
                f'👤 Asignado a: {wo.assigned_to.get_full_name() or wo.assigned_to.username}\n'
                f'📊 Estado: {wo.status}\n\n'
                f'📝 Descripción:\n{wo.description}'
            )
            
            # Botones según el estado
            buttons = []
            if wo.status == 'Pendiente':
                buttons.append([
                    {'text': '✅ Aceptar', 'callback_data': f'wo_accept_{wo.id}'},
                    {'text': '🔄 Iniciar', 'callback_data': f'wo_start_{wo.id}'}
                ])
            elif wo.status == 'En Progreso':
                buttons.append([
                    {'text': '✅ Completar', 'callback_data': f'wo_complete_{wo.id}'}
                ])
            
            buttons.append([{'text': '« Volver', 'callback_data': 'cmd_workorders'}])
            
            return {'text': text, 'buttons': buttons}
        
        except WorkOrder.DoesNotExist:
            return {'text': '❌ Orden de trabajo no encontrada'}
    
    def accept_workorder(self, wo_id: str, user: Optional[User] = None) -> Dict:
        """Acepta una orden de trabajo"""
        try:
            wo = WorkOrder.objects.get(id=wo_id)
            
            if wo.assigned_to != user:
                return {'text': '❌ Esta orden no está asignada a ti'}
            
            # Aquí podrías agregar lógica adicional de aceptación
            
            return {
                'text': (
                    f'✅ Orden {wo.work_order_number} aceptada\n\n'
                    'Puedes iniciarla cuando estés listo.'
                ),
                'buttons': [
                    [{'text': '🔄 Iniciar Ahora', 'callback_data': f'wo_start_{wo.id}'}],
                    [{'text': '« Volver', 'callback_data': 'cmd_workorders'}]
                ]
            }
        
        except WorkOrder.DoesNotExist:
            return {'text': '❌ Orden de trabajo no encontrada'}
    
    def start_workorder(self, wo_id: str, user: Optional[User] = None) -> Dict:
        """Inicia una orden de trabajo"""
        try:
            wo = WorkOrder.objects.get(id=wo_id)
            
            if wo.assigned_to != user:
                return {'text': '❌ Esta orden no está asignada a ti'}
            
            if wo.status == 'Completada':
                return {'text': '❌ Esta orden ya está completada'}
            
            wo.status = 'En Progreso'
            wo.save()
            
            return {
                'text': (
                    f'🔄 Orden {wo.work_order_number} iniciada\n\n'
                    f'Activo: {wo.asset.name}\n'
                    f'Hora de inicio: {timezone.now().strftime("%H:%M")}\n\n'
                    '¡Buena suerte con el trabajo!'
                ),
                'buttons': [
                    [{'text': '« Mis Órdenes', 'callback_data': 'cmd_workorders'}]
                ]
            }
        
        except WorkOrder.DoesNotExist:
            return {'text': '❌ Orden de trabajo no encontrada'}
