/**
 * Authentication service
 */
import api from './api';
import {
  LoginCredentials,
  LoginResponse,
  TokenRefreshResponse,
  User,
  ChangePasswordData,
} from '../types/auth.types';

class AuthService {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login/', credentials);
    return response.data;
  }

  /**
   * Logout user
   */
  async logout(refreshToken: string): Promise<void> {
    try {
      await api.post('/auth/logout/', { refresh_token: refreshToken });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(refreshToken: string): Promise<TokenRefreshResponse> {
    const response = await api.post<TokenRefreshResponse>('/auth/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  }

  /**
   * Get current user data
   */
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me/');
    return response.data;
  }

  /**
   * Change password
   */
  async changePassword(data: ChangePasswordData): Promise<void> {
    await api.post('/auth/change-password/', data);
  }

  /**
   * Verify token
   */
  async verifyToken(token: string): Promise<boolean> {
    try {
      const response = await api.post('/auth/verify/', { token });
      return response.data.valid;
    } catch (error) {
      return false;
    }
  }

  /**
   * Store auth data in localStorage
   */
  storeAuthData(data: LoginResponse): void {
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  /**
   * Clear auth data from localStorage
   */
  clearAuthData(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  }

  /**
   * Get stored user data
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch (error) {
        return null;
      }
    }
    return null;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('accessToken');
  }
}

export default new AuthService();
