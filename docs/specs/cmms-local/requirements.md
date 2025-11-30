# Requirements Document - Sistema CMMS Local

## Introduction

Este documento define los requisitos para un Sistema de Gestión de Mantenimiento Computarizado (CMMS) desarrollado completamente para entorno local. El sistema gestiona activos industriales, órdenes de trabajo, mantenimiento preventivo, inventario de repuestos y checklists específicos por tipo de vehículo. 

**Tecnologías:**
- Backend: Django REST Framework
- Frontend: React + TypeScript + Vite
- Base de Datos: SQLite (desarrollo) / PostgreSQL (producción)
- Almacenamiento: Sistema de archivos local

## Glossary

- **CMMS_System**: Sistema completo de gestión de mantenimiento (backend + frontend)
- **Backend_API**: Servicio Django REST Framework con endpoints HTTP/REST
- **Frontend_App**: Aplicación React con TypeScript y Vite
- **Work_Order**: Orden de Trabajo que representa una tarea de mantenimiento
- **Asset**: Equipo o activo industrial registrado en el sistema
- **Vehicle_Type**: Tipo de vehículo (Camión Supersucker, Camioneta MDO, Retroexcavadora MDO, Cargador Frontal MDO, Minicargador MDO)
- **Maintenance_Plan**: Plan de mantenimiento preventivo programado
- **Checklist**: Lista de verificación para inspecciones de mantenimiento
- **Checklist_Template**: Plantilla predefinida de checklist por tipo de vehículo
- **Spare_Part**: Repuesto o pieza de inventario
- **User_Role**: Rol de usuario (ADMIN, SUPERVISOR, OPERADOR)
- **Local_Database**: Base de datos local (SQLite o PostgreSQL)
- **Notification**: Notificación del sistema almacenada en base de datos

## Requirements

### Requirement 1: Gestión de Vehículos y Activos

**User Story:** Como administrador, quiero gestionar el inventario de vehículos con sus documentos, para mantener un registro centralizado de todos los recursos de la flota.

#### Acceptance Criteria

1. THE Backend_API SHALL provide CRUD endpoints for Asset management including name, Vehicle_Type, model, serial number, license plate, location, installation date, and status
2. THE Backend_API SHALL restrict Vehicle_Type to five predefined types (Camión Supersucker, Camioneta MDO, Retroexcavadora MDO, Cargador Frontal MDO, Minicargador MDO)
3. WHEN a user uploads a document for an Asset, THE Backend_API SHALL store the file locally in media folder and save the reference path in Local_Database
4. THE Frontend_App SHALL display a searchable and filterable list of Assets with pagination and filtering by Vehicle_Type
5. THE Backend_API SHALL validate that Asset serial numbers and license plates are unique within the system
6. WHEN an Asset is deleted, THE Backend_API SHALL archive the record instead of permanent deletion to maintain historical data

### Requirement 2: Órdenes de Trabajo

**User Story:** Como supervisor, quiero crear, asignar y dar seguimiento a órdenes de trabajo, para coordinar las actividades de mantenimiento del equipo técnico.

#### Acceptance Criteria

1. THE Backend_API SHALL provide endpoints to create Work_Order with title, description, priority, assigned technician, Asset reference, scheduled date, and status
2. WHEN a Work_Order is created or updated, THE Backend_API SHALL create Notification records in Local_Database for assigned users
3. THE Frontend_App SHALL display Work_Order status transitions (pending, in-progress, completed, cancelled)
4. THE Backend_API SHALL allow filtering Work_Order by status, priority, assigned user, and date range
5. WHEN a Work_Order is completed, THE Backend_API SHALL require completion notes and actual hours worked before status change

### Requirement 3: Planes de Mantenimiento

**User Story:** Como ingeniero, quiero programar planes de mantenimiento preventivo para los activos, para reducir fallas inesperadas y optimizar la disponibilidad de equipos.

#### Acceptance Criteria

1. THE Backend_API SHALL provide endpoints to create Maintenance_Plan with recurrence rules (daily, weekly, monthly, custom intervals)
2. THE Frontend_App SHALL display a calendar view showing scheduled and completed maintenance activities
3. THE Backend_API SHALL allow pausing and resuming Maintenance_Plan without deleting historical data
4. THE Backend_API SHALL automatically calculate next_due_date based on recurrence rules

### Requirement 4: Inventario de Repuestos

**User Story:** Como técnico, quiero consultar la disponibilidad de repuestos y recibir alertas de stock bajo, para asegurar que tengo las piezas necesarias antes de iniciar un trabajo.

#### Acceptance Criteria

1. THE Backend_API SHALL provide CRUD endpoints for Spare_Part management including part number, description, quantity, minimum stock level, and location
2. WHEN Spare_Part quantity falls below minimum stock level, THE Backend_API SHALL create an alert Notification in Local_Database
3. THE Backend_API SHALL track Spare_Part usage history linked to Work_Order for consumption analysis
4. THE Frontend_App SHALL display Spare_Part inventory with visual indicators for low stock items
5. THE Backend_API SHALL validate that Spare_Part quantities cannot be negative values

### Requirement 5: Checklists por Tipo de Vehículo

**User Story:** Como supervisor, quiero utilizar checklists predefinidos específicos para cada tipo de vehículo y generar PDFs de inspecciones completadas, para estandarizar procedimientos y mantener registros de cumplimiento.

#### Acceptance Criteria

1. THE Backend_API SHALL provide five predefined Checklist_Template for the five Vehicle_Type with codes (F-PR-020-CH01, F-PR-034-CH01, F-PR-037-CH01, F-PR-040-CH01, Camión Supersucker)
2. THE Backend_API SHALL prevent deletion or modification of predefined Checklist_Template structure to maintain standardization
3. WHEN a Checklist is completed, THE Backend_API SHALL generate a PDF report matching the original format and store it in local media folder
4. THE Frontend_App SHALL allow completing Checklist items with response types including yes/no, text, numeric values, and photo uploads
5. THE Backend_API SHALL link completed Checklist to Work_Order and Asset for traceability
6. THE Backend_API SHALL calculate Checklist completion percentage and flag items marked as non-compliant or requiring attention

### Requirement 6: Autenticación y Autorización

**User Story:** Como administrador de seguridad, quiero controlar el acceso al sistema mediante autenticación robusta y tres perfiles específicos (ADMIN, SUPERVISOR, OPERADOR), para proteger información sensible y limitar acciones según responsabilidades.

#### Acceptance Criteria

1. THE Backend_API SHALL implement JWT-based authentication for all protected endpoints
2. THE Backend_API SHALL support exactly three User_Role types (ADMIN, SUPERVISOR, OPERADOR) with specific permissions
3. THE Backend_API SHALL allow ADMIN and SUPERVISOR roles to view all Work_Order, Assets, and Checklists
4. THE Backend_API SHALL restrict OPERADOR role to view only assigned Work_Order and Checklists for their assigned Assets
5. THE Backend_API SHALL allow only ADMIN role to access administration module for user management, master data, and system configuration
6. WHEN a user attempts an unauthorized action, THE Backend_API SHALL return HTTP 403 Forbidden status with descriptive error message
7. THE Backend_API SHALL log all authentication attempts and authorization failures for security audit in Local_Database

### Requirement 7: Sistema de Notificaciones

**User Story:** Como técnico, quiero recibir notificaciones cuando se me asigna una orden de trabajo o hay cambios importantes, para responder rápidamente a las necesidades operativas.

#### Acceptance Criteria

1. THE Backend_API SHALL create Notification records in Local_Database for Work_Order assignments, status changes, and alerts
2. THE Frontend_App SHALL display notifications in a notification center with unread count indicator
3. THE Backend_API SHALL allow users to mark notifications as read
4. THE Backend_API SHALL allow users to configure notification preferences for different event types
5. THE Frontend_App SHALL poll for new notifications every 30 seconds when user is active

### Requirement 8: Reportes y Analíticas

**User Story:** Como gerente de operaciones, quiero generar reportes personalizados sobre indicadores de mantenimiento, para tomar decisiones basadas en datos y presentar resultados a la dirección.

#### Acceptance Criteria

1. THE Backend_API SHALL provide endpoints to generate reports for Work_Order completion rates, Asset downtime, and Spare_Part consumption
2. THE Frontend_App SHALL display interactive charts using Recharts library for KPIs including MTBF, MTTR, OEE, and maintenance costs
3. THE Backend_API SHALL allow exporting report data in CSV and JSON formats
4. THE Frontend_App SHALL provide date range filters and Asset grouping options for custom report generation
5. THE Backend_API SHALL calculate KPIs based on historical data stored in Local_Database

### Requirement 9: Gestión de Ubicaciones

**User Story:** Como administrador, quiero crear y gestionar ubicaciones físicas donde se encuentran los activos, para organizar geográficamente el inventario de equipos y facilitar la planificación logística.

#### Acceptance Criteria

1. THE Backend_API SHALL provide CRUD endpoints for Location management including name, address, coordinates, and description fields
2. THE Backend_API SHALL validate that Location names are unique within the system
3. THE Backend_API SHALL prevent deletion of Location records that are referenced by existing Assets
4. THE Frontend_App SHALL display a list of all locations with search and filter capabilities accessible only to ADMIN role
5. THE Frontend_App SHALL provide a form interface for creating and editing locations accessible only to ADMIN role

### Requirement 10: Gestión de Usuarios

**User Story:** Como administrador, quiero crear y gestionar cuentas de usuario con sus roles y permisos, para controlar el acceso al sistema y asignar responsabilidades apropiadas.

#### Acceptance Criteria

1. THE Backend_API SHALL provide CRUD endpoints for User management including username, email, full name, User_Role, and active status fields
2. THE Backend_API SHALL validate that usernames and email addresses are unique within the system
3. THE Backend_API SHALL allow only ADMIN role to create, modify, and deactivate user accounts
4. THE Frontend_App SHALL display a user management interface with list, create, edit, and deactivate functions accessible only to ADMIN role
5. THE Backend_API SHALL require password change on first login for new user accounts
6. THE Backend_API SHALL hash all passwords using Django's built-in password hashing before storing in Local_Database

### Requirement 11: Monitoreo Completo de Estado de Activos

**User Story:** Como usuario del sistema, quiero visualizar todos los activos con sus características completas y un historial detallado de todas las actividades realizadas, para tener una visión integral del estado y mantenimiento de cada equipo.

#### Acceptance Criteria

1. THE Frontend_App SHALL display a comprehensive dashboard showing all Assets with their complete characteristics including name, Vehicle_Type, model, serial number, license plate, location, installation date, current status, odometer reading, and fuel level
2. THE Frontend_App SHALL provide interactive visualizations using Chart.js or Recharts library showing Asset status distribution, fuel level distribution, maintenance frequency, and downtime trends
3. THE Backend_API SHALL provide an endpoint to retrieve complete Asset history including all status updates, Work_Order assignments, completed maintenance activities, Checklist completions, and Spare_Part usage
4. THE Frontend_App SHALL display a unified timeline view for each Asset showing chronological history of all activities with timestamps, responsible users, and activity details
5. THE Backend_API SHALL allow OPERADOR role to update status only for Assets assigned to them through active Work_Order
6. THE Backend_API SHALL allow ADMIN and SUPERVISOR roles to update status for any Asset and view complete history for all Assets
7. THE Backend_API SHALL create a status history record with timestamp, user, and previous values for each status update in Local_Database
8. WHEN an Asset status is updated to "Fuera de Servicio", THE Backend_API SHALL create an alert Notification to ADMIN and SUPERVISOR roles
9. THE Frontend_App SHALL provide filtering and sorting capabilities for Asset list by status, Vehicle_Type, location, fuel level, and last activity date
10. THE Frontend_App SHALL display real-time KPIs for each Asset including total maintenance hours, number of work orders completed, average downtime, and maintenance cost

### Requirement 12: API Documentation y Extensibilidad

**User Story:** Como desarrollador, quiero que el CMMS tenga documentación completa de la API y sea extensible para futuras funcionalidades, para facilitar el mantenimiento y evolución del sistema.

#### Acceptance Criteria

1. THE Backend_API SHALL expose OpenAPI (Swagger) documentation for all REST endpoints
2. THE Backend_API SHALL support API versioning with /api/v1/ prefix to maintain backward compatibility during updates
3. THE Backend_API SHALL implement rate limiting of 100 requests per minute per user to prevent abuse
4. THE CMMS_System SHALL use environment variables for all configuration parameters to support multiple deployment environments
5. THE Backend_API SHALL provide health check endpoints for monitoring system status

### Requirement 13: Configuración y Datos Maestros

**User Story:** Como administrador del sistema, quiero configurar parámetros globales y gestionar datos maestros como ubicaciones y categorías, para personalizar el sistema según las necesidades de la organización.

#### Acceptance Criteria

1. THE Backend_API SHALL provide endpoints to manage master data including Asset categories, locations, priority levels, and Work_Order types
2. THE Backend_API SHALL validate that master data deletions are prevented when referenced by existing records
3. THE Frontend_App SHALL provide administration interface for User_Role management and permission assignment accessible only to ADMIN
4. THE Backend_API SHALL maintain audit trail of all configuration changes with user and timestamp information in Local_Database
5. THE Backend_API SHALL allow configuration of system parameters including notification settings and report schedules

