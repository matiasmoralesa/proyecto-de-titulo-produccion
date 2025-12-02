# Requirements Document

## Introduction

Este documento especifica los requisitos para corregir tres problemas críticos en el sistema CMMS:
1. KPIs del dashboard mostrando valores negativos incorrectos
2. Error 404 al hacer clic en notificaciones
3. Página de configuración sin funcionalidad CRUD completa

## Glossary

- **CMMS**: Sistema de Gestión de Mantenimiento Computarizado (Computerized Maintenance Management System)
- **KPI**: Indicador Clave de Desempeño (Key Performance Indicator)
- **Dashboard**: Página principal del sistema que muestra estadísticas y métricas
- **Notification System**: Sistema de notificaciones que alerta a los usuarios sobre eventos importantes
- **Configuration Page**: Página de administración para gestionar datos maestros del sistema
- **Work Order**: Orden de Trabajo (OT) - documento que describe tareas de mantenimiento
- **Asset**: Activo - equipo o maquinaria gestionada por el sistema
- **CRUD**: Create, Read, Update, Delete - operaciones básicas de gestión de datos

## Requirements

### Requirement 1

**User Story:** Como supervisor o administrador, quiero ver KPIs con valores correctos y positivos en el dashboard, para poder tomar decisiones basadas en datos precisos.

#### Acceptance Criteria

1. WHEN the system calculates average work order duration THEN the system SHALL ensure the result is never negative
2. WHEN a work order has invalid date data (completed_date before created_at) THEN the system SHALL exclude it from KPI calculations
3. WHEN displaying KPI values THEN the system SHALL format negative values as zero or handle them appropriately
4. WHEN calculating time-based metrics THEN the system SHALL validate date consistency before performing calculations
5. WHEN KPI calculations encounter data errors THEN the system SHALL log the error and continue with valid data only

### Requirement 2

**User Story:** Como usuario del sistema, quiero poder hacer clic en notificaciones y ser dirigido a la página correcta del objeto relacionado, para poder actuar rápidamente sobre los eventos notificados.

#### Acceptance Criteria

1. WHEN a user clicks on a work order notification THEN the system SHALL navigate to the work order detail page if it exists
2. WHEN a user clicks on an asset notification THEN the system SHALL navigate to the asset detail page if it exists
3. WHEN a notification references a non-existent object THEN the system SHALL display an error message instead of showing 404 page
4. WHEN navigating from a notification THEN the system SHALL verify the route exists before navigation
5. WHEN a notification has no related object THEN the system SHALL mark it as read without attempting navigation

### Requirement 3

**User Story:** Como administrador, quiero poder crear, editar y eliminar categorías de activos, prioridades, tipos de órdenes de trabajo y parámetros del sistema desde la página de configuración, para mantener los datos maestros actualizados.

#### Acceptance Criteria

1. WHEN an administrator creates a new asset category THEN the system SHALL validate the data and save it to the database
2. WHEN an administrator edits an existing priority THEN the system SHALL update the record with the new values
3. WHEN an administrator deletes a work order type THEN the system SHALL verify it can be deleted and remove it from the database
4. WHEN an administrator saves a system parameter THEN the system SHALL validate the data type matches the parameter definition
5. WHEN form validation fails THEN the system SHALL display specific error messages for each invalid field
6. WHEN a CRUD operation succeeds THEN the system SHALL refresh the data table and show a success message
7. WHEN a CRUD operation fails THEN the system SHALL display an error message without closing the modal

### Requirement 4

**User Story:** Como administrador, quiero que los formularios de configuración tengan validación completa y campos apropiados, para evitar errores al gestionar datos maestros.

#### Acceptance Criteria

1. WHEN creating or editing a category THEN the system SHALL provide fields for code, name, description, and active status
2. WHEN creating or editing a priority THEN the system SHALL provide fields for level, name, color code, and active status
3. WHEN creating or editing a work order type THEN the system SHALL provide fields for code, name, description, and active status
4. WHEN editing a system parameter THEN the system SHALL only allow editing if is_editable is true
5. WHEN a required field is empty THEN the system SHALL prevent form submission and highlight the field
6. WHEN a color code is entered THEN the system SHALL validate it is a valid hex color format
7. WHEN a code or key already exists THEN the system SHALL prevent duplicate entries and show an error message
