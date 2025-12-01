# Implementation Plan: Sistema de Permisos por Roles

## Phase 1: Backend Core Permissions

- [x] 1. Crear clases de permisos base



  - Crear archivo `backend/apps/core/permissions.py`
  - Implementar `IsOperadorOrAbove`
  - Implementar `IsSupervisorOrAbove`
  - Implementar `IsAdminOnly`
  - Implementar `IsOwnerOrSupervisor`
  - _Requirements: 1.5, 5.4, 6.4_

- [x] 1.1 Escribir tests unitarios para permission classes




  - Test cada clase con diferentes roles
  - Test casos edge (usuario sin rol, rol inválido)
  - _Requirements: 1.5, 5.4, 6.4_

- [x] 2. Crear mixins de QuerySet con filtrado por rol



  - Crear archivo `backend/apps/core/mixins.py`
  - Implementar `RoleBasedQuerySetMixin`
  - Implementar `OwnerFilterMixin`
  - Implementar método `filter_by_role()`
  - _Requirements: 7.1, 7.2_

- [x] 2.1 Escribir tests para mixins


  - Test filtrado para cada rol
  - Test que operadores solo vean sus datos
  - Test que supervisores vean su equipo
  - Test que admins vean todo
  - _Requirements: 7.1, 7.2_

## Phase 2: Work Orders Permissions

- [x] 3. Aplicar permisos a Work Orders ViewSet



  - Actualizar `backend/apps/work_orders/views.py`
  - Agregar permission classes al ViewSet
  - Implementar `get_queryset()` con filtrado por rol
  - Filtrar por `assigned_to` para operadores
  - Filtrar por equipo para supervisores
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 3.1 Escribir property test para aislamiento de operadores


  - **Property 1: Role-Based Access Isolation**
  - **Validates: Requirements 1.1, 1.4**
  - Generar usuarios y work orders aleatorios
  - Verificar que operadores solo vean sus OT
  - _Requirements: 1.1, 1.4_

- [x] 3.2 Escribir property test para visibilidad de supervisor

  - **Property 2: Supervisor Team Visibility**
  - **Validates: Requirements 1.2**
  - Generar equipos aleatorios
  - Verificar que supervisores vean todo su equipo
  - _Requirements: 1.2_

- [x] 4. Agregar validación de permisos en acciones de WO



  - Validar permisos en `create()`
  - Validar permisos en `update()`
  - Validar permisos en `destroy()`
  - Retornar 403 si no tiene permisos
  - _Requirements: 1.4, 7.3, 7.4_

## Phase 3: Assets Permissions

- [x] 5. Aplicar permisos a Assets ViewSet


  - Actualizar `backend/apps/assets/views.py`
  - Agregar permission classes
  - Implementar `get_queryset()` con filtrado
  - Filtrar por activos de OT asignadas (operadores)
  - Filtrar por área (supervisores)
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5.1 Escribir property test para consistencia asset-workorder


  - **Property 4: Asset Access Consistency**
  - **Validates: Requirements 2.1**
  - Generar pares asset-workorder
  - Verificar consistencia de acceso
  - _Requirements: 2.1_

- [x] 6. Actualizar endpoints de asset details


  - Validar permisos en `retrieve()`
  - Retornar 404 en lugar de 403 (no revelar existencia)
  - _Requirements: 2.4_

## Phase 4: Predictions Permissions

- [x] 7. Aplicar permisos a Predictions ViewSet


  - Actualizar `backend/apps/ml_predictions/views.py`
  - Agregar permission classes
  - Implementar filtrado basado en acceso a activos
  - Heredar permisos de activos asociados
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 7.1 Escribir property test para alineación de predicciones

  - **Property 5: Prediction Access Alignment**
  - **Validates: Requirements 3.1, 3.2**
  - Verificar que acceso a predicción = acceso a activo
  - _Requirements: 3.1, 3.2_

- [x] 8. Filtrar notificaciones de predicciones


  - Actualizar `backend/apps/notifications/services.py`
  - Filtrar destinatarios según acceso al activo
  - Solo enviar a usuarios autorizados
  - _Requirements: 3.4, 8.1, 8.2_

## Phase 5: Reports Permissions

- [x] 9. Aplicar permisos a Reports ViewSet


  - Actualizar `backend/apps/reports/views.py`
  - Filtrar estadísticas por datos accesibles
  - Operadores: solo sus estadísticas
  - Supervisores: estadísticas de equipo
  - Admins: estadísticas globales
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 10. Filtrar exportación de datos


  - Actualizar métodos de export
  - Aplicar filtros de rol antes de exportar
  - _Requirements: 4.5_

## Phase 6: Users & Configuration Permissions

- [x] 11. Aplicar permisos a Users ViewSet


  - Actualizar `backend/apps/authentication/views.py`
  - Operadores: 403 en list
  - Supervisores: solo su equipo
  - Admins: todos los usuarios
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 11.1 Escribir property test para restricción de configuración

  - **Property 6: Configuration Modification Restriction**
  - **Validates: Requirements 6.1, 6.2, 6.4**
  - Verificar que no-admins no puedan modificar config
  - _Requirements: 6.1, 6.2, 6.4_

- [x] 12. Proteger endpoints de configuración

  - Actualizar `backend/apps/configuration/views.py`
  - Solo admins pueden modificar
  - Supervisores/operadores: 403
  - _Requirements: 6.1, 6.2, 6.3_

## Phase 7: Auditoría

- [x] 13. Crear modelo AccessLog


  - Crear migración para AccessLog
  - Definir campos: user, resource_type, resource_id, action, success, ip, timestamp
  - Agregar índices para queries eficientes
  - _Requirements: 9.1, 9.2_

- [x] 14. Implementar middleware de auditoría


  - Crear `backend/apps/core/middleware/audit.py`
  - Registrar todos los accesos a recursos
  - Registrar intentos fallidos (403)
  - Capturar IP address y user agent
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 14.1 Escribir property test para completitud de audit log

  - **Property 9: Audit Log Completeness**
  - **Validates: Requirements 9.1, 9.2**
  - Generar accesos aleatorios
  - Verificar que todos se registren
  - _Requirements: 9.1, 9.2_

- [x] 15. Crear endpoint de auditoría

  - Crear ViewSet para AccessLog
  - Solo accesible para admins
  - Filtros por usuario, recurso, fecha
  - _Requirements: 9.3_

- [x] 16. Implementar alertas de seguridad


  - Detectar múltiples intentos fallidos
  - Generar alerta para admins
  - _Requirements: 9.4_

## Phase 8: Frontend - Permission Guards

- [x] 17. Crear componente PermissionGuard


  - Crear `frontend/src/components/auth/PermissionGuard.tsx`
  - Aceptar prop `roles` (array de roles permitidos)
  - Ocultar children si usuario no tiene rol
  - Mostrar mensaje opcional si no tiene permisos
  - _Requirements: 10.1, 10.2, 10.3_

- [x] 18. Crear ProtectedRoute component


  - Crear `frontend/src/routes/ProtectedRoute.tsx`
  - Aceptar prop `requiredRole`
  - Redirigir a 403 page si no tiene permisos
  - _Requirements: 10.1, 10.2, 10.3_

- [x] 18.1 Escribir property test para visibilidad de UI

  - **Property 10: UI Element Visibility**
  - **Validates: Requirements 10.1, 10.2, 10.3**
  - Verificar que elementos solo sean visibles para roles correctos
  - _Requirements: 10.1, 10.2, 10.3_

## Phase 9: Frontend - Menu Adaptation

- [x] 19. Actualizar Sidebar con filtrado por rol




  - Actualizar `frontend/src/components/layout/Sidebar.tsx`
  - Agregar prop `requiredRole` a menu items
  - Filtrar items según rol del usuario
  - Ocultar secciones completas si no tiene acceso
  - _Requirements: 10.4_

- [x] 20. Adaptar Dashboard según rol


  - Actualizar `frontend/src/pages/Dashboard.tsx`
  - Mostrar solo widgets relevantes para cada rol
  - Operadores: sus OT y activos
  - Supervisores: estadísticas de equipo
  - Admins: vista global
  - _Requirements: 10.1, 10.2, 10.3_

## Phase 10: Frontend - Forms & Details

- [x] 21. Deshabilitar campos según permisos


  - Actualizar formularios de Work Orders
  - Operadores: solo pueden editar ciertos campos
  - Supervisores: más campos editables
  - Admins: todos los campos
  - _Requirements: 10.5_

- [x] 22. Agregar mensajes informativos


  - Mostrar por qué un campo está deshabilitado
  - Mostrar qué rol se necesita para editar
  - _Requirements: 10.5_

## Phase 11: Integration & Testing

- [x] 23. Checkpoint - Ejecutar todos los tests


  - Ejecutar tests unitarios
  - Ejecutar property tests
  - Verificar que todos pasen
  - Corregir fallos si los hay
  - Ensure all tests pass, ask the user if questions arise.

- [x] 23.1 Escribir property test para aplicación automática de filtros


  - **Property 7: Automatic Filter Application**
  - **Validates: Requirements 7.1, 7.2**
  - Verificar que todos los endpoints filtren automáticamente
  - _Requirements: 7.1, 7.2_

- [x] 23.2 Escribir property test para filtrado de notificaciones



  - **Property 8: Notification Recipient Filtering**
  - **Validates: Requirements 8.1, 8.2**
  - Verificar que notificaciones solo vayan a usuarios autorizados
  - _Requirements: 8.1, 8.2_

- [x] 24. Tests de integración end-to-end



  - Test flujo completo: login como operador → intentar acceder OT ajena → verificar 403
  - Test flujo: login como supervisor → ver equipo completo
  - Test flujo: login como admin → ver todo
  - _Requirements: All_

## Phase 12: Documentation & Deployment

- [x] 25. Crear documentación para desarrolladores


  - Guía de uso de permission classes
  - Ejemplos de código
  - Guía de testing
  - _Requirements: All_

- [x] 26. Crear documentación para usuarios


  - Documento explicando roles
  - Qué puede hacer cada rol
  - Cómo solicitar cambio de rol
  - _Requirements: All_

- [x] 27. Preparar migración gradual


  - Agregar feature flag `ENABLE_RBAC`
  - Por defecto en False (backward compatible)
  - Documentar proceso de activación
  - _Requirements: All_

- [x] 28. Checkpoint Final - Verificación completa



  - Verificar que operadores solo vean sus datos
  - Verificar que supervisores vean su equipo
  - Verificar que admins vean todo
  - Verificar audit logs funcionando
  - Verificar frontend adaptado
  - Ensure all tests pass, ask the user if questions arise.
