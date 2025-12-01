# Design Document: Sistema de Permisos por Roles

## Overview

Este documento describe el diseño técnico para implementar un sistema completo de control de acceso basado en roles (RBAC) en el sistema CMMS. El objetivo es restringir el acceso a la información según el rol del usuario (OPERADOR, SUPERVISOR, ADMIN), asegurando que cada usuario solo pueda ver y modificar los datos que le corresponden.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  - Menús adaptados por rol                                  │
│  - Componentes con permisos                                 │
│  - Rutas protegidas                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     │
┌────────────────────▼────────────────────────────────────────┐
│              API Layer (Django REST)                         │
│  - Permission Classes                                       │
│  - ViewSet Mixins                                          │
│  - Filtros automáticos                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           Business Logic Layer                               │
│  - RoleBasedQuerySet                                        │
│  - Permission Decorators                                    │
│  - Audit Logging                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Data Layer (PostgreSQL)                         │
│  - Users & Roles                                           │
│  - Work Orders                                             │
│  - Assets, Predictions, etc.                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction

```
User Request
    ↓
Authentication Middleware
    ↓
Permission Check
    ↓
Role-Based Filter
    ↓
Query Database
    ↓
Return Filtered Results
```

## Components and Interfaces

### 1. Permission Classes (Backend)

**Ubicación**: `backend/apps/core/permissions.py`

```python
class IsOperadorOrAbove(BasePermission)
class IsSupervisorOrAbove(BasePermission)  
class IsAdmin(BasePermission)
class IsOwnerOrSupervisor(BasePermission)
```

### 2. QuerySet Mixins (Backend)

**Ubicación**: `backend/apps/core/mixins.py`

```python
class RoleBasedQuerySetMixin:
    def get_queryset(self):
        # Filtra automáticamente según rol
        
class OwnerFilterMixin:
    def filter_by_owner(self, queryset, user):
        # Filtra por propietario
```

### 3. ViewSet Base Classes (Backend)

**Ubicación**: `backend/apps/core/viewsets.py`

```python
class RoleBasedViewSet(viewsets.ModelViewSet):
    # ViewSet base con filtrado automático
    
class ReadOnlyForOperadorViewSet(viewsets.ModelViewSet):
    # Solo lectura para operadores
```

### 4. Frontend Permission HOC

**Ubicación**: `frontend/src/components/auth/PermissionGuard.tsx`

```typescript
<PermissionGuard roles={['ADMIN', 'SUPERVISOR']}>
  <AdminPanel />
</PermissionGuard>
```

### 5. Frontend Route Protection

**Ubicación**: `frontend/src/routes/ProtectedRoute.tsx`

```typescript
<ProtectedRoute requiredRole="ADMIN">
  <UsersPage />
</ProtectedRoute>
```

## Data Models

### Existing Models (No changes needed)

```python
class Role:
    name: str  # ADMIN, SUPERVISOR, OPERADOR
    description: str

class User:
    role: ForeignKey(Role)
    # ... otros campos
```

### New Model: AccessLog (Auditoría)

```python
class AccessLog(models.Model):
    user = ForeignKey(User)
    resource_type = CharField()  # 'workorder', 'asset', etc.
    resource_id = CharField()
    action = CharField()  # 'view', 'create', 'update', 'delete'
    success = BooleanField()
    ip_address = GenericIPAddressField()
    timestamp = DateTimeField(auto_now_add=True)
    details = JSONField()
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Role-Based Access Isolation
*For any* operador user and any work order not assigned to them, attempting to access that work order should result in a 403 Forbidden response.
**Validates: Requirements 1.1, 1.4**

### Property 2: Supervisor Team Visibility
*For any* supervisor user, querying work orders should return all work orders assigned to users in their team and no work orders from other teams.
**Validates: Requirements 1.2**

### Property 3: Admin Global Access
*For any* admin user, querying any resource should return all instances of that resource without filtering.
**Validates: Requirements 1.3, 2.3, 3.3**

### Property 4: Asset Access Consistency
*For any* operador user, if they can access a work order, they should be able to access the associated asset, and vice versa.
**Validates: Requirements 2.1**

### Property 5: Prediction Access Alignment
*For any* user and any prediction, if the user has access to the associated asset, they should have access to the prediction.
**Validates: Requirements 3.1, 3.2**

### Property 6: Configuration Modification Restriction
*For any* non-admin user, attempting to modify system configuration should result in a 403 Forbidden response.
**Validates: Requirements 6.1, 6.2, 6.4**

### Property 7: Automatic Filter Application
*For any* list endpoint and any user, the returned results should only include resources that the user has permission to access based on their role.
**Validates: Requirements 7.1, 7.2**

### Property 8: Notification Recipient Filtering
*For any* notification about a work order, the recipients should only include the assigned operador, their supervisors, and admins.
**Validates: Requirements 8.1, 8.2**

### Property 9: Audit Log Completeness
*For any* resource access attempt, whether successful or failed, an entry should be created in the access log with user, resource, action, and result.
**Validates: Requirements 9.1, 9.2**

### Property 10: UI Element Visibility
*For any* user interface element requiring specific permissions, that element should only be visible to users with the required role.
**Validates: Requirements 10.1, 10.2, 10.3**

## Implementation Strategy

### Phase 1: Backend Permissions (Core)

1. **Create Permission Classes**
   - Implementar clases de permisos reutilizables
   - Agregar a `apps/core/permissions.py`

2. **Create QuerySet Mixins**
   - Implementar filtrado automático por rol
   - Agregar a `apps/core/mixins.py`

3. **Update ViewSets**
   - Aplicar permission classes a todos los ViewSets
   - Agregar filtrado automático en `get_queryset()`

### Phase 2: Specific Resource Permissions

4. **Work Orders**
   - Filtrar por `assigned_to` para operadores
   - Filtrar por equipo para supervisores
   - Sin filtro para admins

5. **Assets**
   - Filtrar por activos de OT asignadas para operadores
   - Filtrar por área para supervisores
   - Sin filtro para admins

6. **Predictions**
   - Filtrar por activos accesibles
   - Heredar permisos de activos

7. **Reports**
   - Filtrar estadísticas por datos accesibles
   - Agregar parámetros de filtro por rol

### Phase 3: Auditoría

8. **Access Logging**
   - Crear modelo AccessLog
   - Implementar middleware de auditoría
   - Registrar todos los accesos

9. **Audit Dashboard**
   - Crear endpoint para consultar logs
   - Solo accesible para admins

### Phase 4: Frontend

10. **Permission Guards**
    - Crear componente PermissionGuard
    - Envolver componentes sensibles

11. **Route Protection**
    - Crear ProtectedRoute component
    - Aplicar a rutas administrativas

12. **Menu Adaptation**
    - Filtrar items de menú por rol
    - Ocultar opciones no disponibles

13. **Form Field Restrictions**
    - Deshabilitar campos según permisos
    - Mostrar mensajes informativos

## Error Handling

### Permission Denied (403)

```json
{
  "error": "Permission denied",
  "detail": "You do not have permission to access this resource",
  "required_role": "ADMIN",
  "your_role": "OPERADOR"
}
```

### Unauthorized (401)

```json
{
  "error": "Authentication required",
  "detail": "You must be logged in to access this resource"
}
```

### Not Found vs Permission Denied

**Strategy**: Retornar 404 en lugar de 403 para recursos que el usuario no puede ver, para no revelar la existencia del recurso.

## Testing Strategy

### Unit Tests

1. **Permission Class Tests**
   - Test cada permission class con diferentes roles
   - Verificar que retornen True/False correctamente

2. **QuerySet Filter Tests**
   - Test filtrado para cada rol
   - Verificar que solo retornen datos autorizados

3. **ViewSet Tests**
   - Test cada endpoint con diferentes roles
   - Verificar responses 200, 403, 404

### Property-Based Tests

**Framework**: Hypothesis (Python)

1. **Property Test: Role Isolation**
   - Generar usuarios aleatorios con diferentes roles
   - Generar work orders aleatorias
   - Verificar que operadores solo vean sus OT

2. **Property Test: Supervisor Team Access**
   - Generar equipos aleatorios
   - Verificar que supervisores vean todo su equipo

3. **Property Test: Admin Global Access**
   - Generar recursos aleatorios
   - Verificar que admins vean todo

4. **Property Test: Asset-WorkOrder Consistency**
   - Generar pares asset-workorder
   - Verificar consistencia de acceso

5. **Property Test: Audit Log Completeness**
   - Generar accesos aleatorios
   - Verificar que todos se registren

### Integration Tests

1. **End-to-End Permission Flow**
   - Login como operador
   - Intentar acceder a OT de otro
   - Verificar 403

2. **Frontend Permission Tests**
   - Verificar que menús se adapten
   - Verificar que rutas estén protegidas

## Security Considerations

### 1. Defense in Depth

- **Frontend**: Ocultar UI elements
- **Backend**: Validar permisos en cada request
- **Database**: Usar RLS (Row Level Security) si es posible

### 2. Principle of Least Privilege

- Usuarios solo tienen acceso mínimo necesario
- Permisos explícitos, no implícitos

### 3. Audit Trail

- Registrar todos los accesos
- Detectar patrones sospechosos
- Alertas para múltiples intentos fallidos

### 4. Token Security

- JWT tokens con claims de rol
- Refresh tokens seguros
- Expiración apropiada

## Performance Considerations

### 1. Query Optimization

```python
# Malo: N+1 queries
for wo in WorkOrder.objects.all():
    if user.can_access(wo):
        # ...

# Bueno: Single query con filtro
WorkOrder.objects.filter(assigned_to=user)
```

### 2. Caching

- Cachear permisos de usuario
- Invalidar cache al cambiar rol
- TTL apropiado

### 3. Database Indexes

```python
class WorkOrder:
    class Meta:
        indexes = [
            models.Index(fields=['assigned_to']),
            models.Index(fields=['status', 'assigned_to']),
        ]
```

## Migration Strategy

### Phase 1: Backend Only (No Breaking Changes)

1. Implementar permisos en backend
2. Por defecto, permitir todo (backward compatible)
3. Agregar flag de feature: `ENABLE_RBAC = False`

### Phase 2: Gradual Rollout

1. Activar RBAC para usuarios de prueba
2. Monitorear logs y errores
3. Ajustar según feedback

### Phase 3: Full Deployment

1. Activar RBAC para todos
2. Actualizar frontend
3. Comunicar cambios a usuarios

## Monitoring and Alerts

### Metrics to Track

1. **Permission Denials**
   - Count de 403 responses
   - Por usuario y recurso

2. **Access Patterns**
   - Recursos más accedidos
   - Usuarios más activos

3. **Suspicious Activity**
   - Múltiples 403 del mismo usuario
   - Intentos de escalación de privilegios

### Alerts

1. **High 403 Rate**
   - Threshold: >10 en 5 minutos
   - Action: Notificar admin

2. **Privilege Escalation Attempt**
   - Threshold: Intento de acceso a admin endpoints
   - Action: Bloquear usuario temporalmente

## Documentation

### For Developers

- README con guía de permisos
- Ejemplos de uso de permission classes
- Guía de testing

### For Users

- Documento explicando roles
- Qué puede hacer cada rol
- Cómo solicitar cambio de rol

## Rollback Plan

### If Issues Arise

1. **Disable RBAC**
   ```python
   ENABLE_RBAC = False
   ```

2. **Revert Frontend Changes**
   - Deploy versión anterior
   - Restaurar menús completos

3. **Analyze Issues**
   - Revisar logs de errores
   - Identificar casos edge
   - Corregir y re-deploy

## Success Criteria

1. ✅ Operadores solo ven sus OT
2. ✅ Supervisores ven su equipo
3. ✅ Admins ven todo
4. ✅ 0 accesos no autorizados
5. ✅ Performance sin degradación
6. ✅ Audit logs completos
7. ✅ Frontend adaptado correctamente
8. ✅ Tests passing al 100%
