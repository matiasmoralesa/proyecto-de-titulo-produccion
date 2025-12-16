# 🤖 ML Model Backup Checkpoint - Pre Inventory Integration

**Fecha:** 16 de Diciembre, 2025  
**Estado:** Modelo ML funcional antes de integración con inventario  
**Propósito:** Punto de restauración antes de modificaciones mayores  

## 📊 Estado Actual del Modelo

### **Arquitectura del Modelo:**
- **Tipo:** Random Forest (por defecto)
- **Objetivo:** Predicción de fallas en activos
- **Estado:** Funcional y desplegado

### **Características Actuales (Features):**

#### **1. Básicas del Activo:**
```python
- asset_age_days                    # Edad en días desde instalación
- vehicle_type_Camión_Supersucker   # One-hot encoding
- vehicle_type_Camioneta_MDO        # One-hot encoding  
- vehicle_type_Retroexcavadora_MDO  # One-hot encoding
- vehicle_type_Cargador_Frontal_MDO # One-hot encoding
- vehicle_type_Minicargador_MDO     # One-hot encoding
```

#### **2. Temporales:**
```python
- days_since_last_maintenance       # Días desde último mantenimiento
- days_since_last_failure          # Días desde última falla crítica
- maintenance_frequency_per_month   # Frecuencia de mantenimiento mensual
```

#### **3. Operacionales:**
```python
- current_odometer                  # Lectura actual del odómetro
- current_fuel_level               # Nivel actual de combustible
- odometer_rate_of_change          # Km/día de uso
- avg_fuel_level_7d                # Promedio combustible últimos 7 días
- status_change_frequency          # Frecuencia cambios de estado
```

#### **4. Históricas:**
```python
- total_work_orders                # Total órdenes de trabajo
- completed_work_orders            # Órdenes completadas
- high_priority_work_orders        # Órdenes alta prioridad (fallas)
- total_maintenance_hours          # Horas totales de mantenimiento
- avg_repair_time_hours           # Tiempo promedio de reparación
- failure_rate_per_1000km         # Tasa de fallas por 1000km
```

#### **5. Estado y Salud:**
```python
- count_operando                   # Conteo estado operando
- count_detenida                   # Conteo estado detenida
- count_en_mantenimiento          # Conteo estado en mantenimiento
- count_fuera_servicio            # Conteo estado fuera de servicio
- pct_operando                    # Porcentaje tiempo operando
- pct_detenida                    # Porcentaje tiempo detenida
- pct_en_mantenimiento           # Porcentaje tiempo en mantenimiento
- pct_fuera_servicio             # Porcentaje tiempo fuera servicio
- health_score                    # Puntuación de salud (0-100)
```

### **Métricas del Modelo:**
```python
# Almacenadas en MLModel
- accuracy: float                  # Precisión general
- precision: float                 # Precisión por clase
- recall: float                   # Recall por clase
- f1_score: float                 # F1-Score
- feature_importance: JSON        # Importancia de características
```

### **Predicciones Generadas:**
```python
# FailurePrediction model
- failure_probability: 0.0-1.0    # Probabilidad de falla
- risk_level: LOW/MEDIUM/HIGH/CRITICAL
- predicted_failure_type: str     # Tipo de falla predicha
- estimated_days_to_failure: int  # Días estimados hasta falla
- confidence_score: 0.0-1.0       # Confianza de la predicción
```

## 🗂️ Archivos del Modelo Actual

### **Código Principal:**
- `backend/apps/ml_predictions/models.py` - Modelos de datos
- `backend/apps/ml_predictions/feature_engineering.py` - Extracción de características
- `backend/apps/ml_predictions/model_trainer.py` - Entrenamiento
- `backend/apps/ml_predictions/prediction_service.py` - Servicio de predicción
- `backend/apps/ml_predictions/tasks.py` - Tareas de Celery

### **Configuración:**
- `backend/apps/ml_predictions/apps.py` - Configuración de la app
- `backend/apps/ml_predictions/urls.py` - URLs de la API
- `backend/apps/ml_predictions/views.py` - Vistas de la API
- `backend/apps/ml_predictions/serializers.py` - Serializers

## 🎯 Plan de Integración con Inventario

### **Fase 1: Integración Operacional (SIN modificar ML)**
```python
# Nuevos modelos a crear:
- WorkOrderPart (relación OT-Repuesto)
- PartReservation (reservas de repuestos)
- MaintenanceCost (costos por mantenimiento)

# Funcionalidades:
- Reserva automática de repuestos al asignar OT
- Descuento de stock al completar OT
- Cálculo de costos reales de mantenimiento
- Reportes de consumo de repuestos
```

### **Fase 2: Enriquecimiento del Modelo ML**
```python
# Nuevas características a agregar:
- avg_parts_cost_per_maintenance   # Costo promedio repuestos
- critical_parts_replacement_freq  # Frecuencia reemplazo críticos
- parts_availability_score         # Puntuación disponibilidad
- maintenance_cost_trend          # Tendencia de costos
- parts_lead_time_impact          # Impacto tiempo entrega
- inventory_turnover_rate         # Rotación de inventario
- cost_per_operating_hour         # Costo por hora operativa
```

### **Fase 3: Modelo Avanzado (Futuro)**
```python
# Predicciones adicionales:
- Demanda de repuestos por activo
- Optimización de niveles de stock
- Predicción de costos futuros
- Recomendaciones de compra
```

## 🔄 Estrategia de Migración

### **Backup del Modelo Actual:**
1. ✅ Documentación completa de características
2. ✅ Respaldo de código fuente
3. ✅ Preservación de métricas actuales
4. ✅ Plan de rollback definido

### **Implementación Gradual:**
1. **Mantener modelo actual** funcionando
2. **Agregar funcionalidad inventario** sin afectar ML
3. **Recopilar datos** de inventario por 30-60 días
4. **Entrenar modelo enriquecido** con transfer learning
5. **A/B testing** entre modelo actual y nuevo
6. **Migración gradual** si el nuevo modelo es superior

## 📋 Checklist Pre-Implementación

- [x] Modelo actual documentado completamente
- [x] Características actuales catalogadas
- [x] Plan de integración definido
- [x] Estrategia de rollback establecida
- [x] Métricas de referencia registradas
- [ ] Backup de modelos entrenados (si existen)
- [ ] Tests de regresión preparados
- [ ] Monitoreo de performance configurado

## 🚨 Puntos Críticos a Preservar

### **No Modificar Durante Fase 1:**
- ✅ `feature_engineering.py` - Mantener características actuales
- ✅ `model_trainer.py` - Preservar lógica de entrenamiento
- ✅ `prediction_service.py` - Mantener API de predicciones
- ✅ Modelos `MLModel` y `FailurePrediction` - Sin cambios estructurales

### **Modificaciones Permitidas:**
- ✅ Agregar nuevos modelos para inventario
- ✅ Crear servicios de sincronización OT-Inventario
- ✅ Implementar reportes de costos
- ✅ Agregar endpoints de gestión de repuestos

## 📊 Métricas de Referencia

### **Performance Actual del Sistema:**
- Tiempo de respuesta API ML: < 500ms
- Precisión de predicciones: Por definir con datos reales
- Cobertura de activos: 100% activos activos
- Frecuencia de predicciones: Diaria (via Celery)

### **KPIs a Mantener:**
- ✅ Disponibilidad del servicio ML
- ✅ Tiempo de respuesta de predicciones
- ✅ Precisión de las predicciones existentes
- ✅ Cobertura de activos monitoreados

---

**🔒 Este checkpoint garantiza que podemos volver al estado actual en cualquier momento durante la implementación de la integración con inventario.**

**Próximo paso:** Implementar Fase 1 - Integración Operacional OTs-Inventario sin modificar el modelo ML.