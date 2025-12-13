/**
 * Property-based tests for required field validation
 */
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';

/**
 * Form data types
 */
interface CategoryFormData {
  code: string;
  name: string;
  description?: string;
  is_active: boolean;
}

interface PriorityFormData {
  level: number;
  name: string;
  color_code: string;
  description?: string;
  is_active: boolean;
}

interface WorkOrderTypeFormData {
  code: string;
  name: string;
  description?: string;
  requires_approval: boolean;
  is_active: boolean;
}

/**
 * Validation functions
 */
function validateCategoryForm(data: Partial<CategoryFormData>): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (!data.code || data.code.trim() === '') {
    errors.push('El código es requerido');
  }
  
  if (!data.name || data.name.trim() === '') {
    errors.push('El nombre es requerido');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

function validatePriorityForm(data: Partial<PriorityFormData>): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (data.level === undefined || data.level === null) {
    errors.push('El nivel es requerido');
  }
  
  if (!data.name || data.name.trim() === '') {
    errors.push('El nombre es requerido');
  }
  
  if (!data.color_code || data.color_code.trim() === '') {
    errors.push('El código de color es requerido');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

function validateWorkOrderTypeForm(data: Partial<WorkOrderTypeFormData>): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (!data.code || data.code.trim() === '') {
    errors.push('El código es requerido');
  }
  
  if (!data.name || data.name.trim() === '') {
    errors.push('El nombre es requerido');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Property 13: Required fields block submission
 * For any form with required fields, submission should be blocked if required fields are empty
 */
describe('Required Field Validation Properties', () => {
  describe('Category Form', () => {
    it('Property 13: Valid category data should pass validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.string({ minLength: 1, maxLength: 20 }).filter(s => s.trim().length > 0),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateCategoryForm(data);
            
            // Property: Valid data should pass validation
            expect(result.valid).toBe(true);
            expect(result.errors).toHaveLength(0);
          }
        ),
        { numRuns: 50 }
      );
    });

    it('Property 13: Missing code should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.constantFrom('', '   ', '\t', '\n'),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateCategoryForm(data);
            
            // Property: Missing code should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('código'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing name should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.string({ minLength: 1, maxLength: 20 }).filter(s => s.trim().length > 0),
            name: fc.constantFrom('', '   ', '\t', '\n'),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateCategoryForm(data);
            
            // Property: Missing name should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing both code and name should fail with multiple errors', () => {
      const result = validateCategoryForm({
        code: '',
        name: '',
        is_active: true
      });
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThanOrEqual(2);
      expect(result.errors.some(e => e.toLowerCase().includes('código'))).toBe(true);
      expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
    });
  });

  describe('Priority Form', () => {
    it('Property 13: Valid priority data should pass validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            level: fc.integer({ min: 1, max: 10 }),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            color_code: fc.hexaString({ minLength: 6, maxLength: 6 }).map(s => `#${s}`),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validatePriorityForm(data);
            
            // Property: Valid data should pass validation
            expect(result.valid).toBe(true);
            expect(result.errors).toHaveLength(0);
          }
        ),
        { numRuns: 50 }
      );
    });

    it('Property 13: Missing level should fail validation', () => {
      const result = validatePriorityForm({
        level: undefined,
        name: 'Test Priority',
        color_code: '#FF0000',
        is_active: true
      });
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.toLowerCase().includes('nivel'))).toBe(true);
    });

    it('Property 13: Missing name should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            level: fc.integer({ min: 1, max: 10 }),
            name: fc.constantFrom('', '   ', '\t', '\n'),
            color_code: fc.hexaString({ minLength: 6, maxLength: 6 }).map(s => `#${s}`),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validatePriorityForm(data);
            
            // Property: Missing name should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing color code should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            level: fc.integer({ min: 1, max: 10 }),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            color_code: fc.constantFrom('', '   ', '\t', '\n'),
            description: fc.string({ maxLength: 200 }),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validatePriorityForm(data);
            
            // Property: Missing color code should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('color'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing all required fields should fail with multiple errors', () => {
      const result = validatePriorityForm({
        level: undefined,
        name: '',
        color_code: '',
        is_active: true
      });
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThanOrEqual(3);
      expect(result.errors.some(e => e.toLowerCase().includes('nivel'))).toBe(true);
      expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
      expect(result.errors.some(e => e.toLowerCase().includes('color'))).toBe(true);
    });
  });

  describe('Work Order Type Form', () => {
    it('Property 13: Valid work order type data should pass validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.string({ minLength: 1, maxLength: 20 }).filter(s => s.trim().length > 0),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            description: fc.string({ maxLength: 200 }),
            requires_approval: fc.boolean(),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateWorkOrderTypeForm(data);
            
            // Property: Valid data should pass validation
            expect(result.valid).toBe(true);
            expect(result.errors).toHaveLength(0);
          }
        ),
        { numRuns: 50 }
      );
    });

    it('Property 13: Missing code should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.constantFrom('', '   ', '\t', '\n'),
            name: fc.string({ minLength: 1, maxLength: 50 }).filter(s => s.trim().length > 0),
            description: fc.string({ maxLength: 200 }),
            requires_approval: fc.boolean(),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateWorkOrderTypeForm(data);
            
            // Property: Missing code should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('código'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing name should fail validation', () => {
      fc.assert(
        fc.property(
          fc.record({
            code: fc.string({ minLength: 1, maxLength: 20 }).filter(s => s.trim().length > 0),
            name: fc.constantFrom('', '   ', '\t', '\n'),
            description: fc.string({ maxLength: 200 }),
            requires_approval: fc.boolean(),
            is_active: fc.boolean()
          }),
          (data) => {
            const result = validateWorkOrderTypeForm(data);
            
            // Property: Missing name should fail validation
            expect(result.valid).toBe(false);
            expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
          }
        ),
        { numRuns: 20 }
      );
    });

    it('Property 13: Missing both code and name should fail with multiple errors', () => {
      const result = validateWorkOrderTypeForm({
        code: '',
        name: '',
        requires_approval: false,
        is_active: true
      });
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThanOrEqual(2);
      expect(result.errors.some(e => e.toLowerCase().includes('código'))).toBe(true);
      expect(result.errors.some(e => e.toLowerCase().includes('nombre'))).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    it('Property 13: Whitespace-only values should be treated as empty', () => {
      const whitespaceValues = ['', ' ', '  ', '\t', '\n', '\r', '   \t\n   '];
      
      whitespaceValues.forEach(value => {
        const categoryResult = validateCategoryForm({ code: value, name: 'Test' });
        expect(categoryResult.valid).toBe(false);
        
        const workOrderTypeResult = validateWorkOrderTypeForm({ code: value, name: 'Test' });
        expect(workOrderTypeResult.valid).toBe(false);
      });
    });

    it('Property 13: Optional fields should not block submission', () => {
      // Category with no description
      const categoryResult = validateCategoryForm({
        code: 'TEST',
        name: 'Test Category',
        is_active: true
      });
      expect(categoryResult.valid).toBe(true);
      
      // Priority with no description
      const priorityResult = validatePriorityForm({
        level: 1,
        name: 'Test Priority',
        color_code: '#FF0000',
        is_active: true
      });
      expect(priorityResult.valid).toBe(true);
      
      // Work Order Type with no description
      const workOrderTypeResult = validateWorkOrderTypeForm({
        code: 'TEST',
        name: 'Test Type',
        requires_approval: false,
        is_active: true
      });
      expect(workOrderTypeResult.valid).toBe(true);
    });

    it('Property 13: Zero should be valid for numeric fields', () => {
      const result = validatePriorityForm({
        level: 0,
        name: 'Test Priority',
        color_code: '#FF0000',
        is_active: true
      });
      
      // Level 0 should be valid (it's a number, not undefined/null)
      expect(result.valid).toBe(true);
    });
  });
});
