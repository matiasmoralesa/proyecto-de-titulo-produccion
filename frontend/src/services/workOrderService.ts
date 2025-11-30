/**
 * Work Order service for API calls
 */
import api from './api';
import { WorkOrder, WorkOrderDetail } from '../types/workOrder.types';

export interface WorkOrderCreateData {
  title: string;
  description: string;
  priority: string;
  asset: string;
  assigned_to: string;
  scheduled_date: string;
}

export interface WorkOrderUpdateData {
  title?: string;
  description?: string;
  priority?: string;
  asset?: string;
  assigned_to?: string;
  scheduled_date?: string;
  status?: string;
}

export interface WorkOrderCompleteData {
  completion_notes: string;
  actual_hours: number;
}

export const workOrderService = {
  /**
   * Get all work orders with optional filters
   */
  async getAll(params?: {
    status?: string;
    priority?: string;
    assigned_to?: string;
    search?: string;
  }): Promise<{ results: WorkOrder[]; count: number }> {
    const response = await api.get('/work-orders/', { params });
    return response.data;
  },

  /**
   * Get a single work order by ID
   */
  async getById(id: string): Promise<WorkOrderDetail> {
    const response = await api.get(`/work-orders/${id}/`);
    return response.data;
  },

  /**
   * Create a new work order
   */
  async create(data: WorkOrderCreateData): Promise<WorkOrder> {
    const response = await api.post('/work-orders/', data);
    return response.data;
  },

  /**
   * Update an existing work order
   */
  async update(id: string, data: WorkOrderUpdateData): Promise<WorkOrder> {
    const response = await api.patch(`/work-orders/${id}/`, data);
    return response.data;
  },

  /**
   * Delete a work order
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/work-orders/${id}/`);
  },

  /**
   * Transition work order status
   */
  async transitionStatus(id: string, newStatus: string): Promise<WorkOrder> {
    const response = await api.post(`/work-orders/${id}/transition_status/`, {
      new_status: newStatus,
    });
    return response.data;
  },

  /**
   * Complete a work order
   */
  async complete(id: string, data: WorkOrderCompleteData): Promise<WorkOrder> {
    const response = await api.post(`/work-orders/${id}/complete/`, data);
    return response.data;
  },

  /**
   * Get work orders assigned to current user
   */
  async getMyAssignments(): Promise<{ results: WorkOrder[]; count: number }> {
    const response = await api.get('/work-orders/my_assignments/');
    return response.data;
  },
};
