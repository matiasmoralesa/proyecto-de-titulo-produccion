# Guía: Carga de Datos en Producción (Railway)

Esta guía te ayudará a exportar datos de tu base de datos local y cargarlos en producción en Railway.

## 📋 Datos que se Exportarán

- ✅ Roles de usuario (ADMIN, SUPERVISOR, OPERADOR)
- ✅ Plantillas de checklist (5 plantillas por tipo de vehículo)
- ✅ Prioridades
- ✅ Tipos de orden de trabajo
- ✅ Categorías de activos
- ✅ Ubicaciones

## 🚀 Paso 1: Exportar Datos Locales

Ejecuta el script de exportación en tu entorno local:

```bash
cd backend
python export_production_data.py
```

Esto creará un archivo JSON con timestamp, por ejemplo: `production_data_20241130_143022.json`

## 📤 Paso 2: Subir Archivo a Railway

Tienes dos opciones:

### Opción A: Usar Railway CLI (Recomendado)

1. **Copiar el archivo al proyecto:**
   ```bash
   # El archivo ya está en backend/
   ```

2. **Subir el archivo a Railway:**
   ```bash
   # Primero, asegúrate de estar en el directorio raíz del proyecto
   cd ..
   
   # Hacer commit del archivo
   git add backend/production_data_*.json
   git commit -m "Add production data export"
   git push origin main
   ```

3. **Ejecutar el script de importación en Railway:**
   ```bash
   railway run python backend/import_production_data.py backend/production_data_YYYYMMDD_HHMMSS.json
   ```
   
   Reemplaza `YYYYMMDD_HHMMSS` con el timestamp de tu archivo.

### Opción B: Usar el Dashboard de Railway

1. **Subir el archivo manualmente:**
   - Ve al dashboard de Railway
   - Selecciona tu proyecto
   - Ve a la sección "Files" o usa el shell

2. **Ejecutar desde el shell de Railway:**
   ```bash
   python backend/import_production_data.py backend/production_data_YYYYMMDD_HHMMSS.json
   ```

## 🔍 Paso 3: Verificar la Carga

### Verificar Plantillas de Checklist

```bash
railway run python backend/manage.py shell
```

Luego en el shell de Python:

```python
from apps.checklists.models import ChecklistTemplate

# Ver todas las plantillas
templates = ChecklistTemplate.objects.all()
print(f"Total plantillas: {templates.count()}")

for t in templates:
    print(f"- {t.code}: {t.name} ({t.vehicle_type})")
```

### Verificar Roles

```python
from apps.authentication.models import Role

roles = Role.objects.all()
print(f"Total roles: {roles.count()}")

for r in roles:
    print(f"- {r.name}: {r.description}")
```

## 🔧 Paso 4: Cargar Plantillas de Checklist (Alternativa)

Si prefieres usar el comando de management existente:

```bash
railway run python backend/manage.py load_checklist_templates
```

## 📊 Verificación Final

Ejecuta este comando para verificar que todo está cargado:

```bash
railway run python backend/check_production_data.py
```

## ⚠️ Troubleshooting

### Error: "Module not found"

Si obtienes errores de módulos no encontrados:

```bash
# Verifica que las dependencias estén instaladas en Railway
railway run pip list | grep Django
```

### Error: "Database connection failed"

Verifica que las variables de entorno estén configuradas:

```bash
railway variables
```

Debe incluir:
- `DATABASE_URL`
- `DJANGO_SETTINGS_MODULE=config.settings.railway`

### Error: "Permission denied"

Asegúrate de que el archivo JSON tenga permisos de lectura:

```bash
railway run ls -la backend/production_data_*.json
```

## 🔄 Actualizar Datos

Si necesitas actualizar los datos más adelante:

1. Exporta nuevamente desde local:
   ```bash
   python backend/export_production_data.py
   ```

2. Sube y ejecuta el nuevo archivo:
   ```bash
   git add backend/production_data_*.json
   git commit -m "Update production data"
   git push origin main
   railway run python backend/import_production_data.py backend/production_data_NUEVO.json
   ```

## 📝 Notas Importantes

- ✅ El script es **idempotente**: puedes ejecutarlo múltiples veces sin crear duplicados
- ✅ Los datos existentes se **actualizarán**, no se duplicarán
- ✅ El script usa **transacciones**: si algo falla, no se aplicará ningún cambio
- ⚠️ **Backup**: Railway hace backups automáticos, pero es buena práctica exportar antes de importar

## 🎯 Siguiente Paso: Configurar Celery y Flower

Una vez que los datos estén cargados, procede a configurar el monitoreo de Celery:

Ver: `CONFIGURAR_CELERY_FLOWER.md`
