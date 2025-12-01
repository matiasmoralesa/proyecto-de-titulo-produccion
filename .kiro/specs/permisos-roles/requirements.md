# Requirements Document: Sistema de Permisos por Roles

## Introduction

El sistema CMMS actualmente permite que todos los usuarios vean toda la información sin restricciones. Se requiere implementar un sistema de control de acceso basado en roles (RBAC) para que cada tipo de usuario solo pueda acceder a la información que le corresponde según su rol.

## Glossary

- **RBAC**: Role-Based Access Control - Control de acceso basado en roles
- **Operador**: Usuario con rol OPERADOR que solo debe ver sus propias asignaciones
- **Supervisor**: Usuario con rol SUPERVISOR que puede ver todo su equipo
- **Admin**: Usuario con rol ADMIN que puede ver todo el sistema
- **OT**: Orden de Trabajo (Work Order)
- **Activo**: Equipo o máquina del sistema
- **Predicción**: Predicción de fallo generada por ML

## Requirements

### Requirement 1: Control de Acceso a Órdenes de Trabajo

**User Story:** Como operador, quiero ver solo mis órdenes de trabajo asignadas, para no confundirme con las de otros operadores.

#### Acceptance Criteria

1. WHEN un operador consulta órdenes de trabajo THEN el sistema SHALL retornar solo las órdenes asignadas a ese operador
2. WHEN un supervisor consulta órdenes de trabajo THEN el sistema SHALL retornar todas las órdenes de su equipo
3. WHEN un admin consulta órdenes de trabajo THEN el sistema SHALL retornar todas las órdenes del sistema
4. WHEN un operador intenta acceder a una OT no asignada THEN el sistema SHALL retornar error 403 Forbidden
5. WHEN un usuario sin rol válido intenta acceder THEN el sistema SHALL retornar error 401 Unauthorized

### Requirement 2: Control de Acceso a Activos

**User Story:** Como operador, quiero ver solo los activos relacionados con mis órdenes de trabajo, para enfocarme en mi trabajo.

#### Acceptance Criteria

1. WHEN un operador consulta activos THEN el sistema SHALL retornar solo activos de sus OT asignadas
2. WHEN un supervisor consulta activos THEN el sistema SHALL retornar todos los activos de su área
3. WHEN un admin consulta activos THEN el sistema SHALL retornar todos los activos del sistema
4. WHEN un operador intenta ver detalles de un activo no relacionado THEN el sistema SHALL retornar error 403
5. WHEN se lista activos THEN el sistema SHALL filtrar automáticamente según el rol del usuario

### Requirement 3: Control de Acceso a Predicciones

**User Story:** Como operador, quiero ver solo las predicciones de los activos que manejo, para no recibir información irrelevante.

#### Acceptance Criteria

1. WHEN un operador consulta predicciones THEN el sistema SHALL retornar solo predicciones de sus activos asignados
2. WHEN un supervisor consulta predicciones THEN el sistema SHALL retornar predicciones de su área
3. WHEN un admin consulta predicciones THEN el sistema SHALL retornar todas las predicciones
4. WHEN se generan notificaciones de predicciones THEN el sistema SHALL enviar solo a usuarios con acceso al activo
5. WHEN un operador intenta acceder a una predicción no autorizada THEN el sistema SHALL retornar error 403

### Requirement 4: Control de Acceso a Reportes

**User Story:** Como supervisor, quiero ver reportes de mi equipo, para evaluar su desempeño sin ver otros equipos.

#### Acceptance Criteria

1. WHEN un operador consulta reportes THEN el sistema SHALL retornar solo sus propias estadísticas
2. WHEN un supervisor consulta reportes THEN el sistema SHALL retornar estadísticas de su equipo
3. WHEN un admin consulta reportes THEN el sistema SHALL retornar estadísticas globales
4. WHEN se generan reportes automáticos THEN el sistema SHALL filtrar datos según el rol del solicitante
5. WHEN se exportan datos THEN el sistema SHALL incluir solo datos autorizados para ese rol

### Requirement 5: Control de Acceso a Usuarios

**User Story:** Como admin, quiero ser el único que pueda gestionar usuarios, para mantener la seguridad del sistema.

#### Acceptance Criteria

1. WHEN un operador intenta listar usuarios THEN el sistema SHALL retornar error 403
2. WHEN un supervisor intenta listar usuarios THEN el sistema SHALL retornar solo su equipo
3. WHEN un admin lista usuarios THEN el sistema SHALL retornar todos los usuarios
4. WHEN un no-admin intenta crear/editar usuarios THEN el sistema SHALL retornar error 403
5. WHEN un admin gestiona usuarios THEN el sistema SHALL permitir todas las operaciones CRUD

### Requirement 6: Control de Acceso a Configuración

**User Story:** Como admin, quiero ser el único que pueda modificar configuraciones del sistema, para evitar cambios no autorizados.

#### Acceptance Criteria

1. WHEN un operador intenta acceder a configuración THEN el sistema SHALL retornar error 403
2. WHEN un supervisor intenta modificar configuración global THEN el sistema SHALL retornar error 403
3. WHEN un admin accede a configuración THEN el sistema SHALL permitir lectura y escritura
4. WHEN se intenta modificar roles/permisos THEN el sistema SHALL verificar que el usuario sea admin
5. WHEN se auditan cambios de configuración THEN el sistema SHALL registrar el usuario que realizó el cambio

### Requirement 7: Filtrado Automático en APIs

**User Story:** Como desarrollador, quiero que las APIs filtren automáticamente según el rol, para no tener que implementar lógica de permisos en cada endpoint.

#### Acceptance Criteria

1. WHEN se consulta cualquier endpoint de listado THEN el sistema SHALL aplicar filtros de rol automáticamente
2. WHEN se consulta un detalle de recurso THEN el sistema SHALL verificar permisos antes de retornar
3. WHEN se intenta crear un recurso THEN el sistema SHALL validar que el usuario tenga permisos
4. WHEN se intenta actualizar un recurso THEN el sistema SHALL verificar propiedad o permisos superiores
5. WHEN se intenta eliminar un recurso THEN el sistema SHALL verificar permisos de admin

### Requirement 8: Notificaciones Filtradas

**User Story:** Como operador, quiero recibir solo notificaciones relevantes a mi trabajo, para no ser interrumpido innecesariamente.

#### Acceptance Criteria

1. WHEN se genera una notificación de OT THEN el sistema SHALL enviar solo al operador asignado y supervisores
2. WHEN se genera una notificación de predicción THEN el sistema SHALL enviar solo a usuarios con acceso al activo
3. WHEN se genera una alerta crítica THEN el sistema SHALL enviar a todos los roles según configuración
4. WHEN un usuario configura preferencias de notificación THEN el sistema SHALL respetar filtros de rol
5. WHEN se envían notificaciones masivas THEN el sistema SHALL filtrar destinatarios según permisos

### Requirement 9: Auditoría de Accesos

**User Story:** Como admin, quiero ver un registro de quién accede a qué información, para detectar accesos no autorizados.

#### Acceptance Criteria

1. WHEN un usuario accede a un recurso THEN el sistema SHALL registrar el acceso en el log de auditoría
2. WHEN se intenta un acceso no autorizado THEN el sistema SHALL registrar el intento fallido
3. WHEN un admin consulta auditoría THEN el sistema SHALL mostrar todos los accesos y intentos
4. WHEN se detectan múltiples intentos fallidos THEN el sistema SHALL generar una alerta de seguridad
5. WHEN se exporta auditoría THEN el sistema SHALL incluir usuario, recurso, acción, timestamp y resultado

### Requirement 10: Interfaz de Usuario Adaptativa

**User Story:** Como usuario, quiero que la interfaz muestre solo las opciones disponibles para mi rol, para no ver opciones que no puedo usar.

#### Acceptance Criteria

1. WHEN un operador accede al sistema THEN la interfaz SHALL ocultar opciones de admin/supervisor
2. WHEN un supervisor accede al sistema THEN la interfaz SHALL mostrar opciones de gestión de equipo
3. WHEN un admin accede al sistema THEN la interfaz SHALL mostrar todas las opciones
4. WHEN se renderiza un menú THEN el sistema SHALL filtrar items según permisos del usuario
5. WHEN se muestra un formulario THEN el sistema SHALL deshabilitar campos no editables según rol
