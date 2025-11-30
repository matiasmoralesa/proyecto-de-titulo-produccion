"""
Maintenance models.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from apps.core.models import TimeStampedModel
from apps.assets.models import Asset
from apps.authentication.models import User


class MaintenancePlan(TimeStampedModel):
    """Maintenance Plan model for scheduled maintenance tasks."""
    
    # Recurrence Type Choices
    RECURRENCE_DAILY = 'Diario'
    RECURRENCE_WEEKLY = 'Semanal'
    RECURRENCE_MONTHLY = 'Mensual'
    RECURRENCE_QUARTERLY = 'Trimestral'
    RECURRENCE_YEARLY = 'Anual'
    RECURRENCE_HOURS = 'Por Horas'
    RECURRENCE_KILOMETERS = 'Por Kilómetros'
    
    RECURRENCE_CHOICES = [
        (RECURRENCE_DAILY, 'Diario'),
        (RECURRENCE_WEEKLY, 'Semanal'),
        (RECURRENCE_MONTHLY, 'Mensual'),
        (RECURRENCE_QUARTERLY, 'Trimestral'),
        (RECURRENCE_YEARLY, 'Anual'),
        (RECURRENCE_HOURS, 'Por Horas de Uso'),
        (RECURRENCE_KILOMETERS, 'Por Kilómetros'),
    ]
    
    # Status Choices
    STATUS_ACTIVE = 'Activo'
    STATUS_PAUSED = 'Pausado'
    STATUS_COMPLETED = 'Completado'
    STATUS_CANCELLED = 'Cancelado'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_PAUSED, 'Pausado'),
        (STATUS_COMPLETED, 'Completado'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name='maintenance_plans'
    )
    recurrence_type = models.CharField(max_length=50, choices=RECURRENCE_CHOICES)
    recurrence_interval = models.IntegerField(
        default=1,
        help_text='Intervalo de recurrencia (ej: cada 2 semanas, cada 3 meses)'
    )
    
    # For time-based recurrence
    start_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    last_completed_date = models.DateField(null=True, blank=True)
    
    # For usage-based recurrence (hours or kilometers)
    usage_threshold = models.IntegerField(
        null=True,
        blank=True,
        help_text='Umbral de uso para mantenimiento (horas o kilómetros)'
    )
    last_usage_value = models.IntegerField(
        null=True,
        blank=True,
        help_text='Último valor de uso registrado'
    )
    
    # Additional fields
    estimated_duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Duración estimada del mantenimiento en horas'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_maintenance_plans'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null=True, blank=True)
    paused_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paused_maintenance_plans'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_maintenance_plans'
    )
    
    class Meta:
        db_table = 'maintenance_plans'
        verbose_name = 'Maintenance Plan'
        verbose_name_plural = 'Maintenance Plans'
        ordering = ['next_due_date', '-created_at']
        indexes = [
            models.Index(fields=['asset']),
            models.Index(fields=['status']),
            models.Index(fields=['next_due_date']),
            models.Index(fields=['recurrence_type']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.asset.name}"
    
    def save(self, *args, **kwargs):
        """Calculate next due date on save if not set."""
        if not self.next_due_date and not self.is_usage_based():
            self.next_due_date = self.calculate_next_due_date()
        super().save(*args, **kwargs)
    
    def is_usage_based(self):
        """Check if this is a usage-based maintenance plan."""
        return self.recurrence_type in [
            self.RECURRENCE_HOURS,
            self.RECURRENCE_KILOMETERS
        ]
    
    def calculate_next_due_date(self, from_date=None):
        """
        Calculate the next due date based on recurrence type and interval.
        
        Args:
            from_date: Date to calculate from (defaults to last_completed_date or start_date)
        
        Returns:
            Next due date
        """
        if self.is_usage_based():
            # Usage-based plans don't have a specific due date
            return None
        
        # Determine the base date
        if from_date:
            base_date = from_date
        elif self.last_completed_date:
            base_date = self.last_completed_date
        else:
            base_date = self.start_date
        
        # Calculate next date based on recurrence type
        if self.recurrence_type == self.RECURRENCE_DAILY:
            next_date = base_date + timedelta(days=self.recurrence_interval)
        
        elif self.recurrence_type == self.RECURRENCE_WEEKLY:
            next_date = base_date + timedelta(weeks=self.recurrence_interval)
        
        elif self.recurrence_type == self.RECURRENCE_MONTHLY:
            next_date = base_date + relativedelta(months=self.recurrence_interval)
        
        elif self.recurrence_type == self.RECURRENCE_QUARTERLY:
            next_date = base_date + relativedelta(months=3 * self.recurrence_interval)
        
        elif self.recurrence_type == self.RECURRENCE_YEARLY:
            next_date = base_date + relativedelta(years=self.recurrence_interval)
        
        else:
            next_date = base_date
        
        return next_date
    
    def is_due(self):
        """Check if maintenance is due."""
        if self.is_paused or self.status != self.STATUS_ACTIVE:
            return False
        
        if self.is_usage_based():
            # Check if usage threshold is reached
            if self.usage_threshold and self.last_usage_value:
                return self.last_usage_value >= self.usage_threshold
            return False
        else:
            # Check if due date has passed
            if self.next_due_date:
                return self.next_due_date <= timezone.now().date()
            return False
    
    def is_overdue(self):
        """Check if maintenance is overdue."""
        if not self.is_due():
            return False
        
        if self.is_usage_based():
            # For usage-based, check if significantly over threshold
            if self.usage_threshold and self.last_usage_value:
                return self.last_usage_value > (self.usage_threshold * 1.1)  # 10% over
            return False
        else:
            # For time-based, check if past due date
            if self.next_due_date:
                return self.next_due_date < timezone.now().date()
            return False
    
    def pause(self, user):
        """Pause the maintenance plan."""
        self.is_paused = True
        self.status = self.STATUS_PAUSED
        self.paused_at = timezone.now()
        self.paused_by = user
        self.save()
    
    def resume(self):
        """Resume the maintenance plan."""
        self.is_paused = False
        self.status = self.STATUS_ACTIVE
        self.paused_at = None
        self.paused_by = None
        self.save()
    
    def complete_maintenance(self, completion_date=None, usage_value=None):
        """
        Mark maintenance as completed and calculate next due date.
        
        Args:
            completion_date: Date of completion (defaults to today)
            usage_value: Current usage value for usage-based plans
        """
        if not completion_date:
            completion_date = timezone.now().date()
        
        self.last_completed_date = completion_date
        
        if self.is_usage_based() and usage_value is not None:
            self.last_usage_value = usage_value
        else:
            # Calculate next due date for time-based plans
            self.next_due_date = self.calculate_next_due_date(from_date=completion_date)
        
        self.save()
    
    def update_usage(self, current_usage):
        """
        Update the current usage value for usage-based plans.
        
        Args:
            current_usage: Current usage value (hours or kilometers)
        """
        if self.is_usage_based():
            self.last_usage_value = current_usage
            self.save()
    
    def days_until_due(self):
        """Get number of days until maintenance is due."""
        if self.is_usage_based() or not self.next_due_date:
            return None
        
        delta = self.next_due_date - timezone.now().date()
        return delta.days
    
    def usage_until_due(self):
        """Get usage remaining until maintenance is due (for usage-based plans)."""
        if not self.is_usage_based() or not self.usage_threshold:
            return None
        
        if self.last_usage_value is None:
            return self.usage_threshold
        
        return max(0, self.usage_threshold - self.last_usage_value)
