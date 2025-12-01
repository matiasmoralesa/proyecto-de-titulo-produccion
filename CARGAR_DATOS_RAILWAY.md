# 🚀 Guía: Cargar Datos en Railway (Producción)

## ✅ Paso 1: Datos Exportados

Los siguientes archivos JSON contienen todos los datos maestros de tu base de datos local:

- `roles_export.json` - 3 roles (ADMIN, SUPERVISOR, OPERADOR)
- `checklist_templates_export.json` - 5 plantillas de checklist
- `priorities_export.json` - 5 niveles de prioridad
- `workorder_types_export.json` - 8 tipos de órdenes de trabajo
- `asset_categories_export.json` - 8 categorías de activos
- `locations_export.json` - 6 ubicaciones

## 📤 Paso 2: Subir Archivos a Git

```bash
# Desde el directorio raíz del proyecto
git add backend/*_export.json
git commit -m "Add production data exports"
git push origin main
```

## 🔄 Paso 3: Cargar Datos en Railway

### Opción A: Usando el Dashboard de Railway (Más Fácil)

1. **Ve al Dashboard de Railway**: https://railway.app/
2. **Selecciona tu proyecto**
3. **Haz clic en tu servicio de backend**
4. **Ve a la pestaña "Settings"**
5. **Busca la sección "Deploy"**
6. **Haz clic en "Redeploy"** para que Railway descargue los nuevos archivos de Git

Una vez que el deploy termine:

7. **Ve a la pestaña "Deployments"**
8. **Haz clic en el deployment activo**
9. **Haz clic en "View Logs"**
10. **Haz clic en el botón "Shell" (terminal icon)**

En el shell de Railway, ejecuta estos comandos uno por uno:

```bash
# 1. Cargar Roles
python backend/manage.py loaddata backend/roles_export.json

# 2. Cargar Plantillas de Checklist
python backend/manage.py loaddata backend/checklist_templates_export.json

# 3. Cargar Prioridades
python backend/manage.py loaddata backend/priorities_export.json

# 4. Cargar Tipos de Orden de Trabajo
python backend/manage.py loaddata backend/workorder_types_export.json

# 5. Cargar Categorías de Activos
python backend/manage.py loaddata backend/asset_categories_export.json

# 6. Cargar Ubicaciones
python backend/manage.py loaddata backend/locations_export.json
```

### Opción B: Usando Railway CLI

Si tienes Railway CLI instalado:

```bash
# Conectarse al shell de Railway
railway shell

# Luego ejecutar los comandos de carga
python backend/manage.py loaddata backend/roles_export.json
python backend/manage.py loaddata backend/checklist_templates_export.json
python backend/manage.py loaddata backend/priorities_export.json
python backend/manage.py loaddata backend/workorder_types_export.json
python backend/manage.py loaddata backend/asset_categories_export.json
python backend/manage.py loaddata backend/locations_export.json
```

## 🔍 Paso 4: Verificar la Carga

### Verificar Plantillas de Checklist

```bash
railway run python manage.py shell
```

En el shell de Python:

```python
from apps.checklists.models import ChecklistTemplate

# Ver todas las plantillas
templates = ChecklistTemplate.objects.all()
print(f"Total plantillas: {templates.count()}")

for t in templates:
    items_count = len(t.items) if t.items else 0
    print(f"- {t.code}: {t.name} ({items_count} items)")

# Debería mostrar:
# Total plantillas: 5
# - SUPERSUCKER-CH01: Check List Camión Supersucker (15 items)
# - F-PR-020-CH01: Check List Camionetas MDO (24 items)
# - F-PR-034-CH01: ...
# - F-PR-037-CH01: ...
# - F-PR-040-CH01: ...
```

### Verificar Roles

```python
from apps.authentication.models import Role

roles = Role.objects.all()
print(f"Total roles: {roles.count()}")

for r in roles:
    print(f"- {r.name}: {r.description}")

# Debería mostrar:
# Total roles: 3
# - ADMIN: ...
# - SUPERVISOR: ...
# - OPERADOR: ...
```

### Verificar Todo con Script

```bash
railway run python backend/check_production_data.py
```

Este script verificará automáticamente que todos los datos estén presentes.

## ⚠️ Troubleshooting

### Error: "No such file or directory"

Si Railway no encuentra los archivos, asegúrate de que se hayan subido a Git:

```bash
git status
git log --oneline -1
```

### Error: "Duplicate key value violates unique constraint"

Si ya cargaste los datos antes, Django intentará crear duplicados. Opciones:

1. **Limpiar la base de datos primero** (⚠️ CUIDADO - borra todo):
   ```bash
   railway run python manage.py flush --no-input
   railway run python manage.py migrate
   ```

2. **Usar `--ignorenonexistent`** para ignorar duplicados:
   ```bash
   railway run python manage.py loaddata backend/roles_export.json --ignorenonexistent
   ```

### Error: "Foreign key constraint fails"

Asegúrate de cargar los datos en el orden correcto:
1. Roles (primero)
2. Ubicaciones
3. Categorías y Prioridades
4. Plantillas de Checklist
5. Tipos de Orden de Trabajo

## 📊 Verificación Final

Ejecuta este comando para ver un resumen completo:

```bash
railway run python backend/check_production_data.py
```

Deberías ver:

```
🔍 VERIFICACIÓN DE DATOS DE PRODUCCIÓN
========================================

📋 Roles de Usuario:
   Total: 3
   ✅ ADMIN
   ✅ SUPERVISOR
   ✅ OPERADOR

📋 Plantillas de Checklist:
   Total: 5
   ✅ SUPERSUCKER-CH01: Check List Camión Supersucker (15 items)
   ✅ F-PR-020-CH01: Check List Camionetas MDO (24 items)
   ✅ F-PR-034-CH01: ...
   ✅ F-PR-037-CH01: ...
   ✅ F-PR-040-CH01: ...

✅ VERIFICACIÓN EXITOSA
```

## 🎯 Siguiente Paso

Una vez que los datos estén cargados, procede a:

1. **Crear un usuario administrador**:
   ```bash
   railway run python manage.py createsuperuser
   ```

2. **Configurar Celery y Flower** (ver `CONFIGURAR_CELERY_FLOWER.md`)

3. **Probar el sistema** accediendo a tu URL de producción

## 📝 Notas Importantes

- ✅ Los archivos JSON son **idempotentes** con `loaddata`
- ✅ Django maneja automáticamente las **foreign keys**
- ✅ Los datos se cargan en una **transacción** (todo o nada)
- ⚠️ Si algo falla, Railway hace **rollback automático**
