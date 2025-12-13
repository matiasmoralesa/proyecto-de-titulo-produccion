/**
 * PermissionGuard Component
 * 
 * Conditionally renders children based on user role permissions.
 * Validates: Requirements 10.1, 10.2, 10.3
 */
import React from 'react';
import { useAuth } from '../../hooks/useAuth';

interface PermissionGuardProps {
  /** Array of roles that are allowed to see the content */
  roles: string[];
  /** Content to render if user has permission */
  children: React.ReactNode;
  /** Optional message to show if user doesn't have permission */
  fallback?: React.ReactNode;
  /** If true, renders nothing instead of fallback when no permission */
  hideOnNoPermission?: boolean;
}

/**
 * PermissionGuard component that shows/hides content based on user role.
 * 
 * @example
 * ```tsx
 * <PermissionGuard roles={['ADMIN', 'SUPERVISOR']}>
 *   <AdminPanel />
 * </PermissionGuard>
 * ```
 */
export const PermissionGuard: React.FC<PermissionGuardProps> = ({
  roles,
  children,
  fallback,
  hideOnNoPermission = false,
}) => {
  const { user } = useAuth();

  // Check if user is authenticated
  if (!user) {
    return hideOnNoPermission ? null : (
      fallback || <div className="text-gray-500">Debe iniciar sesión para ver este contenido.</div>
    );
  }

  // Check if user has required role
  const hasPermission = roles.includes(user.role?.name || '');

  if (!hasPermission) {
    if (hideOnNoPermission) {
      return null;
    }

    return (
      fallback || (
        <div className="text-gray-500">
          No tiene permisos para ver este contenido.
        </div>
      )
    );
  }

  return <>{children}</>;
};

/**
 * Hook to check if user has specific role(s)
 */
export const useHasRole = (roles: string | string[]): boolean => {
  const { user } = useAuth();

  if (!user || !user.role) {
    return false;
  }

  const roleArray = Array.isArray(roles) ? roles : [roles];
  return roleArray.includes(user.role.name);
};

/**
 * Hook to check if user is admin
 */
export const useIsAdmin = (): boolean => {
  return useHasRole('ADMIN');
};

/**
 * Hook to check if user is supervisor or above
 */
export const useIsSupervisorOrAbove = (): boolean => {
  return useHasRole(['ADMIN', 'SUPERVISOR']);
};

/**
 * Hook to check if user is operator or above (any authenticated user)
 */
export const useIsOperadorOrAbove = (): boolean => {
  return useHasRole(['ADMIN', 'SUPERVISOR', 'OPERADOR']);
};
