import api from './api';

export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: number;
  role_name: string;
  role_display: string;
  is_active: boolean;
  must_change_password: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateUserData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: number;
}

export interface UpdateUserData {
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  role?: number;
  is_active?: boolean;
}

export interface ResetPasswordData {
  new_password: string;
  new_password_confirm: string;
}

export interface UserFilters {
  role?: string;
  is_active?: boolean;
  search?: string;
}

const userManagementService = {
  // Get all users with optional filters
  getUsers: async (filters?: UserFilters) => {
    const params = new URLSearchParams();
    if (filters?.role) params.append('role', filters.role);
    if (filters?.is_active !== undefined) params.append('is_active', String(filters.is_active));
    if (filters?.search) params.append('search', filters.search);
    
    const response = await api.get(`/auth/user-management/?${params.toString()}`);
    return response.data;
  },

  // Get single user by ID
  getUser: async (id: string) => {
    const response = await api.get(`/auth/user-management/${id}/`);
    return response.data;
  },

  // Create new user
  createUser: async (data: CreateUserData) => {
    const response = await api.post('/auth/user-management/', data);
    return response.data;
  },

  // Update user
  updateUser: async (id: string, data: UpdateUserData) => {
    const response = await api.patch(`/auth/user-management/${id}/`, data);
    return response.data;
  },

  // Delete user (soft delete)
  deleteUser: async (id: string) => {
    const response = await api.delete(`/auth/user-management/${id}/`);
    return response.data;
  },

  // Activate user
  activateUser: async (id: string) => {
    const response = await api.post(`/auth/user-management/${id}/activate/`);
    return response.data;
  },

  // Deactivate user
  deactivateUser: async (id: string) => {
    const response = await api.post(`/auth/user-management/${id}/deactivate/`);
    return response.data;
  },

  // Reset user password
  resetPassword: async (id: string, data: ResetPasswordData) => {
    const response = await api.post(`/auth/user-management/${id}/reset_password/`, data);
    return response.data;
  },
};

export default userManagementService;
