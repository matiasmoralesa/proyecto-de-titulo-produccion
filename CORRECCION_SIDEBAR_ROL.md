# Corrección del Sidebar por Rol

## Problema Identificado

El sidebar no se estaba filtrando correctamente para el rol OPERADOR. Todos los usuarios veían las mismas opciones de menú independientemente de su rol.

## Causa Raíz

En el componente `MainLayout.tsx`, se estaba intentando acceder a `user.role.name` como si `role` fuera un objeto:

```typescript
return item.roles.includes(user.role.name);
```

Sin embargo, el backend devuelve `role` como un string directamente (ej: "ADMIN", "SUPERVISOR", "OPERADOR"), no como un objeto.

## Solución Implementada

### 1. Frontend - MainLayout.tsx

Cambiamos el acceso de `user.role.name` a `user.role_name`:

```typescript
// ANTES (incorrecto)
return item.roles.includes(user.role.name);

// DESPUÉS (correcto)
return item.roles.includes(user.role_name);
```

### 2. Backend - CustomTokenObtainPairSerializer

Agregamos el campo `role_name` a la respuesta del login para que sea consistente:

```python
data['user'] = {
    'id': str(self.user.id),
    'username': self.user.username,
    'email': self.user.email,
    'first_name': self.user.first_name,
    'last_name': self.user.last_name,
    'role': self.user.role.name,
    'role_name': self.user.role.name,  # ← AGREGADO
    'role_display': self.user.role.get_name_display(),
    'must_change_password': self.user.must_change_password,
}
```

### 3. Frontend - auth.types.ts

Actualizamos el tipo `LoginResponse` para incluir `role_name`:

```typescript
export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    role_name?: string;  // ← AGREGADO
    role_display: string;
    must_change_password: boolean;
  };
}
```

## Resultado Esperado

Ahora cada rol verá solo las opciones de menú que le corresponden:

### OPERADOR
- Dashboard
- Activos
- Órdenes de Trabajo
- Notificaciones

### SUPERVISOR
Todo lo del OPERADOR más:
- Mantenimiento
- Inventario
- Checklists
- Estado de Máquinas
- Predicciones ML
- Reportes
- Ubicaciones
- Usuarios

### ADMIN
Todo lo del SUPERVISOR más:
- Monitor Celery
- Configuración

## Deployment

1. ✅ Frontend desplegado a Vercel
2. ✅ Backend pusheado a GitHub (Railway se redesplegará automáticamente)

## Verificación

Para verificar que funciona correctamente:

1. Cerrar sesión en la aplicación
2. Iniciar sesión con un usuario OPERADOR
3. Verificar que solo se muestren las 4 opciones básicas en el sidebar
4. Repetir con SUPERVISOR y ADMIN para verificar que ven más opciones

## Commit

```
Fix: Corregir filtrado de sidebar por rol - usar role_name en lugar de role.name
```
