# Debug: Verificar Rol en el Frontend

## 🔍 Problema

El rol en la base de datos es correcto (OPERADOR), pero el sidebar sigue mostrando todas las opciones.

## 🎯 Posibles Causas

1. El token JWT tiene el rol antiguo cacheado
2. El frontend está recibiendo el rol incorrecto del backend
3. El código del filtrado no se está ejecutando correctamente

## ✅ Solución: Verificar en la Consola del Navegador

### Paso 1: Abre DevTools

1. En la página donde estás logueado como operador1
2. Presiona `F12` para abrir DevTools
3. Ve a la pestaña **"Console"**

### Paso 2: Verifica el Usuario en el Store

Escribe este código en la consola:

```javascript
// Ver el usuario actual
console.log(JSON.parse(localStorage.getItem('auth-storage')))
```

Esto te mostrará algo como:

```json
{
  "state": {
    "user": {
      "username": "operador1",
      "role": {
        "name": "ADMIN"  // ← Este es el problema si dice ADMIN
      }
    }
  }
}
```

### Paso 3: Verifica qué Rol Tiene

Mira el campo `role.name`:
- Si dice **"OPERADOR"** → El problema está en el código del filtrado
- Si dice **"ADMIN"** o **"SUPERVISOR"** → El token JWT tiene el rol antiguo

## 🔧 Solución según el Resultado

### Si el rol en localStorage es ADMIN o SUPERVISOR:

El token JWT tiene el rol antiguo. Necesitas:

1. **Cerrar sesión completamente**
2. **Limpiar localStorage**:
   ```javascript
   localStorage.clear()
   ```
3. **Recargar la página** (F5)
4. **Volver a iniciar sesión** como operador1

Esto generará un nuevo token JWT con el rol correcto.

### Si el rol en localStorage es OPERADOR:

El problema está en el código del filtrado. Necesitamos verificar:

1. Que el código de Vercel tenga los cambios
2. Que el filtrado se esté ejecutando correctamente

---

**Ejecuta el código de la consola y dime qué rol aparece en `role.name`**
