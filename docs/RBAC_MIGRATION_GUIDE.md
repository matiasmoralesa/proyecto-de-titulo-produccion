# Guía de Migración - Sistema de Permisos por Roles (RBAC)

## Introducción

Este documento describe cómo activar y migrar gradualmente al nuevo sistema de permisos por roles (RBAC) en el sistema CMMS.

---

## Feature Flag: ENABLE_RBAC

El sistema incluye un feature flag que permite activar/desactivar el sistema RBAC sin necesidad de modificar código.

### Configuración

**Ubicación**: `backend/config/settings/base.py` o variables de entorno

```python
# Feature Flags
ENABLE_RBAC = os.getenv('ENABLE_RBAC', 'False').lower() == 'true'
```

### Estados del Feature Flag

#### ENABLE_RBAC = False (Por defecto)
- Sistema funciona en modo legacy (sin restricciones de roles)
- Todos los usuarios autenticados tienen acceso completo
- Backward compatible con versiones anteriores
- **Recomendado para**: Desarrollo, testing inicial

#### ENABLE_RBAC = True
- Sistema RBAC completamente activo
- Permisos aplicados según roles
- Filtrado automático de datos
- Auditoría completa activada
- **Recomendado para**: Producción

---

## Plan de Migración

### Fase 1: Preparación (1-2 días)

#### 1.1 Backup de Base de Datos
```bash
# PostgreSQL
pg_dump -U usuario -d nombre_db > backup_pre_rbac.sql

# MySQL
mysqldump -u usuario -p nombre_db > backup_pre_rbac.sql
```

#### 1.2 Verificar Roles Existentes
```python
python manage.py shell

from apps.authentication.models import Role
print(Role.objects.all())
# Debe mostrar: ADMIN, SUPERVISOR, OPERADOR
```

#### 1.3 Asignar Roles a Usuarios Existentes
```python
from apps.authentication.models import User, Role

# Obtener roles
admin_role = Role.objects.get(name='ADMIN')
supervisor_role = Role.objects.get(name='SUPERVISOR')
operator_role = Role.objects.get(name='OPERADOR')

# Asignar roles a usuarios existentes
# Ejemplo: Asignar admin a superusers
for user in User.objects.filter(is_superuser=True):
    user.role = admin_role
    user.save()

# Asignar roles según criterio de negocio
# (personalizar según necesidades)
```

### Fase 2: Testing en Desarrollo (3-5 días)

#### 2.1 Activar RBAC en Desarrollo
```bash
# .env.development
ENABLE_RBAC=true
```

#### 2.2 Ejecutar Suite de Tests
```bash
# Tests unitarios
python -m pytest backend/apps/core/tests/test_permissions.py -v

# Tests de integración
python -m pytest backend/apps/core/tests/test_integration_e2e.py -v

# Tests de property-based
python -m pytest backend/apps/work_orders/tests_permissions.py -v
python -m pytest backend/apps/assets/tests_permissions.py -v
python -m pytest backend/apps/core/tests/test_notification_filtering.py -v
```

#### 2.3 Testing Manual por Rol

**Como Operador:**
1. Login con usuario operador
2. Verificar que solo ve sus work orders
3. Intentar acceder a work order de otro operador (debe fallar)
4. Verificar que solo ve activos de sus work orders
5. Intentar crear work order (debe fallar)

**Como Supervisor:**
1. Login con usuario supervisor
2. Verificar que ve todas las work orders
3. Crear nueva work order
4. Asignar work order a operador
5. Ver reportes de equipo

**Como Admin:**
1. Login con usuario admin
2. Verificar acceso completo
3. Gestionar usuarios
4. Ver logs de auditoría
5. Modificar configuración

### Fase 3: Staging (1 semana)

#### 3.1 Desplegar a Staging
```bash
# Activar RBAC en staging
export ENABLE_RBAC=true

# Aplicar migraciones
python manage.py migrate

# Reiniciar servicios
systemctl restart gunicorn
systemctl restart nginx
```

#### 3.2 Testing con Usuarios Reales
- Invitar a usuarios clave de cada rol
- Recopilar feedback
- Documentar issues encontrados
- Ajustar según necesidad

#### 3.3 Monitoreo
```bash
# Ver logs de auditoría
python manage.py shell

from apps.configuration.models import AccessLog
print(AccessLog.objects.filter(success=False).count())
# Verificar intentos fallidos
```

### Fase 4: Producción (Rollout Gradual)

#### 4.1 Preparación Pre-Producción

**Checklist:**
- [ ] Backup de base de datos completado
- [ ] Todos los usuarios tienen roles asignados
- [ ] Tests pasando en staging
- [ ] Documentación actualizada
- [ ] Equipo de soporte notificado
- [ ] Plan de rollback preparado

#### 4.2 Activación en Producción

**Opción A: Activación Completa**
```bash
# Activar RBAC para todos
export ENABLE_RBAC=true
python manage.py migrate
systemctl restart gunicorn
```

**Opción B: Activación Gradual por Grupo**
```python
# Implementar lógica de activación gradual
# backend/apps/core/middleware/rbac_toggle.py

class RBACToggleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Activar RBAC solo para usuarios en lista piloto
        if hasattr(request, 'user') and request.user.is_authenticated:
            pilot_users = ['user1', 'user2', 'user3']
            request.rbac_enabled = request.user.username in pilot_users
        
        response = self.get_response(request)
        return response
```

#### 4.3 Monitoreo Post-Activación

**Primeras 24 horas:**
- Monitorear logs de error
- Revisar intentos de acceso fallidos
- Responder a tickets de soporte
- Verificar métricas de rendimiento

**Primera semana:**
- Análisis de logs de auditoría
- Recopilar feedback de usuarios
- Ajustar permisos si es necesario
- Documentar lecciones aprendidas

---

## Rollback Plan

### Si necesitas desactivar RBAC:

#### Paso 1: Desactivar Feature Flag
```bash
export ENABLE_RBAC=false
systemctl restart gunicorn
```

#### Paso 2: Verificar Funcionamiento
```bash
# Verificar que el sistema funciona sin RBAC
curl -H "Authorization: Bearer $TOKEN" http://localhost/api/v1/work-orders/
```

#### Paso 3: Restaurar Backup (si es necesario)
```bash
# PostgreSQL
psql -U usuario -d nombre_db < backup_pre_rbac.sql

# MySQL
mysql -u usuario -p nombre_db < backup_pre_rbac.sql
```

---

## Configuración Avanzada

### Variables de Entorno

```bash
# .env
ENABLE_RBAC=true                    # Activar/desactivar RBAC
RBAC_AUDIT_ENABLED=true             # Activar auditoría
RBAC_STRICT_MODE=false              # Modo estricto (denegar por defecto)
RBAC_CACHE_TIMEOUT=300              # Cache de permisos (segundos)
```

### Configuración en settings.py

```python
# backend/config/settings/production.py

# RBAC Configuration
ENABLE_RBAC = os.getenv('ENABLE_RBAC', 'True').lower() == 'true'

# Audit Configuration
RBAC_AUDIT_ENABLED = os.getenv('RBAC_AUDIT_ENABLED', 'True').lower() == 'true'

# Strict Mode (deny by default)
RBAC_STRICT_MODE = os.getenv('RBAC_STRICT_MODE', 'False').lower() == 'true'

# Permission Cache
RBAC_CACHE_TIMEOUT = int(os.getenv('RBAC_CACHE_TIMEOUT', '300'))

# Middleware Configuration
if ENABLE_RBAC:
    MIDDLEWARE += [
        'apps.core.middleware.audit.AuditMiddleware',
    ]
```

---

## Troubleshooting

### Problema: Usuarios no pueden acceder después de activar RBAC

**Causa**: Usuarios sin rol asignado

**Solución**:
```python
from apps.authentication.models import User, Role

# Asignar rol por defecto a usuarios sin rol
default_role = Role.objects.get(name='OPERADOR')
users_without_role = User.objects.filter(role__isnull=True)

for user in users_without_role:
    user.role = default_role
    user.save()
```

### Problema: Tests fallan después de activar RBAC

**Causa**: Tests no configuran roles para usuarios de prueba

**Solución**:
```python
@pytest.fixture
def setup_roles():
    admin_role, _ = Role.objects.get_or_create(
        name='ADMIN',
        defaults={'description': 'Administrator'}
    )
    # ... crear otros roles
    return {'admin': admin_role, ...}

@pytest.fixture
def test_user(setup_roles):
    return User.objects.create_user(
        username='test',
        role=setup_roles['operator']  # ← Asignar rol
    )
```

### Problema: Rendimiento degradado

**Causa**: Queries adicionales para verificar permisos

**Solución**:
```python
# Usar select_related para optimizar queries
def get_queryset(self):
    return WorkOrder.objects.select_related(
        'assigned_to',
        'assigned_to__role',
        'created_by'
    )
```

---

## Métricas de Éxito

### KPIs a Monitorear

1. **Seguridad**
   - Intentos de acceso no autorizado
   - Violaciones de permisos detectadas
   - Tiempo de respuesta a incidentes

2. **Rendimiento**
   - Tiempo de respuesta de API
   - Queries por request
   - Uso de memoria

3. **Usabilidad**
   - Tickets de soporte relacionados con permisos
   - Tiempo promedio para completar tareas
   - Satisfacción de usuarios

4. **Adopción**
   - % de usuarios con roles asignados
   - % de endpoints con RBAC aplicado
   - Cobertura de tests

---

## Checklist de Migración Completa

### Pre-Migración
- [ ] Backup de base de datos
- [ ] Todos los usuarios tienen roles
- [ ] Tests pasando
- [ ] Documentación actualizada
- [ ] Equipo capacitado

### Durante Migración
- [ ] Feature flag activado
- [ ] Servicios reiniciados
- [ ] Monitoreo activo
- [ ] Equipo de soporte disponible

### Post-Migración
- [ ] Verificación de funcionalidad
- [ ] Análisis de logs
- [ ] Feedback de usuarios recopilado
- [ ] Métricas revisadas
- [ ] Documentación de lecciones aprendidas

---

## Soporte

### Contactos de Emergencia

**Durante Migración:**
- Líder Técnico: [contacto]
- DevOps: [contacto]
- Soporte: [contacto]

### Recursos

- Documentación Técnica: `docs/RBAC_DEVELOPER_GUIDE.md`
- Documentación de Usuario: `docs/RBAC_USER_GUIDE.md`
- Tests: `backend/apps/core/tests/`
- Issues: [URL del sistema de tickets]

---

## Conclusión

La migración al sistema RBAC es un proceso gradual que requiere planificación y testing cuidadoso. Siguiendo esta guía, puedes activar el sistema de manera segura y controlada, con la capacidad de hacer rollback si es necesario.

**Recuerda**: El feature flag `ENABLE_RBAC` te da control total sobre cuándo activar el sistema. No hay prisa - toma el tiempo necesario para testing y validación.
