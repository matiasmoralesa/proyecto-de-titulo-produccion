/**
 * Utilidades para validación de RUT chileno
 */

/**
 * Limpia el RUT removiendo puntos, guiones y espacios
 */
export const cleanRut = (rut: string): string => {
  return rut.replace(/[.\-\s]/g, '').toUpperCase();
};

/**
 * Formatea el RUT con puntos y guión
 */
export const formatRut = (rut: string): string => {
  const cleanedRut = cleanRut(rut);
  
  if (cleanedRut.length < 2) {
    return cleanedRut;
  }
  
  const body = cleanedRut.slice(0, -1);
  const dv = cleanedRut.slice(-1);
  
  // Agregar puntos cada 3 dígitos desde la derecha
  const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  
  return `${formattedBody}-${dv}`;
};

/**
 * Calcula el dígito verificador de un RUT
 */
export const calculateDV = (rutBody: string): string => {
  let sum = 0;
  let multiplier = 2;
  
  // Recorrer el RUT de derecha a izquierda
  for (let i = rutBody.length - 1; i >= 0; i--) {
    sum += parseInt(rutBody[i]) * multiplier;
    multiplier = multiplier === 7 ? 2 : multiplier + 1;
  }
  
  const remainder = sum % 11;
  const dv = 11 - remainder;
  
  if (dv === 11) return '0';
  if (dv === 10) return 'K';
  return dv.toString();
};

/**
 * Valida si un RUT es válido
 */
export const validateRut = (rut: string): boolean => {
  const cleanedRut = cleanRut(rut);
  
  // Verificar formato básico
  if (!/^\d{7,8}[0-9K]$/.test(cleanedRut)) {
    return false;
  }
  
  const body = cleanedRut.slice(0, -1);
  const dv = cleanedRut.slice(-1);
  
  // Calcular dígito verificador esperado
  const expectedDV = calculateDV(body);
  
  return dv === expectedDV;
};

/**
 * Valida RUT y devuelve mensaje de error si es inválido
 */
export const validateRutWithMessage = (rut: string): { isValid: boolean; message?: string } => {
  if (!rut || rut.trim() === '') {
    return { isValid: false, message: 'El RUT es requerido' };
  }
  
  const cleanedRut = cleanRut(rut);
  
  if (cleanedRut.length < 8 || cleanedRut.length > 9) {
    return { isValid: false, message: 'El RUT debe tener entre 8 y 9 caracteres' };
  }
  
  if (!/^\d{7,8}[0-9K]$/.test(cleanedRut)) {
    return { isValid: false, message: 'Formato de RUT inválido. Debe contener solo números y terminar en número o K' };
  }
  
  if (!validateRut(rut)) {
    return { isValid: false, message: 'El RUT ingresado no es válido' };
  }
  
  return { isValid: true };
};