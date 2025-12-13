# 🏢 Implementación del Logo SOMACOR

## Ubicaciones del Logo

El logo de SOMACOR ha sido implementado estratégicamente en las siguientes ubicaciones:

### 1. **Página de Login** (`/login`)
- **Ubicación**: Header principal, centrado
- **Tamaño**: Extra Large (80x80px)
- **Características**: 
  - Logo prominente sin texto
  - Mensaje "SOMACOR - 50 Años de Experiencia"
  - Footer actualizado con branding SOMACOR

### 2. **Sidebar de Navegación** (MainLayout)
- **Ubicación**: Header del sidebar izquierdo
- **Tamaño**: Small (32x32px)
- **Características**:
  - Logo con texto "CMMS" y subtexto "SOMACOR"
  - Fondo blanco circular para contraste
  - Fallback a ícono de herramienta si falla la carga

### 3. **Dashboard Principal** (`/dashboard`)
- **Ubicación**: Header del banner de bienvenida (esquina superior derecha)
- **Tamaño**: Small (32x32px)
- **Características**:
  - Logo discreto sin texto
  - Fondo semi-transparente para integración visual
  - Complementa la información del usuario

## Componente Reutilizable

### `SomacorLogo.tsx`

Componente React reutilizable con las siguientes características:

#### Props:
- `size`: 'sm' | 'md' | 'lg' | 'xl' (default: 'md')
- `showText`: boolean (default: true)
- `showSubtext`: boolean (default: false)
- `className`: string (clases CSS adicionales)

#### Características:
- **Fallback automático**: Si la imagen no carga, muestra ícono de herramienta
- **Responsive**: Diferentes tamaños para diferentes contextos
- **Accesible**: Alt text apropiado y contraste adecuado
- **Consistente**: Estilo uniforme en toda la aplicación

#### Ejemplo de uso:
```tsx
// Logo grande para login
<SomacorLogo size="xl" showText={false} />

// Logo con texto para sidebar
<SomacorLogo size="sm" showText={true} showSubtext={true} />

// Logo discreto para dashboard
<SomacorLogo size="sm" showText={false} />
```

## Archivo de Logo

### Ubicación: `/public/logo-somacor.png`
- **Formato**: PNG con transparencia
- **Diseño**: Logo circular azul con "SOMACOR 50 AÑOS"
- **Optimización**: Tamaño optimizado para web
- **Fallback**: Ícono de herramienta (FiTool) si no carga

## Consideraciones de Diseño

### 1. **Contraste y Visibilidad**
- Fondo blanco circular para asegurar visibilidad
- Bordes sutiles para definición
- Sombras suaves para profundidad

### 2. **Consistencia de Marca**
- Colores corporativos respetados
- Proporciones mantenidas
- Mensaje "50 Años" destacado apropiadamente

### 3. **Responsive Design**
- Tamaños adaptativos según contexto
- Oculto en móviles cuando es necesario
- Mantiene legibilidad en todos los tamaños

### 4. **Performance**
- Carga lazy cuando es posible
- Fallback inmediato sin parpadeo
- Optimización de imágenes

## Futuras Mejoras

- [ ] Versión SVG para mejor escalabilidad
- [ ] Animaciones sutiles de hover
- [ ] Modo oscuro específico del logo
- [ ] Versión horizontal para espacios amplios
- [ ] Integración con favicon del sitio

## Mantenimiento

Para actualizar el logo:
1. Reemplazar `/public/logo-somacor.png`
2. Mantener proporciones cuadradas
3. Asegurar fondo transparente
4. Probar en todos los contextos de uso

---

*Implementado: Diciembre 2024*
*Componente: SomacorLogo.tsx*
*Ubicaciones: Login, Sidebar, Dashboard*