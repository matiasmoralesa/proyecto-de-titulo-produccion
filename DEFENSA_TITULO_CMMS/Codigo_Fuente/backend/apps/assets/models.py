"""
Asset models - Location, Asset, AssetDocument.
"""
import uuid
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel
from apps.authentication.models import User
from .validators import validate_document_file


class Location(models.Model):
    """Location model for asset physical locations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    coordinates = models.CharField(max_length=100, blank=True, help_text="Lat,Long format")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Asset(TimeStampedModel):
    """Asset model for vehicles and equipment."""
    
    # Vehicle Type Choices
    CAMION_SUPERSUCKER = 'Camión Supersucker'
    CAMIONETA_MDO = 'Camioneta MDO'
    RETROEXCAVADORA_MDO = 'Retroexcavadora MDO'
    CARGADOR_FRONTAL_MDO = 'Cargador Frontal MDO'
    MINICARGADOR_MDO = 'Minicargador MDO'
    
    VEHICLE_TYPE_CHOICES = [
        (CAMION_SUPERSUCKER, 'Camión Supersucker'),
        (CAMIONETA_MDO, 'Camioneta MDO'),
        (RETROEXCAVADORA_MDO, 'Retroexcavadora MDO'),
        (CARGADOR_FRONTAL_MDO, 'Cargador Frontal MDO'),
        (MINICARGADOR_MDO, 'Minicargador MDO'),
    ]
    
    # Status Choices
    STATUS_OPERANDO = 'Operando'
    STATUS_DETENIDA = 'Detenida'
    STATUS_EN_MANTENIMIENTO = 'En Mantenimiento'
    STATUS_FUERA_SERVICIO = 'Fuera de Servicio'
    
    STATUS_CHOICES = [
        (STATUS_OPERANDO, 'Operando'),
        (STATUS_DETENIDA, 'Detenida'),
        (STATUS_EN_MANTENIMIENTO, 'En Mantenimiento'),
        (STATUS_FUERA_SERVICIO, 'Fuera de Servicio'),
    ]
    
    name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9\-]+$',
                message='Serial number must contain only uppercase letters, numbers, and hyphens'
            )
        ]
    )
    license_plate = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9\-]+$',
                message='License plate must contain only uppercase letters, numbers, and hyphens'
            )
        ]
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='assets'
    )
    installation_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_OPERANDO
    )
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_assets'
    )
    
    class Meta:
        db_table = 'assets'
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['license_plate']),
            models.Index(fields=['vehicle_type']),
            models.Index(fields=['status']),
            models.Index(fields=['is_archived']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
    def soft_delete(self):
        """Soft delete the asset by archiving it."""
        self.is_archived = True
        self.save()


class AssetDocument(TimeStampedModel):
    """Document attachments for assets."""
    
    DOCUMENT_TYPE_CHOICES = [
        ('manual', 'Manual'),
        ('certificate', 'Certificado'),
        ('invoice', 'Factura'),
        ('photo', 'Fotografía'),
        ('other', 'Otro'),
    ]
    
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=200)
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other'
    )
    file = models.FileField(
        upload_to='assets/documents/%Y/%m/',
        validators=[validate_document_file]
    )
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='uploaded_documents'
    )
    
    class Meta:
        db_table = 'asset_documents'
        verbose_name = 'Asset Document'
        verbose_name_plural = 'Asset Documents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.asset.name}"
