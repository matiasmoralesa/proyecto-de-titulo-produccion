# Verificar Roles de Usuarios en Producción

## 🔍 Problema

El sidebar sigue mostrando todas las opciones para "operador1", lo que significa que este usuario **NO tiene rol OPERADOR** en la base de datos.

## ✅ Solución: Verificar y Corregir Roles

### Paso 1: Verificar Roles en Railway Shell

1. Ve a https://railway.app
2. Abre tu proyecto
3. Selecciona el servicio de Django
4. Haz clic en la pestaña **"Shell"**
5. Ejecuta este código:

```python
from apps.authentication.models import User, Role

# Ver todos los usuarios y sus roles
users = User.objects.all()
for user in users:
    print(f"{user.username}: {user.role.name}")
```

### Paso 2: Corregir el Rol del Usuario

Si "operador1" NO tiene rol OPERADOR, corrígelo:

```python
from apps.authentication.models import User, Role

# Obtener el rol OPERADOR
operador_role = Role.objects.get(name='OPERADOR')

# Obtener el usuario
user = User.objects.get(username='operador1')

# Ver rol actual
print(f"Rol actual: {user.role.name}")

# Cambiar a OPERADOR
user.role = operador_role
user.save()

print(f"Rol nuevo: {user.role.name}")
```

### Paso 3: Verificar en la App

1. Cierra sesión en la app
2. Vuelve a iniciar sesión como "operador1"
3. Verifica el sidebar → Deberías ver SOLO 4 opciones

## 📊 Resultado Esperado

Después de corregir el rol, el sidebar del operador debería mostrar:

```
┌─────────────────────┐
│ 🏠 Dashboard        │
│ 🚚 Activos          │
│ 📋 Órdenes de Trab. │
│ 🔔 Notificaciones   │
└─────────────────────┘
```

**SOLO 4 opciones**, no 14.

## 🎯 Explicación

El código del sidebar está funcionando correctamente. El problema es que:

1. ✅ El código filtra por rol correctamente
2. ✅ El deployment se aplicó en Vercel
3. ❌ El usuario "operador1" tiene rol ADMIN o SUPERVISOR en la base de datos

Por eso ve todas las opciones.

## 🔧 Alternativa: Crear un Nuevo Usuario Operador

Si no quieres modificar "operador1", crea un nuevo usuario:

```python
from apps.authentication.models import User, Role

# Obtener rol OPERADOR
operador_role = Role.objects.get(name='OPERADOR')

# Crear nuevo usuario
new_user = User.objects.create_user(
    username='operador_test',
    email='operador_test@example.com',
    password='test123',
    first_name='Operador',
    last_name='Test',
    role=operador_role
)

print(f"Usuario creado: {new_user.username} con rol {new_user.role.name}")
```

Luego inicia sesión con:
- Usuario: `operador_test`
- Contraseña: `test123`

---

**Próximo paso**: Ejecuta el código del Paso 1 en Railway Shell para ver qué rol tiene realmente "operador1".
