/**
 * Property-based tests for parameter form validation
 */
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';

/**
 * Mock parameter type
 */
interface SystemParameter {
  key: string;
  value: string;
  description: string;
  data_type: 'string' | 'integer' | 'float' | 'boolean' | 'json';
  is_editable: boolean;
}

/**
 * Utility function to check if parameter can be edited
 */
function canEditParameter(parameter: SystemParameter): boolean {
  return parameter.is_editable;
}

/**
 * Utility function to validate parameter value based on data type
 */
function validateParameterValue(value: string, dataType: string): { valid: boolean; error?: string } {
  switch (dataType) {
    case 'integer':
      if (!/^-?\d+$/.test(value)) {
        return { valid: false, error: 'El valor debe ser un número entero' };
      }
      return { valid: true };
    
    case 'float':
      if (!/^-?\d+\.?\d*$/.test(value) && !/^-?\d*\.\d+$/.test(value)) {
        return { valid: false, error: 'El valor debe ser un número decimal' };
      }
      return { valid: true };
    
    case 'boolean':
      if (!['true', 'false', '1', '0'].includes(value.toLowerCase())) {
        return { valid: false, error: 'El valor debe ser true o false' };
      }
      return { valid: true };
    
    case 'json':
      try {
        JSON.parse(value);
        return { valid: true };
      } catch (e) {
        return { valid: false, error: 'El valor debe ser JSON válido' };
      }
    
    case 'string':
    default:
      return { valid: true };
  }
}

/**
 * Property 12: Non-editable parameters cannot be modified
 * For any parameter with is_editable=false, the form should prevent editing
 */
describe('Parameter Validation Properties', () => {
  it('Property 12: Non-editable parameters should be blocked from editing', () => {
    fc.assert(
      fc.property(
        fc.record({
          key: fc.string({ minLength: 1, maxLength: 50 }),
          value: fc.string({ minLength: 0, maxLength: 200 }),
          description: fc.string({ minLength: 0, maxLength: 200 }),
          data_type: fc.constantFrom('string', 'integer', 'float', 'boolean', 'json'),
          is_editable: fc.constant(false)
        }),
        (parameter) => {
          // Property: Non-editable parameters should not be editable
          expect(canEditParameter(parameter)).toBe(false);
        }
      ),
      { numRuns: 50 }
    );
  });

  it('Property 12: Editable parameters should allow editing', () => {
    fc.assert(
      fc.property(
        fc.record({
          key: fc.string({ minLength: 1, maxLength: 50 }),
          value: fc.string({ minLength: 0, maxLength: 200 }),
          description: fc.string({ minLength: 0, maxLength: 200 }),
          data_type: fc.constantFrom('string', 'integer', 'float', 'boolean', 'json'),
          is_editable: fc.constant(true)
        }),
        (parameter) => {
          // Property: Editable parameters should be editable
          expect(canEditParameter(parameter)).toBe(true);
        }
      ),
      { numRuns: 50 }
    );
  });

  it('Property 8: Integer type validation', () => {
    fc.assert(
      fc.property(
        fc.integer(),
        (value) => {
          const result = validateParameterValue(value.toString(), 'integer');
          
          // Property: Valid integers should pass validation
          expect(result.valid).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 8: Invalid integer values should fail', () => {
    const invalidIntegers = [
      '12.5',
      '12.0',
      'abc',
      '12a',
      'a12',
      '1.2.3',
      '',
      ' ',
      '1 2',
      '1e5',
      'NaN',
      'Infinity',
    ];

    invalidIntegers.forEach(value => {
      const result = validateParameterValue(value, 'integer');
      expect(result.valid).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  it('Property 8: Float type validation', () => {
    fc.assert(
      fc.property(
        fc.float(),
        (value) => {
          const result = validateParameterValue(value.toString(), 'float');
          
          // Property: Valid floats should pass validation
          expect(result.valid).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 8: Invalid float values should fail', () => {
    const invalidFloats = [
      'abc',
      '12a',
      'a12',
      '1.2.3',
      ' ',
      '1 2',
      'NaN',
      'Infinity',
    ];

    invalidFloats.forEach(value => {
      const result = validateParameterValue(value, 'float');
      expect(result.valid).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  it('Property 8: Boolean type validation', () => {
    const validBooleans = ['true', 'false', 'True', 'False', 'TRUE', 'FALSE', '1', '0'];

    validBooleans.forEach(value => {
      const result = validateParameterValue(value, 'boolean');
      expect(result.valid).toBe(true);
    });
  });

  it('Property 8: Invalid boolean values should fail', () => {
    const invalidBooleans = [
      'yes',
      'no',
      'y',
      'n',
      '2',
      '-1',
      'abc',
      '',
      ' ',
      'truee',
      'falsee',
    ];

    invalidBooleans.forEach(value => {
      const result = validateParameterValue(value, 'boolean');
      expect(result.valid).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  it('Property 8: JSON type validation with valid JSON', () => {
    fc.assert(
      fc.property(
        fc.oneof(
          fc.jsonValue().map(v => JSON.stringify(v)),
          fc.constant('{}'),
          fc.constant('[]'),
          fc.constant('{"key": "value"}'),
          fc.constant('[1, 2, 3]'),
          fc.constant('null'),
          fc.constant('true'),
          fc.constant('false'),
          fc.constant('123'),
          fc.constant('"string"')
        ),
        (jsonString) => {
          const result = validateParameterValue(jsonString, 'json');
          
          // Property: Valid JSON should pass validation
          expect(result.valid).toBe(true);
        }
      ),
      { numRuns: 50 }
    );
  });

  it('Property 8: Invalid JSON values should fail', () => {
    const invalidJson = [
      '{invalid}',
      '{key: value}',
      "{'key': 'value'}",
      '{',
      '}',
      '[',
      ']',
      '{]',
      '[}',
      '{"key": value}',
      "{'key': \"value\"}",
      '',
      'undefined',
      'NaN',
    ];

    invalidJson.forEach(value => {
      const result = validateParameterValue(value, 'json');
      expect(result.valid).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  it('Property 8: String type accepts any value', () => {
    fc.assert(
      fc.property(
        fc.string(),
        (value) => {
          const result = validateParameterValue(value, 'string');
          
          // Property: String type should accept any value
          expect(result.valid).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 8: Type validation error messages are descriptive', () => {
    const testCases = [
      { value: 'abc', type: 'integer', expectedKeyword: 'entero' },
      { value: 'abc', type: 'float', expectedKeyword: 'decimal' },
      { value: 'abc', type: 'boolean', expectedKeyword: 'true' },
      { value: '{invalid}', type: 'json', expectedKeyword: 'JSON' },
    ];

    testCases.forEach(({ value, type, expectedKeyword }) => {
      const result = validateParameterValue(value, type);
      expect(result.valid).toBe(false);
      expect(result.error).toBeDefined();
      expect(result.error?.toLowerCase()).toContain(expectedKeyword.toLowerCase());
    });
  });

  it('Property 12: Specific non-editable parameters', () => {
    const nonEditableParams: SystemParameter[] = [
      {
        key: 'SYSTEM_VERSION',
        value: '1.0.0',
        description: 'System version',
        data_type: 'string',
        is_editable: false
      },
      {
        key: 'MAX_UPLOAD_SIZE',
        value: '10485760',
        description: 'Maximum upload size in bytes',
        data_type: 'integer',
        is_editable: false
      },
      {
        key: 'ENABLE_DEBUG',
        value: 'false',
        description: 'Enable debug mode',
        data_type: 'boolean',
        is_editable: false
      }
    ];

    nonEditableParams.forEach(param => {
      expect(canEditParameter(param)).toBe(false);
    });
  });

  it('Property 12: Specific editable parameters', () => {
    const editableParams: SystemParameter[] = [
      {
        key: 'COMPANY_NAME',
        value: 'My Company',
        description: 'Company name',
        data_type: 'string',
        is_editable: true
      },
      {
        key: 'SESSION_TIMEOUT',
        value: '3600',
        description: 'Session timeout in seconds',
        data_type: 'integer',
        is_editable: true
      },
      {
        key: 'ENABLE_NOTIFICATIONS',
        value: 'true',
        description: 'Enable notifications',
        data_type: 'boolean',
        is_editable: true
      }
    ];

    editableParams.forEach(param => {
      expect(canEditParameter(param)).toBe(true);
    });
  });
});
