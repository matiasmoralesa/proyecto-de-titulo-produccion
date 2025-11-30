# Datos de Configuración del Sistema CMMS

## 📋 Resumen

Se han creado datos de configuración maestros para el sistema CMMS, incluyendo categorías de activos, prioridades, tipos de órdenes de trabajo y parámetros del sistema.

## 🎯 Datos Creados

### 1. Categorías de Activos (8 categorías)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| VEH-PES | Vehículos Pesados | Camiones, volquetes y vehículos de carga pesada |
| MAQ-CON | Maquinaria de Construcción | Excavadoras, retroexcavadoras, cargadores frontales |
| MAQ-AGR | Maquinaria Agrícola | Tractores, cosechadoras y equipos agrícolas |
| EQP-IND | Equipos Industriales | Compresores, generadores, bombas industriales |
| HER-MEN | Herramientas Menores | Herramientas eléctricas y manuales |
| VEH-LIG | Vehículos Ligeros | Camionetas, autos y vehículos de transporte ligero |
| EQP-OFI | Equipos de Oficina | Computadoras, impresoras y equipos de oficina |
| SIS-INF | Sistemas de Información | Servidores, redes y sistemas IT |

### 2. Prioridades (5 niveles)

| Nivel | Nombre | Descripción | Color |
|-------|--------|-------------|-------|
| 1 | Crítica | Requiere atención inmediata, afecta operaciones críticas | 🔴 #DC2626 |
| 2 | Alta | Importante, debe atenderse pronto | 🟠 #EA580C |
| 3 | Media | Prioridad normal, atender en tiempo regular | 🟡 #F59E0B |
| 4 | Baja | Puede esperar, no es urgente | 🟢 #10B981 |
| 5 | Muy Baja | Mínima prioridad, atender cuando sea posible | ⚪ #6B7280 |

### 3. Tipos de Órdenes de Trabajo (8 tipos)

| Código | Nombre | Descripción | Requiere Aprobación |
|--------|--------|-------------|---------------------|
| PREV | Mantenimiento Preventivo | Mantenimiento programado para prevenir fallas | No |
| CORR | Mantenimiento Correctivo | Reparación de fallas o averías | No |
| PRED | Mantenimiento Predictivo | Basado en predicciones de ML y análisis de datos | No |
| EMRG | Emergencia | Atención inmediata a fallas críticas | ✅ Sí |
| INSP | Inspección | Revisión y evaluación del estado del activo | No |
| MODI | Modificación | Cambios o mejoras en el activo | ✅ Sí |
| INST | Instalación | Instalación de nuevos equipos o componentes | ✅ Sí |
| CALI | Calibración | Ajuste y calibración de equipos | No |

### 4. Parámetros del Sistema (10 parámetros)

| Clave | Valor | Descripción | Tipo | Editable |
|-------|-------|-------------|------|----------|
| system.name | CMMS - Sistema de Gestión de Mantenimiento | Nombre del sistema | string | ✅ |
| system.version | 1.0.0 | Versión del sistema | string | ❌ |
| maintenance.default_duration | 4 | Duración predeterminada de mantenimiento (horas) | integer | ✅ |
| maintenance.advance_notice_days | 7 | Días de anticipación para notificaciones | integer | ✅ |
| ml.prediction_threshold | 0.7 | Umbral de probabilidad para predicciones ML | float | ✅ |
| ml.auto_create_workorder | true | Crear automáticamente órdenes desde predicciones | boolean | ✅ |
| notifications.enabled | true | Habilitar notificaciones del sistema | boolean | ✅ |
| notifications.email_enabled | false | Habilitar notificaciones por email | boolean | ✅ |
| reports.retention_days | 365 | Días de retención de reportes | integer | ✅ |
| security.session_timeout | 3600 | Tiempo de expiración de sesión (segundos) | integer | ✅ |

## 🚀 Cómo Usar

### Opción 1: Script Individual

```bash
cd backend
python seed_configuration.py
```

### Opción 2: Seed Completo (Incluye configuración)

```bash
cd backend
python seed_all_data.py
```

El script `seed_all_data.py` ahora incluye automáticamente la configuración.

## 📊 Verificar Datos

### Desde la Interfaz Web

1. Acceder a: `http://localhost:5173/configuration`
2. Navegar por las pestañas:
   - **Categorías**: Ver categorías de activos
   - **Prioridades**: Ver niveles de prioridad
   - **Tipos de OT**: Ver tipos de órdenes de trabajo
   - **Parámetros**: Ver parámetros del sistema

### Desde Django Admin

1. Acceder a: `http://localhost:8000/admin/`
2. Login con: `admin / admin123`
3. Navegar a la sección "Configuration"

### Desde la Base de Datos

```bash
cd backend
python manage.py shell
```

```python
from apps.configuration.models import AssetCategory, Priority, WorkOrderType, SystemParameter

# Ver categorías
print(f"Categorías: {AssetCategory.objects.count()}")
for cat in AssetCategory.objects.all():
    print(f"  - {cat.code}: {cat.name}")

# Ver prioridades
print(f"\nPrioridades: {Priority.objects.count()}")
for pri in Priority.objects.all():
    print(f"  - Nivel {pri.level}: {pri.name}")

# Ver tipos de OT
print(f"\nTipos de OT: {WorkOrderType.objects.count()}")
for wot in WorkOrderType.objects.all():
    print(f"  - {wot.code}: {wot.name}")

# Ver parámetros
print(f"\nParámetros: {SystemParameter.objects.count()}")
for param in SystemParameter.objects.all():
    print(f"  - {param.key}: {param.value}")
```

## 🔧 Personalización

### Agregar Nuevas Categorías

Editar `backend/seed_configuration.py` y agregar a `categories_data`:

```python
('NUEVO-COD', 'Nombre de Categoría', 'Descripción detallada'),
```

### Agregar Nuevas Prioridades

Editar `backend/seed_configuration.py` y agregar a `priorities_data`:

```python
('Nombre', 'Descripción', nivel, '#CODIGO_COLOR'),
```

### Agregar Nuevos Tipos de OT

Editar `backend/seed_configuration.py` y agregar a `types_data`:

```python
('COD', 'Nombre', 'Descripción', requiere_aprobacion),
```

### Agregar Nuevos Parámetros

Editar `backend/seed_configuration.py` y agregar a `parameters_data`:

```python
('clave.parametro', 'valor', 'Descripción', 'tipo_dato', es_editable),
```

## 📝 Notas Importantes

1. **Códigos Únicos**: Los códigos de categorías y tipos deben ser únicos
2. **Niveles de Prioridad**: Los niveles deben ser únicos (1-5)
3. **Colores**: Usar formato hexadecimal (#RRGGBB)
4. **Parámetros del Sistema**: 
   - Los parámetros no editables no pueden modificarse desde la UI
   - Los tipos de datos deben ser: string, integer, float, boolean, json
5. **Aprobaciones**: Los tipos de OT con aprobación requerida necesitan workflow adicional

## 🔄 Actualizar Datos

Para actualizar datos existentes:

1. Modificar el script `seed_configuration.py`
2. Cambiar la condición de `if not exists()` a `update_or_create()`
3. Ejecutar el script nuevamente

Ejemplo:

```python
AssetCategory.objects.update_or_create(
    code=code,
    defaults={
        'name': name,
        'description': description,
        'is_active': True,
        'created_by': admin_user
    }
)
```

## 🗑️ Limpiar Datos

Para eliminar todos los datos de configuración:

```bash
cd backend
python manage.py shell
```

```python
from apps.configuration.models import AssetCategory, Priority, WorkOrderType, SystemParameter

# Eliminar todos los datos
AssetCategory.objects.all().delete()
Priority.objects.all().delete()
WorkOrderType.objects.all().delete()
SystemParameter.objects.all().delete()

print("✓ Datos de configuración eliminados")
```

## 📈 Uso en el Sistema

### Categorías de Activos

- Se usan al crear/editar activos
- Permiten clasificar y filtrar activos
- Aparecen en reportes y dashboards

### Prioridades

- Se asignan a órdenes de trabajo
- Determinan el orden de atención
- Los colores se muestran en la UI

### Tipos de Órdenes de Trabajo

- Se seleccionan al crear órdenes
- Los que requieren aprobación activan workflow
- Aparecen en filtros y reportes

### Parámetros del Sistema

- Controlan el comportamiento del sistema
- Se pueden editar desde la UI (si es_editable=True)
- Afectan funcionalidades como ML, notificaciones, etc.

## 🔐 Seguridad

- Solo usuarios con rol ADMIN pueden modificar la configuración
- Todos los cambios se registran en audit logs
- Los parámetros críticos están marcados como no editables

## 📞 Soporte

Para problemas o preguntas:
1. Verificar que el usuario admin existe
2. Revisar logs del script
3. Verificar permisos de base de datos
4. Consultar documentación de Django admin

---

**Última actualización:** 27 de Noviembre, 2025
