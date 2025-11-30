/**
 * Tests for authService
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import authService from '../authService';
import api from '../api';

// Mock the api module
vi.mock('../api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.clear();
  });

  describe('login', () => {
    it('should login successfully and store tokens', async () => {
      const mockResponse = {
        data: {
          access: 'access-token',
          refresh: 'refresh-token',
          user: {
            id: '1',
            username: 'testuser',
            email: 'test@example.com',
            role: { name: 'ADMIN' },
          },
        },
      };

      vi.mocked(api.post).mockResolvedValueOnce(mockResponse);

      const result = await authService.login({
        username: 'testuser',
        password: 'password',
      });

      expect(api.post).toHaveBeenCalledWith('/auth/login/', {
        username: 'testuser',
        password: 'password',
      });
      expect(localStorageMock.getItem('accessToken')).toBe('access-token');
      expect(localStorageMock.getItem('refreshToken')).toBe('refresh-token');
      expect(result).toEqual(mockResponse.data);
    });

    it('should throw error on login failure', async () => {
      const mockError = new Error('Invalid credentials');
      vi.mocked(api.post).mockRejectedValueOnce(mockError);

      await expect(
        authService.login({ username: 'testuser', password: 'wrongpassword' })
      ).rejects.toThrow('Invalid credentials');
    });
  });

  describe('logout', () => {
    it('should logout and clear tokens', async () => {
      localStorageMock.setItem('accessToken', 'access-token');
      localStorageMock.setItem('refreshToken', 'refresh-token');
      localStorageMock.setItem('user', JSON.stringify({ id: '1' }));

      vi.mocked(api.post).mockResolvedValueOnce({ data: {} });

      await authService.logout();

      expect(api.post).toHaveBeenCalledWith('/auth/logout/', {
        refresh: 'refresh-token',
      });
      expect(localStorageMock.getItem('accessToken')).toBeNull();
      expect(localStorageMock.getItem('refreshToken')).toBeNull();
      expect(localStorageMock.getItem('user')).toBeNull();
    });
  });

  describe('getStoredUser', () => {
    it('should return stored user', () => {
      const mockUser = {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
      };
      localStorageMock.setItem('user', JSON.stringify(mockUser));

      const result = authService.getStoredUser();

      expect(result).toEqual(mockUser);
    });

    it('should return null if no user stored', () => {
      const result = authService.getStoredUser();

      expect(result).toBeNull();
    });

    it('should return null if stored user is invalid JSON', () => {
      localStorageMock.setItem('user', 'invalid-json');

      const result = authService.getStoredUser();

      expect(result).toBeNull();
    });
  });

  describe('getCurrentUser', () => {
    it('should get current user from API', async () => {
      const mockUser = {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
      };
      vi.mocked(api.get).mockResolvedValueOnce({ data: mockUser });

      const result = await authService.getCurrentUser();

      expect(api.get).toHaveBeenCalledWith('/auth/me/');
      expect(result).toEqual(mockUser);
    });
  });
});
