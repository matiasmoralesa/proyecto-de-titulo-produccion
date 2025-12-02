/**
 * Property-based tests for validation error messages
 */
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';

/**
 * Validation error types
 */
interface ValidationError {
  field: string;
  message: string;
  type: 'required' | 'format' | 'unique' | 'type' | 'range';
}

/**
 * Mock API error response
 */
interface APIErrorResponse {
  [field: string]: string | string[];
}

/**
 * Convert API errors to validation errors
 */
function parseAPIErrors(apiErrors: APIErrorResponse): ValidationError[] {
  const errors: ValidationError[] = [];
  
  for (const [field, messages] of Object.entries(apiErrors)) {
    const messageArray = Array.isArray(messages) ? messages : [messages];
    
    messageArray.forEach(message => {
      let type: ValidationError['type'] = 'format';
      
      if (message.toLowerCase().includes('requerido') || message.toLowerCase().includes('required')) {
        type = 'required';
      } else if (message.toLowerCase().includes('ya existe') || message.toLowerCase().includes('unique')) {
        type = 'unique';
      } else if (message.toLowerCase().includes('tipo') || message.toLowerCase().includes('type')) {
        type = 'type';
      } else if (message.toLowerCase().includes('rango') || message.toLowerCase().includes('range')) {
        type = 'range';
      }
      
      errors.push({
        field,
        message,
        type
      });
    });
  }
  
  return errors;
}

/**
 * Check if error message is field-specific
 */
function isFieldSpecificError(error: ValidationError): boolean {
  return error.field !== 'non_field_errors' && error.field !== 'detail';
}

/**
 * Property 9: Validation errors display field-specific messages
 * For any validation error from the API, the system should display
 * field-specific error messages that help users understand what to fix
 */
describe('Validation Error Messages Properties', () => {
  describe('Property 9: Field-Specific Error Messages', () => {
    it('Property 9: Required field errors should be field-specific', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('code', 'name', 'level', 'color_code', 'value'),
          fc.constantFrom(
            'Este campo es requerido',
            'El campo es obligatorio',
            'Required field',
            'This field is required'
          ),
          (field, message) => {
            const apiErrors: APIErrorResponse = {
              [field]: message
            };
            
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have at least one error
            expect(errors.length).toBeGreaterThan(0);
            
            // Property: Error should be field-specific
            expect(errors[0].field).toBe(field);
            expect(isFieldSpecificError(errors[0])).toBe(true);
            
            // Property: Error type should be 'required'
            expect(errors[0].type).toBe('required');
          }
        ),
        { numRuns: 50 }
      );
    });

    it('Property 9: Unique constraint errors should be field-specific', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('code', 'level', 'key'),
          fc.constantFrom(
            'Este código ya existe',
            'El nivel ya está en uso',
            'Ya existe un registro con este valor',
            'This value already exists'
          ),
          (field, message) => {
            const apiErrors: APIErrorResponse = {
              [field]: message
            };
            
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have at least one error
            expect(errors.length).toBeGreaterThan(0);
            
            // Property: Error should be field-specific
            expect(errors[0].field).toBe(field);
            expect(isFieldSpecificError(errors[0])).toBe(true);
            
            // Property: Error type should be 'unique'
            expect(errors[0].type).toBe('unique');
          }
        ),
        { numRuns: 30 }
      );
    });

    it('Property 9: Format errors should be field-specific', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('color_code', 'email', 'phone', 'url'),
          fc.constantFrom(
            'Formato inválido',
            'El formato no es correcto',
            'Invalid format',
            'Please enter a valid value'
          ),
          (field, message) => {
            const apiErrors: APIErrorResponse = {
              [field]: message
            };
            
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have at least one error
            expect(errors.length).toBeGreaterThan(0);
            
            // Property: Error should be field-specific
            expect(errors[0].field).toBe(field);
            expect(isFieldSpecificError(errors[0])).toBe(true);
          }
        ),
        { numRuns: 30 }
      );
    });

    it('Property 9: Type validation errors should be field-specific', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('value', 'level', 'amount'),
          fc.constantFrom(
            'El valor debe ser un número',
            'Tipo de dato incorrecto',
            'Invalid data type',
            'Must be a valid integer'
          ),
          (field, message) => {
            const apiErrors: APIErrorResponse = {
              [field]: message
            };
            
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have at least one error
            expect(errors.length).toBeGreaterThan(0);
            
            // Property: Error should be field-specific
            expect(errors[0].field).toBe(field);
            expect(isFieldSpecificError(errors[0])).toBe(true);
            
            // Property: Error type should be 'type'
            expect(errors[0].type).toBe('type');
          }
        ),
        { numRuns: 30 }
      );
    });

    it('Property 9: Multiple errors for same field should all be parsed', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('code', 'name', 'value'),
          fc.array(fc.string({ minLength: 5, maxLength: 50 }), { minLength: 2, maxLength: 5 }),
          (field, messages) => {
            const apiErrors: APIErrorResponse = {
              [field]: messages
            };
            
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have same number of errors as messages
            expect(errors.length).toBe(messages.length);
            
            // Property: All errors should be for the same field
            errors.forEach(error => {
              expect(error.field).toBe(field);
              expect(isFieldSpecificError(error)).toBe(true);
            });
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 9: Multiple fields with errors should all be parsed', () => {
      fc.assert(
        fc.property(
          fc.dictionary(
            fc.constantFrom('code', 'name', 'level', 'color_code', 'value'),
            fc.string({ minLength: 5, maxLength: 50 }),
            { minKeys: 2, maxKeys: 5 }
          ),
          (apiErrors) => {
            const errors = parseAPIErrors(apiErrors);
            
            // Property: Should have at least as many errors as fields
            expect(errors.length).toBeGreaterThanOrEqual(Object.keys(apiErrors).length);
            
            // Property: Each field should have at least one error
            Object.keys(apiErrors).forEach(field => {
              const fieldErrors = errors.filter(e => e.field === field);
              expect(fieldErrors.length).toBeGreaterThan(0);
            });
          }
        ),
        { numRuns: 20 }
      );
    });
  });

  describe('Specific Error Scenarios', () => {
    it('Category: Code already exists', () => {
      const apiErrors: APIErrorResponse = {
        code: 'Ya existe una categoría con este código'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('code');
      expect(errors[0].type).toBe('unique');
      expect(isFieldSpecificError(errors[0])).toBe(true);
    });

    it('Priority: Invalid color format', () => {
      const apiErrors: APIErrorResponse = {
        color_code: 'El código de color debe estar en formato hexadecimal (#RRGGBB)'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('color_code');
      expect(isFieldSpecificError(errors[0])).toBe(true);
    });

    it('Priority: Level already exists', () => {
      const apiErrors: APIErrorResponse = {
        level: 'Ya existe una prioridad con este nivel'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('level');
      expect(errors[0].type).toBe('unique');
      expect(isFieldSpecificError(errors[0])).toBe(true);
    });

    it('Parameter: Invalid type', () => {
      const apiErrors: APIErrorResponse = {
        value: 'El valor debe ser un número entero válido'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('value');
      expect(errors[0].type).toBe('type');
      expect(isFieldSpecificError(errors[0])).toBe(true);
    });

    it('Multiple fields with errors', () => {
      const apiErrors: APIErrorResponse = {
        code: 'Este campo es requerido',
        name: 'Este campo es requerido',
        color_code: 'Formato inválido'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(3);
      
      const codeError = errors.find(e => e.field === 'code');
      expect(codeError).toBeDefined();
      expect(codeError?.type).toBe('required');
      
      const nameError = errors.find(e => e.field === 'name');
      expect(nameError).toBeDefined();
      expect(nameError?.type).toBe('required');
      
      const colorError = errors.find(e => e.field === 'color_code');
      expect(colorError).toBeDefined();
    });

    it('Field with multiple errors', () => {
      const apiErrors: APIErrorResponse = {
        code: ['Este campo es requerido', 'El código debe tener al menos 3 caracteres']
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(2);
      expect(errors[0].field).toBe('code');
      expect(errors[1].field).toBe('code');
    });
  });

  describe('Edge Cases', () => {
    it('Non-field errors should be identified', () => {
      const apiErrors: APIErrorResponse = {
        non_field_errors: 'Error general del formulario'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('non_field_errors');
      expect(isFieldSpecificError(errors[0])).toBe(false);
    });

    it('Detail errors should be identified', () => {
      const apiErrors: APIErrorResponse = {
        detail: 'No tiene permisos para realizar esta acción'
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('detail');
      expect(isFieldSpecificError(errors[0])).toBe(false);
    });

    it('Empty error messages should be handled', () => {
      const apiErrors: APIErrorResponse = {
        code: ''
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(1);
      expect(errors[0].field).toBe('code');
      expect(errors[0].message).toBe('');
    });

    it('Empty error array should be handled', () => {
      const apiErrors: APIErrorResponse = {
        code: []
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(0);
    });

    it('Mixed string and array errors', () => {
      const apiErrors: APIErrorResponse = {
        code: 'Error simple',
        name: ['Error 1', 'Error 2']
      };
      
      const errors = parseAPIErrors(apiErrors);
      
      expect(errors.length).toBe(3);
      
      const codeErrors = errors.filter(e => e.field === 'code');
      expect(codeErrors.length).toBe(1);
      
      const nameErrors = errors.filter(e => e.field === 'name');
      expect(nameErrors.length).toBe(2);
    });
  });

  describe('Error Type Classification', () => {
    it('Should correctly classify required errors', () => {
      const messages = [
        'Este campo es requerido',
        'El campo es obligatorio',
        'Required field',
        'This field is required'
      ];
      
      messages.forEach(message => {
        const errors = parseAPIErrors({ field: message });
        expect(errors[0].type).toBe('required');
      });
    });

    it('Should correctly classify unique errors', () => {
      const messages = [
        'Ya existe un registro con este valor',
        'Este código ya existe',
        'Unique constraint violation',
        'This value already exists'
      ];
      
      messages.forEach(message => {
        const errors = parseAPIErrors({ field: message });
        expect(errors[0].type).toBe('unique');
      });
    });

    it('Should correctly classify type errors', () => {
      const messages = [
        'El valor debe ser un número',
        'Tipo de dato incorrecto',
        'Invalid data type',
        'Must be a valid integer'
      ];
      
      messages.forEach(message => {
        const errors = parseAPIErrors({ field: message });
        expect(errors[0].type).toBe('type');
      });
    });

    it('Should default to format for unclassified errors', () => {
      const messages = [
        'Formato inválido',
        'Invalid format',
        'Some other error'
      ];
      
      messages.forEach(message => {
        const errors = parseAPIErrors({ field: message });
        expect(errors[0].type).toBe('format');
      });
    });
  });
});
