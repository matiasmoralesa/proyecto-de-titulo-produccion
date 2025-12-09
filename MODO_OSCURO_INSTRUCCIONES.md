# Instrucciones para Activar el Modo Oscuro

## ✅ Estado de Implementación

El modo oscuro ha sido implementado completamente en:

### Formularios (100%)
- ✅ WorkOrderForm
- ✅ MaintenancePlanForm
- ✅ AssetForm
- ✅ SparePartForm
- ✅ UserForm
- ✅ CategoryForm
- ✅ PriorityForm
- ✅ WorkOrderTypeForm
- ✅ ParameterForm
- ✅ StatusUpdateForm

### Listas y Tablas (100%)
- ✅ UserList
- ✅ SparePartList

### Páginas (100%)
- ✅ Dashboard
- ✅ WorkOrders
- ✅ Assets
- ✅ UsersPage
- ✅ NotificationsPage
- ✅ Inventory
- ✅ ReportsPage
- ✅ MLPredictionsPage
- ✅ MaintenancePlans
- ✅ ChecklistsPage
- ✅ ConfigurationPage
- ✅ LocationsPage
- ✅ MachineStatusPage

### Layout (100%)
- ✅ MainLayout (sidebar, header, fondo)

## 🎨 Cómo Funciona

El modo oscuro se activa **automáticamente** según la preferencia del sistema operativo del usuario.

### Configuración en Windows 11

1. Presiona `Windows + I` para abrir Configuración
2. Ve a **Personalización** → **Colores**
3. En "Elegir el modo", selecciona **Oscuro**
4. La aplicación cambiará automáticamente a modo oscuro

### Configuración en Windows 10

1. Presiona `Windows + I` para abrir Configuración
2. Ve a **Personalización** → **Colores**
3. En "Elegir el modo de aplicación predeterminado", selecciona **Oscuro**
4. La aplicación cambiará automáticamente a modo oscuro

### Configuración en macOS

1. Ve a **Preferencias del Sistema** → **General**
2. En "Apariencia", selecciona **Oscuro**
3. La aplicación cambiará automáticamente a modo oscuro

## 🔄 Cómo Ver los Cambios

Si ya tienes la aplicación abierta y no ves los cambios:

### Opción 1: Forzar Recarga (Recomendado)
- **Windows/Linux**: Presiona `Ctrl + Shift + R`
- **Mac**: Presiona `Cmd + Shift + R`

### Opción 2: Limpiar Caché del Navegador
1. Presiona `F12` para abrir DevTools
2. Haz clic derecho en el botón de recargar (junto a la barra de direcciones)
3. Selecciona **"Vaciar caché y recargar de forma forzada"**

### Opción 3: Modo Incógnito
- Abre una ventana de incógnito/privada
- Navega a la aplicación
- Esto evitará problemas de caché

## 🎯 Verificar que Funciona

1. **Activa el modo oscuro en tu sistema operativo** (ver instrucciones arriba)
2. **Abre la aplicación** en tu navegador
3. **Deberías ver**:
   - Fondo oscuro en toda la aplicación
   - Sidebar oscuro
   - Formularios con campos oscuros
   - Tablas con fondo oscuro
   - Texto claro sobre fondos oscuros

## 🛠️ Configuración Técnica

La aplicación usa:
- **Tailwind CSS** con `darkMode: 'media'`
- Detecta automáticamente `prefers-color-scheme: dark`
- Clases CSS: `dark:bg-gray-800`, `dark:text-white`, etc.

## 📱 Compatibilidad

El modo oscuro funciona en:
- ✅ Chrome/Edge (versión 76+)
- ✅ Firefox (versión 67+)
- ✅ Safari (versión 12.1+)
- ✅ Opera (versión 62+)

## 🐛 Solución de Problemas

### El modo oscuro no se activa

1. **Verifica que tu sistema esté en modo oscuro**
   - Windows: Configuración → Personalización → Colores → Modo Oscuro
   - Mac: Preferencias del Sistema → General → Apariencia Oscuro

2. **Limpia la caché del navegador**
   - Presiona `Ctrl + Shift + R` (Windows) o `Cmd + Shift + R` (Mac)

3. **Verifica la versión del navegador**
   - Asegúrate de tener una versión actualizada

4. **Prueba en modo incógnito**
   - Esto descarta problemas de extensiones o caché

### Algunos componentes no están en modo oscuro

Si encuentras algún componente que no esté en modo oscuro, por favor reporta:
- Nombre de la página
- Componente específico
- Captura de pantalla

## 📝 Notas Adicionales

- El modo oscuro se aplica **instantáneamente** cuando cambias la preferencia del sistema
- No requiere recargar la página después del cambio
- Los colores están optimizados para reducir la fatiga visual
- Todos los contrastes cumplen con las pautas de accesibilidad WCAG 2.1

## 🚀 Despliegue

Los cambios están desplegados en:
- **Frontend (Vercel)**: Se actualiza automáticamente con cada push a `main`
- **Backend (Railway)**: No requiere cambios para el modo oscuro

Última actualización: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
