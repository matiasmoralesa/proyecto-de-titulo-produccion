# 🔴 Instrucciones para Limpiar Datos de PRODUCCIÓN

## ⚠️ ADVERTENCIA CRÍTICA

**ESTE PROCESO ELIMINARÁ TODOS LOS DATOS DE PRODUCCIÓN**

- ❌ Se eliminarán todos los usuarios (excepto superusuarios)
- ❌ Se eliminarán todos los activos
- ❌ Se eliminarán todas las órdenes de trabajo
- ❌ Se eliminarán todos los planes de mantenimiento
- ❌ Se eliminará todo el inventario
- ❌ Se eliminarán todas las configuraciones
- ✅ Se mantendrán las plantillas de checklist

**Solo procede si estás 100% seguro de que quieres eliminar todos los datos de producción.**

---

## 📋 Requisitos Previos

1. Tener Railway CLI instalado
2. Estar autenticado en Railway
3. Tener acceso al proyecto en Railway

### Instalar Railway CLI (si no lo tienes)

**Windows (PowerShell como Administrador)**:
```powershell
iwr https://railway.app/install.ps1 | iex
```

**Verificar instalación**:
```bash
railway --version
```

### Autenticarse en Railway

```bash
railway login
```

### Vincular al proyecto

```bash
railway link
```

---

## 🚀 Métodos para Ejecutar

### Método 1: Script Batch Automático (Recomendado)

```bash
reset_produccion_railway.bat
```

Este script:
1. Te pedirá confirmación
2. Ejecutará el comando en Railway
3. Mostrará el progreso en tiempo real

### Método 2: Comando Manual

```bash
railway run python manage.py reset_and_populate --no-input
```

### Método 3: Shell Interactivo de Railway

```bash
# Abrir shell en Railway
railway shell

# Una vez dentro, ejecutar:
cd backend
python manage.py reset_and_populate --no-input
```

---

## 📊 Datos que se Crearán

Después de limpiar, se crearán automáticamente:

### 👥 Usuarios (6 total)
- **Admin**: `admin / admin123`
- **Supervisores**: `supervisor1, supervisor2 / super123`
- **Operadores**: `operador1, operador2, operador3 / oper123`

### 📍 Ubicaciones (4)
- Planta Central
- Almacén Norte
- Taller de Mantenimiento
- Base Operativa Sur

### 🚛 Activos (7)
- 2 Camiones Supersucker
- 2 Camionetas MDO
- 1 Retroexcavadora
- 1 Cargador Frontal
- 1 Minicargador

### 📋 Órdenes de Trabajo (10)
- 4 Completadas
- 3 En Progreso
- 3 Pendientes

### 🔄 Planes de Mantenimiento (7)
- Planes diarios, semanales, mensuales, trimestrales, anuales
- Planes basados en horas de uso

### 🔧 Repuestos (10)
- Filtros (aceite, aire, combustible)
- Lubricantes
- Sistema de frenos
- Baterías
- Neumáticos
- Mangueras hidráulicas

### ⚙️ Configuración
- 4 Categorías de activos
- 4 Niveles de prioridad
- 5 Tipos de órdenes de trabajo
- 3 Parámetros del sistema

---

## 🔍 Verificar el Proceso

### Ver logs en tiempo real

```bash
railway logs --tail 100
```

### Verificar que se completó

```bash
railway run python manage.py shell
```

Luego en el shell de Python:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
print(f"Total usuarios: {User.objects.count()}")

from apps.assets.models import Asset
print(f"Total activos: {Asset.objects.count()}")

from apps.work_orders.models import WorkOrder
print(f"Total órdenes: {WorkOrder.objects.count()}")
```

---

## 🔄 Alternativa: Usar la API de Railway

Si prefieres no usar Railway CLI, puedes:

1. Ir al dashboard de Railway: https://railway.app
2. Seleccionar tu proyecto
3. Ir a la pestaña "Settings"
4. Buscar "Deploy Trigger" o "Run Command"
5. Ejecutar: `python manage.py reset_and_populate --no-input`

---

## 🆘 Solución de Problemas

### Error: "railway: command not found"
**Solución**: Instala Railway CLI siguiendo las instrucciones arriba.

### Error: "Not logged in"
**Solución**: Ejecuta `railway login`

### Error: "No project linked"
**Solución**: Ejecuta `railway link` y selecciona tu proyecto

### Error: "Permission denied"
**Solución**: Verifica que tienes permisos de administrador en el proyecto de Railway

### El comando se queda colgado
**Solución**: 
1. Presiona Ctrl+C
2. Verifica los logs: `railway logs --tail 50`
3. Intenta nuevamente

---

## ⏮️ Rollback (Deshacer)

**IMPORTANTE**: Este proceso NO tiene rollback automático. Una vez ejecutado, los datos se pierden permanentemente.

Si necesitas recuperar datos:
1. Debes tener un backup previo de la base de datos
2. Restaurar desde el backup de PostgreSQL en Railway

### Crear backup ANTES de ejecutar (Recomendado)

```bash
# Conectarse a la base de datos de Railway
railway connect postgres

# Dentro de psql, crear backup
\copy (SELECT * FROM users) TO 'users_backup.csv' CSV HEADER;
\copy (SELECT * FROM assets) TO 'assets_backup.csv' CSV HEADER;
# ... etc para cada tabla importante
```

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de Railway: `railway logs --tail 100`
2. Verifica que el comando existe: `railway run python manage.py help`
3. Contacta al equipo de desarrollo

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar, verifica:

- [ ] Tengo Railway CLI instalado
- [ ] Estoy autenticado en Railway
- [ ] He vinculado el proyecto correcto
- [ ] Entiendo que esto eliminará TODOS los datos de producción
- [ ] He creado un backup (si es necesario)
- [ ] Estoy 100% seguro de que quiero proceder

---

**Última actualización**: Diciembre 2024
**Versión del script**: 1.0
