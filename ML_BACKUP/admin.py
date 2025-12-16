"""
Admin configuration for ML predictions.
"""
from django.contrib import admin
from .models import MLModel, FailurePrediction, OperatorSkill, OperatorAvailability, OperatorPerformance


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    """Admin for ML models."""
    list_display = ['model_name', 'model_version', 'training_date', 'accuracy', 'is_active', 'is_production']
    list_filter = ['is_active', 'is_production', 'model_type', 'training_date']
    search_fields = ['model_name', 'model_version']
    readonly_fields = ['id', 'training_date']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('id', 'model_name', 'model_version', 'model_type')
        }),
        ('Files', {
            'fields': ('model_file_path', 'scaler_file_path', 'encoder_file_path')
        }),
        ('Training Metadata', {
            'fields': ('training_date', 'training_data_size', 'training_duration_seconds')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score', 'feature_importance')
        }),
        ('Status', {
            'fields': ('is_active', 'is_production')
        }),
        ('Configuration', {
            'fields': ('hyperparameters',)
        }),
    )


@admin.register(FailurePrediction)
class FailurePredictionAdmin(admin.ModelAdmin):
    """Admin for failure predictions."""
    list_display = ['asset', 'prediction_date', 'risk_level', 'failure_probability', 'notification_sent']
    list_filter = ['risk_level', 'prediction_date', 'notification_sent', 'actual_failure_occurred']
    search_fields = ['asset__name', 'asset__code']
    readonly_fields = ['id', 'prediction_date']
    date_hierarchy = 'prediction_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'asset', 'prediction_date')
        }),
        ('Prediction Results', {
            'fields': ('failure_probability', 'risk_level', 'predicted_failure_type', 
                      'estimated_days_to_failure', 'confidence_score')
        }),
        ('Model Information', {
            'fields': ('model_version', 'features_snapshot')
        }),
        ('Recommendations', {
            'fields': ('recommended_action', 'estimated_repair_cost')
        }),
        ('Outcome Tracking', {
            'fields': ('actual_failure_occurred', 'actual_failure_date', 'prediction_accuracy')
        }),
        ('Actions', {
            'fields': ('work_order_created', 'notification_sent')
        }),
    )


@admin.register(OperatorSkill)
class OperatorSkillAdmin(admin.ModelAdmin):
    """Admin for operator skills."""
    list_display = ['operator', 'skill_name', 'skill_category', 'proficiency_level', 'is_certified']
    list_filter = ['skill_category', 'is_certified', 'proficiency_level']
    search_fields = ['operator__first_name', 'operator__last_name', 'skill_name']
    readonly_fields = ['id', 'acquired_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'operator', 'skill_category', 'skill_name', 'proficiency_level')
        }),
        ('Certification', {
            'fields': ('is_certified', 'certification_number', 'certification_date', 'expiration_date')
        }),
        ('Performance', {
            'fields': ('tasks_completed', 'average_completion_time', 'success_rate')
        }),
        ('Metadata', {
            'fields': ('acquired_date', 'last_used_date', 'notes')
        }),
    )


@admin.register(OperatorAvailability)
class OperatorAvailabilityAdmin(admin.ModelAdmin):
    """Admin for operator availability."""
    list_display = ['operator', 'is_available', 'current_location', 'active_work_orders', 'last_updated']
    list_filter = ['is_available', 'current_location']
    search_fields = ['operator__first_name', 'operator__last_name']
    readonly_fields = ['id', 'last_updated']


@admin.register(OperatorPerformance)
class OperatorPerformanceAdmin(admin.ModelAdmin):
    """Admin for operator performance."""
    list_display = ['operator', 'period_start', 'period_end', 'performance_score', 'work_orders_completed']
    list_filter = ['period_start', 'period_end']
    search_fields = ['operator__first_name', 'operator__last_name']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'period_end'
