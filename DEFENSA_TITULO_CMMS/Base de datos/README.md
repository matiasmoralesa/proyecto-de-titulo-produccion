# 🗄️ 02_BASE_DE_DATOS - Scripts y Modelo de Datos

## 📋 Contenido de esta Carpeta

Esta carpeta incluye el archivo script SQL de creación de objetos de la BD, carga de datos, diagramas de diseño y capturas de pantalla del modelo de la base de datos.

### 📊 Archivos Incluidos

#### 1. Scripts SQL
- `01_create_database.sql` - Script de creación de la base de datos
- `02_create_tables.sql` - Creación de todas las tablas del sistema
- `03_create_indexes.sql` - Índices para optimización de performance
- `04_create_constraints.sql` - Restricciones de integridad referencial
- `05_insert_initial_data.sql` - Datos iniciales y configuración
- `06_insert_sample_data.sql` - Datos de prueba para testing

#### 2. Diagramas del Modelo
- `modelo_entidad_relacion.png` - Diagrama ER completo
- `modelo_logico.pdf` - Modelo lógico detallado
- `modelo_fisico.png` - Implementación física en PostgreSQL
- `diagrama_dependencias.pdf` - Dependencias entre tablas

#### 3. Documentación
- `diccionario_datos.xlsx` - Diccionario completo de datos
- `descripcion_tablas.pdf` - Descripción detallada de cada tabla
- `reglas_negocio.md` - Reglas de negocio implementadas en BD

#### 4. Capturas de Pantalla
- `captura_pgadmin_estructura.png` - Vista de estructura en pgAdmin
- `captura_tablas_principales.png` - Tablas principales del sistema
- `captura_relaciones.png` - Relaciones entre entidades

## 🏗️ Estructura de la Base de Datos

### Módulos Principales

#### 1. **Autenticación y Usuarios**
- `auth_user` - Usuarios del sistema
- `auth_user_groups` - Relación usuarios-grupos
- `auth_group` - Grupos de permisos
- `auth_permission` - Permisos específicos

#### 2. **Gestión de Activos**
- `assets` - Información principal de activos
- `locations` - Ubicaciones de activos
- `asset_categories` - Categorías de activos

#### 3. **Órdenes de Trabajo**
- `work_orders` - Órdenes de trabajo principales
- `work_order_types` - Tipos de órdenes
- `priorities` - Niveles de prioridad

#### 4. **Machine Learning**
- `ml_models` - Metadatos de modelos ML
- `failure_predictions` - Predicciones de fallos
- `operator_skills` - Habilidades de operadores
- `operator_availability` - Disponibilidad de operadores
- `operator_performance` - Métricas de rendimiento

#### 5. **Mantenimiento**
- `maintenance_plans` - Planes de mantenimiento
- `maintenance_schedules` - Programación de mantenimiento
- `maintenance_history` - Historial de mantenimientos

#### 6. **Inventario**
- `spare_parts` - Repuestos y materiales
- `inventory_transactions` - Movimientos de inventario
- `suppliers` - Proveedores

#### 7. **Notificaciones**
- `notifications` - Sistema de notificaciones
- `notification_preferences` - Preferencias de usuario

#### 8. **Reportes y Auditoría**
- `reports` - Reportes generados
- `audit_logs` - Logs de auditoría
- `system_logs` - Logs del sistema

## 📊 Características Técnicas

### Motor de Base de Datos
- **SGBD**: PostgreSQL 15.x
- **Encoding**: UTF-8
- **Timezone**: America/Santiago
- **Collation**: es_ES.UTF-8

### Optimizaciones Implementadas
- **Índices**: En campos de búsqueda frecuente
- **Particionamiento**: Tablas de logs por fecha
- **Constraints**: Integridad referencial completa
- **Triggers**: Auditoría automática de cambios

### Seguridad
- **Roles**: Separación por funcionalidad
- **Permisos**: Granulares por tabla y operación
- **Encriptación**: Contraseñas con hash seguro
- **Auditoría**: Registro de todas las operaciones críticas

## 🔧 Instrucciones de Instalación

### 1. Crear Base de Datos
```sql
-- Ejecutar como superusuario de PostgreSQL
CREATE DATABASE cmms_production;
CREATE USER cmms_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE cmms_production TO cmms_user;
```

### 2. Ejecutar Scripts en Orden
```bash
# 1. Estructura básica
psql -d cmms_production -f 01_create_database.sql

# 2. Tablas principales
psql -d cmms_production -f 02_create_tables.sql

# 3. Índices y optimizaciones
psql -d cmms_production -f 03_create_indexes.sql

# 4. Restricciones de integridad
psql -d cmms_production -f 04_create_constraints.sql

# 5. Datos iniciales
psql -d cmms_production -f 05_insert_initial_data.sql

# 6. Datos de prueba (opcional)
psql -d cmms_production -f 06_insert_sample_data.sql
```

### 3. Verificar Instalación
```sql
-- Verificar tablas creadas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' ORDER BY table_name;

-- Verificar datos iniciales
SELECT COUNT(*) as total_users FROM auth_user;
SELECT COUNT(*) as total_assets FROM assets;
SELECT COUNT(*) as total_locations FROM locations;
```

## 📈 Métricas de la Base de Datos

### Volumen de Datos (Estimado)
- **Usuarios**: ~50 registros
- **Activos**: ~200 registros
- **Órdenes de Trabajo**: ~1,000 registros/mes
- **Predicciones ML**: ~200 registros/día
- **Notificaciones**: ~500 registros/día

### Performance
- **Tiempo de consulta promedio**: <100ms
- **Consultas complejas (reportes)**: <2 segundos
- **Inserción de predicciones**: <50ms por lote
- **Backup completo**: ~5 minutos

## 🔄 Mantenimiento y Backup

### Backup Automático
```bash
# Script de backup diario
pg_dump -h localhost -U cmms_user -d cmms_production \
  --format=custom --compress=9 \
  --file=backup_$(date +%Y%m%d_%H%M%S).backup
```

### Limpieza de Datos
```sql
-- Limpiar logs antiguos (>90 días)
DELETE FROM system_logs WHERE created_at < NOW() - INTERVAL '90 days';

-- Limpiar notificaciones leídas (>30 días)
DELETE FROM notifications 
WHERE is_read = true AND created_at < NOW() - INTERVAL '30 days';
```

### Monitoreo
- **Tamaño de BD**: Monitoreo semanal
- **Performance de queries**: Log de queries lentas
- **Conexiones activas**: Alertas por límites
- **Espacio en disco**: Alertas automáticas

---
*Documentación de Base de Datos - Sistema CMMS v1.0 - Diciembre 2025*