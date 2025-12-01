"""
Canal de Telegram para el bot omnicanal
"""
import requests
from typing import Dict, Optional
from .base import BaseChannel
import logging

logger = logging.getLogger(__name__)


class TelegramChannel(BaseChannel):
    """
    Canal de comunicación vía Telegram Bot API
    """
    
    def __init__(self, config: Dict):
        self.bot_token = config.get('bot_token', '')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        super().__init__(config)
    
    def validate_config(self) -> bool:
        """Valida que el token del bot sea válido"""
        if not self.bot_token:
            logger.error("Telegram bot token no configurado")
            return False
        
        try:
            response = requests.get(f"{self.api_url}/getMe", timeout=5)
            if response.status_code == 200:
                bot_info = response.json()
                logger.info(f"Bot de Telegram conectado: {bot_info.get('result', {}).get('username')}")
                return True
            else:
                logger.error(f"Error al validar bot de Telegram: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error al conectar con Telegram: {str(e)}")
            return False
    
    def send_message(self, chat_id: str, title: str, message: str, **kwargs) -> Dict:
        """
        Envía un mensaje de texto a través de Telegram
        
        Args:
            chat_id: ID del chat de Telegram
            title: Título del mensaje
            message: Contenido del mensaje
            **kwargs: Parámetros adicionales (parse_mode, reply_markup, etc.)
        
        Returns:
            Dict con resultado del envío
        """
        logger.info(f"[TELEGRAM] Intentando enviar mensaje a chat_id: {chat_id}")
        logger.info(f"[TELEGRAM] Bot token configurado: {bool(self.bot_token)}")
        logger.info(f"[TELEGRAM] Canal configurado: {self.is_configured}")
        
        if not self.is_configured:
            logger.error("[TELEGRAM] Canal no configurado correctamente")
            return {
                'success': False,
                'error': 'Canal de Telegram no configurado correctamente'
            }
        
        formatted_message = self.format_message(title, message)
        logger.info(f"[TELEGRAM] Mensaje formateado (primeros 100 chars): {formatted_message[:100]}")
        
        payload = {
            'chat_id': chat_id,
            'text': formatted_message,
            'parse_mode': kwargs.get('parse_mode', 'Markdown'),
        }
        
        # Agregar teclado inline si se proporciona
        if 'reply_markup' in kwargs:
            payload['reply_markup'] = kwargs['reply_markup']
            logger.info(f"[TELEGRAM] Botones agregados: {len(kwargs['reply_markup'].get('inline_keyboard', []))} filas")
        
        logger.info(f"[TELEGRAM] URL de API: {self.api_url}/sendMessage")
        logger.info(f"[TELEGRAM] Payload: {payload}")
        
        try:
            logger.info("[TELEGRAM] Enviando petición POST a Telegram API...")
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json=payload,
                timeout=10
            )
            
            logger.info(f"[TELEGRAM] Status code de respuesta: {response.status_code}")
            logger.info(f"[TELEGRAM] Respuesta completa: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"[TELEGRAM] ✅ Mensaje enviado exitosamente. Message ID: {result['result']['message_id']}")
                return {
                    'success': True,
                    'message_id': str(result['result']['message_id']),
                    'chat_id': str(result['result']['chat']['id'])
                }
            else:
                error_msg = response.json().get('description', 'Error desconocido')
                logger.error(f"[TELEGRAM] ❌ Error al enviar mensaje: {error_msg}")
                logger.error(f"[TELEGRAM] Respuesta completa: {response.text}")
                return {
                    'success': False,
                    'error': error_msg
                }
        
        except requests.exceptions.Timeout:
            logger.error("[TELEGRAM] ❌ Timeout al enviar mensaje a Telegram API")
            return {
                'success': False,
                'error': 'Timeout al conectar con Telegram'
            }
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[TELEGRAM] ❌ Error de conexión: {str(e)}")
            return {
                'success': False,
                'error': f'Error de conexión: {str(e)}'
            }
        except Exception as e:
            logger.error(f"[TELEGRAM] ❌ Excepción al enviar mensaje: {str(e)}")
            import traceback
            logger.error(f"[TELEGRAM] Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_notification(self, chat_id: str, notification_data: Dict) -> Dict:
        """
        Envía una notificación formateada con botones interactivos
        
        Args:
            chat_id: ID del chat de Telegram
            notification_data: Datos de la notificación
        """
        title = notification_data.get('title', 'Notificación')
        message = notification_data.get('message', '')
        notification_type = notification_data.get('type', 'info')
        
        # Agregar emoji según el tipo
        emoji_map = {
            'work_order_assigned': '📋',
            'critical_alert': '🚨',
            'prediction_high_risk': '⚠️',
            'maintenance_reminder': '🔧',
            'info': 'ℹ️'
        }
        
        emoji = emoji_map.get(notification_type, 'ℹ️')
        title = f"{emoji} {title}"
        
        # Crear botones inline si hay acciones
        reply_markup = None
        if 'actions' in notification_data:
            buttons = []
            for action in notification_data['actions']:
                buttons.append([{
                    'text': action['text'],
                    'callback_data': action['callback_data']
                }])
            reply_markup = {'inline_keyboard': buttons}
        
        return self.send_message(
            chat_id=chat_id,
            title=title,
            message=message,
            reply_markup=reply_markup
        )
    
    def format_message(self, title: str, message: str) -> str:
        """Formatea el mensaje para Telegram con Markdown"""
        if title:
            return f"*{title}*\n\n{message}"
        return message
    
    def send_document(self, chat_id: str, document_path: str, caption: str = "") -> Dict:
        """Envía un documento (PDF, imagen, etc.)"""
        if not self.is_configured:
            return {'success': False, 'error': 'Canal no configurado'}
        
        try:
            with open(document_path, 'rb') as doc:
                files = {'document': doc}
                data = {
                    'chat_id': chat_id,
                    'caption': caption
                }
                
                response = requests.post(
                    f"{self.api_url}/sendDocument",
                    data=data,
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        'success': True,
                        'message_id': str(result['result']['message_id'])
                    }
                else:
                    return {
                        'success': False,
                        'error': response.json().get('description', 'Error desconocido')
                    }
        
        except Exception as e:
            logger.error(f"Error al enviar documento: {str(e)}")
            return {'success': False, 'error': str(e)}
