"""
Views para predicciones ML
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from apps.core.mixins import AssetAccessMixin
from apps.core.permissions import IsOperadorOrAbove, IsSupervisorOrAbove
from .models import FailurePrediction
from .serializers import FailurePredictionSerializer
from .tasks import run_daily_predictions, predict_single_asset


class FailurePredictionViewSet(AssetAccessMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para predicciones de fallos con control de acceso basado en roles.
    
    - ADMIN: Ve todas las predicciones
    - SUPERVISOR: Ve todas las predicciones
    - OPERADOR: Ve solo predicciones de activos de sus work orders
    
    Validates: Requirements 3.1, 3.2, 3.3
    """
    queryset = FailurePrediction.objects.all().select_related('asset').order_by('-prediction_date')
    serializer_class = FailurePredictionSerializer
    permission_classes = [IsAuthenticated, IsOperadorOrAbove]
    asset_field = 'asset'  # Field that links to Asset model
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """
        Obtener predicciones de alto riesgo
        """
        predictions = self.queryset.filter(
            risk_level__in=['HIGH', 'CRITICAL'],
            prediction_date__gte=timezone.now() - timedelta(days=7)
        )
        serializer = self.get_serializer(predictions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Obtener estadísticas de predicciones
        """
        total = self.queryset.count()
        high_risk = self.queryset.filter(risk_level__in=['HIGH', 'CRITICAL']).count()
        medium_risk = self.queryset.filter(risk_level='MEDIUM').count()
        low_risk = self.queryset.filter(risk_level='LOW').count()
        
        # Predicciones con OT creada
        with_wo = self.queryset.filter(work_order_created__isnull=False).count()
        
        return Response({
            'total': total,
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'low_risk': low_risk,
            'with_work_order': with_wo,
            'work_order_percentage': (with_wo / total * 100) if total > 0 else 0
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsSupervisorOrAbove])
    def run_predictions(self, request):
        """
        Ejecutar predicciones manualmente.
        Solo supervisores y admins pueden ejecutar predicciones.
        
        Validates: Requirements 3.3
        """
        task = run_daily_predictions.delay()
        return Response({
            'message': 'Predicciones iniciadas',
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsSupervisorOrAbove])
    def predict_asset(self, request):
        """
        Predecir un activo específico.
        Solo supervisores y admins pueden ejecutar predicciones.
        
        Validates: Requirements 3.3
        """
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response(
                {'error': 'asset_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task = predict_single_asset.delay(asset_id)
        return Response({
            'message': 'Predicción iniciada',
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
