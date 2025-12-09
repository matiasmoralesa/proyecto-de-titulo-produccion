# Fix: Redirección al Login después de Cambio de Contraseña Obligatoria

## Problema

Cuando un usuario nuevo cambiaba su contraseña obligatoria en el primer login, el sistema se quedaba en la misma página en lugar de redirigir al login para que iniciara sesión con la nueva contraseña.

## Causa

El componente `FirstLoginPasswordChange` solo actualizaba el estado local (`onSuccess()`) pero no hacía logout ni limpiaba los tokens de autenticación. Esto causaba que:

1. El usuario seguía "autenticado" con tokens de la contraseña vieja
2. El flag `must_change_password` se actualizaba localmente pero no en el servidor
3. La sesión quedaba en un estado inconsistente

## Solución

**Archivo modificado**: `frontend/src/components/auth/FirstLoginPasswordChange.tsx`

### Antes:
```typescript
try {
  await authService.changePassword({...});
  
  alert('Contraseña cambiada exitosamente');
  onSuccess(); // Solo actualiza estado local
} catch (error) {
  // ...
} finally {
  setLoading(false);
}
```

### Después:
```typescript
try {
  await authService.changePassword({...});
  
  // Show success message
  alert('Contraseña cambiada exitosamente. Por favor, inicia sesión con tu nueva contraseña.');
  
  // Clear auth data and redirect to login
  authService.clearAuthData();
  window.location.href = '/login';
} catch (error) {
  // ...
  setLoading(false); // Solo en error
}
```

## Cambios Implementados

1. **Limpia datos de autenticación**: `authService.clearAuthData()`
   - Elimina tokens de localStorage
   - Elimina datos de usuario
   - Invalida la sesión actual

2. **Redirección forzada**: `window.location.href = '/login'`
   - Usa `window.location.href` en lugar de `navigate()` para forzar recarga completa
   - Asegura que el estado de la aplicación se reinicie completamente

3. **Mensaje mejorado**: Indica al usuario que debe iniciar sesión con la nueva contraseña

4. **Manejo de loading**: Solo se desactiva en caso de error (no en éxito porque redirige)

## Flujo Completo

### Antes del Fix:
```
1. Usuario nuevo inicia sesión → must_change_password = true
2. Sistema muestra modal de cambio de contraseña
3. Usuario cambia contraseña exitosamente
4. onSuccess() actualiza estado local
5. ❌ Usuario se queda en la misma página
6. ❌ Tokens siguen siendo de la contraseña vieja
```

### Después del Fix:
```
1. Usuario nuevo inicia sesión → must_change_password = true
2. Sistema muestra modal de cambio de contraseña
3. Usuario cambia contraseña exitosamente
4. ✅ Sistema limpia tokens y datos de autenticación
5. ✅ Sistema redirige a /login
6. ✅ Usuario inicia sesión con nueva contraseña
7. ✅ Sistema actualiza must_change_password = false en el servidor
```

## Testing

### Prueba Manual:

1. **Crear usuario nuevo**:
   ```bash
   python manage.py create_test_users
   ```

2. **Iniciar sesión con usuario nuevo**:
   - Username: `operador1`
   - Password: `temporal123`

3. **Verificar modal de cambio de contraseña**:
   - Debe aparecer automáticamente
   - No se puede cerrar (modal bloqueante)

4. **Cambiar contraseña**:
   - Contraseña actual: `temporal123`
   - Nueva contraseña: `MiNuevaPassword123!`
   - Confirmar contraseña: `MiNuevaPassword123!`

5. **Verificar redirección**:
   - ✅ Debe mostrar mensaje de éxito
   - ✅ Debe redirigir a `/login`
   - ✅ Debe limpiar la sesión

6. **Iniciar sesión nuevamente**:
   - Username: `operador1`
   - Password: `MiNuevaPassword123!`
   - ✅ Debe iniciar sesión exitosamente
   - ✅ No debe mostrar modal de cambio de contraseña

### Prueba Automatizada:

```typescript
// frontend/src/components/auth/__tests__/FirstLoginPasswordChange.test.tsx
describe('FirstLoginPasswordChange', () => {
  it('should redirect to login after successful password change', async () => {
    const mockChangePassword = jest.fn().mockResolvedValue({});
    const mockClearAuthData = jest.fn();
    
    authService.changePassword = mockChangePassword;
    authService.clearAuthData = mockClearAuthData;
    
    const { getByLabelText, getByText } = render(
      <FirstLoginPasswordChange onSuccess={jest.fn()} />
    );
    
    // Fill form
    fireEvent.change(getByLabelText('Contraseña Actual *'), {
      target: { value: 'oldpass123' }
    });
    fireEvent.change(getByLabelText('Nueva Contraseña *'), {
      target: { value: 'newpass123' }
    });
    fireEvent.change(getByLabelText('Confirmar Nueva Contraseña *'), {
      target: { value: 'newpass123' }
    });
    
    // Submit
    fireEvent.click(getByText('Cambiar Contraseña'));
    
    await waitFor(() => {
      expect(mockChangePassword).toHaveBeenCalled();
      expect(mockClearAuthData).toHaveBeenCalled();
      expect(window.location.href).toBe('/login');
    });
  });
});
```

## Consideraciones de Seguridad

1. **Invalidación de tokens**: Los tokens viejos quedan inválidos después del cambio de contraseña
2. **Sesión limpia**: No hay riesgo de usar tokens de contraseña anterior
3. **Forzar nuevo login**: El usuario debe autenticarse con la nueva contraseña
4. **Recarga completa**: `window.location.href` asegura que no quede estado residual

## Alternativas Consideradas

### Opción 1: Usar navigate() de react-router
```typescript
navigate('/login');
```
❌ **Rechazada**: No limpia completamente el estado de la aplicación

### Opción 2: Hacer logout desde authStore
```typescript
await useAuthStore.getState().logout();
navigate('/login');
```
❌ **Rechazada**: Más complejo y puede tener race conditions

### Opción 3: Recargar página actual
```typescript
window.location.reload();
```
❌ **Rechazada**: No redirige al login, usuario queda en página protegida

### Opción 4: Usar window.location.href (SELECCIONADA)
```typescript
authService.clearAuthData();
window.location.href = '/login';
```
✅ **Seleccionada**: Simple, efectiva, limpia todo el estado

## Impacto

- **Usuarios afectados**: Todos los usuarios nuevos en su primer login
- **Breaking changes**: Ninguno
- **Mejora de UX**: Alta - flujo más claro y seguro
- **Seguridad**: Mejorada - tokens viejos no quedan activos

## Commit

```bash
git commit -m "fix: Redirigir al login después de cambiar contraseña obligatoria

- Después de cambiar contraseña en primer login, ahora hace logout y redirige a /login
- Limpia los datos de autenticación (tokens) para forzar nuevo login
- Muestra mensaje indicando que debe iniciar sesión con la nueva contraseña
- Soluciona el problema de quedarse en la misma página después del cambio"
```

**Commit hash**: `67f003b`

## Referencias

- Issue: Usuario se queda en la misma página después de cambiar contraseña
- Componente: `frontend/src/components/auth/FirstLoginPasswordChange.tsx`
- Servicio: `frontend/src/services/authService.ts`
- Store: `frontend/src/store/authStore.ts`
