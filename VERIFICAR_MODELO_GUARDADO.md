# 🔍 Verificar si el Modelo ML se Guardó Correctamente

## Comandos para Ejecutar en Railway SSH

```bash
# 1. Conectarse a Railway
railway ssh

# 2. Verificar si existe el directorio de modelos
ls -la backend/ml_models/

# 3. Verificar si existe el archivo del modelo
ls -lh backend/ml_models/failure_prediction_model.pkl

# 4. Verificar si existen los encoders
ls -lh backend/ml_models/label_encoders.pkl

# 5. Ver el tamaño de los archivos (deben ser > 0 bytes)
du -h backend/ml_models/*

# 6. Salir
exit
```

## ✅ Qué Esperar

Si el modelo se guardó correctamente, deberías ver:

```
backend/ml_models/
  failure_prediction_model.pkl  (~ 500KB - 2MB)
  label_encoders.pkl            (~ 1KB - 10KB)
```

## 🎯 Si los Archivos Existen

¡Perfecto! El modelo está guardado. Ahora puedes:

1. Ir a la aplicación web
2. Ejecutar predicciones
3. Deberías ver resultados

## ❌ Si los Archivos NO Existen

El error al final del script impidió que se guardaran. Necesitas:

1. Corregir el script (ya lo hice)
2. Volver a ejecutar: `python backend/retrain_model.py`

## 🔄 Alternativa: Verificar desde los Logs

También puedes verificar en los logs de Railway si el modelo se está usando:

```bash
railway logs --tail 50 | grep -i "model\|prediction"
```

Busca mensajes como:
- "Modelo cargado exitosamente"
- "Model loaded"
- "Predictions completed"
