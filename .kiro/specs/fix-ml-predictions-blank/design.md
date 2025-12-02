# Design Document

## Overview

Este documento describe el diseño de la solución para el problema de la página de predicciones ML que aparece en blanco en producción. El problema ocurre cuando el usuario hace clic en "Ejecutar Predicciones" y la página se queda en blanco sin mostrar ningún mensaje de error.

### Root Cause Analysis

Basado en el análisis del código, los posibles problemas son:

1. **Error no manejado en el frontend**: El componente React no tiene un try-catch adecuado que capture errores de renderizado
2. **Respuesta inesperada del API**: El backend puede estar retornando un error que el frontend no maneja correctamente
3. **Modelo ML no disponible**: El archivo del modelo puede no existir en Railway o estar corrupto
4. **Error en la tarea de Celery**: La tarea puede fallar silenciosamente sin retornar un error HTTP apropiado

### Solution Approach

La solución implementará:

1. **Error Boundaries en React**: Para capturar errores de renderizado y mostrar un mensaje amigable
2. **Manejo robusto de errores en el API**: Para retornar respuestas HTTP apropiadas con mensajes descriptivos
3. **Health Check Endpoint**: Para verificar el estado del modelo ML antes de ejecutar predicciones
4. **Logging mejorado**: Para facilitar el diagnóstico en producción usando `railway logs`
5. **Validación del modelo**: Para verificar que el modelo existe y es válido antes de usarlo

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Vercel)                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  MLPredictionsPage.tsx                                 │ │
│  │  - Error Boundary                                      │ │
│  │  - Try-Catch en API calls                             │ │
│  │  - Estado de loading/error                            │ │
│  │  - Mensajes de error específicos                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend (Railway)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  views.py                                              │ │
│  │  - run_predictions() con try-catch                    │ │
│  │  - health_check() endpoint                            │ │
│  │  - Validación del modelo                              │ │
│  │  - Logging detallado                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│                            ▼                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  prediction_service.py                                 │ │
│  │  - _validate_model() método                           │ │
│  │  - Try-catch en load_model()                          │ │
│  │  - Try-catch en predict()                             │ │
│  │  - Logging de errores                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│                            ▼                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  tasks.py (Celery)                                     │ │
│  │  - Try-catch en run_daily_predictions()               │ │
│  │  - Logging de inicio/fin                              │ │
│  │  - Retorno de errores estructurados                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Frontend Error Handling

#### MLPredictionsPage Component

**Responsibilities:**
- Capturar errores de API calls
- Mostrar mensajes de error específicos al usuario
- Manejar estados de loading/error/success
- Prevenir que la página se quede en blanco

**Key Methods:**
```typescript
interface ErrorState {
  hasError: boolean;
  errorMessage: string;
  errorType: 'network' | 'server' | 'model' | 'unknown';
}

const runPredictions = async () => {
  try {
    setLoading(true);
    setError({ hasError: false, errorMessage: '', errorType: 'unknown' });
    
    const response = await api.post('/ml-predictions/predictions/run_predictions/');
    
    // Handle success
    toast.success('Predicciones iniciadas');
    setTimeout(() => fetchPredictions(), 5000);
    
  } catch (error) {
    // Handle different error types
    handlePredictionError(error);
  } finally {
    setLoading(false);
  }
};

const handlePredictionError = (error: any) => {
  if (error.response) {
    // Server responded with error
    const status = error.response.status;
    const data = error.response.data;
    
    if (status === 503) {
      setError({
        hasError: true,
        errorMessage: 'El modelo ML no está disponible. Por favor contacte al administrador.',
        errorType: 'model'
      });
    } else if (status === 500) {
      setError({
        hasError: true,
        errorMessage: data.error || 'Error interno del servidor',
        errorType: 'server'
      });
    }
  } else if (error.request) {
    // Network error
    setError({
      hasError: true,
      errorMessage: 'Error de conexión. Verifique su conexión a internet.',
      errorType: 'network'
    });
  }
};
```

### 2. Backend Error Handling

#### FailurePredictionViewSet

**New Methods:**

```python
@action(detail=False, methods=['get'])
def health_check(self, request):
    """
    Verifica el estado del modelo ML
    
    Returns:
        200: Modelo disponible y funcionando
        503: Modelo no disponible
        500: Error al cargar el modelo
    """
    try:
        service = PredictionService()
        model_info = service.get_model_info()
        
        return Response({
            'status': 'healthy',
            'model_version': model_info['version'],
            'model_path': model_info['path'],
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
    Ejecutar predicciones manualmente con manejo robusto de errores
    """
    try:
        # Validar que el modelo existe
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
```

#### PredictionService

**New Methods:**

```python
def is_model_available(self):
    """
    Verifica si el modelo está disponible
    
    Returns:
        bool: True si el modelo existe y puede cargarse
    """
    try:
        return os.path.exists(self.model_trainer.model_path)
    except Exception:
        return False

def get_model_info(self):
    """
    Obtiene información del modelo
    
    Returns:
        dict: Información del modelo
    """
    model_path = self.model_trainer.model_path
    
    info = {
        'version': '1.0',
        'path': model_path,
        'exists': os.path.exists(model_path),
        'size_mb': 0
    }
    
    if info['exists']:
        size_bytes = os.path.getsize(model_path)
        info['size_mb'] = round(size_bytes / (1024 * 1024), 2)
    
    return info

def _load_model(self):
    """Load the trained ML model with error handling"""
    from .model_trainer import FailurePredictionTrainer
    from .data_generator import SyntheticDataGenerator
    
    try:
        logger.info("Cargando modelo ML...")
        self.model_trainer = FailurePredictionTrainer()
        
        if not os.path.exists(self.model_trainer.model_path):
            logger.error(f"Archivo del modelo no encontrado: {self.model_trainer.model_path}")
            raise FileNotFoundError(
                f"No se encontró el modelo en: {self.model_trainer.model_path}. "
                "Por favor ejecute: python manage.py train_ml_model"
            )
        
        self.model_trainer.load_model()
        self.data_generator = SyntheticDataGenerator()
        logger.info("Modelo ML cargado exitosamente")
        
    except FileNotFoundError as e:
        logger.error(f"Modelo no encontrado: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error al cargar modelo: {str(e)}", exc_info=True)
        raise Exception(f"Error al cargar el modelo ML: {str(e)}")
```

### 3. Celery Task Error Handling

#### run_daily_predictions Task

**Enhanced Error Handling:**

```python
@shared_task(name='apps.ml_predictions.tasks.run_daily_predictions')
def run_daily_predictions():
    """
    Tarea programada para ejecutar predicciones ML diariamente
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
```

## Data Models

No se requieren cambios en los modelos de datos existentes.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Frontend error handling completeness

*For any* API error response (503, 500, 4xx, network error), the frontend should capture the error and display an appropriate user message without causing the page to go blank or crash.

**Validates: Requirements 1.1**

### Property 2: Successful API responses render correctly

*For any* valid API response containing prediction data, the frontend should render the data in the table without JavaScript errors or rendering failures.

**Validates: Requirements 1.4**

### Property 3: Prediction list rendering robustness

*For any* non-empty array of predictions returned by the API, the frontend should render all predictions in the table without errors, regardless of the specific values in the prediction objects.

**Validates: Requirements 1.5**

### Property 4: Backend exception handling

*For any* exception that occurs during prediction execution, the backend should capture the exception and return an HTTP 500 response with error details in JSON format, never allowing the exception to propagate unhandled.

**Validates: Requirements 2.2**

### Property 5: Successful prediction execution response

*For any* successful prediction execution request, the backend should return HTTP 202 with a valid Celery task ID in the response body.

**Validates: Requirements 2.4**

### Property 6: Prediction query response completeness

*For any* query to the predictions endpoint, the backend should return HTTP 200 with a response containing all required fields (id, asset, failure_probability, risk_level, estimated_days_to_failure, prediction_date, recommended_action, work_order_created) for each prediction.

**Validates: Requirements 2.5**

### Property 7: Model validation before prediction

*For any* request to execute predictions, the backend should first verify that the model file exists before attempting to load or use it.

**Validates: Requirements 4.1**

### Property 8: Health check model verification

*For any* call to the health check endpoint, the backend should verify the existence of the model file and return appropriate status information.

**Validates: Requirements 5.1**

## Error Handling

### Error Types and Responses

| Error Type | HTTP Status | Response Format | User Message |
|------------|-------------|-----------------|--------------|
| Model Not Found | 503 | `{"error": "...", "details": "..."}` | "El modelo ML no está disponible. Contacte al administrador." |
| Model Load Error | 500 | `{"error": "...", "details": "..."}` | "Error al cargar el modelo ML. Contacte al administrador." |
| No Assets | 200 | `{"message": "...", "assets_count": 0}` | "No hay activos disponibles para predicciones." |
| Network Error | N/A | Client-side | "Error de conexión. Verifique su conexión a internet." |
| Unknown Error | 500 | `{"error": "...", "details": "..."}` | "Error inesperado. Por favor intente nuevamente." |

### Logging Strategy

**Log Levels:**
- `INFO`: Operaciones normales (inicio/fin de predicciones, estadísticas)
- `WARNING`: Situaciones anormales pero manejables (no hay activos)
- `ERROR`: Errores que impiden la operación (modelo no encontrado, errores de predicción)

**Log Format:**
```
[TIMESTAMP] [LEVEL] [MODULE] Message
```

**Key Log Points:**
1. Inicio de predicciones (con timestamp y conteo de activos)
2. Fin de predicciones (con estadísticas)
3. Errores de carga del modelo (con ruta del archivo)
4. Errores de predicción (con stack trace)
5. Health check requests

## Testing Strategy

### Unit Tests

1. **Test Frontend Error Handling**
   - Test que `handlePredictionError` maneja correctamente errores 503
   - Test que `handlePredictionError` maneja correctamente errores 500
   - Test que `handlePredictionError` maneja correctamente errores de red
   - Test que el componente no se rompe cuando hay errores

2. **Test Backend Error Handling**
   - Test que `health_check` retorna 503 cuando el modelo no existe
   - Test que `health_check` retorna 200 cuando el modelo existe
   - Test que `run_predictions` retorna 503 cuando el modelo no está disponible
   - Test que `run_predictions` retorna 202 cuando todo está bien
   - Test que `run_predictions` retorna 200 cuando no hay activos

3. **Test PredictionService**
   - Test que `is_model_available` retorna False cuando el modelo no existe
   - Test que `is_model_available` retorna True cuando el modelo existe
   - Test que `get_model_info` retorna información correcta
   - Test que `_load_model` lanza FileNotFoundError cuando el modelo no existe

### Integration Tests

1. **Test End-to-End Prediction Flow**
   - Test que el flujo completo funciona cuando el modelo existe
   - Test que el flujo completo maneja correctamente cuando el modelo no existe
   - Test que el frontend muestra el mensaje correcto para cada tipo de error

### Manual Testing in Production

1. **Verificar Health Check**
   ```bash
   curl https://tu-backend.railway.app/api/ml-predictions/predictions/health_check/
   ```

2. **Verificar Logs en Railway**
   ```bash
   railway logs --tail 50 | grep -i "prediction\|model\|error"
   ```

3. **Test de Predicciones**
   - Hacer clic en "Ejecutar Predicciones"
   - Verificar que aparece el mensaje de loading
   - Verificar que aparece un mensaje de éxito o error (no página en blanco)
   - Verificar que las predicciones se cargan después de 5 segundos

## Deployment Considerations

### Railway Deployment

1. **Verificar que el modelo existe en Railway**
   ```bash
   railway ssh
   ls -lh backend/ml_models/
   ```

2. **Si el modelo no existe, entrenarlo**
   ```bash
   railway run python backend/manage.py train_ml_model
   ```

3. **Verificar logs después del deployment**
   ```bash
   railway logs --tail 100
   ```

### Vercel Deployment

1. **Rebuild del frontend** para incluir los cambios de manejo de errores
2. **Verificar variables de entorno** que apunten al backend correcto en Railway

### Rollback Plan

Si la solución causa problemas:

1. Revertir el commit en Git
2. Hacer redeploy en Vercel y Railway
3. Verificar que el sistema vuelve al estado anterior

## Performance Considerations

- El health check endpoint debe ser ligero (solo verificar existencia del archivo)
- Los logs no deben afectar el performance (usar logging asíncrono si es necesario)
- El manejo de errores no debe agregar latencia significativa

## Security Considerations

- No exponer rutas completas del sistema de archivos en mensajes de error
- No exponer stack traces completos al usuario final
- Logs deben estar protegidos y solo accesibles por administradores
- Health check endpoint debe requerir autenticación

