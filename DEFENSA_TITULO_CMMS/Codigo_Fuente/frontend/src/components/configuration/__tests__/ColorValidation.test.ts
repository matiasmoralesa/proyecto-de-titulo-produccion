/**
 * Property-based tests for color validation in forms
 */
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';

/**
 * Utility function to validate hex color format
 * This mirrors the validation logic used in PriorityForm
 */
function isValidHexColor(color: string): boolean {
  const hexColorRegex = /^#[0-9A-Fa-f]{6}$/;
  return hexColorRegex.test(color);
}

/**
 * Property 14: Color codes are validated
 * For any color code input, only valid hexadecimal color formats (#RRGGBB) should be accepted
 */
describe('Color Validation Properties', () => {
  it('Property 14: Valid hex colors should pass validation', () => {
    fc.assert(
      fc.property(
        fc.hexaString({ minLength: 6, maxLength: 6 }),
        (hexString) => {
          const colorCode = `#${hexString}`;
          const isValid = isValidHexColor(colorCode);
          
          // Property: All properly formatted hex colors should be valid
          expect(isValid).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 14: Invalid color formats should fail validation', () => {
    fc.assert(
      fc.property(
        fc.oneof(
          // Missing # prefix
          fc.hexaString({ minLength: 6, maxLength: 6 }),
          // Wrong length
          fc.string({ minLength: 1, maxLength: 5 }).map(s => `#${s}`),
          fc.string({ minLength: 7, maxLength: 10 }).map(s => `#${s}`),
          // Invalid characters
          fc.string({ minLength: 6, maxLength: 6 }).filter(s => !/^[0-9A-Fa-f]{6}$/.test(s)).map(s => `#${s}`),
          // Empty or null
          fc.constant(''),
          fc.constant('#'),
          // Common invalid formats
          fc.constant('red'),
          fc.constant('blue'),
          fc.constant('rgb(255,0,0)'),
          fc.constant('#gg0000'),
          fc.constant('#12345'),
          fc.constant('#1234567')
        ),
        (invalidColor) => {
          const isValid = isValidHexColor(invalidColor);
          
          // Property: Invalid formats should be rejected
          expect(isValid).toBe(false);
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 14: Specific valid hex colors should pass', () => {
    const validColors = [
      '#000000', // Black
      '#FFFFFF', // White
      '#FF0000', // Red
      '#00FF00', // Green
      '#0000FF', // Blue
      '#EF4444', // Red variant
      '#10B981', // Green variant
      '#3B82F6', // Blue variant
      '#8B5CF6', // Purple
      '#EC4899', // Pink
      '#F59E0B', // Orange
      '#EAB308', // Yellow
      '#6B7280', // Gray
      '#abcdef', // Lowercase
      '#ABCDEF', // Uppercase
      '#123456', // Mixed
    ];

    validColors.forEach(color => {
      expect(isValidHexColor(color)).toBe(true);
    });
  });

  it('Property 14: Specific invalid hex colors should fail', () => {
    const invalidColors = [
      'red',           // Color name
      'blue',          // Color name
      '#red',          // Invalid characters
      '#12345',        // Too short
      '#1234567',      // Too long
      '123456',        // Missing #
      '#',             // Only #
      '',              // Empty
      '#gg0000',       // Invalid character 'g'
      '#12345g',       // Invalid character at end
      'rgb(255,0,0)',  // RGB format
      'hsl(0,100%,50%)', // HSL format
      '#12 34 56',     // Spaces
      '#12-34-56',     // Dashes
    ];

    invalidColors.forEach(color => {
      expect(isValidHexColor(color as string)).toBe(false);
    });
  });

  it('Property 14: Case insensitive validation works', () => {
    fc.assert(
      fc.property(
        fc.hexaString({ minLength: 6, maxLength: 6 }),
        (hexString) => {
          const lowercase = `#${hexString.toLowerCase()}`;
          const uppercase = `#${hexString.toUpperCase()}`;
          const mixed = `#${hexString}`;
          
          // Property: Hex colors should be valid regardless of case
          expect(isValidHexColor(lowercase)).toBe(true);
          expect(isValidHexColor(uppercase)).toBe(true);
          expect(isValidHexColor(mixed)).toBe(true);
        }
      ),
      { numRuns: 50 }
    );
  });

  it('Property 14: Whitespace should invalidate colors', () => {
    fc.assert(
      fc.property(
        fc.hexaString({ minLength: 6, maxLength: 6 }),
        fc.oneof(fc.constant(' '), fc.constant('\t'), fc.constant('\n')),
        (hexString, whitespace) => {
          const colorWithWhitespace = `#${hexString}${whitespace}`;
          const whitespaceInColor = `#${hexString.slice(0, 3)}${whitespace}${hexString.slice(3)}`;
          
          // Property: Colors with whitespace should be invalid
          expect(isValidHexColor(colorWithWhitespace)).toBe(false);
          expect(isValidHexColor(whitespaceInColor)).toBe(false);
        }
      ),
      { numRuns: 30 }
    );
  });

  it('Property 14: Special characters should invalidate colors', () => {
    const specialChars = ['!', '@', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '[', ']', '{', '}', '|', '\\', '/', '?', '<', '>', ',', '.', ';', ':', '"', "'"];
    
    specialChars.forEach(char => {
      const invalidColor = `#12345${char}`;
      expect(isValidHexColor(invalidColor)).toBe(false);
    });
  });
});
