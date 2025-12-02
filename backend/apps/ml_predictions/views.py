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
from .prediction_service import PredictionService
import logging

logger = logging.getLogger(__name__)


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
    
    @action(detail=False, methods=['get'])
    def health_check(self, request):
        """
        Verifica el estado del modelo ML
        
        Returns:
            200: Modelo disponible y funcionando
            503: Modelo no disponible
            500: Error al cargar el modelo
        
        Validates: Requirements 5.1, 5.2, 5.3, 5.4
        """
        try:
            service = PredictionService()
            model_info = service.get_model_info()
            
            if not model_info['exists']:
                logger.warning(f"Modelo no encontrado en: {model_info['path']}")
                return Response({
                    'status': 'unavailable',
                    'error': 'Modelo ML no encontrado',
                    'details': f"El archivo del modelo no existe en la ruta esperada",
                    'model_path': model_info['path']
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            return Response({
                'status': 'healthy',
                'model_version': model_info['version'],
                'model_exists': model_info['exists'],
                'model_size_mb': model_info['size_mb']
            }, status=status.HTTP_200_OK)
            
        except FileNotFoundError as e:
            logger.error(f"Modelo no encontrado: {str(e)}")
            return Response({
                'status': 'unavailable',
                'error': 'Modelo ML no encontrado',
                'details': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        except Exception as e:
            logger.error(f"Error en health check: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'error': 'Error al verificar el modelo',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsSupervisorOrAbove])
    def run_predictions(self, request):
        """
        Ejecutar predicciones manualmente con manejo robusto de errores.
        Solo supervisores y admins pueden ejecutar predicciones.
        
        Validates: Requirements 2.1, 2.2, 2.3, 2.4, 4.1, 4.2, 4.3
        """
        try:
            # Validar que el modelo existe
            from apps.assets.models import Asset
            service = PredictionService()
            
            if not service.is_model_available():
                logger.error("Intento de ejecutar predicciones sin modelo disponible")
                return Response({
                    'error': 'Modelo ML no disponible',
                    'details': 'El modelo debe ser entrenado antes de ejecutar predicciones',
                    'action': 'Contacte al administrador para entrenar el modelo'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            # Verificar que hay activos
            assets_count = Asset.objects.filter(
                is_archived=False,
                status__in=['Operando', 'En Mantenimiento']
            ).count()
            
            if assets_count == 0:
                logger.warning("No hay activos disponibles para predicciones")
                return Response({
                    'message': 'No hay activos disponibles para predicciones',
                    'assets_count': 0
                }, status=status.HTTP_200_OK)
            
            # Ejecutar tarea
            logger.info(f"Iniciando predicciones para {assets_count} activos")
            task = run_daily_predictions.delay()
            
            return Response({
                'message': 'Predicciones iniciadas',
                'task_id': task.id,
                'assets_count': assets_count
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            logger.error(f"Error al iniciar predicciones: {str(e)}", exc_info=True)
            return Response({
                'error': 'Error al iniciar predicciones',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
