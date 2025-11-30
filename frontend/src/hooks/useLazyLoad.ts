/**
 * Hook for lazy loading components
 */
import { lazy, ComponentType } from 'react';

export function useLazyLoad<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>
) {
  return lazy(importFunc);
}

// Preload function for critical routes
export function preloadComponent<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>
) {
  return importFunc();
}
