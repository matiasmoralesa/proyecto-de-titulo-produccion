# Ejecutar Corrección de Roles en Railway

## 🎯 Objetivo

Corregir los roles de los usuarios "operador1", "operador2" y "operador3" para que tengan rol **OPERADOR** en la base de datos de producción.

## ⏰ Espera el Deployment

Primero, espera a que Railway termine de desplegar el nuevo código (1-2 minutos).

## 📋 Pasos para Ejecutar el Comando

### Paso 1: Abre Railway Dashboard

1. Ve a https://railway.app
2. Inicia sesión
3. Abre tu proyecto: **vibrant-vitality**
4. Selecciona el servicio de Django (proyecto-de-titulo-produccion)

### Paso 2: Abre el Shell

1. Haz clic en la pestaña **"Shell"** (arriba, junto a "Deployments", "Logs", etc.)
2. Espera a que se abra el terminal

### Paso 3: Ejecuta el Comando

En el shell de Railway, escribe:

```bash
python manage.py fix_operator_roles
```

Presiona **Enter**.

### Paso 4: Verifica la Salida

Deberías ver algo como:

```
================================================================================
VERIFICACIÓN DE ROLES DE USUARIOS
================================================================================

📋 Usuarios actuales:

   admin                → Rol: ADMIN
   supervisor1          → Rol: SUPERVISOR
   operador1            → Rol: ADMIN  (o SUPERVISOR)
   operador2            → Rol: OPERADOR
   operador3            → Rol: OPERADOR

================================================================================
CORRECCIÓN DE ROLES
================================================================================

✅ Rol OPERADOR encontrado: OPERADOR

✅ operador1             → Cambiado de ADMIN a OPERADOR
✓  operador2             → Ya tiene rol OPERADOR
✓  operador3             → Ya tiene rol OPERADOR

================================================================================
VERIFICACIÓN FINAL
================================================================================

   operador1            → Rol: OPERADOR
   operador2            → Rol: OPERADOR
   operador3            → Rol: OPERADOR

================================================================================
✅ Proceso completado
```

## ✅ Verificar en la App

Después de ejecutar el comando:

1. Ve a tu app en producción
2. Cierra sesión si estás logueado
3. Inicia sesión como **operador1**
4. Verifica el sidebar → Deberías ver **SOLO 4 opciones**:
   - Dashboard
   - Activos
   - Órdenes de Trabajo
   - Notificaciones

## 🐛 Si Algo Sale Mal

### Error: "Command not found"

Espera 1-2 minutos más a que Railway termine el deployment y vuelve a intentar.

### Error: "Role OPERADOR does not exist"

Ejecuta primero:

```bash
python manage.py shell
```

Luego:

```python
from apps.authentication.models import Role
roles = Role.objects.all()
for role in roles:
    print(role.name)
exit()
```

Esto te mostrará qué roles existen en la base de datos.

### El comando se ejecutó pero el sidebar sigue igual

1. Cierra sesión en la app
2. Limpia el caché del navegador (Ctrl+Shift+R)
3. Vuelve a iniciar sesión como operador1

## 📊 Resultado Esperado

Después de ejecutar el comando y volver a iniciar sesión, el sidebar del operador debería mostrar:

```
┌─────────────────────┐
│ 🏠 Dashboard        │
│ 🚚 Activos          │
│ 📋 Órdenes de Trab. │
│ 🔔 Notificaciones   │
└─────────────────────┘
```

**SOLO 4 opciones**, no 14.

---

**Próximo paso**: Ejecuta el comando en Railway Shell y avísame qué salida te da.
