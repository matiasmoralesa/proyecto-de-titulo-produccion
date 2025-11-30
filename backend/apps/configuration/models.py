"""
Models for configuration and master data management.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.authentication.models import User


class AssetCategory(TimeStampedModel):
    """
    Model representing an asset category for classification.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asset_categories_created',
        verbose_name='Creado Por'
    )
    
    class Meta:
        db_table = 'asset_categories'
        verbose_name = 'Categoría de Activo'
        verbose_name_plural = 'Categorías de Activos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def can_delete(self):
        """Check if category can be deleted (not referenced by any asset)."""
        # This would check if any assets use this category
        # For now, we'll implement a simple check
        return not hasattr(self, 'assets') or self.assets.count() == 0


class Priority(TimeStampedModel):
    """
    Model representing priority levels for work orders and tasks.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    level = models.IntegerField(unique=True, verbose_name='Nivel')  # 1=Highest, 5=Lowest
    color_code = models.CharField(max_length=7, default='#000000', verbose_name='Código de Color')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='priorities_created',
        verbose_name='Creado Por'
    )
    
    class Meta:
        db_table = 'priorities'
        verbose_name = 'Prioridad'
        verbose_name_plural = 'Prioridades'
        ordering = ['level']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} (Nivel {self.level})"
    
    def can_delete(self):
        """Check if priority can be deleted (not referenced by any work order)."""
        return not hasattr(self, 'work_orders') or self.work_orders.count() == 0


class WorkOrderType(TimeStampedModel):
    """
    Model representing types of work orders.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    requires_approval = models.BooleanField(default=False, verbose_name='Requiere Aprobación')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='work_order_types_created',
        verbose_name='Creado Por'
    )
    
    class Meta:
        db_table = 'work_order_types'
        verbose_name = 'Tipo de Orden de Trabajo'
        verbose_name_plural = 'Tipos de Órdenes de Trabajo'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def can_delete(self):
        """Check if type can be deleted (not referenced by any work order)."""
        return not hasattr(self, 'work_orders') or self.work_orders.count() == 0


class SystemParameter(TimeStampedModel):
    """
    Model representing system configuration parameters.
    """
    key = models.CharField(max_length=100, unique=True, verbose_name='Clave')
    value = models.TextField(verbose_name='Valor')
    description = models.TextField(blank=True, verbose_name='Descripción')
    data_type = models.CharField(
        max_length=20,
        choices=[
            ('string', 'Texto'),
            ('integer', 'Entero'),
            ('float', 'Decimal'),
            ('boolean', 'Booleano'),
            ('json', 'JSON'),
        ],
        default='string',
        verbose_name='Tipo de Dato'
    )
    is_editable = models.BooleanField(default=True, verbose_name='Editable')
    
    # Audit fields
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='system_parameters_modified',
        verbose_name='Modificado Por'
    )
    
    class Meta:
        db_table = 'system_parameters'
        verbose_name = 'Parámetro del Sistema'
        verbose_name_plural = 'Parámetros del Sistema'
        ordering = ['key']
        indexes = [
            models.Index(fields=['key']),
        ]
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    
    def get_typed_value(self):
        """Return the value converted to its proper type."""
        if self.data_type == 'integer':
            return int(self.value)
        elif self.data_type == 'float':
            return float(self.value)
        elif self.data_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes')
        elif self.data_type == 'json':
            import json
            return json.loads(self.value)
        return self.value


class AuditLog(models.Model):
    """
    Model for tracking configuration changes and important system events.
    """
    ACTION_CREATE = 'CREATE'
    ACTION_UPDATE = 'UPDATE'
    ACTION_DELETE = 'DELETE'
    
    ACTION_CHOICES = [
        (ACTION_CREATE, 'Crear'),
        (ACTION_UPDATE, 'Actualizar'),
        (ACTION_DELETE, 'Eliminar'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name='Usuario'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
    model_name = models.CharField(max_length=100, verbose_name='Modelo')
    object_id = models.CharField(max_length=255, verbose_name='ID del Objeto')
    object_repr = models.CharField(max_length=255, verbose_name='Representación del Objeto')
    changes = models.JSONField(default=dict, verbose_name='Cambios')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['model_name']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} - {self.model_name}"
