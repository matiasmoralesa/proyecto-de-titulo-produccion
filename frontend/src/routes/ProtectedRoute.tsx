/**
 * ProtectedRoute Component
 * 
 * Route wrapper that redirects to 403 page if user doesn't have required role.
 * Validates: Requirements 10.1, 10.2, 10.3
 */
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  /** Required role to access this route */
  requiredRole?: string | string[];
  /** Redirect path if no permission (default: /403) */
  redirectTo?: string;
  /** Optional children (if not using Outlet) */
  children?: React.ReactNode;
}

/**
 * ProtectedRoute component that redirects if user doesn't have required role.
 * 
 * @example
 * ```tsx
 * <Route element={<ProtectedRoute requiredRole="ADMIN" />}>
 *   <Route path="/users" element={<UsersPage />} />
 * </Route>
 * ```
 */
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  requiredRole,
  redirectTo = '/403',
  children,
}) => {
  const { user, isAuthenticated, isLoading } = useAuth();

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // If no role required, just check authentication
  if (!requiredRole) {
    return children ? <>{children}</> : <Outlet />;
  }

  // Check if user has required role
  const roleArray = Array.isArray(requiredRole) ? requiredRole : [requiredRole];
  const hasPermission = user.role && roleArray.includes(user.role.name);

  if (!hasPermission) {
    return <Navigate to={redirectTo} replace />;
  }

  return children ? <>{children}</> : <Outlet />;
};

/**
 * AdminRoute - Shortcut for admin-only routes
 */
export const AdminRoute: React.FC<Omit<ProtectedRouteProps, 'requiredRole'>> = (props) => {
  return <ProtectedRoute {...props} requiredRole="ADMIN" />;
};

/**
 * SupervisorRoute - Shortcut for supervisor and admin routes
 */
export const SupervisorRoute: React.FC<Omit<ProtectedRouteProps, 'requiredRole'>> = (props) => {
  return <ProtectedRoute {...props} requiredRole={['ADMIN', 'SUPERVISOR']} />;
};
