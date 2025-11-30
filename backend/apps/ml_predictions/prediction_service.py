import joblib
import numpy as np
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F, Count, Avg
from .models import FailurePrediction, MLModel, OperatorSkill, OperatorAvailability
from .feature_engineering import FeatureEngineer
from apps.work_orders.models import WorkOrder
from apps.authentication.models import User, Role
import os


class PredictionService:
    """
    Service for making failure predictions using trained ML models
    """
    
    def __init__(self):
        self.model_trainer = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model"""
        from .model_trainer import FailurePredictionTrainer
        from .data_generator import SyntheticDataGenerator
        
        try:
            self.model_trainer = FailurePredictionTrainer()
            self.model_trainer.load_model()
            self.data_generator = SyntheticDataGenerator()
        except FileNotFoundError:
            raise Exception("No trained model found. Please run: python manage.py train_ml_model")
    
    def predict_single_asset(self, asset):
        """
        Generate failure prediction for a single asset
        """
        if not self.model_trainer:
            raise Exception("Model not loaded")
        
        # Extract features from real asset data
        features = self.data_generator.generate_asset_data(asset)
        
        # Make prediction
        prediction_result = self.model_trainer.predict(features)
        
        probability = prediction_result['failure_probability']
        risk_level = prediction_result['risk_level'].lower()
        
        # Calculate predicted failure date
        predicted_date = self._estimate_failure_date(probability, features)
        recommended_action = self._generate_recommendation(risk_level, features)
        
        # Get or create ML model record
        ml_model_record, _ = MLModel.objects.get_or_create(
            model_version='1.0',
            defaults={
                'model_name': 'Failure Prediction Model',
                'model_type': 'random_forest',
                'is_active': True,
                'is_production': True,
                'accuracy': 0.72,
                'precision': 0.80,
                'recall': 0.81,
                'f1_score': 0.81,
                'training_data_size': 1000,
                'training_duration_seconds': 5.0,
                'model_file_path': 'ml_models/failure_prediction_model.pkl'
            }
        )
        
        # Calculate days to failure
        days_to_failure = (predicted_date - timezone.now().date()).days
        
        # Save prediction
        prediction = FailurePrediction.objects.create(
            asset=asset,
            model_version=ml_model_record.model_version,
            failure_probability=probability,
            estimated_days_to_failure=days_to_failure,
            risk_level=risk_level.upper(),
            confidence_score=self._calculate_confidence(probability),
            recommended_action=recommended_action,
            features_snapshot=features
        )
        
        return prediction
    
    def predict_batch(self, assets):
        """
        Generate predictions for multiple assets
        """
        predictions = []
        
        for asset in assets:
            try:
                prediction = self.predict_single_asset(asset)
                predictions.append(prediction)
            except Exception as e:
                print(f"Error predicting for asset {asset.id}: {str(e)}")
                continue
        
        return predictions
    
    def _calculate_risk_level(self, probability):
        """Calculate risk level based on failure probability"""
        if probability >= 0.7:
            return 'high'
        elif probability >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_failure_date(self, probability, features):
        """Estimate when failure might occur based on probability and features"""
        # Simple heuristic: higher probability = sooner failure
        if probability >= 0.8:
            days = 7  # Within a week
        elif probability >= 0.6:
            days = 14  # Within 2 weeks
        elif probability >= 0.4:
            days = 30  # Within a month
        else:
            days = 60  # Within 2 months
        
        # Adjust based on maintenance history
        if features.get('days_since_last_maintenance', 0) > 90:
            days = int(days * 0.7)  # Reduce time if overdue
        
        return timezone.now().date() + timedelta(days=days)
    
    def _calculate_confidence(self, probability):
        """Calculate confidence score for the prediction"""
        # Confidence is higher when probability is closer to 0 or 1
        return abs(probability - 0.5) * 2
    
    def _generate_recommendation(self, risk_level, features):
        """Generate recommended action based on risk level"""
        if risk_level == 'high':
            return 'Programar mantenimiento preventivo urgente en los próximos 7 días'
        elif risk_level == 'medium':
            return 'Incluir en próximo ciclo de mantenimiento preventivo'
        else:
            return 'Continuar con programa de mantenimiento regular'
    
    def create_preventive_work_order(self, prediction):
        """
        Create a preventive work order based on a high-risk prediction
        """
        from apps.work_orders.models import WorkOrder
        from .operator_assignment_service import OperatorAssignmentService
        
        if prediction.risk_level not in ['high', 'critical']:
            return None
        
        # Create work order
        work_order = WorkOrder.objects.create(
            asset=prediction.asset,
            title=f'Mantenimiento Preventivo - Predicción de Falla',
            description=f'Probabilidad de falla: {prediction.failure_probability:.1%}\n'
                       f'Acción recomendada: {prediction.recommended_action}',
            priority='high' if prediction.risk_level == 'high' else 'critical',
            status='pending',
            work_order_type='preventive',
            scheduled_date=timezone.now() + timedelta(days=1)
        )
        
        # Assign best operator
        assignment_service = OperatorAssignmentService()
        operator = assignment_service.assign_operator_to_work_order(
            work_order,
            required_skills=[prediction.asset.vehicle_type],
            auto_assign=True
        )
        
        # Link prediction to work order
        prediction.work_order_created = work_order
        prediction.save()
        
        return work_order
