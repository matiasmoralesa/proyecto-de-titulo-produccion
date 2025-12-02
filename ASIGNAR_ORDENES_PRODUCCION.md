# Asignar Órdenes de Trabajo a Operadores en Producción

## 🎯 Problema

El operador ve **0 en todo** en el dashboard porque no tiene órdenes de trabajo asignadas en producción.

## ✅ Solución

Necesitas asignar órdenes de trabajo a los operadores en Railway.

## 📋 Opción 1: Desde el Admin de Django (Recomendado)

### Paso 1: Accede al Admin
1. Ve a: `https://tu-app.up.railway.app/admin/`
2. Inicia sesión como admin

### Paso 2: Asigna Órdenes
1. Ve a **Work Orders** → **Work orders**
2. Selecciona algunas órdenes de trabajo
3. Haz clic en el botón de edición
4. En el campo **"Assigned to"**, selecciona un operador (ej: operador2)
5. Guarda los cambios
6. Repite para 3-5 órdenes

### Paso 3: Verifica
1. Cierra sesión del admin
2. Inicia sesión como operador
3. Ve al Dashboard
4. Deberías ver las órdenes asignadas

## 📋 Opción 2: Desde Railway Shell

### Paso 1: Abre Railway Shell
1. Ve a https://railway.app
2. Abre tu proyecto
3. Selecciona el servicio de Django
4. Haz clic en la pestaña **"Shell"**

### Paso 2: Ejecuta el Script
```python
# Importar modelos
from apps.authentication.models import User, Role
from apps.work_orders.models import WorkOrder

# Obtener operador
operador = User.objects.filter(role__name='OPERADOR').first()
print(f"Operador: {operador.username}")

# Obtener órdenes sin asignar
ordenes = WorkOrder.objects.filter(assigned_to__isnull=True)[:3]
print(f"Órdenes disponibles: {ordenes.count()}")

# Asignar órdenes
for orden in ordenes:
    orden.assigned_to = operador
    orden.save()
    print(f"✅ Asignada: {orden.work_order_number}")

# Verificar
total = WorkOrder.objects.filter(assigned_to=operador).count()
print(f"\n✅ Total asignadas a {operador.username}: {total}")
```

### Paso 3: Verifica
1. Inicia sesión como operador en la app
2. Ve al Dashboard
3. Deberías ver las órdenes asignadas

## 📋 Opción 3: Crear Datos de Prueba

Si no hay órdenes de trabajo en producción, necesitas crearlas primero:

### Desde Railway Shell:
```python
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.authentication.models import User, Role

# Obtener un activo
asset = Asset.objects.first()
print(f"Activo: {asset.name}")

# Obtener operador
operador = User.objects.filter(role__name='OPERADOR').first()
print(f"Operador: {operador.username}")

# Crear órdenes de trabajo
for i in range(3):
    wo = WorkOrder.objects.create(
        title=f"Mantenimiento preventivo {i+1}",
        description=f"Revisión y mantenimiento del activo {asset.name}",
        asset=asset,
        assigned_to=operador,
        priority="Media",
        status="Pendiente"
    )
    print(f"✅ Creada: {wo.work_order_number}")

print(f"\n✅ Total creadas: 3")
```

## 🔍 Verificar que Funciona

### Paso 1: Login como Operador
1. Ve a tu app en producción
2. Inicia sesión como operador

### Paso 2: Verifica el Dashboard
Deberías ver:
- **Activos**: Número > 0 (los activos de tus órdenes)
- **Órdenes de Trabajo**: Número > 0 (tus órdenes asignadas)
- **Total**: Número > 0

### Paso 3: Verifica las Listas
1. Ve a **Órdenes de Trabajo**
2. Deberías ver solo tus órdenes asignadas
3. Ve a **Activos**
4. Deberías ver solo los activos de tus órdenes

## ⚠️ Nota Importante

El caché del dashboard dura **5 minutos**. Si acabas de asignar órdenes:

1. **Opción A**: Espera 5 minutos
2. **Opción B**: Limpia el caché del navegador (Ctrl+Shift+R)
3. **Opción C**: Abre en modo incógnito

## 🐛 Si Sigue Mostrando 0

### Verifica en Railway Shell:
```python
from apps.authentication.models import User
from apps.work_orders.models import WorkOrder

# Verificar operador
operador = User.objects.get(username='operador2')
print(f"Operador: {operador.username}")
print(f"Rol: {operador.role.name}")

# Verificar órdenes asignadas
ordenes = WorkOrder.objects.filter(assigned_to=operador)
print(f"Órdenes asignadas: {ordenes.count()}")

for orden in ordenes:
    print(f"  - {orden.work_order_number}: {orden.title}")
```

Si muestra 0, entonces el operador no tiene órdenes asignadas y necesitas asignarlas.

## 📝 Resumen

1. ✅ El código de filtrado está correcto
2. ✅ Funciona localmente
3. ⚠️  En producción el operador no tiene órdenes asignadas
4. 🔧 Necesitas asignar órdenes usando una de las 3 opciones

---

**Recomendación**: Usa la **Opción 1 (Admin de Django)** porque es la más visual y fácil.
