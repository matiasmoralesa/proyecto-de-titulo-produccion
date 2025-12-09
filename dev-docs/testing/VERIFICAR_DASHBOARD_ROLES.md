# Verificación de Filtrado de Dashboard por Roles

## 🎯 Cambio Implementado

Se corrigió el endpoint del dashboard para que filtre correctamente los datos según el rol del usuario:

- **ADMIN**: Ve todos los datos del sistema
- **SUPERVISOR**: Ve todos los datos (puede ser filtrado por departamento en el futuro)
- **OPERADOR**: Solo ve sus órdenes de trabajo asignadas y activos relacionados

## 📋 Archivo Modificado

- `backend/apps/core/dashboard_views.py`

## ✅ Verificación Local

Ya se verificó localmente que el filtrado funciona correctamente:

```
✅ El dashboard está filtrando correctamente por roles
✅ Los operadores solo ven sus datos asignados
```

## 🚀 Despliegue a Producción

### Paso 1: Verificar que Railway detectó el cambio

1. Ve a https://railway.app
2. Abre tu proyecto
3. Ve a la pestaña "Deployments"
4. Deberías ver un nuevo deployment con el mensaje:
   ```
   fix: Aplicar filtrado por roles en dashboard - Los operadores ahora solo ven sus datos asignados
   ```

### Paso 2: Esperar a que termine el deployment

- El deployment puede tardar 2-5 minutos
- Espera a que el estado cambie a "Success" ✅

### Paso 3: Verificar en producción

#### Como ADMIN:
1. Inicia sesión como admin
2. Ve al Dashboard
3. Deberías ver **TODOS** los datos del sistema

#### Como OPERADOR:
1. Inicia sesión como operador (por ejemplo: operador2)
2. Ve al Dashboard
3. Deberías ver **SOLO**:
   - Tus órdenes de trabajo asignadas
   - Los activos relacionados con tus órdenes
   - Las predicciones de esos activos

## 🔍 Qué Cambió Exactamente

### Antes:
```python
# Todos los usuarios veían los mismos datos globales
total_assets = Asset.objects.count()
total_work_orders = WorkOrder.objects.count()
```

### Después:
```python
# Los datos se filtran según el rol del usuario
if role_name == Role.OPERADOR:
    # Operadores solo ven sus órdenes asignadas
    work_orders_qs = WorkOrder.objects.filter(assigned_to=user)
    
    # Y los activos relacionados
    assigned_asset_ids = work_orders_qs.values_list('asset_id', flat=True).distinct()
    assets_qs = Asset.objects.filter(id__in=assigned_asset_ids)
```

## 📊 Ejemplo de Datos Esperados

Si un operador tiene asignadas 3 órdenes de trabajo que involucran 3 activos diferentes:

**Dashboard del Operador mostrará:**
- Total de Activos: **3** (no 7)
- Total de Órdenes de Trabajo: **3** (no 10)
- Predicciones: **Solo de esos 3 activos**

**Dashboard del Admin mostrará:**
- Total de Activos: **7** (todos)
- Total de Órdenes de Trabajo: **10** (todas)
- Predicciones: **Todas**

## ⚠️ Nota Importante

El caché del dashboard ahora es **por usuario y rol**, lo que significa:
- Cada usuario tiene su propio caché
- Los datos se actualizan cada 5 minutos
- Si haces cambios, puede tardar hasta 5 minutos en reflejarse

## 🐛 Si algo no funciona

1. **Verifica que el deployment terminó exitosamente**
   - Ve a Railway → Deployments
   - Confirma que el último deployment está en "Success"

2. **Limpia el caché del navegador**
   - Presiona Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)
   - O abre en modo incógnito

3. **Verifica los logs de Railway**
   ```bash
   # En Railway, ve a la pestaña "Logs"
   # Busca errores relacionados con dashboard_views
   ```

4. **Verifica que el usuario tiene el rol correcto**
   - Ve a la sección de Usuarios
   - Confirma que el operador tiene rol "OPERADOR"

## 📝 Próximos Pasos (Opcional)

Si quieres filtrar también los datos del supervisor por departamento/área:

1. Agrega un campo `department` o `area` al modelo User
2. Modifica el filtrado en `dashboard_views.py`:
   ```python
   elif role_name == Role.SUPERVISOR:
       # Filtrar por departamento del supervisor
       work_orders_qs = WorkOrder.objects.filter(
           assigned_to__department=user.department
       )
   ```

## ✅ Checklist de Verificación

- [ ] Deployment en Railway completado exitosamente
- [ ] Login como ADMIN → Dashboard muestra todos los datos
- [ ] Login como OPERADOR → Dashboard muestra solo datos asignados
- [ ] Los números en el dashboard del operador son menores que los del admin
- [ ] No hay errores en los logs de Railway
- [ ] El frontend se ve correctamente (sin errores de consola)

---

**Fecha de implementación:** 2 de diciembre de 2025
**Commit:** `fix: Aplicar filtrado por roles en dashboard`
