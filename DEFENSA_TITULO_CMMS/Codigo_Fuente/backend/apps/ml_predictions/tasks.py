"""
Tareas de Celery para predicciones ML
"""
from celery import shared_task
from django.utils import timezone
from .prediction_service import PredictionService
from apps.assets.models import Asset
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.ml_predictions.tasks.run_daily_predictions')
def run_daily_predictions():
    """
    Tarea programada para ejecutar predicciones ML diariamente
    
    Validates: Requirements 3.1, 3.2, 3.3
    """
    logger.info("=" * 60)
    logger.info("Iniciando predicciones ML diarias...")
    logger.info(f"Timestamp: {timezone.now().isoformat()}")
    logger.info("=" * 60)
    
    try:
        # Verificar que el modelo existe
        prediction_service = PredictionService()
        if not prediction_service.is_model_available():
            error_msg = "Modelo ML no disponible"
            logger.error(error_msg)
            return {
                'status': 'error',
                'error': error_msg,
                'timestamp': timezone.now().isoformat()
            }
        
        # Obtener activos activos
        assets = Asset.objects.filter(
            is_archived=False,
            status__in=['Operando', 'En Mantenimiento']
        )
        
        total_assets = assets.count()
        logger.info(f"Activos a analizar: {total_assets}")
        
        if total_assets == 0:
            logger.warning("No hay activos disponibles para predicciones")
            return {
                'status': 'success',
                'message': 'No hay activos disponibles',
                'total_predictions': 0,
                'timestamp': timezone.now().isoformat()
            }
        
        # Ejecutar predicciones
        predictions = prediction_service.predict_batch(assets)
        
        # Estadísticas
        high_risk = sum(1 for p in predictions if p.risk_level in ['HIGH', 'CRITICAL'])
        
        logger.info("=" * 60)
        logger.info(f"Predicciones completadas exitosamente")
        logger.info(f"Total: {len(predictions)}")
        logger.info(f"Alto riesgo: {high_risk}")
        logger.info("=" * 60)
        
        return {
            'status': 'success',
            'total_predictions': len(predictions),
            'high_risk_count': high_risk,
            'timestamp': timezone.now().isoformat()
        }
    
    except FileNotFoundError as e:
        logger.error("=" * 60)
        logger.error(f"ERROR: Modelo no encontrado")
        logger.error(f"Detalles: {str(e)}")
        logger.error("=" * 60)
        return {
            'status': 'error',
            'error': 'Modelo no encontrado',
            'details': str(e),
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"ERROR en predicciones diarias")
        logger.error(f"Tipo: {type(e).__name__}")
        logger.error(f"Mensaje: {str(e)}")
        logger.error("=" * 60)
        logger.exception("Stack trace completo:")
        return {
            'status': 'error',
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': timezone.now().isoformat()
        }


@shared_task(name='apps.ml_predictions.tasks.predict_single_asset')
def predict_single_asset(asset_id):
    """
    Tarea para predecir un solo activo (puede ser llamada manualmente)
    """
    logger.info(f"Prediciendo activo {asset_id}...")
    
    try:
        asset = Asset.objects.get(id=asset_id)
        prediction_service = PredictionService()
        prediction = prediction_service.predict_single_asset(asset)
        
        logger.info(
            f"Predicción completada para {asset.name}: "
            f"{prediction.risk_level} ({prediction.failure_probability:.1%})"
        )
        
        return {
            'status': 'success',
            'asset_id': str(asset_id),
            'asset_name': asset.name,
            'risk_level': prediction.risk_level,
            'probability': prediction.failure_probability,
            'timestamp': timezone.now().isoformat()
        }
    
    except Asset.DoesNotExist:
        logger.error(f"Activo {asset_id} no encontrado")
        return {
            'status': 'error',
            'error': 'Asset not found',
            'asset_id': str(asset_id)
        }
    except Exception as e:
        logger.error(f"Error prediciendo activo {asset_id}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'asset_id': str(asset_id)
        }


@shared_task(name='apps.ml_predictions.tasks.train_model')
def train_model(samples=1000):
    """
    Tarea para entrenar el modelo ML (puede tardar varios minutos)
    """
    logger.info(f"Iniciando entrenamiento del modelo con {samples} muestras...")
    
    try:
        from .model_trainer import FailurePredictionTrainer
        from .data_generator import SyntheticDataGenerator
        
        # Generar datos
        data_generator = SyntheticDataGenerator()
        X, y = data_generator.generate_training_data(n_samples=samples)
        
        # Entrenar modelo
        trainer = FailurePredictionTrainer()
        metrics = trainer.train(X, y)
        
        logger.info(f"Modelo entrenado exitosamente: {metrics}")
        
        return {
            'status': 'success',
            'metrics': metrics,
            'samples': samples,
            'timestamp': timezone.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error entrenando modelo: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }
