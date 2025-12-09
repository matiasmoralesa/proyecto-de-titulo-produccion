# 🔐 Aplicar Sistema de Permisos en Producción

## 📋 Situación Actual

El sistema de permisos por roles (RBAC) está implementado en el código (commit `8f4aaff`) pero necesita ser activado en producción.

## 🎯 Pasos para Aplicar

### Opción 1: Desde Railway Dashboard (Recomendado)

#### Paso 1: Abrir Railway Shell

1. Ve a https://railway.app/
2. Abre tu proyecto
3. Click en el servicio **Django Backend**
4. Ve a la pestaña **"Deployments"**
5. Click en el **deployment activo** (el que tiene luz verde)
6. Scroll hasta abajo hasta encontrar la sección **"Shell"** o **"Console"**

#### Paso 2: Aplicar Migraciones

En la shell de Railway, ejecuta:

```bash
cd backend && python manage.py migrate
```

**Debe mostrar:**
```
Running migrations:
  Applying configuration.0002_add_access_log_model... OK
```

Si ya está aplicada, dirá: `No migrations to apply.`

#### Paso 3: Crear Roles

```bash
cd backend && python manage.py create_roles
```

**Debe crear:**
- ADMIN
- SUPERVISOR  
- OPERADOR

#### Paso 4: Asignar Roles a Usuarios Existentes

```bash
cd backend && python manage.py shell
```

Luego ejecuta este código Python:

```python
from apps.authentication.models import User, Role

# Obtener rol de admin
admin_role = Role.objects.get(name='ADMIN')

# Asignar rol a usuarios sin rol
users_without_role = User.objects.filter(role__isnull=True)
print(f"Usuarios sin rol: {users_without_role.count()}")

for user in users_without_role:
    user.role = admin_role
    user.save()
    print(f"✅ Rol ADMIN asignado a: {user.username}")

# Salir
exit()
```

#### Paso 5: Verificar que Funciona

```bash
cd backend && python manage.py shell
```

```python
from apps.authentication.models import User

# Ver todos los usuarios con sus roles
for user in User.objects.all():
    print(f"{user.username}: {user.role.name if user.role else 'SIN ROL'}")

exit()
```

**Todos los usuarios deben tener un rol asignado.**

---

### Opción 2: Usando el Script Automático

Si Railway permite ejecutar scripts bash:

1. En Railway Shell:
```bash
chmod +x aplicar_permisos_railway.sh
./aplicar_permisos_railway.sh
```

---

### Opción 3: Desde Railway CLI (Si lo tienes instalado)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar migraciones
railway run python backend/manage.py migrate

# Crear roles
railway run python backend/manage.py create_roles

# Asignar roles (ejecutar script Python)
railway run python backend/manage.py shell < assign_roles.py
```

---

## ✅ Verificación Post-Aplicación

### 1. Verificar en Django Admin

1. Ve a: `https://TU-URL.railway.app/admin/`
2. Login con tu superusuario
3. Ve a **"Authentication"** → **"Roles"**
4. **Debe haber 3 roles:**
   - ADMIN
   - SUPERVISOR
   - OPERADOR

5. Ve a **"Users"**
6. **Todos los usuarios deben tener un rol asignado**

### 2. Verificar AccessLog

1. En Django Admin
2. Ve a **"Configuration"** → **"Access logs"**
3. **Debe existir la tabla** (puede estar vacía)

### 3. Verificar Permisos en API

**Test con curl o Postman:**

```bash
# 1. Login como admin y obtener token
curl -X POST https://TU-URL.railway.app/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu-password"}'

# Copia el token de la respuesta

# 2. Intentar acceder a configuración (solo admins)
curl -H "Authorization: Bearer TU_TOKEN" \
  https://TU-URL.railway.app/api/v1/configuration/categories/

# Debe responder 200 OK con datos
```

### 4. Verificar Frontend

1. **Login como Admin**
2. **Verifica que veas:**
   - Menú completo
   - Opción "Configuración"
   - Opción "Usuarios"

3. **Crea un usuario Operador** (si no tienes)
4. **Logout y login como Operador**
5. **Verifica que NO veas:**
   - Configuración
   - Usuarios
   - Reportes Globales

---

## 📊 Checklist de Aplicación

```
Migraciones:
[ ] configuration.0002_add_access_log_model aplicada
[ ] Tabla AccessLog existe

Roles:
[ ] Rol ADMIN existe
[ ] Rol SUPERVISOR existe
[ ] Rol OPERADOR existe

Usuarios:
[ ] Todos los usuarios tienen rol asignado
[ ] Al menos un usuario es ADMIN

Permisos Backend:
[ ] Endpoint /configuration/ requiere admin
[ ] Work orders se filtran por rol
[ ] Assets se filtran por rol
[ ] Predictions se filtran por rol

Permisos Frontend:
[ ] Sidebar se adapta según rol
[ ] Configuración solo visible para admins
[ ] Usuarios solo visible para admins/supervisores
[ ] Dashboard muestra datos según rol
```

---

## 🚨 Si Nada Funciona

Si después de aplicar todo sigue sin funcionar:

### Verificar que el Commit Correcto Está Deployado

```bash
# En Railway Shell
git log --oneline -5
```

**Debe mostrar:**
```
39b0616 test: Agregar tests de propiedades...
6791b7d Docs: Agregar documentación...
d29915b Fix: Corregir KPIs negativos...
...
8f4aaff feat: Implementación completa del sistema de permisos por roles (RBAC)
```

**Si NO aparece el commit `8f4aaff`:**

El código de permisos no está en Railway. Necesitas:

1. Verificar que esté en GitHub:
```bash
git log --oneline --all | grep "8f4aaff"
```

2. Si está en GitHub pero no en Railway:
   - Forzar re-deploy en Railway
   - O hacer un commit vacío para trigger:
   ```bash
   git commit --allow-empty -m "trigger: Force redeploy"
   git push origin main
   ```

---

## 📞 Siguiente Paso

**Ejecuta los pasos de "Opción 1: Desde Railway Dashboard"** y anota:

1. ¿Las migraciones se aplicaron correctamente?
2. ¿Los roles se crearon?
3. ¿Los usuarios tienen roles asignados?
4. ¿Qué errores aparecen (si los hay)?

Con esa información puedo ayudarte a resolver cualquier problema específico.
