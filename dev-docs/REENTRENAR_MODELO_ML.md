# 🤖 Reentrenar Modelo ML en Producción

## ✅ Cambios Realizados

1. ✅ Actualizado `requirements.txt` con scikit-learn y dependencias ML
2. ✅ Corregidos los tipos de vehículos en `data_generator.py`
3. ✅ Creado script `retrain_model.py` para reentrenamiento
4. ✅ Cambios subidos a Git y desplegados en Railway

## 🎯 Próximo Paso: Reentrenar el Modelo

Railway ya tiene los cambios desplegados. Ahora necesitas reentrenar el modelo con los datos correctos.

### Opción 1: Desde Railway SSH (Recomendado)

```bash
# 1. Conectarse a Railway
railway ssh

# 2. Ir al directorio backend
cd backend

# 3. Reentrenar el modelo
python retrain_model.py

# 4. Salir
exit
```

### Opción 2: Desde tu PC (Alternativa)

Si prefieres entrenar localmente y subir el modelo:

```bash
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Ir a backend
cd backend

# 3. Reentrenar
python retrain_model.py

# 4. El modelo se guardará en backend/ml_models/
```

Luego necesitarías subir el modelo a Railway (más complejo).

## 📊 Qué Esperar

Cuando ejecutes `python retrain_model.py` verás:

```
============================================================
  REENTRENAMIENTO DEL MODELO ML
============================================================

📊 Generando datos de entrenamiento...
  ✓ 2000 muestras generadas

📋 Tipos de vehículos en los datos:
Camión Supersucker        400
Camioneta MDO             400
Retroexcavadora MDO       400
Cargador Frontal MDO      400
Minicargador MDO          400

🤖 Entrenando modelo...
Datos de entrenamiento: 1600
Datos de prueba: 400
...

============================================================
  ✅ ENTRENAMIENTO COMPLETADO
============================================================

📊 Métricas del modelo:
  • Accuracy:  0.850
  • Precision: 0.823
  • Recall:    0.867
  • F1 Score:  0.844

💾 Modelo guardado en:
  /app/backend/ml_models/failure_prediction_model.pkl
```

## ✅ Verificar que Funcionó

Después de reentrenar:

1. Ve a la aplicación web
2. Inicia sesión como admin
3. Ve a "Predicciones ML"
4. Haz clic en "Ejecutar Predicciones"
5. Espera 5-10 segundos
6. Recarga la página
7. Deberías ver predicciones para los 7 activos

## 🔍 Monitorear el Proceso

Mientras entrenas, puedes ver los logs en otra terminal:

```bash
railway logs --tail 50
```

Busca mensajes como:
- "Entrenando Random Forest..."
- "Modelo guardado exitosamente"
- "Training completed"

## 🐛 Solución de Problemas

### Error: "No module named 'sklearn'"
**Solución**: Railway aún no instaló las dependencias. Espera 1-2 minutos más.

### Error: "Permission denied"
**Solución**: Asegúrate de estar en el directorio correcto (`cd backend`)

### El modelo se entrena pero las predicciones siguen vacías
**Solución**: 
1. Verifica que el modelo se guardó: `ls -la ml_models/`
2. Reinicia el servicio: `railway restart`

## 📝 Notas Importantes

- El entrenamiento toma 30-60 segundos
- Se generan 2000 muestras sintéticas
- El modelo se guarda automáticamente
- No necesitas reiniciar Railway después de entrenar
- El modelo se carga automáticamente en la próxima predicción

---

**¿Listo para entrenar?** Ejecuta:
```bash
railway ssh
cd backend
python retrain_model.py
```
