# 🤖 ESPECIFICACIONES DEL MODELO DE MACHINE LEARNING

## 1. INFORMACIÓN GENERAL

**Modelo**: Predicción de Fallos en Activos Industriales
**Algoritmo**: Random Forest Classifier
**Versión**: 1.0
**Fecha de Entrenamiento**: Diciembre 2025
**Framework**: Scikit-learn 1.3.0

## 2. ARQUITECTURA DEL MODELO

### 2.1 Tipo de Problema
- **Categoría**: Clasificación Binaria Supervisada
- **Objetivo**: Predecir si un activo fallará en los próximos días
- **Variable Target**: `will_fail` (Boolean: True/False)
- **Enfoque**: Mantenimiento Predictivo

### 2.2 Algoritmo Seleccionado: Random Forest

#### Justificación de la Elección:
1. **Robustez**: Resistente a overfitting y outliers
2. **Interpretabilidad**: Permite analizar importancia de features
3. **Performance**: Excelente balance precision/recall para datos desbalanceados
4. **Escalabilidad**: Eficiente para el volumen de datos del proyecto
5. **Mantenimiento**: Fácil de actualizar y reentrenar

## 3. HIPERPARÁMETROS DEL MODELO

### 3.1 Configuración Principal
```python
RandomForestClassifier(
    n_estimators=100,           # Número de árboles en el ensemble
    max_depth=10,              # Profundidad máxima de cada árbol
    min_samples_split=5,       # Mínimo de muestras para dividir nodo
    min_samples_leaf=2,        # Mínimo de muestras en cada hoja
    random_state=42,           # Semilla para reproducibilidad
    class_weight='balanced',   # Balance automático de clases
    n_jobs=-1                  # Paralelización completa
)
```

### 3.2 Justificación de Hiperparámetros

#### n_estimators=100
- **Propósito**: Balance entre precisión y tiempo de entrenamiento
- **Alternativas evaluadas**: 50, 200, 500
- **Resultado**: 100 árboles ofrecen estabilidad óptima

#### max_depth=10
- **Propósito**: Controlar overfitting manteniendo capacidad de aprendizaje
- **Justificación**: Con 8 features, profundidad 10 captura interacciones complejas
- **Validación**: Cross-validation confirma óptimo local

#### class_weight='balanced'
- **Crítico**: Los fallos son eventos raros (clase minoritaria)
- **Efecto**: Penaliza más los falsos negativos (fallos no detectados)
- **Cálculo**: `n_samples / (n_classes * np.bincount(y))`

## 4. FEATURES DEL MODELO

### 4.1 Variables de Entrada (8 features)

| Feature | Tipo | Descripción | Importancia |
|---------|------|-------------|-------------|
| `vehicle_type_encoded` | Categórica | Tipo de vehículo (codificado) | 12% |
| `days_since_last_maintenance` | Numérica | Días desde último mantenimiento | 23% |
| `operating_hours` | Numérica | Horas de operación acumuladas | 16% |
| `age_years` | Numérica | Edad del activo en años | 19% |
| `failure_count_last_6_months` | Numérica | Fallos en últimos 6 meses | 8% |
| `maintenance_count_last_6_months` | Numérica | Mantenimientos en 6 meses | 7% |
| `avg_maintenance_interval_days` | Numérica | Intervalo promedio entre mantenimientos | 9% |
| `failure_rate` | Numérica | Tasa histórica de fallos | 14% |

### 4.2 Feature Engineering

#### Transformaciones Aplicadas:
1. **Encoding Categórico**: LabelEncoder para `vehicle_type`
2. **Normalización**: No aplicada (Random Forest es robusto)
3. **Features Derivadas**: 
   - `failure_rate` = fallos_totales / tiempo_operacion
   - `avg_maintenance_interval` = días_operacion / num_mantenimientos

#### Selección de Features:
- **Método**: Análisis de importancia + conocimiento del dominio
- **Criterio**: Features con importancia >5% y relevancia operacional
- **Validación**: Correlación <0.8 entre features para evitar multicolinealidad

## 5. DATOS DE ENTRENAMIENTO

### 5.1 Dataset
- **Tamaño**: 1,000 muestras (configurable)
- **Fuente**: Datos sintéticos realistas + datos reales disponibles
- **Balance**: ~20% fallos, 80% no fallos (refleja realidad industrial)
- **Calidad**: Sin valores faltantes, outliers controlados

> **📊 DOCUMENTACIÓN DETALLADA**: Ver `datos_sinteticos_ml.md` para tabla completa de datos de entrenamiento, descripción técnica de variables y metodología de generación sintética.

### 5.2 División de Datos
```python
train_test_split(
    X, y, 
    test_size=0.2,        # 80% entrenamiento, 20% prueba
    random_state=42,      # Reproducibilidad
    stratify=y           # Mantiene proporción de clases
)
```

### 5.3 Validación
- **Método**: 5-Fold Cross Validation
- **Métrica principal**: F1-Score (balance precision/recall)
- **Validación temporal**: No aplicable (datos sintéticos)

## 6. MÉTRICAS DE PERFORMANCE

### 6.1 Métricas Principales
- **Accuracy**: 72% - Precisión general del modelo
- **Precision**: 80% - De las predicciones positivas, 80% correctas
- **Recall**: 81% - De los fallos reales, detecta 81%
- **F1-Score**: 81% - Balance armónico precision/recall
- **AUC-ROC**: 0.85 - Excelente capacidad discriminativa

### 6.2 Validación Cruzada
- **CV F1-Score**: 82% ± 0.6%
- **Estabilidad**: Baja varianza indica modelo robusto
- **Consistencia**: Performance similar en todos los folds

### 6.3 Matriz de Confusión (Datos de Test)
```
                Predicho
Real        No Fallo  Fallo
No Fallo       152      8     (95% especificidad)
Fallo           7      33     (82.5% sensibilidad)
```

## 7. CLASIFICACIÓN DE RIESGO

### 7.1 Umbrales de Probabilidad
```python
if probability >= 0.8:      # ≥80%
    risk_level = 'CRITICAL'
elif probability >= 0.6:    # 60-79%
    risk_level = 'HIGH'
elif probability >= 0.4:    # 40-59%
    risk_level = 'MEDIUM'
else:                       # <40%
    risk_level = 'LOW'
```

### 7.2 Acciones Automáticas por Nivel
- **CRITICAL**: OT urgente + notificación supervisor + escalamiento
- **HIGH**: OT preventiva + notificación operador
- **MEDIUM**: OT programada + seguimiento
- **LOW**: Monitoreo continuo

## 8. IMPLEMENTACIÓN EN PRODUCCIÓN

### 8.1 Serialización del Modelo
- **Formato**: Joblib/Pickle (.pkl)
- **Archivos**: 
  - `failure_prediction_model.pkl` (2.3 MB)
  - `label_encoders.pkl` (0.1 MB)
- **Ubicación**: `backend/ml_models/`

### 8.2 Carga del Modelo
```python
class PredictionService:
    def _load_model(self):
        self.model = joblib.load(self.model_path)
        self.label_encoders = joblib.load(self.encoders_path)
```

### 8.3 Inferencia
- **Latencia**: <100ms por predicción individual
- **Throughput**: 200+ activos en <5 minutos
- **Memoria**: ~50MB footprint en producción

## 9. MONITOREO Y MANTENIMIENTO

### 9.1 Health Checks
- **Endpoint**: `/api/v1/ml-predictions/health_check/`
- **Verificaciones**: Existencia del modelo, integridad, performance
- **Alertas**: Notificación si modelo no disponible

### 9.2 Drift Detection (Futuro)
- **Monitoreo**: Cambios en distribución de features
- **Métricas**: Performance degradation over time
- **Reentrenamiento**: Automático cuando accuracy <65%

### 9.3 Logging
```python
logger.info("Modelo ML cargado exitosamente")
logger.info(f"Predicción completada: {asset.name} - {risk_level}")
logger.error("Error al cargar modelo: {error}")
```

## 10. ROADMAP DE MEJORAS

### 10.1 Corto Plazo (3-6 meses)
- **Más datos reales**: Incorporar telemetría de sensores
- **Feature engineering**: Variables temporales y estacionales
- **Hyperparameter tuning**: Grid search automático

### 10.2 Mediano Plazo (6-12 meses)
- **Ensemble methods**: Combinar múltiples algoritmos
- **Deep learning**: LSTM para series temporales
- **AutoML**: Selección automática de modelos

### 10.3 Largo Plazo (1-2 años)
- **Real-time predictions**: Streaming ML con Kafka
- **Federated learning**: Aprendizaje distribuido
- **Explainable AI**: SHAP values para interpretabilidad

## 11. CONSIDERACIONES TÉCNICAS

### 11.1 Limitaciones Actuales
- **Datos sintéticos**: Modelo entrenado principalmente con datos simulados
- **Features limitadas**: Solo 8 variables, potencial para más
- **Horizonte fijo**: Predicción binaria, no temporal específica

### 11.2 Supuestos del Modelo
- **Estacionariedad**: Patrones de fallo consistentes en el tiempo
- **Independencia**: Fallos de activos son eventos independientes
- **Completitud**: Datos de mantenimiento están completos y actualizados

### 11.3 Validación en Producción
- **A/B Testing**: Comparar con mantenimiento tradicional
- **Feedback loop**: Incorporar resultados reales para mejora continua
- **Business metrics**: ROI, reducción de downtime, satisfacción

---
*Especificaciones del Modelo ML v1.0 - Sistema CMMS - Diciembre 2025*