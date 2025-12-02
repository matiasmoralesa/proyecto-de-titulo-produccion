# ✅ Checklist de Pruebas Manuales

## Estado: En Progreso
**Fecha**: 2 de Diciembre de 2025
**Tester**: [Tu nombre]

---

## 🎯 Objetivo
Verificar que las 3 correcciones principales funcionen correctamente en el sistema.

---

## 📋 Instrucciones Generales

1. **Accede al sistema**:
   - Local: http://localhost:5173
   - Producción: [Tu URL de Railway]

2. **Inicia sesión** con credenciales de administrador

3. **Marca cada item** cuando lo hayas verificado

---

## 1. ✅ Dashboard - KPIs Sin Valores Negativos

### Preparación
- [ ] Acceder al dashboard principal
- [ ] Esperar a que carguen todos los KPIs

### Verificaciones
- [ ] **"Disponibilidad"**: Muestra un porcentaje (0-100%)
- [ ] **"Tasa de Completitud"**: Muestra un porcentaje (0-100%)
- [ ] **"Tiempo Promedio"**: Muestra un número >= 0 (NO negativo)
- [ ] **"Mantenimiento Preventivo"**: Muestra un porcentaje (0-100%)
- [ ] **"Backlog"**: Muestra un número >= 0
- [ ] **"Activos Críticos"**: Muestra un número >= 0
- [ ] **"OT Este Mes"**: Muestra un número >= 0
- [ ] **"Precisión ML"**: Muestra un porcentaje (0-100%)

### Resultado Esperado
✅ **NINGÚN KPI debe mostrar valores negativos**

### Notas
```
Valor de "Tiempo Promedio": _____ días
¿Hay valores negativos?: [ ] Sí  [ ] No
```

---

## 2. ✅ Notificaciones - Sin Error 404

### Preparación
- [ ] Hacer clic en el ícono de campana (arriba derecha)
- [ ] Verificar que haya notificaciones

### Prueba 1: Notificación de Orden de Trabajo Existente
- [ ] Hacer clic en una notificación de orden de trabajo
- [ ] **Resultado**: Debe navegar a la página de detalle de la orden
- [ ] **NO debe aparecer**: Página 404

### Prueba 2: Notificación de Activo Existente
- [ ] Hacer clic en una notificación de activo
- [ ] **Resultado**: Debe navegar a la página de detalle del activo
- [ ] **NO debe aparecer**: Página 404

### Prueba 3: Notificación de Objeto Eliminado (Si aplica)
- [ ] Si hay notificaciones de objetos eliminados, hacer clic
- [ ] **Resultado**: Debe mostrar mensaje "El objeto relacionado ya no existe"
- [ ] **Verificar**: La notificación se marca como leída
- [ ] **NO debe aparecer**: Página 404

### Prueba 4: Verificar Marcado como Leída
- [ ] Hacer clic en cualquier notificación
- [ ] **Resultado**: La notificación debe marcarse como leída (sin punto azul)

### Resultado Esperado
✅ **NO debe aparecer página 404 en ningún caso**
✅ **Mensajes de error claros cuando el objeto no existe**

### Notas
```
¿Apareció error 404?: [ ] Sí  [ ] No
¿Mensajes de error claros?: [ ] Sí  [ ] No
```

---

## 3. ✅ Configuración - CRUD Completo

### Preparación
- [ ] Ir a "Configuración" en el menú lateral
- [ ] Verificar que solo sea accesible como administrador

---

### 3.1 Categorías de Activos

#### Crear Nueva Categoría
- [ ] Hacer clic en pestaña "📁 Categorías"
- [ ] Hacer clic en "Nueva Categoría"
- [ ] Completar formulario:
  - Código: `TEST001`
  - Nombre: `Categoría de Prueba`
  - Descripción: `Esta es una prueba`
  - ✓ Activo
- [ ] Hacer clic en "Crear"
- [ ] **Resultado**: Debe mostrar toast verde "Categoría creada exitosamente"
- [ ] **Verificar**: La categoría aparece en la tabla

#### Validación de Código Duplicado
- [ ] Intentar crear otra categoría con código `TEST001`
- [ ] **Resultado**: Debe mostrar error "Ya existe una categoría con este código"
- [ ] **Verificar**: El modal permanece abierto para corregir

#### Editar Categoría
- [ ] Hacer clic en ícono de lápiz de la categoría de prueba
- [ ] Cambiar nombre a `Categoría Editada`
- [ ] Hacer clic en "Actualizar"
- [ ] **Resultado**: Toast verde "Categoría actualizada exitosamente"
- [ ] **Verificar**: El nombre cambió en la tabla

#### Eliminar Categoría
- [ ] Hacer clic en ícono de papelera de la categoría de prueba
- [ ] Confirmar eliminación
- [ ] **Resultado**: Toast verde "Categoría eliminada exitosamente"
- [ ] **Verificar**: La categoría desapareció de la tabla

---

### 3.2 Prioridades

#### Crear Nueva Prioridad
- [ ] Hacer clic en pestaña "⚡ Prioridades"
- [ ] Hacer clic en "Nueva Prioridad"
- [ ] Completar formulario:
  - Nivel: `99`
  - Nombre: `Prioridad de Prueba`
  - Color: Seleccionar rojo (#EF4444) de los predefinidos
  - ✓ Activo
- [ ] **Verificar**: El preview del color se muestra correctamente
- [ ] Hacer clic en "Crear"
- [ ] **Resultado**: Toast verde "Prioridad creada exitosamente"

#### Validación de Color Hexadecimal
- [ ] Crear nueva prioridad con nivel `98`
- [ ] En color escribir: `rojo` (inválido)
- [ ] Intentar guardar
- [ ] **Resultado**: Error "El código de color debe estar en formato hexadecimal (#RRGGBB)"

#### Validación de Nivel Duplicado
- [ ] Intentar crear prioridad con nivel `99` (ya existe)
- [ ] **Resultado**: Error "Ya existe una prioridad con este nivel"

#### Editar Color de Prioridad
- [ ] Editar la prioridad de prueba
- [ ] Cambiar color a verde (#10B981)
- [ ] **Verificar**: El preview cambia en tiempo real
- [ ] Guardar
- [ ] **Resultado**: El color cambió en la tabla

#### Eliminar Prioridad
- [ ] Eliminar la prioridad de prueba (nivel 99)
- [ ] **Resultado**: Toast verde de éxito

---

### 3.3 Tipos de Órdenes de Trabajo

#### Crear Nuevo Tipo
- [ ] Hacer clic en pestaña "📋 Tipos de OT"
- [ ] Hacer clic en "Nuevo Tipo"
- [ ] Completar:
  - Código: `TEST_TYPE`
  - Nombre: `Tipo de Prueba`
  - Descripción: `Prueba de CRUD`
  - ✓ Requiere Aprobación
  - ✓ Activo
- [ ] Hacer clic en "Crear"
- [ ] **Resultado**: Toast verde de éxito

#### Validación de Código Único
- [ ] Intentar crear tipo con código `TEST_TYPE`
- [ ] **Resultado**: Error de código duplicado

#### Editar Tipo
- [ ] Editar el tipo de prueba
- [ ] Desmarcar "Requiere Aprobación"
- [ ] Guardar
- [ ] **Resultado**: Cambio guardado correctamente

#### Eliminar Tipo
- [ ] Eliminar el tipo de prueba
- [ ] **Resultado**: Toast verde de éxito

---

### 3.4 Parámetros del Sistema

#### Ver Parámetros
- [ ] Hacer clic en pestaña "⚙️ Parámetros"
- [ ] **Verificar**: Se muestran los parámetros del sistema

#### Editar Parámetro Editable
- [ ] Buscar un parámetro con "Editable: Sí"
- [ ] Hacer clic en editar
- [ ] Cambiar el valor
- [ ] Guardar
- [ ] **Resultado**: Toast verde de éxito

#### Intentar Editar Parámetro No Editable
- [ ] Buscar un parámetro con "Editable: No"
- [ ] Hacer clic en editar
- [ ] **Resultado**: Debe mostrar mensaje "Este parámetro no es editable"
- [ ] **Verificar**: Los campos están deshabilitados

#### Validación de Tipo de Dato
- [ ] Editar un parámetro de tipo "integer"
- [ ] Intentar poner texto: `abc`
- [ ] Intentar guardar
- [ ] **Resultado**: Error de validación de tipo

---

### 3.5 Registro de Auditoría

#### Ver Auditoría
- [ ] Hacer clic en pestaña "📜 Auditoría"
- [ ] **Verificar**: Se muestran todas las operaciones realizadas

#### Verificar Registro de Cambios
- [ ] **Verificar**: Aparecen las categorías creadas/editadas/eliminadas
- [ ] **Verificar**: Aparecen las prioridades creadas/editadas/eliminadas
- [ ] **Verificar**: Aparecen los tipos creados/editados/eliminados
- [ ] **Verificar**: Se muestra el usuario que hizo cada cambio
- [ ] **Verificar**: Se muestra la fecha y hora
- [ ] **Verificar**: Se muestra el tipo de acción (Crear/Actualizar/Eliminar)

---

## 4. ✅ Pruebas de Validación

### Campos Requeridos
- [ ] Intentar crear categoría sin código
- [ ] **Resultado**: Error "El código es requerido"
- [ ] Intentar crear categoría sin nombre
- [ ] **Resultado**: Error "El nombre es requerido"

### Formato de Código
- [ ] Intentar crear categoría con código en minúsculas: `test001`
- [ ] **Resultado**: Debe aceptarse o mostrar error según validación

### Modal en Errores
- [ ] Provocar un error de validación
- [ ] **Verificar**: El modal NO se cierra
- [ ] **Verificar**: Se puede corregir el error y reintentar

### Modal en Éxito
- [ ] Crear una categoría exitosamente
- [ ] **Verificar**: El modal SE cierra automáticamente
- [ ] **Verificar**: La tabla se actualiza con el nuevo elemento

---

## 5. ✅ Pruebas de Seguridad

### Acceso Solo Admin
- [ ] Cerrar sesión
- [ ] Iniciar sesión como Operador o Supervisor (no admin)
- [ ] Intentar acceder a /configuration
- [ ] **Resultado**: Debe redirigir o mostrar "Acceso denegado"

---

## 📊 Resumen de Resultados

### Dashboard
- KPIs sin negativos: [ ] ✅ Pasa  [ ] ❌ Falla
- Todos los valores correctos: [ ] ✅ Pasa  [ ] ❌ Falla

### Notificaciones
- Sin error 404: [ ] ✅ Pasa  [ ] ❌ Falla
- Mensajes de error claros: [ ] ✅ Pasa  [ ] ❌ Falla
- Marcado como leída: [ ] ✅ Pasa  [ ] ❌ Falla

### Configuración - Categorías
- Crear: [ ] ✅ Pasa  [ ] ❌ Falla
- Editar: [ ] ✅ Pasa  [ ] ❌ Falla
- Eliminar: [ ] ✅ Pasa  [ ] ❌ Falla
- Validaciones: [ ] ✅ Pasa  [ ] ❌ Falla

### Configuración - Prioridades
- Crear: [ ] ✅ Pasa  [ ] ❌ Falla
- Editar color: [ ] ✅ Pasa  [ ] ❌ Falla
- Validación hex: [ ] ✅ Pasa  [ ] ❌ Falla
- Eliminar: [ ] ✅ Pasa  [ ] ❌ Falla

### Configuración - Tipos OT
- Crear: [ ] ✅ Pasa  [ ] ❌ Falla
- Editar: [ ] ✅ Pasa  [ ] ❌ Falla
- Eliminar: [ ] ✅ Pasa  [ ] ❌ Falla

### Configuración - Parámetros
- Editar editable: [ ] ✅ Pasa  [ ] ❌ Falla
- Bloqueo no editable: [ ] ✅ Pasa  [ ] ❌ Falla
- Validación tipo: [ ] ✅ Pasa  [ ] ❌ Falla

### Auditoría
- Registro completo: [ ] ✅ Pasa  [ ] ❌ Falla

---

## 🐛 Bugs Encontrados

### Bug #1
**Descripción**: 
**Pasos para reproducir**:
1. 
2. 
3. 

**Resultado esperado**:
**Resultado actual**:
**Severidad**: [ ] Crítico  [ ] Alto  [ ] Medio  [ ] Bajo

---

## ✅ Conclusión

**Estado General**: [ ] ✅ Todas las pruebas pasaron  [ ] ⚠️ Algunas pruebas fallaron  [ ] ❌ Muchas pruebas fallaron

**Recomendación**: [ ] Aprobar para producción  [ ] Requiere correcciones  [ ] Requiere más pruebas

**Comentarios adicionales**:
```
[Escribe aquí cualquier observación adicional]
```

---

**Probado por**: _______________
**Fecha**: _______________
**Firma**: _______________
