/**
 * Authentication types
 */

export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: string;
  role_name: string;
  role_display: string;
  is_active: boolean;
  must_change_password: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    role_name?: string;
    role_display: string;
    must_change_password: boolean;
  };
}

export interface TokenRefreshResponse {
  access: string;
  refresh?: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export type UserRole = 'ADMIN' | 'SUPERVISOR' | 'OPERADOR';
