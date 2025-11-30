"""
Servicio de enrutamiento de mensajes a través de múltiples canales
"""
from typing import List, Dict, Optional
from django.utils import timezone
from .models import ChannelConfig, UserChannelPreference, MessageLog
from .channels.telegram import TelegramChannel
import logging

logger = logging.getLogger(__name__)


class MessageRouter:
    """
    Enruta mensajes a través de los canales configurados
    """
    
    def __init__(self):
        self.channels = {}
        self._load_channels()
    
    def _load_channels(self):
        """Carga los canales habilitados"""
        configs = ChannelConfig.objects.filter(is_enabled=True)
        
        for config in configs:
            if config.channel_type == 'TELEGRAM':
                self.channels['TELEGRAM'] = TelegramChannel(config.config)
            # Aquí se agregarían otros canales (WhatsApp, Email, SMS)
        
        logger.info(f"Canales cargados: {list(self.channels.keys())}")
    
    def send_to_user(
        self,
        user,
        title: str,
        message: str,
        message_type: str = 'notification',
        priority: str = 'normal',
        related_object_type: str = '',
        related_object_id: str = ''
    ) -> Dict[str, bool]:
        """
        Envía un mensaje a un usuario a través de todos sus canales habilitados
        
        Args:
            user: Usuario destinatario
            title: Título del mensaje
            message: Contenido del mensaje
            message_type: Tipo de mensaje (notification, alert, reminder, etc.)
            priority: Prioridad (normal, high, critical)
            related_object_type: Tipo de objeto relacionado (work_order, prediction, etc.)
            related_object_id: ID del objeto relacionado
        
        Returns:
            Dict con el resultado por canal: {'TELEGRAM': True, 'EMAIL': False}
        """
        results = {}
        
        # Obtener preferencias del usuario
        preferences = UserChannelPreference.objects.filter(
            user=user,
            is_enabled=True
        )
        
        # Si no hay preferencias, intentar enviar por todos los canales disponibles
        if not preferences.exists():
            logger.warning(f"Usuario {user.username} no tiene preferencias de canal configuradas")
            return results
        
        for pref in preferences:
            channel_type = pref.channel_type
            
            # Verificar si el canal está disponible
            if channel_type not in self.channels:
                logger.warning(f"Canal {channel_type} no está disponible")
                continue
            
            # Verificar si el usuario quiere recibir este tipo de notificación
            if pref.notify_critical_only and priority != 'critical':
                logger.info(f"Usuario {user.username} solo recibe notificaciones críticas en {channel_type}")
                continue
            
            # Enviar mensaje
            try:
                channel = self.channels[channel_type]
                result = channel.send_message(
                    chat_id=pref.channel_user_id,
                    title=title,
                    message=message
                )
                
                # Registrar en log
                message_log = MessageLog.objects.create(
                    user=user,
                    channel_type=channel_type,
                    title=title,
                    message=message,
                    message_type=message_type,
                    status='SENT' if result['success'] else 'FAILED',
                    error_message=result.get('error', ''),
                    external_message_id=result.get('message_id', ''),
                    related_object_type=related_object_type,
                    related_object_id=related_object_id,
                    sent_at=timezone.now() if result['success'] else None
                )
                
                results[channel_type] = result['success']
                
                # Actualizar estadísticas del canal
                config = ChannelConfig.objects.get(channel_type=channel_type)
                if result['success']:
                    config.messages_sent += 1
                else:
                    config.messages_failed += 1
                config.last_used = timezone.now()
                config.save()
                
                logger.info(f"Mensaje enviado a {user.username} vía {channel_type}: {result['success']}")
            
            except Exception as e:
                logger.error(f"Error al enviar mensaje vía {channel_type}: {str(e)}")
                results[channel_type] = False
        
        return results
    
    def send_notification(
        self,
        user,
        notification_data: Dict,
        priority: str = 'normal'
    ) -> Dict[str, bool]:
        """
        Envía una notificación formateada con acciones interactivas
        
        Args:
            user: Usuario destinatario
            notification_data: Datos de la notificación (title, message, type, actions)
            priority: Prioridad del mensaje
        """
        return self.send_to_user(
            user=user,
            title=notification_data.get('title', ''),
            message=notification_data.get('message', ''),
            message_type=notification_data.get('type', 'notification'),
            priority=priority,
            related_object_type=notification_data.get('related_object_type', ''),
            related_object_id=notification_data.get('related_object_id', '')
        )
    
    def broadcast_to_role(
        self,
        role_name: str,
        title: str,
        message: str,
        message_type: str = 'broadcast',
        priority: str = 'normal'
    ) -> Dict:
        """
        Envía un mensaje a todos los usuarios con un rol específico
        
        Returns:
            Dict con estadísticas: {'total': 10, 'success': 8, 'failed': 2}
        """
        from apps.authentication.models import User, Role
        
        try:
            role = Role.objects.get(name=role_name)
            users = User.objects.filter(role=role, is_active=True)
            
            stats = {'total': 0, 'success': 0, 'failed': 0}
            
            for user in users:
                stats['total'] += 1
                results = self.send_to_user(
                    user=user,
                    title=title,
                    message=message,
                    message_type=message_type,
                    priority=priority
                )
                
                if any(results.values()):
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
            
            logger.info(f"Broadcast a rol {role_name}: {stats}")
            return stats
        
        except Role.DoesNotExist:
            logger.error(f"Rol {role_name} no existe")
            return {'total': 0, 'success': 0, 'failed': 0}
