"""
Clase base para canales de comunicación
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseChannel(ABC):
    """
    Interfaz base para todos los canales de comunicación
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.is_configured = self.validate_config()
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Valida que la configuración del canal sea correcta"""
        pass
    
    @abstractmethod
    def send_message(self, user_id: str, title: str, message: str, **kwargs) -> Dict:
        """
        Envía un mensaje a través del canal
        
        Returns:
            Dict con 'success': bool, 'message_id': str, 'error': str (opcional)
        """
        pass
    
    @abstractmethod
    def send_notification(self, user_id: str, notification_data: Dict) -> Dict:
        """Envía una notificación formateada"""
        pass
    
    def format_message(self, title: str, message: str) -> str:
        """Formatea el mensaje según el canal"""
        return f"*{title}*\n\n{message}"
