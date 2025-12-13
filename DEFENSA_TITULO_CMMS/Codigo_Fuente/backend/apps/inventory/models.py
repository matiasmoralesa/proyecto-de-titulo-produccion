"""
Models for inventory management.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.authentication.models import User


class SparePart(models.Model):
    """
    Model representing a spare part in inventory.
    """
    # Basic Information
    part_number = models.CharField(max_length=100, unique=True, verbose_name='Número de Parte')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    # Category and Classification
    category = models.CharField(max_length=100, blank=True, verbose_name='Categoría')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='Fabricante')
    
    # Stock Information
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad en Stock'
    )
    min_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad Mínima'
    )
    unit_of_measure = models.CharField(
        max_length=50,
        default='unidad',
        verbose_name='Unidad de Medida'
    )
    
    # Pricing
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Costo Unitario'
    )
    
    # Location
    storage_location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación de Almacenamiento'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spare_parts_created',
        verbose_name='Creado Por'
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        db_table = 'spare_parts'
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['part_number']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.part_number} - {self.name}"
    
    def is_low_stock(self):
        """Check if the spare part is below minimum quantity."""
        return self.quantity <= self.min_quantity
    
    def stock_status(self):
        """Return stock status as a string."""
        if self.quantity == 0:
            return 'Sin Stock'
        elif self.is_low_stock():
            return 'Stock Bajo'
        else:
            return 'Stock Normal'
    
    def total_value(self):
        """Calculate total value of stock."""
        return self.quantity * self.unit_cost
    
    def adjust_stock(self, quantity_change, movement_type, user, notes=''):
        """
        Adjust stock quantity and create a stock movement record.
        
        Args:
            quantity_change: Positive for additions, negative for removals
            movement_type: Type of movement (see StockMovement.MOVEMENT_TYPES)
            user: User performing the adjustment
            notes: Optional notes about the movement
        
        Returns:
            StockMovement instance
        
        Raises:
            ValueError: If adjustment would result in negative quantity
        """
        new_quantity = self.quantity + quantity_change
        
        if new_quantity < 0:
            raise ValueError(
                f"No se puede ajustar el stock. "
                f"Cantidad actual: {self.quantity}, "
                f"Cambio solicitado: {quantity_change}"
            )
        
        old_quantity = self.quantity
        self.quantity = new_quantity
        self.save()
        
        # Create stock movement record
        movement = StockMovement.objects.create(
            spare_part=self,
            movement_type=movement_type,
            quantity=abs(quantity_change),
            quantity_before=old_quantity,
            quantity_after=new_quantity,
            unit_cost=self.unit_cost,
            user=user,
            notes=notes
        )
        
        return movement


class StockMovement(models.Model):
    """
    Model representing a stock movement for audit trail.
    """
    # Movement Types
    MOVEMENT_IN = 'IN'
    MOVEMENT_OUT = 'OUT'
    MOVEMENT_ADJUSTMENT = 'ADJUSTMENT'
    MOVEMENT_RETURN = 'RETURN'
    MOVEMENT_TRANSFER = 'TRANSFER'
    MOVEMENT_INITIAL = 'INITIAL'
    
    MOVEMENT_TYPES = [
        (MOVEMENT_IN, 'Entrada'),
        (MOVEMENT_OUT, 'Salida'),
        (MOVEMENT_ADJUSTMENT, 'Ajuste'),
        (MOVEMENT_RETURN, 'Devolución'),
        (MOVEMENT_TRANSFER, 'Transferencia'),
        (MOVEMENT_INITIAL, 'Inventario Inicial'),
    ]
    
    # Related Objects
    spare_part = models.ForeignKey(
        SparePart,
        on_delete=models.CASCADE,
        related_name='stock_movements',
        verbose_name='Repuesto'
    )
    
    # Movement Details
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
        verbose_name='Tipo de Movimiento'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad'
    )
    quantity_before = models.IntegerField(
        verbose_name='Cantidad Anterior'
    )
    quantity_after = models.IntegerField(
        verbose_name='Cantidad Posterior'
    )
    
    # Cost Information
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Costo Unitario'
    )
    
    # Reference Information
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Tipo de Referencia'
    )
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID de Referencia'
    )
    
    # Additional Information
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    # Metadata
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='stock_movements',
        verbose_name='Usuario'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Movimiento')
    
    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['spare_part', '-created_at']),
            models.Index(fields=['movement_type']),
            models.Index(fields=['user']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.spare_part.name} - {self.quantity}"
    
    def total_cost(self):
        """Calculate total cost of this movement."""
        return self.quantity * self.unit_cost
