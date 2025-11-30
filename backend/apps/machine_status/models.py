"""
Machine Status models - AssetStatus and AssetStatusHistory.
"""
from django.db import models
from django.conf import settings
import uuid


class AssetStatus(models.Model):
    """Current status of an asset."""
    
    # Status type choices
    OPERANDO = 'OPERANDO'
    DETENIDA = 'DETENIDA'
    EN_MANTENIMIENTO = 'EN_MANTENIMIENTO'
    FUERA_DE_SERVICIO = 'FUERA_DE_SERVICIO'
    
    STATUS_TYPE_CHOICES = [
        (OPERANDO, 'Operando'),
        (DETENIDA, 'Detenida'),
        (EN_MANTENIMIENTO, 'En Mantenimiento'),
        (FUERA_DE_SERVICIO, 'Fuera de Servicio'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.OneToOneField(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='current_status'
    )
    status_type = models.CharField(
        max_length=50,
        choices=STATUS_TYPE_CHOICES,
        default=OPERANDO
    )
    odometer_reading = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Odometer or hour meter reading'
    )
    fuel_level = models.IntegerField(
        null=True,
        blank=True,
        help_text='Fuel level percentage (0-100)'
    )
    condition_notes = models.TextField(blank=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='asset_status_updates'
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asset_status'
        verbose_name = 'Asset Status'
        verbose_name_plural = 'Asset Statuses'
        indexes = [
            models.Index(fields=['asset']),
            models.Index(fields=['status_type']),
        ]
    
    def __str__(self):
        return f"{self.asset.name} - {self.get_status_type_display()}"
    
    def save(self, *args, **kwargs):
        """Override save to create history record."""
        # Check if this is an update (not a new record)
        if self.pk:
            # Get the old status before saving
            try:
                old_status = AssetStatus.objects.get(pk=self.pk)
                # Create history record
                AssetStatusHistory.objects.create(
                    asset=self.asset,
                    status_type=old_status.status_type,
                    odometer_reading=old_status.odometer_reading,
                    fuel_level=old_status.fuel_level,
                    condition_notes=old_status.condition_notes,
                    updated_by=old_status.last_updated_by,
                    timestamp=old_status.updated_at
                )
            except AssetStatus.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)


class AssetStatusHistory(models.Model):
    """Historical record of asset status changes."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status_type = models.CharField(max_length=50)
    odometer_reading = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    fuel_level = models.IntegerField(null=True, blank=True)
    condition_notes = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='status_history_records'
    )
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asset_status_history'
        verbose_name = 'Asset Status History'
        verbose_name_plural = 'Asset Status Histories'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', '-timestamp']),
            models.Index(fields=['status_type']),
        ]
    
    def __str__(self):
        return f"{self.asset.name} - {self.status_type} at {self.timestamp}"
