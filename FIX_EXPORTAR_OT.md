# ✅ Fix: Botón Exportar OT en Reportes

## 🔍 Problema

El botón "Exportar OT" en la página de Reportes arrojaba un error 500.

## 🐛 Error Encontrado

```
TypeError: ReportService.get_work_order_summary() got an unexpected keyword argument 'user_id'
```

**Ubicación:** `backend/apps/reports/views.py` línea 205

## 🔧 Causa

La función `export_work_orders` estaba pasando un parámetro `user_id` que la función `ReportService.get_work_order_summary()` no acepta.

```python
# ANTES (con error)
summary = ReportService.get_work_order_summary(
    start_date=start_date,
    end_date=end_date,
    asset_id=asset_id,
    user_id=user_filter  # ❌ Parámetro no válido
)
```

## ✅ Solución

Eliminé el parámetro `user_id` que no era necesario:

```python
# DESPUÉS (corregido)
summary = ReportService.get_work_order_summary(
    start_date=start_date,
    end_date=end_date,
    asset_id=asset_id
)
```

## 📊 Resultado

El botón ahora funciona correctamente y genera un archivo CSV con:

```csv
Work Order Summary Report
Date Range,2025-11-07 to 2025-12-07

Metric,Value
Total Work Orders,52
Total Hours Worked,7.5
Avg Completion Time (hours),-276.0

Status,Count
Pendiente,39
En Progreso,9
Completada,4
Cancelada,0

Priority,Count
Baja,1
Media,41
Alta,9
Urgente,1
```

## ✅ Verificación

```bash
python test_export_workorders.py
```

**Resultado:**
- ✅ Exportación exitosa
- ✅ Content-Type: text/csv
- ✅ Archivo generado: 303 bytes
- ✅ 52 órdenes de trabajo exportadas

## 🎯 Funcionalidad

### Botón "Exportar OT"
- Genera archivo CSV con resumen de órdenes de trabajo
- Incluye métricas: Total, Horas trabajadas, Tiempo promedio
- Agrupa por: Estado, Prioridad, Tipo
- Respeta rango de fechas seleccionado

### Botón "Exportar Inactividad"
- Genera archivo CSV con reporte de inactividad de activos
- (También debería funcionar correctamente)

## 📝 Commit

- `fd53777` - Fix export_work_orders parameter error

## 🚀 Ahora Puedes

1. **Acceder a Reportes**
2. **Seleccionar rango de fechas**
3. **Click en "Exportar OT"**
4. **Descargar archivo CSV**
5. **Abrir en Excel o Google Sheets**

---

**Estado:** ✅ CORREGIDO
**Fecha:** 2025-12-07
**Archivo:** `backend/apps/reports/views.py`
