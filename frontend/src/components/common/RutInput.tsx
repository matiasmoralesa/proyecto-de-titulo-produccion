/**
 * RUT Input Component
 * Provides automatic formatting and validation for Chilean RUT
 */
import React, { useState, useEffect } from 'react';
import { formatRut, validateRutWithMessage, cleanRut } from '../../utils/rutValidator';

interface RutInputProps {
  value: string;
  onChange: (value: string) => void;
  onValidationChange?: (isValid: boolean) => void;
  name?: string;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  error?: string;
}

export default function RutInput({
  value,
  onChange,
  onValidationChange,
  name = 'rut',
  placeholder = 'Ej: 12.345.678-9',
  required = false,
  disabled = false,
  className = '',
  error,
}: RutInputProps) {
  const [displayValue, setDisplayValue] = useState('');
  const [validationError, setValidationError] = useState<string>('');

  // Update display value when prop value changes
  useEffect(() => {
    if (value) {
      setDisplayValue(formatRut(value));
    } else {
      setDisplayValue('');
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    
    // Allow only numbers, dots, hyphens, and K
    const sanitized = inputValue.replace(/[^0-9.\-kK]/g, '');
    
    // Format the RUT as user types
    const formatted = formatRut(sanitized);
    setDisplayValue(formatted);
    
    // Clean the RUT for validation and storage
    const cleaned = cleanRut(sanitized);
    
    // Validate RUT
    let isValid = true;
    let errorMessage = '';
    
    if (cleaned) {
      const validation = validateRutWithMessage(cleaned);
      isValid = validation.isValid;
      errorMessage = validation.message || '';
    } else if (required) {
      isValid = false;
      errorMessage = 'El RUT es requerido';
    }
    
    setValidationError(errorMessage);
    
    // Notify parent components
    onChange(cleaned);
    if (onValidationChange) {
      onValidationChange(isValid);
    }
  };

  const handleBlur = () => {
    // Final validation on blur
    if (value) {
      const validation = validateRutWithMessage(value);
      setValidationError(validation.message || '');
      if (onValidationChange) {
        onValidationChange(validation.isValid);
      }
    }
  };

  const inputClassName = `
    w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent 
    dark:bg-gray-700 dark:text-white dark:border-gray-600
    ${error || validationError ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'}
    ${disabled ? 'bg-gray-100 dark:bg-gray-600 cursor-not-allowed' : ''}
    ${className}
  `.trim();

  const displayError = error || validationError;

  return (
    <div>
      <input
        type="text"
        name={name}
        value={displayValue}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        className={inputClassName}
        maxLength={12} // Max length for formatted RUT (XX.XXX.XXX-X)
      />
      {displayError && (
        <p className="text-red-500 dark:text-red-400 text-sm mt-1">{displayError}</p>
      )}
    </div>
  );
}