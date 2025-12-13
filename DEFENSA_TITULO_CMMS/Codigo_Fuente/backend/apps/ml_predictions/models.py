"""
Models for ML predictions and operator skills.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class MLModel(models.Model):
    """
    Stores ML model metadata and artifacts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Model identification
    model_name = models.CharField(max_length=100)
    model_version = models.CharField(max_length=50)
    model_type = models.CharField(max_length=50, default='RANDOM_FOREST')
    
    # Model artifacts (file paths)
    model_file_path = models.CharField(max_length=500)
    scaler_file_path = models.CharField(max_length=500, null=True, blank=True)
    encoder_file_path = models.CharField(max_length=500, null=True, blank=True)
    
    # Training metadata
    training_date = models.DateTimeField(auto_now_add=True)
    training_data_size = models.IntegerField()
    training_duration_seconds = models.FloatField()
    
    # Performance metrics
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    
    # Feature importance (JSON)
    feature_importance = models.JSONField(default=dict)
    
    # Status
    is_active = models.BooleanField(default=False)
    is_production = models.BooleanField(default=False)
    
    # Hyperparameters (JSON)
    hyperparameters = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'ml_models'
        ordering = ['-training_date']
    
    def __str__(self):
        return f"{self.model_name} v{self.model_version}"


class FailurePrediction(models.Model):
    """
    Stores failure predictions for assets.
    """
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='predictions')
    prediction_date = models.DateTimeField(auto_now_add=True)
    
    # Prediction results
    failure_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    predicted_failure_type = models.CharField(max_length=100, blank=True)
    estimated_days_to_failure = models.IntegerField(null=True, blank=True)
    
    # Model metadata
    model_version = models.CharField(max_length=50)
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    # Features used (JSON snapshot)
    features_snapshot = models.JSONField(default=dict)
    
    # Recommendations
    recommended_action = models.TextField(blank=True)
    estimated_repair_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    
    # Outcome tracking
    actual_failure_occurred = models.BooleanField(null=True, blank=True)
    actual_failure_date = models.DateTimeField(null=True, blank=True)
    prediction_accuracy = models.FloatField(null=True, blank=True)
    
    # Actions taken
    work_order_created = models.ForeignKey(
        'work_orders.WorkOrder',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='triggering_prediction'
    )
    notification_sent = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'failure_predictions'
        ordering = ['-prediction_date']
        indexes = [
            models.Index(fields=['asset', '-prediction_date']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['failure_probability']),
        ]
    
    def __str__(self):
        return f"Prediction for {self.asset.name} - {self.risk_level} ({self.failure_probability:.2%})"


class OperatorSkill(models.Model):
    """
    Tracks operator skills and certifications.
    """
    SKILL_CATEGORIES = [
        ('VEHICLE_TYPE', 'Vehicle Type'),
        ('MAINTENANCE_TASK', 'Maintenance Task'),
        ('TOOL', 'Tool/Equipment'),
        ('SAFETY', 'Safety Certification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='skills'
    )
    
    # Skill details
    skill_category = models.CharField(max_length=50, choices=SKILL_CATEGORIES)
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Beginner, 5=Expert"
    )
    
    # Certification
    is_certified = models.BooleanField(default=False)
    certification_number = models.CharField(max_length=100, null=True, blank=True)
    certification_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    # Performance tracking
    tasks_completed = models.IntegerField(default=0)
    average_completion_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Average hours to complete tasks"
    )
    success_rate = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage of successful completions"
    )
    
    # Metadata
    acquired_date = models.DateField(auto_now_add=True)
    last_used_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'operator_skills'
        ordering = ['operator', 'skill_category', 'skill_name']
        unique_together = ['operator', 'skill_category', 'skill_name']
    
    def __str__(self):
        return f"{self.operator.get_full_name()} - {self.skill_name} (Level {self.proficiency_level})"


class OperatorAvailability(models.Model):
    """
    Tracks operator availability and current workload.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='availability'
    )
    
    # Availability
    is_available = models.BooleanField(default=True)
    current_location = models.ForeignKey(
        'assets.Location',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    # Workload
    active_work_orders = models.IntegerField(default=0)
    estimated_hours_remaining = models.FloatField(default=0.0)
    
    # Schedule
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)
    
    # Status
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'operator_availability'
        verbose_name_plural = 'Operator availabilities'
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.operator.get_full_name()} - {status}"


class OperatorPerformance(models.Model):
    """
    Tracks operator performance metrics over time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='performance_records'
    )
    
    # Time period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Metrics
    work_orders_completed = models.IntegerField(default=0)
    total_hours_worked = models.FloatField(default=0.0)
    average_completion_time = models.FloatField(default=0.0)
    success_rate = models.FloatField(default=100.0)
    
    # Quality metrics
    rework_count = models.IntegerField(default=0)
    customer_satisfaction = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    
    # Calculated score
    performance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'operator_performance'
        ordering = ['-period_end']
        unique_together = ['operator', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.operator.get_full_name()} - {self.period_start} to {self.period_end}"
