# 📋 Resumen: Carga de Datos en Producción

## ✅ Lo que ya hicimos

1. ✅ Exportamos todos los datos de tu base de datos local
2. ✅ Creamos 6 archivos JSON con los datos maestros
3. ✅ Subimos los archivos a Git
4. ✅ Pusheamos a GitHub (ya están en Railway)

## 📦 Archivos Exportados

Los siguientes archivos están listos en `backend/`:

| Archivo | Contenido | Cantidad |
|---------|-----------|----------|
| `roles_export.json` | Roles de usuario | 3 roles |
| `checklist_templates_export.json` | Plantillas de checklist | 5 plantillas |
| `priorities_export.json` | Niveles de prioridad | 5 prioridades |
| `workorder_types_export.json` | Tipos de órdenes de trabajo | 8 tipos |
| `asset_categories_export.json` | Categorías de activos | 8 categorías |
| `locations_export.json` | Ubicaciones | 6 ubicaciones |

## 🚀 Siguiente Paso: Cargar en Railway

### Método 1: Dashboard de Railway (Recomendado - Más Visual)

1. **Ir a Railway Dashboard**
   - Abre: https://railway.app/
   - Selecciona tu proyecto
   - Haz clic en tu servicio de backend

2. **Redeploy para obtener los archivos nuevos**
   - Ve a "Settings"
   - Haz clic en "Redeploy"
   - Espera a que termine el deploy (2-3 minutos)

3. **Abrir el Shell de Railway**
   - Ve a la pestaña "Deployments"
   - Haz clic en el deployment activo (el que tiene el punto verde)
   - Busca el botón "Shell" o "Terminal" (icono de terminal)
   - Se abrirá una terminal en el navegador

4. **Ejecutar los comandos de carga**
   
   Copia y pega estos comandos UNO POR UNO en el shell:

   ```bash
   python backend/manage.py loaddata backend/roles_export.json
   ```
   
   Espera a que termine (verás "Installed X object(s)"), luego:

   ```bash
   python backend/manage.py loaddata backend/checklist_templates_export.json
   ```

   Luego:

   ```bash
   python backend/manage.py loaddata backend/priorities_export.json
   ```

   Luego:

   ```bash
   python backend/manage.py loaddata backend/workorder_types_export.json
   ```

   Luego:

   ```bash
   python backend/manage.py loaddata backend/asset_categories_export.json
   ```

   Finalmente:

   ```bash
   python backend/manage.py loaddata backend/locations_export.json
   ```

5. **Verificar que todo se cargó**

   ```bash
   python backend/check_production_data.py
   ```

   Deberías ver:
   ```
   ✅ VERIFICACIÓN EXITOSA
   Todos los datos esenciales están presentes
   ```

### Método 2: Railway CLI (Si tienes CLI instalado)

```bash
# Conectarse al shell
railway shell

# Ejecutar todos los comandos
python backend/manage.py loaddata backend/roles_export.json
python backend/manage.py loaddata backend/checklist_templates_export.json
python backend/manage.py loaddata backend/priorities_export.json
python backend/manage.py loaddata backend/workorder_types_export.json
python backend/manage.py loaddata backend/asset_categories_export.json
python backend/manage.py loaddata backend/locations_export.json

# Verificar
python backend/check_production_data.py
```

## 🔍 Cómo Verificar que Funcionó

### Desde el Shell de Railway:

```bash
python backend/manage.py shell
```

Luego en Python:

```python
from apps.checklists.models import ChecklistTemplate
print(f"Plantillas: {ChecklistTemplate.objects.count()}")
# Debería mostrar: Plantillas: 5

from apps.authentication.models import Role
print(f"Roles: {Role.objects.count()}")
# Debería mostrar: Roles: 3
```

### Desde tu Frontend:

1. Abre tu aplicación en Vercel
2. Inicia sesión (si ya tienes un usuario admin)
3. Ve a la sección de Checklists
4. Deberías ver las 5 plantillas disponibles

## ⚠️ Problemas Comunes

### "No such file or directory"

**Solución**: Asegúrate de haber hecho redeploy en Railway después de pushear los archivos.

### "Duplicate key value violates unique constraint"

**Solución**: Los datos ya están cargados. Puedes ignorar este error o limpiar la base de datos:

```bash
# ⚠️ CUIDADO: Esto borra TODOS los datos
railway shell
python backend/manage.py flush --no-input
python backend/manage.py migrate
# Luego vuelve a cargar los datos
```

### "Foreign key constraint fails"

**Solución**: Carga los datos en el orden correcto (roles primero, luego el resto).

## 📊 Resultado Esperado

Después de cargar todos los datos, deberías tener:

- ✅ 3 roles de usuario (ADMIN, SUPERVISOR, OPERADOR)
- ✅ 5 plantillas de checklist completas con todos sus items
- ✅ 5 niveles de prioridad
- ✅ 8 tipos de órdenes de trabajo
- ✅ 8 categorías de activos
- ✅ 6 ubicaciones

## 🎯 Siguiente Paso

Una vez que los datos estén cargados:

1. **Crear un usuario administrador**:
   ```bash
   railway shell
   python backend/manage.py createsuperuser
   ```

2. **Probar el sistema**:
   - Accede a tu URL de Vercel
   - Inicia sesión con el usuario admin
   - Verifica que puedes ver las plantillas de checklist
   - Crea un activo de prueba
   - Crea una orden de trabajo de prueba

3. **Configurar Celery y Flower** (opcional, para tareas asíncronas)

## 📝 Notas

- Los comandos `loaddata` son **idempotentes**: si ejecutas dos veces, Django actualiza en lugar de duplicar
- Railway hace **backups automáticos** de la base de datos
- Puedes exportar y cargar datos cuantas veces necesites
- Los archivos JSON están en formato Django, no son editables manualmente

## 🆘 ¿Necesitas Ayuda?

Si algo no funciona:

1. Revisa los logs de Railway (pestaña "Logs")
2. Verifica que las variables de entorno estén configuradas
3. Asegúrate de que el deploy terminó correctamente
4. Prueba ejecutar los comandos uno por uno en lugar de todos juntos
