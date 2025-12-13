/**
 * Tests for ProtectedRoute component
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../auth/ProtectedRoute';
import { useAuthStore } from '../../store/authStore';

// Mock the auth store
vi.mock('../../store/authStore', () => ({
  useAuthStore: vi.fn(),
}));

const TestComponent = () => <div>Protected Content</div>;

const renderProtectedRoute = (allowedRoles?: string[]) => {
  return render(
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<div>Login Page</div>} />
        <Route
          path="/protected"
          element={
            <ProtectedRoute allowedRoles={allowedRoles}>
              <TestComponent />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

describe('ProtectedRoute', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render children when user is authenticated', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: true,
      isInitialized: true,
      user: { id: '1', username: 'testuser', email: 'test@example.com', role: { name: 'ADMIN' } },
      accessToken: 'token',
      refreshToken: 'refresh',
      isLoading: false,
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      clearError: vi.fn(),
      changePassword: vi.fn(),
      loadUserFromStorage: vi.fn(),
      refreshUser: vi.fn(),
    });

    renderProtectedRoute();
    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('should show loading when not initialized', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: false,
      isInitialized: false,
      user: null,
      accessToken: null,
      refreshToken: null,
      isLoading: false,
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      clearError: vi.fn(),
      changePassword: vi.fn(),
      loadUserFromStorage: vi.fn(),
      refreshUser: vi.fn(),
    });

    renderProtectedRoute();
    expect(screen.getByText(/cargando/i)).toBeInTheDocument();
  });

  it('should render children when user has allowed role', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: true,
      isInitialized: true,
      user: { id: '1', username: 'testuser', email: 'test@example.com', role: { name: 'ADMIN' } },
      accessToken: 'token',
      refreshToken: 'refresh',
      isLoading: false,
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      clearError: vi.fn(),
      changePassword: vi.fn(),
      loadUserFromStorage: vi.fn(),
      refreshUser: vi.fn(),
    });

    renderProtectedRoute(['ADMIN', 'SUPERVISOR']);
    expect(screen.getByText('Protected Content')).toBeInTheDocument();
  });

  it('should show access denied when user does not have allowed role', () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: true,
      isInitialized: true,
      user: { id: '1', username: 'testuser', email: 'test@example.com', role: { name: 'OPERADOR' } },
      accessToken: 'token',
      refreshToken: 'refresh',
      isLoading: false,
      error: null,
      login: vi.fn(),
      logout: vi.fn(),
      clearError: vi.fn(),
      changePassword: vi.fn(),
      loadUserFromStorage: vi.fn(),
      refreshUser: vi.fn(),
    });

    renderProtectedRoute(['ADMIN']);
    expect(screen.getByText(/acceso denegado/i)).toBeInTheDocument();
  });
});
