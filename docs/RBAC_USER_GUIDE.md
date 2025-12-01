# Guía de Usuario - Sistema de Permisos por Roles

## Introducción

Este documento explica cómo funciona el sistema de permisos en la aplicación CMMS y qué puede hacer cada tipo de usuario.

---

## Roles de Usuario

El sistema tiene tres roles principales, cada uno con diferentes niveles de acceso:

### 🔧 Operador
**Nivel de acceso**: Básico

Los operadores son usuarios que ejecutan tareas de mantenimiento y operan los activos.

**Qué pueden hacer:**
- ✅ Ver sus propias órdenes de trabajo asignadas
- ✅ Actualizar el estado de sus órdenes de trabajo
- ✅ Ver los activos relacionados con sus órdenes de trabajo
- ✅ Registrar horas trabajadas en sus tareas
- ✅ Ver notificaciones relacionadas con sus tareas
- ✅ Completar checklists asignados

**Qué NO pueden hacer:**
- ❌ Ver órdenes de trabajo de otros operadores
- ❌ Crear nuevas órdenes de trabajo
- ❌ Asignar tareas a otros usuarios
- ❌ Modificar activos
- ❌ Ver reportes globales
- ❌ Gestionar usuarios

### 👔 Supervisor
**Nivel de acceso**: Intermedio

Los supervisores coordinan equipos de operadores y supervisan las operaciones.

**Qué pueden hacer:**
- ✅ Todo lo que puede hacer un Operador, más:
- ✅ Ver todas las órdenes de trabajo del sistema
- ✅ Crear nuevas órdenes de trabajo
- ✅ Asignar órdenes de trabajo a operadores
- ✅ Ver y modificar todos los activos
- ✅ Generar reportes de su equipo
- ✅ Ver estadísticas de rendimiento
- ✅ Gestionar operadores (crear, editar)
- ✅ Ejecutar predicciones de mantenimiento

**Qué NO pueden hacer:**
- ❌ Crear usuarios administradores
- ❌ Modificar configuración del sistema
- ❌ Eliminar registros de auditoría

### 👨‍💼 Administrador
**Nivel de acceso**: Completo

Los administradores tienen control total sobre el sistema.

**Qué pueden hacer:**
- ✅ Todo lo que puede hacer un Supervisor, más:
- ✅ Gestionar todos los usuarios (crear, editar, eliminar)
- ✅ Modificar configuración del sistema
- ✅ Ver logs de auditoría
- ✅ Gestionar roles y permisos
- ✅ Exportar datos del sistema
- ✅ Configurar integraciones
- ✅ Acceder a todas las funciones administrativas

---

## Funcionalidades por Rol

### Órdenes de Trabajo

| Acción | Operador | Supervisor | Admin |
|--------|----------|------------|-------|
| Ver propias OT | ✅ | ✅ | ✅ |
| Ver todas las OT | ❌ | ✅ | ✅ |
| Crear OT | ❌ | ✅ | ✅ |
| Asignar OT | ❌ | ✅ | ✅ |
| Actualizar estado | ✅ (propias) | ✅ | ✅ |
| Eliminar OT | ❌ | ✅ | ✅ |

### Activos

| Acción | Operador | Supervisor | Admin |
|--------|----------|------------|-------|
| Ver activos asignados | ✅ | ✅ | ✅ |
| Ver todos los activos | ❌ | ✅ | ✅ |
| Crear activos | ❌ | ✅ | ✅ |
| Modificar activos | ❌ | ✅ | ✅ |
| Eliminar activos | ❌ | ❌ | ✅ |

### Reportes y Estadísticas

| Acción | Operador | Supervisor | Admin |
|--------|----------|------------|-------|
| Ver propias estadísticas | ✅ | ✅ | ✅ |
| Ver estadísticas de equipo | ❌ | ✅ | ✅ |
| Ver estadísticas globales | ❌ | ❌ | ✅ |
| Exportar reportes | ❌ | ✅ | ✅ |

### Gestión de Usuarios

| Acción | Operador | Supervisor | Admin |
|--------|----------|------------|-------|
| Ver perfil propio | ✅ | ✅ | ✅ |
| Ver otros usuarios | ❌ | ✅ (su equipo) | ✅ |
| Crear operadores | ❌ | ✅ | ✅ |
| Crear supervisores | ❌ | ❌ | ✅ |
| Crear administradores | ❌ | ❌ | ✅ |
| Modificar usuarios | ❌ | ✅ (operadores) | ✅ |

### Predicciones de Mantenimiento

| Acción | Operador | Supervisor | Admin |
|--------|----------|------------|-------|
| Ver predicciones | ✅ (sus activos) | ✅ | ✅ |
| Ejecutar predicciones | ❌ | ✅ | ✅ |
| Configurar modelos | ❌ | ❌ | ✅ |

---

## Notificaciones

El sistema envía notificaciones automáticas según tu rol:

### Operadores reciben notificaciones sobre:
- Nueva orden de trabajo asignada
- Cambios en sus órdenes de trabajo
- Predicciones de falla en sus activos
- Recordatorios de tareas pendientes

### Supervisores reciben notificaciones sobre:
- Órdenes de trabajo de alta prioridad
- Órdenes de trabajo completadas
- Predicciones críticas de falla
- Alertas de rendimiento del equipo

### Administradores reciben notificaciones sobre:
- Alertas de seguridad
- Intentos de acceso no autorizado
- Problemas del sistema
- Todas las notificaciones críticas

---

## Interfaz de Usuario Adaptada

La interfaz se adapta automáticamente según tu rol:

### Dashboard del Operador
- **Mis Órdenes de Trabajo**: Lista de tus tareas asignadas
- **Mis Activos**: Activos que estás operando
- **Mis Estadísticas**: Tu rendimiento personal
- **Notificaciones**: Alertas relevantes para ti

### Dashboard del Supervisor
- **Órdenes de Trabajo del Equipo**: Todas las OT activas
- **Estadísticas del Equipo**: Rendimiento del equipo
- **Gestión de Recursos**: Asignación de tareas
- **Reportes**: Generación de reportes

### Dashboard del Administrador
- **Vista Global**: Estadísticas de toda la organización
- **Gestión de Usuarios**: Administración completa
- **Configuración**: Ajustes del sistema
- **Auditoría**: Logs de acceso y cambios

---

## Preguntas Frecuentes

### ¿Cómo sé qué rol tengo?

Tu rol se muestra en la esquina superior derecha de la aplicación, junto a tu nombre de usuario.

### ¿Puedo tener más de un rol?

No, cada usuario tiene un único rol asignado. Si necesitas permisos diferentes, contacta a tu administrador.

### ¿Cómo solicito un cambio de rol?

Contacta a tu supervisor o administrador del sistema. Solo los administradores pueden cambiar roles de usuario.

### ¿Por qué no puedo ver ciertas órdenes de trabajo?

Por seguridad y organización, los operadores solo ven las órdenes de trabajo que les han sido asignadas. Si necesitas ver otras órdenes de trabajo, contacta a tu supervisor.

### ¿Puedo ver el trabajo de otros operadores?

Los operadores no pueden ver el trabajo de otros operadores. Los supervisores y administradores sí pueden ver todo el trabajo del equipo.

### ¿Qué pasa si intento acceder a algo sin permisos?

El sistema te mostrará un mensaje indicando que no tienes permisos para esa acción. Todos los intentos de acceso son registrados por seguridad.

### ¿Cómo se registran mis acciones?

El sistema mantiene un registro de auditoría de todas las acciones importantes. Los administradores pueden revisar estos registros si es necesario.

---

## Seguridad y Privacidad

### Protección de Datos

- Solo puedes ver datos relevantes para tu rol
- Tus credenciales están encriptadas
- Todas las acciones son auditadas
- Los datos sensibles están protegidos

### Buenas Prácticas

1. **No compartas tu contraseña** con nadie
2. **Cierra sesión** cuando termines de usar el sistema
3. **Reporta actividad sospechosa** a tu administrador
4. **Mantén tu información actualizada**

---

## Soporte

### ¿Necesitas ayuda?

**Operadores**: Contacta a tu supervisor
**Supervisores**: Contacta al administrador del sistema
**Administradores**: Consulta la documentación técnica o contacta a soporte técnico

### Reportar Problemas

Si encuentras un problema o error:
1. Anota qué estabas haciendo cuando ocurrió
2. Toma una captura de pantalla si es posible
3. Contacta a tu supervisor o administrador
4. Proporciona la mayor cantidad de detalles posible

---

## Glosario

**Rol**: Conjunto de permisos asignados a un usuario

**Orden de Trabajo (OT)**: Tarea de mantenimiento asignada a un operador

**Activo**: Equipo o maquinaria que requiere mantenimiento

**Dashboard**: Pantalla principal con resumen de información

**Auditoría**: Registro de acciones realizadas en el sistema

**Predicción**: Estimación de cuándo un activo puede fallar

**Notificación**: Alerta o mensaje del sistema

---

## Cambios Recientes

### Versión 2.0 - Sistema de Permisos por Roles

**Fecha**: Diciembre 2024

**Cambios principales**:
- Implementación de roles (Operador, Supervisor, Admin)
- Filtrado automático de datos según rol
- Dashboard adaptado por rol
- Sistema de auditoría mejorado
- Notificaciones filtradas por permisos

**Impacto para usuarios**:
- Mayor seguridad de datos
- Interfaz más limpia y relevante
- Mejor organización del trabajo
- Acceso más rápido a información relevante

---

## Contacto

Para más información o soporte, contacta a:
- **Soporte Técnico**: [email de soporte]
- **Administrador del Sistema**: [email del admin]
- **Documentación**: Consulta la documentación técnica en el sistema
