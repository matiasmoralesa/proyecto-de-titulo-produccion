# Verificar y Corregir CORS en Railway

## Problema
El frontend en Vercel no puede conectarse al backend en Railway debido a errores de CORS.

## Solución

Necesitas agregar la URL de Vercel a las variables de entorno de Railway:

### Paso 1: Ir a Railway
1. Ve a https://railway.app
2. Inicia sesión
3. Selecciona el proyecto "proyecto-de-titulo-produccion"
4. Haz clic en el servicio del backend

### Paso 2: Agregar/Verificar Variables de Entorno
En la sección "Variables", verifica que existan estas variables:

```
CORS_ALLOWED_ORIGINS=https://proyecto-de-titulo-produccion.vercel.app,https://proyecto-de-titulo-produccion-btest1ht.vercel.app
```

Si no existe o está incompleta, agrégala o actualízala.

### Paso 3: Redesplegar
Después de agregar/actualizar la variable, Railway redesplegará automáticamente el backend.

Espera unos 2-3 minutos para que el redespliegue termine.

### Paso 4: Probar
Una vez que Railway termine de redesplegar:
1. Ve a https://proyecto-de-titulo-produccion.vercel.app
2. Intenta iniciar sesión
3. Debería funcionar correctamente

## Alternativa Rápida
Si no quieres esperar el redespliegue de Railway, puedes probar localmente:

1. Inicia el backend local
2. Actualiza el `.env.local` del frontend para apuntar a localhost
3. Prueba el sidebar con el usuario operador localmente
