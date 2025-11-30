"""
Models for checklists app.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.authentication.models import User
from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder


class ChecklistTemplate(models.Model):
    """
    Model representing a checklist template.
    System templates are predefined and cannot be modified or deleted.
    """
    # Vehicle Types (matching Asset model)
    VEHICLE_TYPE_SUPERSUCKER = 'CAMION_SUPERSUCKER'
    VEHICLE_TYPE_CAMIONETA = 'CAMIONETA_MDO'
    VEHICLE_TYPE_RETROEXCAVADORA = 'RETROEXCAVADORA_MDO'
    VEHICLE_TYPE_CARGADOR = 'CARGADOR_FRONTAL_MDO'
    VEHICLE_TYPE_MINICARGADOR = 'MINICARGADOR_MDO'
    
    VEHICLE_TYPES = [
        (VEHICLE_TYPE_SUPERSUCKER, 'Camión Supersucker'),
        (VEHICLE_TYPE_CAMIONETA, 'Camioneta MDO'),
        (VEHICLE_TYPE_RETROEXCAVADORA, 'Retroexcavadora MDO'),
        (VEHICLE_TYPE_CARGADOR, 'Cargador Frontal MDO'),
        (VEHICLE_TYPE_MINICARGADOR, 'Minicargador MDO'),
    ]
    
    # Basic Information
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    vehicle_type = models.CharField(
        max_length=50,
        choices=VEHICLE_TYPES,
        verbose_name='Tipo de Vehículo'
    )
    
    # Template Configuration
    is_system_template = models.BooleanField(
        default=False,
        verbose_name='Plantilla del Sistema'
    )
    passing_score = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Puntuación Mínima (%)'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checklist_templates_created',
        verbose_name='Creado Por'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        db_table = 'checklist_templates'
        verbose_name = 'Plantilla de Checklist'
        verbose_name_plural = 'Plantillas de Checklists'
        ordering = ['vehicle_type', 'code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['vehicle_type']),
            models.Index(fields=['is_system_template']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def total_items(self):
        """Get total number of items in this template."""
        return self.items.count()
    
    def required_items_count(self):
        """Get count of required items."""
        return self.items.filter(required=True).count()


class ChecklistTemplateItem(models.Model):
    """
    Model representing an item in a checklist template.
    """
    # Response Types
    RESPONSE_YES_NO_NA = 'yes_no_na'
    RESPONSE_TEXT = 'text'
    RESPONSE_NUMERIC = 'numeric'
    RESPONSE_PHOTO = 'photo'
    
    RESPONSE_TYPES = [
        (RESPONSE_YES_NO_NA, 'Sí / No / No Aplica'),
        (RESPONSE_TEXT, 'Texto Libre'),
        (RESPONSE_NUMERIC, 'Valor Numérico'),
        (RESPONSE_PHOTO, 'Foto Requerida'),
    ]
    
    # Related Template
    template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Plantilla'
    )
    
    # Item Information
    section = models.CharField(max_length=200, verbose_name='Sección')
    order = models.IntegerField(verbose_name='Orden')
    question = models.TextField(verbose_name='Pregunta')
    response_type = models.CharField(
        max_length=20,
        choices=RESPONSE_TYPES,
        default=RESPONSE_YES_NO_NA,
        verbose_name='Tipo de Respuesta'
    )
    
    # Configuration
    required = models.BooleanField(default=True, verbose_name='Requerido')
    observations_allowed = models.BooleanField(
        default=True,
        verbose_name='Permite Observaciones'
    )
    
    class Meta:
        db_table = 'checklist_template_items'
        verbose_name = 'Item de Plantilla'
        verbose_name_plural = 'Items de Plantilla'
        ordering = ['template', 'order']
        indexes = [
            models.Index(fields=['template', 'order']),
        ]
    
    def __str__(self):
        return f"{self.template.code} - {self.order}. {self.question[:50]}"


class ChecklistResponse(models.Model):
    """
    Model representing a completed checklist.
    """
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    
    STATUSES = [
        (STATUS_IN_PROGRESS, 'En Progreso'),
        (STATUS_COMPLETED, 'Completado'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_REJECTED, 'Rechazado'),
    ]
    
    # Related Objects
    template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.PROTECT,
        related_name='responses',
        verbose_name='Plantilla'
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='checklist_responses',
        verbose_name='Activo'
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checklist_responses',
        verbose_name='Orden de Trabajo'
    )
    
    # Response Information
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checklist_responses_completed',
        verbose_name='Completado Por'
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Completado')
    
    # Scoring
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Puntuación (%)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=STATUS_IN_PROGRESS,
        verbose_name='Estado'
    )
    
    # Digital Signature
    signature_data = models.TextField(blank=True, verbose_name='Firma Digital')
    
    # PDF Generation
    pdf_file = models.FileField(
        upload_to='checklists/pdfs/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Archivo PDF'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        db_table = 'checklist_responses'
        verbose_name = 'Respuesta de Checklist'
        verbose_name_plural = 'Respuestas de Checklists'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset', '-created_at']),
            models.Index(fields=['work_order']),
            models.Index(fields=['completed_by']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.template.code} - {self.asset} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def calculate_score(self):
        """Calculate the score based on responses."""
        total_items = self.item_responses.count()
        if total_items == 0:
            return 0
        
        # Count items that passed (yes or na)
        passed_items = self.item_responses.filter(
            models.Q(response_value='yes') | models.Q(response_value='na')
        ).count()
        
        score = (passed_items / total_items) * 100
        return round(score, 2)
    
    def update_score_and_status(self):
        """Update score and status based on responses."""
        self.score = self.calculate_score()
        
        if self.status == self.STATUS_IN_PROGRESS:
            # Check if all required items are answered
            required_items = self.template.items.filter(required=True).count()
            answered_required = self.item_responses.filter(
                template_item__required=True
            ).exclude(response_value='').count()
            
            if answered_required >= required_items:
                self.status = self.STATUS_COMPLETED
                self.completed_at = timezone.now()
                
                # Determine if approved or rejected
                if self.score >= self.template.passing_score:
                    self.status = self.STATUS_APPROVED
                else:
                    self.status = self.STATUS_REJECTED
        
        self.save()
    
    def completion_percentage(self):
        """Calculate completion percentage."""
        total_items = self.template.total_items()
        if total_items == 0:
            return 0
        
        answered_items = self.item_responses.exclude(response_value='').count()
        return round((answered_items / total_items) * 100, 2)


class ChecklistItemResponse(models.Model):
    """
    Model representing a response to a checklist item.
    """
    # Related Objects
    checklist_response = models.ForeignKey(
        ChecklistResponse,
        on_delete=models.CASCADE,
        related_name='item_responses',
        verbose_name='Respuesta de Checklist'
    )
    template_item = models.ForeignKey(
        ChecklistTemplateItem,
        on_delete=models.PROTECT,
        related_name='responses',
        verbose_name='Item de Plantilla'
    )
    
    # Response Data
    response_value = models.CharField(max_length=50, blank=True, verbose_name='Valor de Respuesta')
    observations = models.TextField(blank=True, verbose_name='Observaciones')
    photo = models.ImageField(
        upload_to='checklists/photos/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='Foto'
    )
    
    # Metadata
    answered_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Respuesta')
    
    class Meta:
        db_table = 'checklist_item_responses'
        verbose_name = 'Respuesta de Item'
        verbose_name_plural = 'Respuestas de Items'
        ordering = ['checklist_response', 'template_item__order']
        unique_together = ['checklist_response', 'template_item']
        indexes = [
            models.Index(fields=['checklist_response']),
        ]
    
    def __str__(self):
        return f"{self.checklist_response} - {self.template_item.order}"
