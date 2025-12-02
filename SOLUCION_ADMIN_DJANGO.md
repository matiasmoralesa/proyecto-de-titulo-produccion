# Solución: Corregir Roles desde Admin de Django

## 🎯 Objetivo

Cambiar el rol de "operador1" a OPERADOR desde el Admin de Django.

## 📋 Pasos

### 1. Accede al Admin de Django

1. Abre tu navegador
2. Ve a: `https://tu-app.railway.app/admin/`
3. Inicia sesión como **admin**

### 2. Ve a Usuarios

1. En el menú lateral, busca **"AUTHENTICATION"** o **"Autenticación"**
2. Haz clic en **"Users"** o **"Usuarios"**

### 3. Busca y Edita "operador1"

1. En la lista de usuarios, busca **"operador1"**
2. Haz clic en el nombre para editarlo

### 4. Cambia el Rol

1. Busca el campo **"Role"** o **"Rol"**
2. En el dropdown, selecciona **"OPERADOR"**
3. Haz scroll hasta abajo
4. Haz clic en **"Save"** o **"Guardar"**

### 5. Repite para otros operadores (opcional)

Si quieres, repite los pasos 3-4 para:
- operador2
- operador3

### 6. Verifica en la App

1. Ve a tu app en producción
2. Cierra sesión si estás logueado
3. Inicia sesión como **operador1**
4. Verifica el sidebar → Deberías ver **SOLO 4 opciones**:
   - Dashboard
   - Activos
   - Órdenes de Trabajo
   - Notificaciones

## ✅ Resultado Esperado

Después de cambiar el rol, el sidebar del operador debería mostrar:

```
┌─────────────────────┐
│ 🏠 Dashboard        │
│ 🚚 Activos          │
│ 📋 Órdenes de Trab. │
│ 🔔 Notificaciones   │
└─────────────────────┘
```

**SOLO 4 opciones**, no 14.

## 🐛 Si No Funciona

### El sidebar sigue mostrando todas las opciones

1. Cierra sesión completamente
2. Limpia el caché del navegador (Ctrl+Shift+R)
3. Abre en modo incógnito
4. Vuelve a iniciar sesión como operador1

### No puedo acceder al Admin

Verifica que:
- Estás usando el usuario admin correcto
- La URL es correcta: `https://tu-app.railway.app/admin/`
- El servicio de Railway está corriendo

---

**Esta es la forma más fácil y visual de cambiar el rol.** Solo toma 1 minuto.
