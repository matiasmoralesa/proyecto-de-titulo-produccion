# 🚀 Deployment Dashboard con Datos Reales

## ✅ Resumen de Cambios

### Backend
- ✅ 4 funciones nuevas para generar datos de gráficos
- ✅ Endpoint `/dashboard/stats/` actualizado con campo `charts`
- ✅ Datos reales de los últimos 6 meses (órdenes) y 4 semanas (predicciones)
- ✅ Respeta permisos por rol (charts solo para Supervisor/Admin)

### Frontend
- ✅ Eliminados todos los datos mock
- ✅ Usa 100% datos reales del backend
- ✅ Mensajes amigables cuando no hay datos
- ✅ Validación de datos antes de renderizar

## 🚀 Comandos de Deployment

### Opción 1: Deployment Rápido (10 minutos)

```bash
# 1. Verificar que todo compila
cd frontend
npm run build
cd ..

# 2. Commit de cambios
git add backend/apps/core/dashboard_views.py
git add frontend/src/pages/Dashboard.tsx
git add backend/clear_dashboard_cache.py
git add DATOS_REALES_DASHBOARD.md
git add DEPLOYMENT_DATOS_REALES.md

git commit -m "feat: Implementar datos reales en dashboard

Backend:
- Agregar funciones para generar datos de gráficos
- Actualizar endpoint con campo charts
- Datos de últimos 6 meses y 4 semanas

Frontend:
- Eliminar datos mock
- Usar datos reales del API
- Agregar validación y mensajes sin datos"

# 3. Push a producción
git push origin main

# 4. Esperar deployment (5 minutos)
# Railway: ~2-3 minutos
# Vercel: ~2-3 minutos

# 5. Limpiar caché en Railway (IMPORTANTE)
# Opción A: Desde Railway Dashboard
#   - Ir a tu proyecto en Railway
#   - Abrir Shell
#   - Ejecutar: python clear_dashboard_cache.py

# Opción B: Desde local (si tienes Railway CLI)
railway run python clear_dashboard_cache.py
```

### Opción 2: Deployment con Preview (15 minutos)

```bash
# 1. Crear rama
git checkout -b feature/dashboard-real-data

# 2. Commit
git add .
git commit -m "feat: Implementar datos reales en dashboard"

# 3. Push
git push origin feature/dashboard-real-data

# 4. Crear Pull Request en GitHub

# 5. Vercel creará preview automáticamente

# 6. Revisar preview

# 7. Hacer merge a main

# 8. Limpiar caché en Railway
railway run python clear_dashboard_cache.py
```

## 📋 Checklist de Deployment

### Pre-Deployment
- [x] Backend actualizado con funciones de gráficos
- [x] Frontend actualizado sin datos mock
- [x] Build local exitoso
- [x] Sin errores de TypeScript
- [x] Sin errores de Python

### Durante Deployment
- [ ] Push a GitHub exitoso
- [ ] Railway build exitoso
- [ ] Vercel build exitoso
- [ ] Sin errores en logs

### Post-Deployment (CRÍTICO)
- [ ] **Limpiar caché del dashboard** (ver comandos abajo)
- [ ] Verificar endpoint `/dashboard/stats/`
- [ ] Verificar gráficos en frontend
- [ ] Probar con Admin
- [ ] Probar con Supervisor
- [ ] Probar con Operador

## 🔧 Limpiar Caché (IMPORTANTE)

### Opción 1: Railway Dashboard (Recomendado)

1. Ir a https://railway.app/dashboard
2. Seleccionar tu proyecto
3. Click en "Shell" o "Terminal"
4. Ejecutar:
   ```bash
   python clear_dashboard_cache.py
   ```

### Opción 2: Railway CLI

```bash
# Instalar Railway CLI (si no está instalado)
npm i -g @railway/cli

# Login
railway login

# Ejecutar script
railway run python clear_dashboard_cache.py
```

### Opción 3: Django Shell Manual

```bash
# En Railway Shell
python manage.py shell

# Ejecutar en Python
>>> from django.core.cache import cache
>>> cache.clear()
>>> print("✅ Caché limpiado")
>>> exit()
```

## ✅ Verificaciones Post-Deployment

### 1. Verificar Backend (Railway)

```bash
# Verificar que el endpoint responde
curl -X GET https://tu-api.railway.app/api/dashboard/stats/ \
  -H "Authorization: Bearer TU_TOKEN"

# Debe retornar JSON con campo "charts"
```

### 2. Verificar Frontend (Vercel)

1. [ ] Abrir https://tu-proyecto.vercel.app
2. [ ] Login como Admin
3. [ ] Ir al Dashboard
4. [ ] Verificar que se muestran 4 gráficos
5. [ ] Verificar que tienen datos reales
6. [ ] No hay errores en consola

### 3. Verificar por Rol

#### Como Admin:
- [ ] Ve header con quick stats
- [ ] Ve KPIs de activos
- [ ] Ve órdenes de trabajo
- [ ] Ve 4 gráficos con datos reales
- [ ] Ve 8 KPIs premium

#### Como Supervisor:
- [ ] Ve header con quick stats
- [ ] Ve KPIs de activos
- [ ] Ve órdenes del equipo
- [ ] Ve 4 gráficos con datos reales
- [ ] Ve KPIs del equipo

#### Como Operador:
- [ ] Ve header con quick stats
- [ ] Ve sus activos
- [ ] Ve sus órdenes
- [ ] NO ve gráficos
- [ ] NO ve KPIs avanzados

## 🐛 Troubleshooting

### Problema: Gráficos vacíos después del deployment

**Causa:** Caché no limpiado
**Solución:**
```bash
railway run python clear_dashboard_cache.py
```

### Problema: Error 500 en /dashboard/stats/

**Causa:** Error en queries del backend
**Solución:**
```bash
# Ver logs de Railway
railway logs

# Verificar que no hay errores de sintaxis
cd backend
python manage.py check
```

### Problema: Frontend muestra "No hay datos disponibles"

**Posibles causas:**
1. No hay datos históricos en la BD
2. Caché no limpiado
3. Error en el backend

**Solución:**
```bash
# 1. Verificar que el backend retorna datos
curl https://tu-api.railway.app/api/dashboard/stats/ \
  -H "Authorization: Bearer TOKEN"

# 2. Limpiar caché
railway run python clear_dashboard_cache.py

# 3. Si no hay datos, generar datos de prueba
python manage.py seed_all_data
```

### Problema: Gráficos se muestran para Operador

**Causa:** Error en lógica de permisos
**Solución:**
- Verificar que el usuario tiene rol OPERADOR
- Revisar logs del backend
- Verificar que el endpoint retorna charts=null para operadores

## 📊 Datos Esperados

### Si hay datos en el sistema:
- **Tendencia de OT:** 6 barras (últimos 6 meses)
- **Distribución de Activos:** 3 segmentos (Operativo, Mantenimiento, Detenido)
- **Tipos de Mantenimiento:** 4 barras (Preventivo, Correctivo, Predictivo, Emergencia)
- **Timeline de Predicciones:** 4 áreas (últimas 4 semanas)

### Si NO hay datos suficientes:
- Mensaje: "No hay datos disponibles"
- Icono gris
- Sin errores en consola

## 🎯 Próximos Pasos (Opcional)

### Después del deployment exitoso:

1. **Monitorear primeras 24 horas:**
   - Revisar logs de Railway
   - Verificar métricas de Vercel
   - Recopilar feedback de usuarios

2. **Generar datos si es necesario:**
   ```bash
   # Si no hay suficientes datos históricos
   python manage.py seed_all_data
   ```

3. **Optimizar queries (si es lento):**
   - Agregar índices en campos de fecha
   - Implementar paginación
   - Usar select_related

4. **Documentar para usuarios:**
   - Crear guía de uso del dashboard
   - Explicar cada gráfico
   - Compartir con el equipo

## 📝 Notas Finales

### ✅ Ventajas de Datos Reales
- Dashboard refleja estado real del sistema
- Decisiones basadas en datos actuales
- Tendencias y patrones visibles
- Mayor confianza en el sistema

### ⚠️ Consideraciones
- Requiere datos históricos para gráficos significativos
- Caché de 5 minutos (datos pueden estar ligeramente desactualizados)
- Performance depende de cantidad de datos

### 🎉 Resultado Final
- Dashboard 100% funcional con datos reales
- Sin datos mock
- Respeta permisos por rol
- Maneja casos sin datos correctamente
- Listo para producción

---

## 🚀 Comando Final de Deployment

```bash
# Todo en uno (copiar y pegar)
cd frontend && npm run build && cd .. && \
git add . && \
git commit -m "feat: Implementar datos reales en dashboard" && \
git push origin main && \
echo "✅ Push exitoso. Ahora limpia el caché en Railway:"
echo "   railway run python clear_dashboard_cache.py"
```

---

**Fecha:** 6 de Diciembre, 2025
**Versión:** 2.0.0
**Estado:** ✅ Listo para Producción con Datos Reales
**Tiempo estimado:** 10-15 minutos
