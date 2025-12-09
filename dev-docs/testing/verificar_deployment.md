# 🔍 Verificación de Deployment - Correcciones Dashboard, Notificaciones y Configuración

## 📋 URLs del Proyecto

Basándome en tu repositorio `proyecto-de-titulo-produccion`, tus URLs deberían ser:

**Backend (Railway):**
```
https://proyecto-de-titulo-produccion-production.up.railway.app
```

**Frontend (Vercel):**
```
https://proyecto-de-titulo-produccion.vercel.app
```

---

## ✅ Checklist de Verificación

### 1. Verificar que el Deployment Terminó

**Railway:**
1. Ve a https://railway.app/
2. Abre tu proyecto
3. Verifica que todos los servicios tengan luz verde 🟢:
   - Django Backend
   - PostgreSQL
   - Redis
   - Celery Worker
   - Celery Beat

**Vercel:**
1. Ve a https://vercel.com/
2. Abre tu proyecto
3. Ve a "Deployments"
4. El último deployment debe estar "Ready" ✅

---

### 2. Verificar Backend (Railway)

Abre estas URLs en tu navegador (reemplaza con tu URL real):

#### A. Health Check
```
https://TU-URL.railway.app/api/v1/health/
```
**Debe responder:** `{"status": "ok"}` o similar

#### B. API Documentation
```
https://TU-URL.railway.app/api/docs/
```
**Debe mostrar:** Swagger UI con la documentación de la API

#### C. Dashboard Stats (requiere autenticación)
```
https://TU-URL.railway.app/api/v1/dashboard/stats/
```
**Debe devolver:** JSON con KPIs

#### D. Configuration Endpoints (nuevos)
```
https://TU-URL.railway.app/api/v1/configuration/categories/
https://TU-URL.railway.app/api/v1/configuration/priorities/
https://TU-URL.railway.app/api/v1/configuration/work-order-types/
https://TU-URL.railway.app/api/v1/configuration/parameters/
```
**Debe responder:** JSON con datos o lista vacía

---

### 3. Verificar Frontend (Vercel)

#### A. Página Principal
```
https://TU-URL.vercel.app/
```
**Debe mostrar:** Página de login o dashboard

#### B. Login
```
https://TU-URL.vercel.app/login
```
**Debe mostrar:** Formulario de login

---

### 4. Verificar Funcionalidades Nuevas (Después de Login)

Una vez que hayas iniciado sesión:

#### A. Dashboard KPIs ✅
1. Ve al Dashboard
2. **Verificar:**
   - [ ] NO hay valores negativos en los KPIs
   - [ ] Todos los valores son >= 0
   - [ ] Los porcentajes están entre 0-100%

**Ejemplo de KPIs correctos:**
```
✅ Disponibilidad: 85.5%
✅ Tasa de Completitud: 72.3%
✅ Duración Promedio: 3.2 días (NO -12.5 días)
✅ Ratio Preventivo: 65.0%
```

#### B. Navegación de Notificaciones ✅
1. Click en el ícono de notificaciones (🔔)
2. **Prueba 1 - Notificación válida:**
   - Click en una notificación de una orden de trabajo existente
   - **Debe:** Navegar a la página de detalle de la OT
   - **NO debe:** Mostrar error 404

3. **Prueba 2 - Notificación de objeto eliminado:**
   - Si tienes notificaciones de objetos eliminados
   - Click en la notificación
   - **Debe:** Mostrar mensaje de error tipo toast
   - **Debe:** Marcar la notificación como leída
   - **NO debe:** Navegar a página 404

#### C. Página de Configuración ✅
1. Ve a **Configuración** en el menú lateral
2. **Verificar pestañas:**
   - [ ] Categorías de Activos
   - [ ] Prioridades
   - [ ] Tipos de Órdenes de Trabajo
   - [ ] Parámetros del Sistema

3. **Prueba CRUD - Categorías:**
   - Click en "Nueva Categoría"
   - **Verificar formulario tiene:**
     - [ ] Campo Código (requerido)
     - [ ] Campo Nombre (requerido)
     - [ ] Campo Descripción (opcional)
     - [ ] Campo Activo (checkbox)
   - Intenta crear sin llenar campos requeridos
   - **Debe:** Mostrar mensajes de error
   - Llena todos los campos y guarda
   - **Debe:** Mostrar mensaje de éxito
   - **Debe:** Aparecer en la tabla

4. **Prueba CRUD - Prioridades:**
   - Click en pestaña "Prioridades"
   - Click en "Nueva Prioridad"
   - **Verificar formulario tiene:**
     - [ ] Campo Nivel (número, requerido)
     - [ ] Campo Nombre (requerido)
     - [ ] Campo Color (con selector de color)
     - [ ] Campo Descripción (opcional)
   - Intenta poner un color inválido (ej: "rojo")
   - **Debe:** Mostrar error de validación
   - Usa el selector de color
   - **Debe:** Aceptar formato #RRGGBB

5. **Prueba CRUD - Parámetros:**
   - Click en pestaña "Parámetros del Sistema"
   - Click en editar un parámetro
   - Si el parámetro NO es editable:
     - **Debe:** Mostrar mensaje de advertencia
     - **Debe:** Deshabilitar campos
   - Si el parámetro ES editable:
     - **Debe:** Permitir edición
     - **Debe:** Validar tipo de dato (integer, float, boolean, json)

---

### 5. Verificar Logs en Railway (Si hay problemas)

Si algo no funciona:

1. Ve a Railway Dashboard
2. Click en tu servicio Django
3. Ve a "Deployments"
4. Click en el deployment activo (el más reciente)
5. Scroll hasta "Logs"
6. Busca líneas en rojo (errores)

**Errores comunes:**
- `ModuleNotFoundError`: Falta instalar dependencia
- `OperationalError`: Problema con base de datos
- `CORS error`: Problema de configuración CORS
- `500 Internal Server Error`: Error en el código

---

### 6. Verificar Migraciones de Base de Datos

Las nuevas tablas de configuración deben existir:

1. Ve a Railway Dashboard
2. Click en tu servicio Django
3. Ve a "Deployments" → Click en el activo
4. En la consola/shell ejecuta:
```bash
cd backend && python manage.py showmigrations configuration
```

**Debe mostrar:**
```
configuration
 [X] 0001_initial
 [X] 0002_add_access_log_model
```

Si hay migraciones sin aplicar `[ ]`, ejecuta:
```bash
cd backend && python manage.py migrate
```

---

## 📊 Resumen de Cambios Desplegados

### Commit: `39b0616`
**Título:** Tests de propiedades (8/8 pasando)
**Archivos:**
- `backend/apps/configuration/tests/test_validation_properties.py`
- `backend/apps/core/tests/test_dashboard_properties.py`
- `backend/apps/notifications/tests/test_navigation_properties.py`

### Commit: `d29915b`
**Título:** Correcciones principales
**Cambios:**
1. **Dashboard KPIs:**
   - Validación de fechas
   - Logging de errores
   - Eliminación de valores negativos

2. **Notificaciones:**
   - Validación antes de navegar
   - Manejo de errores con toasts
   - Marca como leída incluso si falla

3. **Configuración:**
   - Modelos: AssetCategory, Priority, WorkOrderType, SystemParameter
   - Serializers con validación
   - Viewsets con CRUD completo
   - Formularios en frontend

---

## ✅ Checklist Final

```
Deployment:
[ ] Railway: Todos los servicios 🟢
[ ] Vercel: Deployment exitoso ✅
[ ] Backend responde: /api/v1/health/
[ ] Frontend carga correctamente

Funcionalidades:
[ ] Dashboard: KPIs sin valores negativos
[ ] Notificaciones: Navegación funciona
[ ] Notificaciones: Errores se manejan correctamente
[ ] Configuración: 4 pestañas visibles
[ ] Configuración: CRUD de categorías funciona
[ ] Configuración: CRUD de prioridades funciona
[ ] Configuración: Validación de formularios funciona
[ ] Configuración: Selector de color funciona

Base de Datos:
[ ] Migraciones aplicadas
[ ] Tablas de configuración creadas
[ ] Datos se guardan correctamente
```

---

## 🐛 Troubleshooting

### Problema: "Cannot connect to backend"
**Solución:**
1. Verifica que Railway esté corriendo
2. Verifica CORS en Railway variables:
   ```
   CORS_ALLOWED_ORIGINS=https://tu-proyecto.vercel.app
   ALLOWED_HOSTS=*.railway.app,tu-proyecto.vercel.app
   ```

### Problema: "404 Not Found en /api/v1/configuration/"
**Solución:**
1. Verifica que las migraciones estén aplicadas
2. Verifica que las URLs estén registradas en `config/urls.py`
3. Reinicia el servicio en Railway

### Problema: "KPIs siguen mostrando valores negativos"
**Solución:**
1. Verifica que el código de `dashboard_views.py` esté actualizado
2. Limpia el cache de Redis:
   - En Railway Shell: `redis-cli FLUSHALL`
3. Reinicia el servicio Django

### Problema: "Formularios de configuración no aparecen"
**Solución:**
1. Verifica que el frontend se haya re-deployado en Vercel
2. Limpia cache del navegador (Ctrl+Shift+R)
3. Verifica que `VITE_API_URL` esté configurado en Vercel

---

## 📞 Siguiente Paso

**Copia este checklist y ve marcando cada item mientras verificas.**

Si encuentras algún problema, anótalo y podemos resolverlo juntos.

¿Todo funciona correctamente? ✅
