/**
 * Maintenance service for API calls
 */
import api from './api';
import { MaintenancePlan, MaintenancePlanDetail, MaintenancePlanFormData } from '../types/maintenance.types';

export const maintenanceService = {
  /**
   * Get all maintenance plans with optional filters
   */
  async getAll(params?: {
    status?: string;
    recurrence_type?: string;
    asset?: string;
    assigned_to?: string;
    is_paused?: boolean;
    search?: string;
  }): Promise<{ results: MaintenancePlan[]; count: number }> {
    const response = await api.get('/maintenance/plans/', { params });
    return response.data;
  },

  /**
   * Get a single maintenance plan by ID
   */
  async getById(id: string): Promise<MaintenancePlanDetail> {
    const response = await api.get(`/maintenance/plans/${id}/`);
    return response.data;
  },

  /**
   * Create a new maintenance plan
   */
  async create(data: MaintenancePlanFormData): Promise<MaintenancePlan> {
    const response = await api.post('/maintenance/plans/', data);
    return response.data;
  },

  /**
   * Update an existing maintenance plan
   */
  async update(id: string, data: Partial<MaintenancePlanFormData>): Promise<MaintenancePlan> {
    const response = await api.patch(`/maintenance/plans/${id}/`, data);
    return response.data;
  },

  /**
   * Delete a maintenance plan
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/maintenance/plans/${id}/`);
  },

  /**
   * Pause a maintenance plan
   */
  async pause(id: string): Promise<MaintenancePlanDetail> {
    const response = await api.post(`/maintenance/plans/${id}/pause_resume/`, {
      action: 'pause',
    });
    return response.data.data;
  },

  /**
   * Resume a maintenance plan
   */
  async resume(id: string): Promise<MaintenancePlanDetail> {
    const response = await api.post(`/maintenance/plans/${id}/pause_resume/`, {
      action: 'resume',
    });
    return response.data.data;
  },

  /**
   * Complete maintenance
   */
  async complete(
    id: string,
    data: {
      completion_date?: string;
      usage_value?: number;
      notes?: string;
    }
  ): Promise<MaintenancePlanDetail> {
    const response = await api.post(`/maintenance/plans/${id}/complete/`, data);
    return response.data.data;
  },

  /**
   * Update usage value
   */
  async updateUsage(id: string, currentUsage: number): Promise<MaintenancePlanDetail> {
    const response = await api.post(`/maintenance/plans/${id}/update_usage/`, {
      current_usage: currentUsage,
    });
    return response.data.data;
  },

  /**
   * Get maintenance plans due soon
   */
  async getDueSoon(): Promise<{ results: MaintenancePlan[]; count: number }> {
    const response = await api.get('/maintenance/plans/due_soon/');
    return response.data;
  },

  /**
   * Get overdue maintenance plans
   */
  async getOverdue(): Promise<{ results: MaintenancePlan[]; count: number }> {
    const response = await api.get('/maintenance/plans/overdue/');
    return response.data;
  },

  /**
   * Get maintenance statistics
   */
  async getStatistics(): Promise<any> {
    const response = await api.get('/maintenance/plans/statistics/');
    return response.data;
  },
};
