# 🚀 Ejecutar Reset de Datos en Producción

## Comando a Ejecutar Manualmente

Dado que Railway CLI tiene limitaciones con comandos complejos desde Windows, necesitas ejecutar esto manualmente:

### Opción 1: Desde el Dashboard de Railway (MÁS FÁCIL)

1. Ve a https://railway.app
2. Abre tu proyecto "vibrant-vitality"
3. Selecciona el servicio "proyecto-de-titulo-produccion"
4. Ve a la pestaña "Settings"
5. Busca la sección "Deploy"
6. En "Custom Start Command" o "Run Command", ejecuta:
   ```
   cd backend && python manage.py reset_and_populate --no-input
   ```

### Opción 2: Usando Railway CLI con Shell Interactivo

```bash
# Paso 1: Abrir shell de Railway
railway shell

# Paso 2: Una vez dentro del shell, ejecutar:
cd backend
python manage.py reset_and_populate --no-input
```

### Opción 3: Crear un Deployment Temporal

1. Edita el `Procfile` temporalmente
2. Cambia la línea `web:` por:
   ```
   web: cd backend && python manage.py reset_and_populate --no-input && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```
3. Haz commit y push
4. Railway ejecutará el reset automáticamente al desplegar
5. **IMPORTANTE**: Revierte el Procfile después

### Opción 4: Usando la API de Railway

Si tienes acceso a la API de Railway, puedes ejecutar comandos remotamente.

## ⚠️ IMPORTANTE

Este comando eliminará TODOS los datos de producción y creará datos de muestra nuevos.

## 📊 Datos que se Crearán

- 6 Usuarios (admin, 2 supervisores, 3 operadores)
- 7 Activos
- 10 Órdenes de Trabajo
- 7 Planes de Mantenimiento
- 10 Repuestos
- 4 Ubicaciones
- Configuración completa

## ✅ Verificar que Funcionó

Después de ejecutar, verifica en:
```
https://proyecto-de-titulo-produccion-production.up.railway.app/admin
```

Credenciales:
- Usuario: `admin`
- Password: `admin123`
