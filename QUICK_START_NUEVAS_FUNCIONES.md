# 🚀 Guía Rápida - Nuevas Funcionalidades

## ✨ 3 Mejoras Principales

### 1. ✅ KPIs Corregidos
**Qué cambió**: Ya no verás números negativos en el dashboard
**Dónde**: Dashboard principal
**Quién**: Todos los usuarios

### 2. ✅ Notificaciones Arregladas
**Qué cambió**: Hacer clic en notificaciones ya no da error 404
**Dónde**: Campana de notificaciones (arriba derecha)
**Quién**: Todos los usuarios

### 3. ✅ Configuración Completa
**Qué cambió**: Ahora puedes crear, editar y eliminar configuraciones
**Dónde**: Menú → Configuración
**Quién**: Solo Administradores

---

## 🎯 Acceso Rápido

### Para Probar en Producción:
1. Ve a tu URL de producción
2. Inicia sesión como administrador
3. Prueba las nuevas funciones

### Para Probar en Local:
```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev

# Accede a: http://localhost:5173
```

---

## 📝 Cómo Usar Configuración (Solo Admin)

### Crear Nueva Categoría
1. Configuración → 📁 Categorías
2. Clic en "Nueva Categoría"
3. Completa:
   - Código: CAT001 (único)
   - Nombre: Vehículos Pesados
   - Descripción: (opcional)
   - ✓ Activo
4. Clic en "Crear"

### Crear Nueva Prioridad
1. Configuración → ⚡ Prioridades
2. Clic en "Nueva Prioridad"
3. Completa:
   - Nivel: 1 (1=más alta, 10=más baja)
   - Nombre: Urgente
   - Color: Selecciona rojo o escribe #EF4444
   - ✓ Activo
4. Clic en "Crear"

### Editar Existente
1. Encuentra en la tabla
2. Clic en ícono de lápiz ✏️
3. Modifica lo necesario
4. Clic en "Actualizar"

### Eliminar
1. Clic en ícono de papelera 🗑️
2. Confirma
3. **Nota**: Solo si no está en uso

---

## ⚠️ Validaciones Importantes

### Códigos Únicos
- ❌ No puedes crear dos categorías con el mismo código
- ✅ Usa códigos descriptivos: CAT001, PRIO001, etc.

### Colores
- ❌ "rojo" no funciona
- ✅ Usa formato hex: #EF4444
- 💡 Usa el selector de colores predefinidos

### Niveles de Prioridad
- ❌ No puedes tener dos prioridades con el mismo nivel
- ✅ Usa 1 para más urgente, 10 para menos urgente

### Parámetros del Sistema
- ⚠️ Algunos parámetros no son editables (seguridad)
- ✅ Solo edita si sabes qué hace el parámetro

---

## 🎨 Colores Predefinidos para Prioridades

- 🔴 Rojo: #EF4444 (Urgente)
- 🟠 Naranja: #F59E0B (Alta)
- 🟡 Amarillo: #EAB308 (Media)
- 🟢 Verde: #10B981 (Baja)
- 🔵 Azul: #3B82F6 (Normal)
- 🟣 Morado: #8B5CF6 (Planificada)
- 🩷 Rosa: #EC4899 (Especial)
- ⚫ Gris: #6B7280 (Inactiva)

---

## 📊 Registro de Auditoría

### Ver Cambios
1. Configuración → 📜 Auditoría
2. Verás:
   - Quién hizo el cambio
   - Qué cambió
   - Cuándo lo hizo
   - Tipo de acción (Crear/Actualizar/Eliminar)

### Filtrar
- Por usuario
- Por tipo de acción
- Por modelo (Categoría, Prioridad, etc.)

---

## 🐛 Solución de Problemas

### "Ya existe una categoría con este código"
**Solución**: Usa un código diferente (deben ser únicos)

### "El código de color debe estar en formato hexadecimal"
**Solución**: Usa formato #RRGGBB (ej: #EF4444)

### "Este parámetro no es editable"
**Solución**: Es correcto, algunos parámetros están protegidos

### "No se puede eliminar porque está en uso"
**Solución**: Primero elimina o cambia los elementos que lo usan

### No veo el botón "Nueva Categoría"
**Solución**: Verifica que estés logueado como Administrador

---

## ✅ Checklist de Prueba Rápida

- [ ] Dashboard muestra KPIs positivos
- [ ] Clic en notificación funciona
- [ ] Puedo crear nueva categoría
- [ ] Puedo editar prioridad
- [ ] Puedo cambiar color de prioridad
- [ ] Veo registro de auditoría
- [ ] Mensajes de error son claros
- [ ] Mensajes de éxito aparecen

---

## 💡 Tips

1. **Códigos Descriptivos**: Usa CAT001, CAT002 en lugar de C1, C2
2. **Nombres Claros**: "Vehículos Pesados" mejor que "VH"
3. **Colores Consistentes**: Rojo para urgente, verde para baja
4. **Revisa Auditoría**: Útil para ver quién cambió qué
5. **Prueba Primero**: Crea una categoría de prueba antes de las reales

---

## 📞 ¿Necesitas Ayuda?

1. Revisa los mensajes de error en pantalla
2. Presiona F12 para ver la consola del navegador
3. Contacta al equipo de desarrollo

---

**Versión**: 1.1.0
**Última Actualización**: 2 de Diciembre de 2025
**Estado**: ✅ Funcionando en Producción
