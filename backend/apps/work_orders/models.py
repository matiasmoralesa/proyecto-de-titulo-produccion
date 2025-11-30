"""
Work Order models.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.assets.models import Asset
from apps.authentication.models import User
from apps.core.utils import generate_unique_code


class WorkOrder(TimeStampedModel):
    """Work Order model for maintenance tasks."""
    
    # Priority Choices
    PRIORITY_LOW = 'Baja'
    PRIORITY_MEDIUM = 'Media'
    PRIORITY_HIGH = 'Alta'
    PRIORITY_URGENT = 'Urgente'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Baja'),
        (PRIORITY_MEDIUM, 'Media'),
        (PRIORITY_HIGH, 'Alta'),
        (PRIORITY_URGENT, 'Urgente'),
    ]
    
    # Status Choices
    STATUS_PENDING = 'Pendiente'
    STATUS_IN_PROGRESS = 'En Progreso'
    STATUS_COMPLETED = 'Completada'
    STATUS_CANCELLED = 'Cancelada'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_IN_PROGRESS, 'En Progreso'),
        (STATUS_COMPLETED, 'Completada'),
        (STATUS_CANCELLED, 'Cancelada'),
    ]
    
    work_order_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_PENDING)
    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name='work_orders'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_work_orders'
    )
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_work_orders'
    )
    
    class Meta:
        db_table = 'work_orders'
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['work_order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['scheduled_date']),
        ]
    
    def __str__(self):
        return f"{self.work_order_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Generate work order number on creation."""
        if not self.work_order_number:
            self.work_order_number = generate_unique_code('WO', WorkOrder, 'work_order_number')
        super().save(*args, **kwargs)
    
    def can_transition_to(self, new_status):
        """Check if status transition is valid."""
        valid_transitions = {
            self.STATUS_PENDING: [self.STATUS_IN_PROGRESS, self.STATUS_CANCELLED],
            self.STATUS_IN_PROGRESS: [self.STATUS_COMPLETED, self.STATUS_CANCELLED],
            self.STATUS_COMPLETED: [],
            self.STATUS_CANCELLED: [],
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def complete(self, completion_notes, actual_hours):
        """Complete the work order."""
        from django.utils import timezone
        
        if not completion_notes:
            raise ValueError("Completion notes are required")
        if not actual_hours:
            raise ValueError("Actual hours are required")
        
        self.status = self.STATUS_COMPLETED
        self.completed_date = timezone.now()
        self.completion_notes = completion_notes
        self.actual_hours = actual_hours
        self.save()
