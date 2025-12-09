# 📊 Dashboard con Datos Reales - Implementación Completa

## ✅ Cambios Realizados

### Backend (Django)

#### Archivo: `backend/apps/core/dashboard_views.py`

**Funciones Agregadas:**

1. **`get_work_orders_trend(work_orders_qs)`**
   - Obtiene tendencia de órdenes de trabajo de los últimos 6 meses
   - Retorna: `[{ month: 'Ene', completed: 12, pending: 5 }, ...]`
   - Datos: Completadas vs Pendientes por mes

2. **`get_asset_status_distribution(assets_qs)`**
   - Obtiene distribución de estado de activos
   - Retorna: `[{ name: 'Operativo', value: 45 }, ...]`
   - Datos: Operativo, Mantenimiento, Detenido

3. **`get_maintenance_types(work_orders_qs)`**
   - Obtiene tipos de mantenimiento basado en prioridad
   - Retorna: `[{ type: 'Preventivo', count: 45 }, ...]`
   - Datos: Preventivo, Correctivo, Predictivo, Emergencia

4. **`get_predictions_timeline(predictions_qs)`**
   - Obtiene timeline de predicciones de las últimas 4 semanas
   - Retorna: `[{ date: 'Sem 1', high_risk: 3, medium_risk: 5, low_risk: 8 }, ...]`
   - Datos: Alto, Medio y Bajo riesgo por semana

**Endpoint Actualizado:**

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    # ... código existente ...
    
    # Nuevo: Generar datos de gráficos (solo para Supervisor y Admin)
    charts_data = None
    if role_name in [Role.ADMIN, Role.SUPERVISOR]:
        charts_data = {
            'work_orders_trend': get_work_orders_trend(work_orders_qs),
            'asset_status_distribution': get_asset_status_distribution(assets_qs),
            'maintenance_types': get_maintenance_types(work_orders_qs),
            'predictions_timeline': get_predictions_timeline(predictions_qs)
        }
    
    data = {
        # ... campos existentes ...
        'charts': charts_data  # ← NUEVO
    }
```

### Frontend (React)

#### Archivo: `frontend/src/pages/Dashboard.tsx`

**Cambios Realizados:**

1. **Eliminados datos mock:**
   ```typescript
   // ANTES (datos mock)
   const workOrdersTrend = stats?.charts?.work_orders_trend || [
     { month: 'Ene', completed: 12, pending: 5 },
     // ... datos hardcodeados
   ];
   
   // AHORA (datos reales)
   const workOrdersTrend = stats?.charts?.work_orders_trend || [];
   ```

2. **Agregados mensajes cuando no hay datos:**
   - Cada gráfico muestra un mensaje amigable si no hay datos
   - Icono + texto "No hay datos disponibles"
   - Mantiene la estructura visual

3. **Validación de datos:**
   - Verifica que existan datos antes de renderizar
   - Maneja arrays vacíos correctamente
   - Evita errores de renderizado

## 📊 Estructura de Datos

### Response del API `/dashboard/stats/`

```json
{
  "total_assets": 50,
  "operational_assets": 42,
  "maintenance_assets": 5,
  "stopped_assets": 3,
  "total_work_orders": 120,
  "pending_work_orders": 15,
  "in_progress_work_orders": 8,
  "completed_work_orders": 97,
  "total_predictions": 45,
  "high_risk_predictions": 3,
  "kpis": {
    "availability_rate": 84.0,
    "completion_rate": 80.8,
    "avg_duration_days": 3.5,
    "preventive_ratio": 65.0,
    "maintenance_backlog": 23,
    "critical_assets_count": 3,
    "work_orders_this_month": 12,
    "prediction_accuracy": 85.0
  },
  "charts": {
    "work_orders_trend": [
      { "month": "Jul", "completed": 15, "pending": 3 },
      { "month": "Ago", "completed": 18, "pending": 5 },
      { "month": "Sep", "completed": 16, "pending": 4 },
      { "month": "Oct", "completed": 20, "pending": 6 },
      { "month": "Nov", "completed": 17, "pending": 2 },
      { "month": "Dic", "completed": 11, "pending": 3 }
    ],
    "asset_status_distribution": [
      { "name": "Operativo", "value": 42 },
      { "name": "Mantenimiento", "value": 5 },
      { "name": "Detenido", "value": 3 }
    ],
    "maintenance_types": [
      { "type": "Preventivo", "count": 45 },
      { "type": "Correctivo", "count": 35 },
      { "type": "Predictivo", "count": 25 },
      { "type": "Emergencia", "count": 15 }
    ],
    "predictions_timeline": [
      { "date": "Sem 1", "high_risk": 2, "medium_risk": 5, "low_risk": 8 },
      { "date": "Sem 2", "high_risk": 3, "medium_risk": 6, "low_risk": 7 },
      { "date": "Sem 3", "high_risk": 1, "medium_risk": 7, "low_risk": 9 },
      { "date": "Sem 4", "high_risk": 2, "medium_risk": 4, "low_risk": 10 }
    ]
  }
}
```

**Nota:** El campo `charts` es `null` para usuarios con rol OPERADOR.

## 🔐 Permisos por Rol

### Operador
- **Ve:** Stats básicos de activos y órdenes asignadas
- **NO ve:** Campo `charts` (es null)
- **Gráficos:** No se muestran en el frontend

### Supervisor
- **Ve:** Stats del equipo + gráficos
- **Campo `charts`:** Incluido con datos reales
- **Gráficos:** 4 gráficos interactivos

### Admin
- **Ve:** Stats globales + gráficos
- **Campo `charts`:** Incluido con datos reales
- **Gráficos:** 4 gráficos interactivos

## 🎯 Lógica de Datos

### 1. Tendencia de Órdenes de Trabajo
- **Período:** Últimos 6 meses
- **Cálculo:** Cuenta órdenes creadas en cada mes
- **Categorías:**
  - Completadas: status = 'Completada'
  - Pendientes: status in ['Pendiente', 'En Progreso']

### 2. Distribución de Estado de Activos
- **Fuente:** Tabla Assets
- **Estados:**
  - Operativo: status = 'OPERATIONAL'
  - Mantenimiento: status = 'MAINTENANCE'
  - Detenido: status = 'OUT_OF_SERVICE'

### 3. Tipos de Mantenimiento
- **Proxy:** Usa prioridad como indicador de tipo
- **Mapeo:**
  - Preventivo: priority = 'Baja'
  - Correctivo: priority = 'Media'
  - Predictivo: priority = 'Alta'
  - Emergencia: priority = 'Urgente'

### 4. Timeline de Predicciones
- **Período:** Últimas 4 semanas
- **Cálculo:** Cuenta predicciones creadas por semana
- **Niveles:**
  - Alto Riesgo: risk_level in ['HIGH', 'CRITICAL']
  - Riesgo Medio: risk_level = 'MEDIUM'
  - Bajo Riesgo: risk_level = 'LOW'

## 🚀 Deployment

### Backend

```bash
# 1. Verificar cambios
cd backend
python manage.py check

# 2. Limpiar caché (importante)
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()

# 3. Reiniciar servidor (Railway)
# Se reiniciará automáticamente al hacer push
```

### Frontend

```bash
# 1. Verificar build
cd frontend
npm run build

# 2. Verificar que no hay errores
npm run lint
```

### Deployment Completo

```bash
# 1. Commit de cambios
git add backend/apps/core/dashboard_views.py
git add frontend/src/pages/Dashboard.tsx
git add DATOS_REALES_DASHBOARD.md

git commit -m "feat: Implementar datos reales en dashboard

- Agregar funciones para generar datos de gráficos en backend
- Actualizar endpoint /dashboard/stats/ con campo charts
- Eliminar datos mock del frontend
- Agregar validación y mensajes cuando no hay datos
- Respetar permisos por rol (charts solo para Supervisor/Admin)"

# 2. Push a producción
git push origin main

# 3. Verificar deployment
# Backend (Railway): ~2-3 minutos
# Frontend (Vercel): ~2-3 minutos
```

## ✅ Verificaciones Post-Deployment

### Backend
1. [ ] Endpoint responde correctamente
   ```bash
   curl -H "Authorization: Bearer <token>" \
        https://api.tu-proyecto.railway.app/api/dashboard/stats/
   ```

2. [ ] Campo `charts` presente para Admin/Supervisor
3. [ ] Campo `charts` es null para Operador
4. [ ] Datos de gráficos tienen formato correcto

### Frontend
1. [ ] Dashboard carga sin errores
2. [ ] Gráficos se muestran para Admin/Supervisor
3. [ ] Gráficos NO se muestran para Operador
4. [ ] Mensaje "No hay datos" aparece cuando corresponde
5. [ ] No hay errores en consola del navegador

## 🐛 Troubleshooting

### Problema: Gráficos no se muestran

**Causa:** Caché del backend
**Solución:**
```python
# En Django shell
from django.core.cache import cache
cache.clear()
```

### Problema: Datos vacíos en gráficos

**Causa:** No hay datos históricos suficientes
**Solución:**
- Crear más órdenes de trabajo
- Generar predicciones ML
- Esperar acumulación de datos

### Problema: Error 500 en endpoint

**Causa:** Posible error en queries
**Solución:**
```bash
# Ver logs de Railway
railway logs

# O en local
python manage.py runserver
# Revisar terminal
```

## 📈 Mejoras Futuras (Opcional)

### Fase 1: Optimización
- [ ] Agregar índices en campos de fecha
- [ ] Implementar paginación en queries grandes
- [ ] Optimizar queries con select_related

### Fase 2: Funcionalidades
- [ ] Filtros de fecha en gráficos
- [ ] Exportación de gráficos a PDF/PNG
- [ ] Drill-down (click en gráfico para detalles)
- [ ] Comparación de períodos

### Fase 3: Tiempo Real
- [ ] WebSocket para actualización automática
- [ ] Notificaciones de cambios importantes
- [ ] Refresh automático cada X minutos

## 📝 Notas Importantes

### ✅ Ventajas
- Datos 100% reales del sistema
- Respeta permisos por rol
- Maneja casos sin datos correctamente
- Performance optimizado con caché
- Backward compatible

### ⚠️ Consideraciones
- Caché de 5 minutos (puede mostrar datos ligeramente desactualizados)
- Requiere datos históricos para gráficos significativos
- Tipos de mantenimiento basados en prioridad (proxy)

### 🎯 Recomendaciones
1. Limpiar caché después del deployment
2. Monitorear performance de queries
3. Generar datos de prueba si es necesario
4. Documentar para usuarios finales

---

**Fecha:** 6 de Diciembre, 2025
**Versión:** 2.0.0
**Estado:** ✅ Listo para Producción con Datos Reales
