"""
Serializers for ML predictions API.
"""
from rest_framework import serializers
from .models import FailurePrediction, MLModel, OperatorSkill, OperatorAvailability


class MLModelSerializer(serializers.ModelSerializer):
    """Serializer for ML model metadata."""
    
    class Meta:
        model = MLModel
        fields = [
            'id', 'model_name', 'model_version', 'model_type',
            'training_date', 'training_data_size', 'training_duration_seconds',
            'accuracy', 'precision', 'recall', 'f1_score',
            'feature_importance', 'is_active', 'is_production',
            'hyperparameters'
        ]
        read_only_fields = ['id', 'training_date']


class FailurePredictionSerializer(serializers.ModelSerializer):
    """Serializer for failure predictions."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_code = serializers.CharField(source='asset.code', read_only=True)
    asset_type = serializers.CharField(source='asset.asset_type', read_only=True)
    asset = serializers.SerializerMethodField()
    
    def get_asset(self, obj):
        return {
            'id': str(obj.asset.id),
            'name': obj.asset.name,
            'vehicle_type': obj.asset.vehicle_type if hasattr(obj.asset, 'vehicle_type') else obj.asset.asset_type
        }
    
    class Meta:
        model = FailurePrediction
        fields = [
            'id', 'asset', 'asset_name', 'asset_code', 'asset_type',
            'prediction_date', 'failure_probability', 'risk_level',
            'predicted_failure_type', 'estimated_days_to_failure',
            'model_version', 'confidence_score', 'features_snapshot',
            'recommended_action', 'estimated_repair_cost',
            'actual_failure_occurred', 'actual_failure_date',
            'prediction_accuracy', 'work_order_created',
            'notification_sent'
        ]
        read_only_fields = ['id', 'prediction_date']


class FailurePredictionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for prediction lists."""
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_code = serializers.CharField(source='asset.code', read_only=True)
    
    class Meta:
        model = FailurePrediction
        fields = [
            'id', 'asset', 'asset_name', 'asset_code',
            'prediction_date', 'failure_probability', 'risk_level',
            'estimated_days_to_failure', 'confidence_score',
            'notification_sent'
        ]


class OperatorSkillSerializer(serializers.ModelSerializer):
    """Serializer for operator skills."""
    operator_name = serializers.CharField(source='operator.get_full_name', read_only=True)
    
    class Meta:
        model = OperatorSkill
        fields = [
            'id', 'operator', 'operator_name', 'skill_category',
            'skill_name', 'proficiency_level', 'is_certified',
            'certification_number', 'certification_date', 'expiration_date',
            'tasks_completed', 'average_completion_time', 'success_rate',
            'acquired_date', 'last_used_date', 'notes'
        ]
        read_only_fields = ['id', 'acquired_date']


class OperatorAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for operator availability."""
    operator_name = serializers.CharField(source='operator.get_full_name', read_only=True)
    location_name = serializers.CharField(source='current_location.name', read_only=True)
    
    class Meta:
        model = OperatorAvailability
        fields = [
            'id', 'operator', 'operator_name', 'is_available',
            'current_location', 'location_name', 'active_work_orders',
            'estimated_hours_remaining', 'shift_start', 'shift_end',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']
