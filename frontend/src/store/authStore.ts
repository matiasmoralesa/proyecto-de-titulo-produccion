/**
 * Authentication store using Zustand
 */
import { create } from 'zustand';
import authService from '../services/authService';
import { User, LoginCredentials, ChangePasswordData } from '../types/auth.types';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isInitialized: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  changePassword: (data: ChangePasswordData) => Promise<void>;
  loadUserFromStorage: () => void;
  clearError: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  isInitialized: false,
  error: null,

  /**
   * Login user
   */
  login: async (credentials: LoginCredentials) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login(credentials);
      authService.storeAuthData(response);
      
      set({
        user: response.user as unknown as User,
        accessToken: response.access,
        refreshToken: response.refresh,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Error al iniciar sesión';
      set({
        error: errorMessage,
        isLoading: false,
        isAuthenticated: false,
      });
      throw error;
    }
  },

  /**
   * Logout user
   */
  logout: async () => {
    const { refreshToken } = get();
    if (refreshToken) {
      await authService.logout(refreshToken);
    }
    authService.clearAuthData();
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      error: null,
    });
  },

  /**
   * Change password
   */
  changePassword: async (data: ChangePasswordData) => {
    set({ isLoading: true, error: null });
    try {
      await authService.changePassword(data);
      
      // Update user's must_change_password flag
      const { user } = get();
      if (user) {
        const updatedUser = { ...user, must_change_password: false };
        set({ user: updatedUser, isLoading: false });
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Error al cambiar contraseña';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  /**
   * Load user from localStorage
   */
  loadUserFromStorage: () => {
    const user = authService.getStoredUser();
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    if (user && accessToken && refreshToken) {
      set({
        user,
        accessToken,
        refreshToken,
        isAuthenticated: true,
        isInitialized: true,
      });
    } else {
      set({
        isInitialized: true,
      });
    }
  },

  /**
   * Refresh user data from API
   */
  refreshUser: async () => {
    try {
      const user = await authService.getCurrentUser();
      set({ user });
      localStorage.setItem('user', JSON.stringify(user));
    } catch (error) {
      console.error('Error refreshing user:', error);
    }
  },

  /**
   * Clear error
   */
  clearError: () => {
    set({ error: null });
  },
}));
