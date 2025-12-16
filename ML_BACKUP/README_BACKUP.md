# 🔒 ML Model Backup - Pre Inventory Integration

**Fecha de Backup:** 16 de Diciembre, 2025  
**Commit Hash:** Antes de integración inventario-OTs  
**Propósito:** Respaldo completo del modelo ML antes de modificaciones  

## 📁 Contenido del Backup

Este directorio contiene una copia completa de `backend/apps/ml_predictions/` en el estado actual:

### **Archivos Respaldados:**
- `models.py` - Modelos de datos ML
- `feature_engineering.py` - Extracción de características
- `model_trainer.py` - Lógica de entrenamiento
- `prediction_service.py` - Servicio de predicciones
- `tasks.py` - Tareas de Celery
- `views.py` - API endpoints
- `serializers.py` - Serializers DRF
- `urls.py` - Configuración URLs
- `admin.py` - Configuración admin
- `apps.py` - Configuración de la app
- `signals.py` - Señales Django
- `tests.py` - Tests unitarios
- `data_generator.py` - Generador de datos sintéticos
- `operator_assignment_service.py` - Asignación de operadores

### **Directorios:**
- `migrations/` - Migraciones de base de datos
- `management/` - Comandos de gestión
- `__pycache__/` - Cache de Python

## 🔄 Instrucciones de Restauración

Si necesitas restaurar el modelo ML al estado actual:

```bash
# 1. Detener servicios
railway run python manage.py shell -c "from django_celery_beat.models import PeriodicTask; PeriodicTask.objects.filter(name__contains='ml').update(enabled=False)"

# 2. Restaurar archivos
cp -r ML_BACKUP/* backend/apps/ml_predictions/

# 3. Ejecutar migraciones si es necesario
railway run python manage.py migrate ml_predictions

# 4. Reiniciar servicios
railway redeploy
```

## ⚠️ Notas Importantes

- Este backup NO incluye modelos entrenados (.pkl files)
- Los modelos entrenados se almacenan en el directorio `ml_models/`
- Las migraciones pueden requerir ajustes según cambios realizados
- Verificar compatibilidad de dependencias al restaurar

## 📊 Estado del Modelo en este Backup

- **Características:** 25+ features de activos, temporales, operacionales
- **Algoritmo:** Random Forest (configurable)
- **Predicciones:** Probabilidad de falla, nivel de riesgo, días hasta falla
- **Performance:** Funcional en producción
- **Cobertura:** Todos los activos activos

---

**🛡️ Este backup garantiza la capacidad de rollback completo del sistema ML.**