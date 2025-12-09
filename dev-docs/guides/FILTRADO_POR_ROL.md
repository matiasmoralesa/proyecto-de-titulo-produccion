# Filtrado por Rol - Sistema de Asignación y Dashboards

## Resumen de Cambios

Se implementó un sistema de filtrado por rol que afecta dos áreas principales:
1. **Asignación automática de OT**: Solo usuarios con rol OPERADOR pueden ser asignados
2. **Dashboards y reportes**: Filtrados según el rol del usuario

---

## 1. Asignación Automática de OT

### Cambio Implementado

**Archivo**: `backend/apps/ml_predictions/operator_assignment_service.py`

**Antes**:
```python
# Buscaba operadores con roles 'operator' o 'technician' (strings)
operators = User.objects.filter(
    Q(role='operator') | Q(role='technician'),
    is_active=True
)
```

**Después**:
```python
from apps.authentication.models import Role

# Solo busca usuarios con rol OPERADOR
operators = User.objects.filter(
    role__name=Role.OPERADOR,
    is_active=True
)
```

### Impacto

- ✅ Las predicciones ML solo crean OT asignadas a usuarios con rol `OPERADOR`
- ✅ Los usuarios `ADMIN` y `SUPERVISOR` no pueden ser asignados automáticamente
- ✅ Mantiene la lógica de scoring (skills, availability, performance, location)

### Flujo Completo

1. **Predicción ML detecta riesgo alto** → `PredictionService.create_preventive_work_order()`
2. **Sistema crea OT preventiva** → `WorkOrder.objects.create(...)`
3. **Sistema busca mejor operador** → `OperatorAssignmentService.find_best_operator()`
   - Filtra solo usuarios con `role__name=Role.OPERADOR`
   - Calcula score basado en 4 factores
4. **Sistema asigna operador** → `work_order.assigned_to = best_operator`

---

## 2. Dashboards y Reportes Filtrados

### Cambios Implementados

#### A. ReportService (`backend/apps/reports/services.py`)

**Método actualizado**: `get_dashboard_kpis()`

```python
@staticmethod
def get_dashboard_kpis(start_date=None, end_date=None, user_id=None):
    """
    Get all KPIs for dashboard filtered by user role.
    
    Args:
        user_id: None para ADMIN/SUPERVISOR, user_id para OPERADOR
    """
    return {
        'mtbf': ReportService.calculate_mtbf(..., user_id=user_id),
        'mttr': ReportService.calculate_mttr(..., user_id=user_id),
        'oee': ReportService.calculate_oee(..., user_id=user_id),
        'work_order_summary': ReportService.get_work_order_summary(..., user_id=user_id),
        ...
    }
```

**Métodos que ya soportaban `user_id`**:
- `calculate_mtbf()` - Filtra por `assigned_to_id=user_id`
- `calculate_mttr()` - Filtra por `assigned_to_id=user_id`
- `calculate_oee()` - Filtra por `assigned_to_id=user_id`
- `get_work_order_summary()` - Filtra por `assigned_to_id=user_id`

#### B. ReportViewSet (`backend/apps/reports/views.py`)

**Método helper**: `_get_user_filter()`

```python
def _get_user_filter(self):
    """
    Determina el filtro según el rol del usuario.
    
    Returns:
        - None: Para ADMIN y SUPERVISOR (ven todo)
        - user.id: Para OPERADOR (solo sus OT)
    """
    user = self.request.user
    
    if user.role.name == Role.OPERADOR:
        return user.id  # Solo sus OT
    elif user.role.name in [Role.SUPERVISOR, Role.ADMIN]:
        return None  # Todas las OT
```

**Endpoints actualizados**:
- `/api/v1/reports/kpis/` - Usa `user_filter`
- `/api/v1/reports/work_order_summary/` - Usa `user_filter`
- `/api/v1/reports/dashboard/` - Usa `user_filter`

#### C. Dashboard Stats (`backend/apps/core/dashboard_views.py`)

**Ya implementado correctamente**:

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    role_name = user.role.name
    
    if role_name == Role.ADMIN:
        # Ve todo el sistema
        assets_qs = Asset.objects.all()
        work_orders_qs = WorkOrder.objects.all()
        predictions_qs = FailurePrediction.objects.all()
    
    elif role_name == Role.SUPERVISOR:
        # Ve todo (puede filtrarse por departamento en el futuro)
        assets_qs = Asset.objects.all()
        work_orders_qs = WorkOrder.objects.all()
        predictions_qs = FailurePrediction.objects.all()
    
    elif role_name == Role.OPERADOR:
        # Solo ve sus OT asignadas y activos relacionados
        work_orders_qs = WorkOrder.objects.filter(assigned_to=user)
        assigned_asset_ids = work_orders_qs.values_list('asset_id', flat=True).distinct()
        assets_qs = Asset.objects.filter(id__in=assigned_asset_ids)
        predictions_qs = FailurePrediction.objects.filter(asset_id__in=assigned_asset_ids)
```

---

## 3. Matriz de Permisos

### Asignación de OT

| Rol | Puede ser asignado automáticamente | Puede asignar manualmente |
|-----|-----------------------------------|---------------------------|
| ADMIN | ❌ No | ✅ Sí |
| SUPERVISOR | ❌ No | ✅ Sí |
| OPERADOR | ✅ Sí | ❌ No |

### Visualización de Dashboards

| Métrica | ADMIN | SUPERVISOR | OPERADOR |
|---------|-------|------------|----------|
| Total OT | Todas | Todas | Solo asignadas |
| Total Activos | Todos | Todos | Solo de sus OT |
| Predicciones ML | Todas | Todas | Solo de sus activos |
| KPIs (MTBF, MTTR, OEE) | Globales | Globales | Personales |
| Gráficos | ✅ Sí | ✅ Sí | ❌ No |

### Endpoints de Reportes

| Endpoint | ADMIN | SUPERVISOR | OPERADOR |
|----------|-------|------------|----------|
| `/api/v1/reports/kpis/` | Todos | Todos | Solo suyos |
| `/api/v1/reports/work_order_summary/` | Todos | Todos | Solo suyos |
| `/api/v1/reports/dashboard/` | Todos | Todos | Solo suyos |
| `/api/v1/dashboard/stats/` | Todos | Todos | Solo suyos |
| `/api/v1/reports/asset_downtime/` | Todos | Todos | Todos |
| `/api/v1/reports/spare_part_consumption/` | Todos | Todos | Todos |

---

## 4. Ejemplos de Uso

### Ejemplo 1: Predicción ML crea OT

```python
# 1. Sistema detecta predicción de alto riesgo
prediction = FailurePrediction.objects.create(
    asset=camion_volvo,
    failure_probability=0.85,
    risk_level='HIGH'
)

# 2. Sistema crea OT preventiva
work_order = prediction_service.create_preventive_work_order(prediction)

# 3. Sistema busca mejor operador (solo OPERADORES)
operators = User.objects.filter(
    role__name=Role.OPERADOR,  # ✅ Solo operadores
    is_active=True
)

# 4. Sistema calcula scores y asigna
best_operator = assignment_service.find_best_operator(work_order)
work_order.assigned_to = best_operator  # Juan (OPERADOR)
```

### Ejemplo 2: Dashboard de OPERADOR

```python
# Usuario: Juan (OPERADOR)
GET /api/v1/dashboard/stats/

# Response:
{
    "total_work_orders": 5,        # Solo las 5 OT asignadas a Juan
    "total_assets": 3,              # Solo los 3 activos de sus OT
    "total_predictions": 2,         # Solo predicciones de sus activos
    "kpis": {
        "mtbf": 120.5,              # Calculado solo con sus OT
        "mttr": 4.2,                # Calculado solo con sus OT
        "oee": 87.3                 # Calculado solo con sus OT
    },
    "charts": null                  # Operadores no ven gráficos
}
```

### Ejemplo 3: Dashboard de ADMIN

```python
# Usuario: Admin (ADMIN)
GET /api/v1/dashboard/stats/

# Response:
{
    "total_work_orders": 150,       # Todas las OT del sistema
    "total_assets": 45,             # Todos los activos
    "total_predictions": 23,        # Todas las predicciones
    "kpis": {
        "mtbf": 145.8,              # Calculado con todas las OT
        "mttr": 3.8,                # Calculado con todas las OT
        "oee": 92.1                 # Calculado con todas las OT
    },
    "charts": {                     # Admin ve todos los gráficos
        "work_orders_trend": [...],
        "asset_status_distribution": [...],
        "maintenance_types": [...],
        ...
    }
}
```

---

## 5. Testing

### Pruebas Recomendadas

1. **Asignación automática**:
   ```bash
   python manage.py test backend.apps.ml_predictions.tests.test_operator_assignment
   ```

2. **Dashboard por rol**:
   ```bash
   python manage.py test backend.test_dashboard_roles
   ```

3. **Reportes filtrados**:
   ```bash
   python manage.py test backend.apps.reports.tests
   ```

### Verificación Manual

```python
# 1. Crear usuarios de prueba
admin = User.objects.create(username='admin', role=admin_role)
supervisor = User.objects.create(username='supervisor', role=supervisor_role)
operador = User.objects.create(username='operador', role=operador_role)

# 2. Crear OT asignada al operador
wo = WorkOrder.objects.create(
    asset=asset,
    assigned_to=operador,
    ...
)

# 3. Verificar dashboard del operador
# GET /api/v1/dashboard/stats/ (como operador)
# Debe mostrar solo 1 OT

# 4. Verificar dashboard del admin
# GET /api/v1/dashboard/stats/ (como admin)
# Debe mostrar todas las OT
```

---

## 6. Caché

El dashboard usa caché con claves específicas por rol y usuario:

```python
cache_key = f'dashboard_stats_{user.role.name}_{user.id}'
cache.set(cache_key, data, 300)  # 5 minutos
```

**Importante**: 
- Cada usuario tiene su propia caché
- La caché se invalida automáticamente después de 5 minutos
- Para limpiar manualmente: `python manage.py clear_dashboard_cache`

---

## 7. Consideraciones Futuras

### Filtrado por Departamento/Área

Para SUPERVISOR, se puede agregar filtrado por departamento:

```python
elif role_name == Role.SUPERVISOR:
    # Filtrar por departamento del supervisor
    department = user.department
    work_orders_qs = WorkOrder.objects.filter(
        asset__location__department=department
    )
```

### Permisos Granulares

Se puede implementar permisos más específicos:

```python
# Ejemplo: Supervisor puede ver solo su equipo
if role_name == Role.SUPERVISOR:
    team_members = User.objects.filter(supervisor=user)
    work_orders_qs = WorkOrder.objects.filter(
        assigned_to__in=team_members
    )
```

---

## 8. Commit

```bash
git commit -m "feat: Filtrado por rol en asignación y dashboards

- Asignación de OT solo a usuarios con rol OPERADOR
- Dashboards filtrados por rol:
  * ADMIN/SUPERVISOR: ven todas las OT del sistema
  * OPERADOR: solo ven sus OT asignadas
- Actualizado OperatorAssignmentService para filtrar por Role.OPERADOR
- Actualizado ReportService.get_dashboard_kpis con parámetro user_id
- Dashboard stats ya tenía filtrado por rol implementado"
```

**Commit hash**: `1843c74`
