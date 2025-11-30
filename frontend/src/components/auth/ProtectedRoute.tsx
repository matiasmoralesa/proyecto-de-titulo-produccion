/**
 * Protected route component
 */
import { useState, useEffect } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { UserRole } from '../../types/auth.types';
import FirstLoginPasswordChange from './FirstLoginPasswordChange';

interface ProtectedRouteProps {
  allowedRoles?: UserRole[];
  children?: React.ReactNode;
}

export default function ProtectedRoute({ allowedRoles, children }: ProtectedRouteProps) {
  const { isAuthenticated, user, isInitialized, loadUserFromStorage } = useAuthStore();
  const [showPasswordChange, setShowPasswordChange] = useState(false);

  useEffect(() => {
    // Check if user must change password
    if (user && user.must_change_password) {
      setShowPasswordChange(true);
    }
  }, [user]);

  // Wait for initialization
  if (!isInitialized) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // Not authenticated - redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check role-based access
  if (allowedRoles && user) {
    const hasRequiredRole = allowedRoles.includes(user.role as UserRole);
    if (!hasRequiredRole) {
      return <Navigate to="/unauthorized" replace />;
    }
  }

  // Show password change modal if required
  if (showPasswordChange) {
    return (
      <FirstLoginPasswordChange
        onSuccess={() => {
          setShowPasswordChange(false);
          // Reload user data to update must_change_password flag
          loadUserFromStorage();
        }}
      />
    );
  }

  // Render children or outlet
  return children ? <>{children}</> : <Outlet />;
}
