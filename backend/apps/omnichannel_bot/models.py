"""
Modelos para el sistema de bot omnicanal
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class ChannelConfig(models.Model):
    """
    Configuración de canales de comunicación
    """
    CHANNEL_TYPES = [
        ('TELEGRAM', 'Telegram'),
        ('WHATSAPP', 'WhatsApp'),
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('IN_APP', 'In-App'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES, unique=True)
    is_enabled = models.BooleanField(default=False)
    
    # Configuración específica del canal (JSON)
    config = models.JSONField(default=dict, help_text="Configuración específica del canal")
    
    # Estadísticas
    messages_sent = models.IntegerField(default=0)
    messages_failed = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'channel_configs'
        verbose_name = 'Channel Configuration'
        verbose_name_plural = 'Channel Configurations'
    
    def __str__(self):
        status = "Enabled" if self.is_enabled else "Disabled"
        return f"{self.get_channel_type_display()} - {status}"


class UserChannelPreference(models.Model):
    """
    Preferencias de canal por usuario
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='channel_preferences')
    channel_type = models.CharField(max_length=20, choices=ChannelConfig.CHANNEL_TYPES)
    is_enabled = models.BooleanField(default=True)
    
    # Identificador del usuario en el canal (ej: telegram_id, phone_number, email)
    channel_user_id = models.CharField(max_length=200, blank=True)
    
    # Preferencias de notificación
    notify_work_orders = models.BooleanField(default=True)
    notify_predictions = models.BooleanField(default=True)
    notify_critical_only = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_channel_preferences'
        unique_together = ['user', 'channel_type']
        verbose_name = 'User Channel Preference'
        verbose_name_plural = 'User Channel Preferences'
    
    def __str__(self):
        return f"{self.user.username} - {self.channel_type}"


class MessageLog(models.Model):
    """
    Registro de mensajes enviados
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('READ', 'Read'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='messages')
    channel_type = models.CharField(max_length=20, choices=ChannelConfig.CHANNEL_TYPES)
    
    # Contenido del mensaje
    title = models.CharField(max_length=200)
    message = models.TextField()
    message_type = models.CharField(max_length=50)
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True)
    
    # Metadata
    external_message_id = models.CharField(max_length=200, blank=True, help_text="ID del mensaje en el canal externo")
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'message_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['channel_type', 'status']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.channel_type} - {self.user.username} - {self.status}"
