# Guía de Desarrollo - Sistema de Permisos por Roles (RBAC)

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Clases de Permisos](#clases-de-permisos)
4. [Mixins de QuerySet](#mixins-de-queryset)
5. [Aplicar Permisos a ViewSets](#aplicar-permisos-a-viewsets)
6. [Sistema de Auditoría](#sistema-de-auditoría)
7. [Testing](#testing)
8. [Ejemplos de Código](#ejemplos-de-código)

---

## Introducción

El sistema RBAC (Role-Based Access Control) implementado en este proyecto proporciona control de acceso granular basado en tres roles principales:

- **OPERADOR**: Acceso limitado a recursos asignados
- **SUPERVISOR**: Acceso a recursos de su equipo
- **ADMIN**: Acceso completo a todos los recursos

### Principios de Diseño

1. **Filtrado Automático**: Los datos se filtran automáticamente según el rol del usuario
2. **Seguridad por Defecto**: Acceso denegado por defecto, debe ser explícitamente permitido
3. **Consistencia**: Los permisos son consistentes a través de todos los endpoints
4. **Auditoría**: Todos los accesos son registrados para auditoría

---

## Arquitectura del Sistema

### Componentes Principales

```
backend/apps/core/
├── permissions.py      # Clases de permisos reutilizables
├── mixins.py          # Mixins para filtrado automático
└── middleware/
    └── audit.py       # Middleware de auditoría
```

### Flujo de Autorización

```
Request → Authentication → Permission Check → QuerySet Filtering → Response
                                    ↓
                            Audit Logging
```

---

## Clases de Permisos

### Ubicación
`backend/apps/core/permissions.py`

### Clases Disponibles

#### 1. IsAdminOnly
Permite acceso solo a usuarios con rol ADMIN.

```python
from apps.core.permissions import IsAdminOnly

class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOnly]
```

**Uso típico**: Endpoints de configuración, gestión de usuarios

#### 2. IsSupervisorOrAbove
Permite acceso a SUPERVISOR y ADMIN.

```python
from apps.core.permissions import IsSupervisorOrAbove

class ReportsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSupervisorOrAbove]
```

**Uso típico**: Reportes, estadísticas, gestión de equipo

#### 3. IsOperadorOrAbove
Permite acceso a todos los roles autenticados (OPERADOR, SUPERVISOR, ADMIN).

```python
from apps.core.permissions import IsOperadorOrAbove

class WorkOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOperadorOrAbove]
```

**Uso típico**: Recursos principales que todos pueden ver (con filtrado)

#### 4. IsOwnerOrSupervisor
Permite acceso al propietario del recurso o a supervisores/admins.

```python
from apps.core.permissions import IsOwnerOrSupervisor

class WorkOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrSupervisor]
    
    def get_queryset(self):
        # El filtrado se aplica automáticamente
        return WorkOrder.objects.all()
```

**Uso típico**: Recursos con ownership (work orders, tareas)

#### 5. ReadOnlyForOperador
Permite lectura a operadores, escritura solo a supervisores/admins.

```python
from apps.core.permissions import ReadOnlyForOperador

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ReadOnlyForOperador]
```

**Uso típico**: Recursos que operadores pueden ver pero no modificar

---

## Mixins de QuerySet

### Ubicación
`backend/apps/core/mixins.py`

### Mixins Disponibles

#### 1. RoleBasedQuerySetMixin
Filtra automáticamente el queryset según el rol del usuario.

```python
from apps.core.mixins import RoleBasedQuerySetMixin

class WorkOrderViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_by_role(queryset, assigned_to_field='assigned_to')
```

**Parámetros de filter_by_role**:
- `queryset`: QuerySet a filtrar
- `assigned_to_field`: Campo que indica el usuario asignado (default: 'assigned_to')
- `created_by_field`: Campo que indica el creador (default: 'created_by')

#### 2. OwnerFilterMixin
Filtra recursos por propietario.

```python
from apps.core.mixins import OwnerFilterMixin

class MyViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_by_owner(queryset, owner_field='user')
```

#### 3. AssetAccessMixin
Filtra activos basándose en work orders asignadas.

```python
from apps.core.mixins import AssetAccessMixin

class AssetViewSet(AssetAccessMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_assets_by_access(queryset)
```

---

## Aplicar Permisos a ViewSets

### Ejemplo Completo: Work Orders

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsOperadorOrAbove, IsOwnerOrSupervisor
from apps.core.mixins import RoleBasedQuerySetMixin
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
    """
    ViewSet para Work Orders con permisos por rol.
    
    - Operadores: Solo ven sus work orders asignadas
    - Supervisores: Ven todas las work orders
    - Admins: Ven todas las work orders
    """
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated, IsOperadorOrAbove]
    
    def get_queryset(self):
        """Filtra work orders según el rol del usuario."""
        queryset = super().get_queryset()
        return self.filter_by_role(
            queryset,
            assigned_to_field='assigned_to'
        )
    
    def get_permissions(self):
        """Permisos específicos por acción."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrSupervisor()]
        return super().get_permissions()
```

### Ejemplo: Assets con Acceso Basado en Work Orders

```python
from apps.core.mixins import AssetAccessMixin

class AssetViewSet(AssetAccessMixin, viewsets.ModelViewSet):
    """
    ViewSet para Assets.
    
    - Operadores: Solo ven assets de sus work orders
    - Supervisores/Admins: Ven todos los assets
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, IsOperadorOrAbove]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_assets_by_access(queryset)
```

---

## Sistema de Auditoría

### Modelo AccessLog

Ubicación: `backend/apps/configuration/models.py`

```python
class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
```

### Middleware de Auditoría

El middleware registra automáticamente todos los accesos a recursos.

Ubicación: `backend/apps/core/middleware/audit.py`

**Configuración en settings.py**:
```python
MIDDLEWARE = [
    # ... otros middlewares
    'apps.core.middleware.audit.AuditMiddleware',
]
```

### Consultar Logs de Auditoría

```python
from apps.configuration.models import AccessLog

# Logs de un usuario específico
user_logs = AccessLog.objects.filter(user=user)

# Intentos fallidos
failed_attempts = AccessLog.objects.filter(success=False)

# Accesos a un recurso específico
resource_logs = AccessLog.objects.filter(
    resource_type='work_order',
    resource_id='123'
)
```

---

## Testing

### Tests Unitarios de Permisos

```python
import pytest
from apps.core.permissions import IsAdminOnly

@pytest.mark.django_db
def test_admin_has_permission(api_factory, admin_user):
    request = api_factory.get('/')
    request.user = admin_user
    
    permission = IsAdminOnly()
    assert permission.has_permission(request, None) is True
```

### Property-Based Tests

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_operator_isolation(api_client, operator1, operator2, work_order):
    """Verifica que operadores solo vean sus recursos."""
    token = get_token(operator1)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    response = api_client.get('/api/v1/work-orders/')
    assert response.status_code == 200
    
    # Verificar que solo ve sus work orders
    ids = [wo['id'] for wo in response.data['results']]
    assert work_order.id in ids  # Su work order
```

### Tests de Integración E2E

```python
@pytest.mark.django_db
def test_complete_operator_flow(api_client, setup_data):
    """Test flujo completo: login → acceso → denegación."""
    # 1. Login
    token = get_token(operator)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    # 2. Acceso a recurso propio
    response = api_client.get(f'/api/v1/work-orders/{own_wo.id}/')
    assert response.status_code == 200
    
    # 3. Denegación a recurso ajeno
    response = api_client.get(f'/api/v1/work-orders/{other_wo.id}/')
    assert response.status_code == 404
```

---

## Ejemplos de Código

### Ejemplo 1: Nuevo ViewSet con Permisos

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsSupervisorOrAbove
from apps.core.mixins import RoleBasedQuerySetMixin

class MyResourceViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
    queryset = MyResource.objects.all()
    serializer_class = MyResourceSerializer
    permission_classes = [IsAuthenticated, IsSupervisorOrAbove]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_by_role(queryset)
```

### Ejemplo 2: Permisos Personalizados por Acción

```python
class WorkOrderViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsSupervisorOrAbove()]
        elif self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrSupervisor()]
        return [IsAuthenticated(), IsOperadorOrAbove()]
```

### Ejemplo 3: Filtrado Complejo

```python
def get_queryset(self):
    queryset = super().get_queryset()
    user = self.request.user
    
    if user.role.name == 'OPERADOR':
        # Operadores: solo sus recursos
        return queryset.filter(assigned_to=user)
    elif user.role.name == 'SUPERVISOR':
        # Supervisores: recursos de su equipo
        team_users = User.objects.filter(team=user.team)
        return queryset.filter(assigned_to__in=team_users)
    else:
        # Admins: todos los recursos
        return queryset
```

### Ejemplo 4: Validación en Serializer

```python
class WorkOrderSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = self.context['request'].user
        
        # Solo supervisores pueden asignar a otros usuarios
        if 'assigned_to' in data:
            if user.role.name == 'OPERADOR':
                if data['assigned_to'] != user:
                    raise ValidationError(
                        "Operadores solo pueden asignarse a sí mismos"
                    )
        
        return data
```

---

## Mejores Prácticas

### 1. Siempre Usar Filtrado Automático
```python
# ✅ CORRECTO
def get_queryset(self):
    queryset = super().get_queryset()
    return self.filter_by_role(queryset)

# ❌ INCORRECTO - No filtrar deja datos expuestos
def get_queryset(self):
    return MyModel.objects.all()
```

### 2. Combinar Permisos Apropiadamente
```python
# ✅ CORRECTO - Múltiples capas de seguridad
permission_classes = [IsAuthenticated, IsOperadorOrAbove]

def get_queryset(self):
    return self.filter_by_role(queryset)
```

### 3. Retornar 404 en Lugar de 403
```python
# ✅ CORRECTO - No revela existencia del recurso
def retrieve(self, request, pk=None):
    queryset = self.filter_queryset(self.get_queryset())
    obj = get_object_or_404(queryset, pk=pk)
    # ...
```

### 4. Testear Todos los Roles
```python
@pytest.mark.parametrize('role,expected_count', [
    ('OPERADOR', 1),
    ('SUPERVISOR', 5),
    ('ADMIN', 10),
])
def test_access_by_role(role, expected_count):
    # Test para cada rol
    pass
```

---

## Troubleshooting

### Problema: Usuario ve recursos que no debería

**Solución**: Verificar que `get_queryset()` aplica filtrado:
```python
def get_queryset(self):
    queryset = super().get_queryset()
    return self.filter_by_role(queryset)  # ← Asegurar esto
```

### Problema: Tests fallan con 403

**Solución**: Verificar que el usuario de test tiene el rol correcto:
```python
user = User.objects.create_user(
    username='test',
    role=Role.objects.get(name='OPERADOR')  # ← Asignar rol
)
```

### Problema: Audit logs no se crean

**Solución**: Verificar que el middleware está configurado:
```python
# settings.py
MIDDLEWARE = [
    # ...
    'apps.core.middleware.audit.AuditMiddleware',  # ← Debe estar presente
]
```

---

## Referencias

- **Clases de Permisos**: `backend/apps/core/permissions.py`
- **Mixins**: `backend/apps/core/mixins.py`
- **Tests**: `backend/apps/core/tests/`
- **Documentación de Usuario**: `docs/RBAC_USER_GUIDE.md`
