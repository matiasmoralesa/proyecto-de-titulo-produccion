# Requirements Document - Production Data Setup

## Introduction

Este documento define los requisitos para configurar y cargar datos esenciales en el entorno de producción del Sistema CMMS desplegado en Railway. El sistema está actualmente desplegado pero requiere datos maestros (plantillas de checklist) y herramientas de monitoreo (Celery/Flower) para estar completamente operativo.

**Contexto:**
- Backend desplegado en Railway con PostgreSQL
- Frontend desplegado en Vercel
- Base de datos vacía que requiere datos maestros
- Celery configurado pero sin interfaz de monitoreo

## Glossary

- **Production_Environment**: Entorno de producción en Railway con PostgreSQL
- **Checklist_Template**: Plantilla predefinida de checklist específica por tipo de vehículo
- **Celery**: Sistema de cola de tareas asíncronas de Python
- **Flower**: Herramienta web de monitoreo para Celery
- **Management_Command**: Comando Django personalizado ejecutable desde CLI
- **Railway_CLI**: Herramienta de línea de comandos para interactuar con Railway
- **Seed_Data**: Datos iniciales necesarios para el funcionamiento del sistema
- **Vehicle_Type**: Tipo de vehículo (Camión Supersucker, Camioneta MDO, Retroexcavadora MDO, Cargador Frontal MDO, Minicargador MDO)

## Requirements

### Requirement 1: Carga de Plantillas de Checklist en Producción

**User Story:** Como administrador del sistema, quiero cargar las 5 plantillas de checklist predefinidas en la base de datos de producción, para que los usuarios puedan ejecutar inspecciones estandarizadas desde el primer día.

#### Acceptance Criteria

1. THE Management_Command SHALL cargar exactamente 5 Checklist_Template correspondientes a los 5 Vehicle_Type del sistema
2. THE Management_Command SHALL asignar códigos únicos a cada plantilla (F-PR-020-CH01, F-PR-034-CH01, F-PR-037-CH01, F-PR-040-CH01, Camión Supersucker)
3. THE Management_Command SHALL marcar todas las plantillas cargadas con is_system_template=True para prevenir modificaciones
4. THE Management_Command SHALL ser idempotente, permitiendo ejecución múltiple sin crear duplicados
5. THE Management_Command SHALL validar que cada plantilla contiene items válidos en formato JSON antes de guardar
6. WHEN el comando se ejecuta en Production_Environment, THE Management_Command SHALL conectarse a la base de datos PostgreSQL de Railway
7. THE Management_Command SHALL reportar el número de plantillas creadas y actualizadas al finalizar

### Requirement 2: Configuración de Flower para Monitoreo de Celery

**User Story:** Como administrador del sistema, quiero acceder a una interfaz web de Flower para monitorear tareas de Celery en tiempo real, para diagnosticar problemas y verificar el estado de tareas asíncronas.

#### Acceptance Criteria

1. THE Production_Environment SHALL ejecutar Flower como proceso separado conectado al broker de Celery
2. THE Flower SHALL estar accesible mediante URL pública con autenticación básica HTTP
3. THE Flower SHALL mostrar tareas activas, completadas, fallidas y programadas de Celery
4. THE Production_Environment SHALL configurar variables de entorno para credenciales de autenticación de Flower
5. THE Flower SHALL persistir métricas de tareas para análisis histórico
6. WHEN un usuario accede a Flower sin credenciales válidas, THE Flower SHALL retornar HTTP 401 Unauthorized

### Requirement 3: Script de Verificación de Datos de Producción

**User Story:** Como administrador del sistema, quiero ejecutar un script de verificación que confirme que todos los datos maestros están cargados correctamente, para asegurar que el sistema está listo para uso productivo.

#### Acceptance Criteria

1. THE Management_Command SHALL verificar la existencia de las 5 Checklist_Template en la base de datos
2. THE Management_Command SHALL verificar que cada plantilla tiene el código correcto y Vehicle_Type asignado
3. THE Management_Command SHALL verificar que existen roles de usuario (ADMIN, SUPERVISOR, OPERADOR) en el sistema
4. THE Management_Command SHALL reportar un resumen con conteo de plantillas, usuarios, y roles encontrados
5. THE Management_Command SHALL retornar código de salida 0 si todas las verificaciones pasan, 1 si alguna falla
6. THE Management_Command SHALL listar elementos faltantes con mensajes descriptivos cuando detecte datos incompletos

### Requirement 4: Documentación de Procedimientos de Carga de Datos

**User Story:** Como administrador del sistema, quiero documentación clara de cómo cargar datos en producción usando Railway CLI, para poder repetir el proceso de forma confiable.

#### Acceptance Criteria

1. THE Documentation SHALL incluir comandos exactos para ejecutar Management_Command usando Railway_CLI
2. THE Documentation SHALL incluir pasos para verificar que los datos se cargaron correctamente
3. THE Documentation SHALL incluir comandos para acceder a logs de Railway para troubleshooting
4. THE Documentation SHALL incluir URLs de acceso a Flower y credenciales de configuración
5. THE Documentation SHALL incluir procedimiento de rollback en caso de errores durante la carga

### Requirement 5: Configuración de Variables de Entorno para Producción

**User Story:** Como administrador del sistema, quiero configurar todas las variables de entorno necesarias para Celery y Flower en Railway, para que los servicios funcionen correctamente en producción.

#### Acceptance Criteria

1. THE Production_Environment SHALL tener configurada variable CELERY_BROKER_URL apuntando al broker Redis o RabbitMQ
2. THE Production_Environment SHALL tener configurada variable CELERY_RESULT_BACKEND para almacenar resultados de tareas
3. THE Production_Environment SHALL tener configuradas variables FLOWER_BASIC_AUTH con usuario y contraseña
4. THE Production_Environment SHALL tener configurada variable FLOWER_PORT para el puerto de escucha de Flower
5. THE Documentation SHALL listar todas las variables de entorno requeridas con valores de ejemplo
6. WHEN una variable de entorno requerida está ausente, THE Backend_API SHALL registrar error en logs y fallar el inicio del servicio

### Requirement 6: Backup de Datos Maestros

**User Story:** Como administrador del sistema, quiero exportar las plantillas de checklist a archivos JSON, para tener respaldo de los datos maestros y poder restaurarlos si es necesario.

#### Acceptance Criteria

1. THE Management_Command SHALL exportar todas las Checklist_Template a archivo JSON con formato legible
2. THE Management_Command SHALL incluir todos los campos de cada plantilla incluyendo items, código, y Vehicle_Type
3. THE Management_Command SHALL permitir especificar ruta de salida del archivo JSON mediante argumento
4. THE Management_Command SHALL crear archivo con timestamp en el nombre para evitar sobrescritura accidental
5. THE Management_Command SHALL validar que el JSON exportado es válido y puede ser re-importado
