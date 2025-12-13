/**
 * Utility functions for formatting values
 */

/**
 * Format currency in Chilean Pesos (CLP)
 */
export const formatCurrency = (value: number | string): string => {
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return '$0';
  }
  
  return `$${numValue.toLocaleString('es-CL', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })}`;
};

/**
 * Format date in Chilean format
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-CL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format datetime in Chilean format
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('es-CL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format number with thousands separator
 */
export const formatNumber = (value: number | string): string => {
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return '0';
  }
  
  return numValue.toLocaleString('es-CL');
};
