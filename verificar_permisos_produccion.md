# 🔐 Verificación y Corrección del Sistema de Permisos en Producción

## 📋 Problema Identificado

Los cambios del sistema de permisos por roles (RBAC) del commit `8f4aaff` no se están aplicando en producción.

## ✅ Verificación Paso a Paso

### 1. Verificar que el Código Está en Railway

1. Ve a https://railway.app/
2. Abre tu proyecto
3. Click en el servicio Django
4. Ve a "Deployments"
5. Click en el deployment activo
6. Ve a la pestaña "Source"
7. **Verifica que el commit sea:** `39b0616` o posterior

**Si el commit es anterior a `8f4aaff`:**
- Railway no tiene los cambios de permisos
- Necesitas forzar un re-deploy

### 2. Verificar Migraciones de Base de Datos

El sistema de permisos requiere la tabla `AccessLog`. Verifica que exista:

**En Railway Shell:**
```bash
cd backend && python manage.py showmigrations configuration
```

**Debe mostrar:**
```
configuration
 [X] 0001_initial
 [X] 0002_add_access_log_model
```

**Si `0002_add_access_log_model` tiene `[ ]` (sin aplicar):**

```bash
cd backend && python manage.py migrate configuration
```

### 3. Verificar Archivos de Permisos

**En Railway Shell, verifica que existan estos archivos:**

```bash
# Verificar permissions.py
ls -la backend/apps/core/permissions.py

# Verificar mixins.py
ls -la backend/apps/core/mixins.py

# Verificar middleware de auditoría
ls -la backend/apps/core/audit.py
```

**Si algún archivo no existe:**
- El código no se deployó correctamente
- Necesitas forzar un re-deploy

### 4. Verificar Frontend

**Verifica que estos componentes existan en Vercel:**

1. Ve a https://vercel.com/
2. Abre tu proyecto
3. Ve a "Deployments" → Click en el activo
4. Ve a "Source"
5. **Verifica que existan:**
   - `frontend/src/components/auth/PermissionGuard.tsx`
   - `frontend/src/routes/ProtectedRoute.tsx`

**Si no existen:**
- El frontend no tiene los cambios
- Necesitas forzar un re-deploy

---

## 🔧 Soluciones

### Solución 1: Forzar Re-Deploy en Railway

Si el código está en GitHub pero no en Railway:

1. Ve a Railway Dashboard
2. Click en tu servicio Django
3. Ve a "Settings"
4. Scroll hasta "Service"
5. Click en "Redeploy"
6. Espera a que termine (luz verde)

### Solución 2: Aplicar Migraciones Manualmente

Si las migraciones no se aplicaron:

**Opción A: Desde Railway Dashboard**

1. Ve a Railway Dashboard
2. Click en tu servicio Django
3. Ve a "Deployments"
4. Click en el deployment activo
5. En la consola/shell ejecuta:

```bash
cd backend && python manage.py migrate
```

**Opción B: Desde Railway CLI (si lo tienes instalado)**

```bash
railway run python backend/manage.py migrate
```

### Solución 3: Verificar Variables de Entorno

El sistema de permisos puede tener un feature flag. Verifica:

1. Ve a Railway Dashboard
2. Click en tu servicio Django
3. Ve a "Variables"
4. **Busca:** `ENABLE_RBAC`

**Si existe y está en `False`:**
- Cámbialo a `True`
- Railway re-deployará automáticamente

**Si no existe:**
- No es necesario, el sistema debería estar activo por defecto

### Solución 4: Forzar Re-Deploy en Vercel

Si el frontend no tiene los cambios:

1. Ve a Vercel Dashboard
2. Abre tu proyecto
3. Ve a "Deployments"
4. Click en los tres puntos (...) del último deployment
5. Click en "Redeploy"
6. Espera a que termine

---

## 🧪 Pruebas de Verificación

Una vez que hayas aplicado las soluciones, verifica:

### Backend - Permisos Funcionando

**Test 1: Endpoint de Configuración (Solo Admins)**

```bash
# Sin autenticación - debe dar 401
curl https://TU-URL.railway.app/api/v1/configuration/categories/

# Con token de operador - debe dar 403
curl -H "Authorization: Bearer TOKEN_OPERADOR" \
  https://TU-URL.railway.app/api/v1/configuration/categories/

# Con token de admin - debe dar 200
curl -H "Authorization: Bearer TOKEN_ADMIN" \
  https://TU-URL.railway.app/api/v1/configuration/categories/
```

**Test 2: Work Orders Filtradas por Rol**

```bash
# Como operador - solo debe ver sus OT
curl -H "Authorization: Bearer TOKEN_OPERADOR" \
  https://TU-URL.railway.app/api/v1/work-orders/

# Como admin - debe ver todas las OT
curl -H "Authorization: Bearer TOKEN_ADMIN" \
  https://TU-URL.railway.app/api/v1/work-orders/
```

### Frontend - Componentes de Permisos

**Test 1: Sidebar Adaptado**

1. Login como **Operador**
2. **Debe ver:**
   - Dashboard
   - Mis Órdenes de Trabajo
   - Mis Activos
3. **NO debe ver:**
   - Configuración
   - Usuarios
   - Reportes Globales

**Test 2: Login como Supervisor**

1. Login como **Supervisor**
2. **Debe ver:**
   - Dashboard
   - Órdenes de Trabajo (de su equipo)
   - Activos (de su área)
   - Reportes (de su equipo)
3. **NO debe ver:**
   - Configuración
   - Usuarios (excepto su equipo)

**Test 3: Login como Admin**

1. Login como **Admin**
2. **Debe ver:**
   - TODO el menú
   - Configuración
   - Usuarios
   - Reportes Globales

---

## 📊 Checklist de Verificación

```
Código en Repositorio:
[ ] Commit 8f4aaff está en GitHub
[ ] Commit 39b0616 está en GitHub

Railway (Backend):
[ ] Deployment activo es 39b0616 o posterior
[ ] Archivo permissions.py existe
[ ] Archivo mixins.py existe
[ ] Archivo audit.py existe
[ ] Migración 0002_add_access_log_model aplicada
[ ] Tabla AccessLog existe en base de datos

Vercel (Frontend):
[ ] Deployment activo incluye componentes de permisos
[ ] PermissionGuard.tsx existe
[ ] ProtectedRoute.tsx existe
[ ] Sidebar.tsx actualizado con filtrado

Funcionalidad:
[ ] Operadores solo ven sus datos
[ ] Supervisores ven su equipo
[ ] Admins ven todo
[ ] Configuración solo accesible para admins
[ ] Sidebar se adapta según rol
[ ] Audit logs se registran
```

---

## 🐛 Troubleshooting

### Error: "Permission denied" para todos los usuarios

**Causa:** Usuarios no tienen rol asignado

**Solución:**
```bash
# En Railway Shell
cd backend && python manage.py shell

# Ejecutar:
from apps.authentication.models import User, Role
admin_role = Role.objects.get(name='ADMIN')
for user in User.objects.filter(role__isnull=True):
    user.role = admin_role
    user.save()
```

### Error: "AccessLog table doesn't exist"

**Causa:** Migración no aplicada

**Solución:**
```bash
cd backend && python manage.py migrate configuration
```

### Error: "PermissionGuard is not defined" en frontend

**Causa:** Frontend no tiene los cambios

**Solución:**
1. Verifica que el código esté en GitHub
2. Fuerza re-deploy en Vercel
3. Limpia cache del navegador

---

## 📞 Siguiente Paso

1. **Ejecuta las verificaciones** de la sección "Verificación Paso a Paso"
2. **Anota qué falla** (código no está, migraciones no aplicadas, etc.)
3. **Aplica la solución correspondiente**
4. **Ejecuta las pruebas de verificación**

¿Qué encontraste en la verificación?
