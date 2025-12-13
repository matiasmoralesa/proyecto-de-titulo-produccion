/**
 * Tests for authStore
 */
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useAuthStore } from '../authStore';
import { authService } from '../../services/authService';

// Mock authService
vi.mock('../../services/authService');
const mockedAuthService = authService as any;

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('authStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset store state
    useAuthStore.setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      isInitialized: false,
      error: null,
    });
  });

  describe('login', () => {
    it('should login successfully', async () => {
      const mockUser = {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
        role: { name: 'ADMIN' },
      };
      const mockResponse = {
        access: 'access-token',
        refresh: 'refresh-token',
        user: mockUser,
      };

      mockedAuthService.login.mockResolvedValueOnce(mockResponse);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.login({ username: 'testuser', password: 'password' });
      });

      expect(result.current.user).toEqual(mockUser);
      expect(result.current.accessToken).toBe('access-token');
      expect(result.current.refreshToken).toBe('refresh-token');
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.error).toBeNull();
    });

    it('should handle login error', async () => {
      const mockError = new Error('Invalid credentials');
      mockedAuthService.login.mockRejectedValueOnce(mockError);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.login({ username: 'testuser', password: 'wrong' });
      });

      expect(result.current.user).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.error).toBe('Invalid credentials');
    });
  });

  describe('logout', () => {
    it('should logout successfully', async () => {
      mockedAuthService.logout.mockResolvedValueOnce(undefined);

      const { result } = renderHook(() => useAuthStore());

      // Set initial authenticated state
      act(() => {
        useAuthStore.setState({
          user: { id: '1', username: 'testuser', email: 'test@example.com' },
          accessToken: 'token',
          refreshToken: 'refresh',
          isAuthenticated: true,
        });
      });

      await act(async () => {
        await result.current.logout();
      });

      expect(result.current.user).toBeNull();
      expect(result.current.accessToken).toBeNull();
      expect(result.current.refreshToken).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
    });
  });

  describe('loadUserFromStorage', () => {
    it('should load user from storage', async () => {
      const mockUser = {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
      };

      mockedAuthService.getStoredUser.mockReturnValue(mockUser);
      mockedAuthService.getCurrentUser.mockResolvedValueOnce(mockUser);
      localStorageMock.getItem.mockImplementation((key) => {
        if (key === 'accessToken') return 'access-token';
        if (key === 'refreshToken') return 'refresh-token';
        return null;
      });

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.loadUserFromStorage();
      });

      expect(result.current.user).toEqual(mockUser);
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.isInitialized).toBe(true);
    });

    it('should handle no stored user', async () => {
      mockedAuthService.getStoredUser.mockReturnValue(null);
      localStorageMock.getItem.mockReturnValue(null);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.loadUserFromStorage();
      });

      expect(result.current.user).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.isInitialized).toBe(true);
    });
  });

  describe('clearError', () => {
    it('should clear error', () => {
      const { result } = renderHook(() => useAuthStore());

      act(() => {
        useAuthStore.setState({ error: 'Some error' });
      });

      expect(result.current.error).toBe('Some error');

      act(() => {
        result.current.clearError();
      });

      expect(result.current.error).toBeNull();
    });
  });
});
