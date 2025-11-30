/**
 * Service for Configuration API operations
 */
import api from './api';
import {
  AssetCategory,
  Priority,
  WorkOrderType,
  SystemParameter,
  AuditLog,
} from '../types/configuration';

const CONFIG_BASE_URL = '/configuration';

export const configurationService = {
  // Asset Categories
  async getAssetCategories(): Promise<AssetCategory[]> {
    const response = await api.get(`${CONFIG_BASE_URL}/asset-categories/`);
    return response.data.results || response.data;
  },

  async getAssetCategory(id: number): Promise<AssetCategory> {
    const response = await api.get(`${CONFIG_BASE_URL}/asset-categories/${id}/`);
    return response.data;
  },

  async createAssetCategory(data: Partial<AssetCategory>): Promise<AssetCategory> {
    const response = await api.post(`${CONFIG_BASE_URL}/asset-categories/`, data);
    return response.data;
  },

  async updateAssetCategory(id: number, data: Partial<AssetCategory>): Promise<AssetCategory> {
    const response = await api.put(`${CONFIG_BASE_URL}/asset-categories/${id}/`, data);
    return response.data;
  },

  async deleteAssetCategory(id: number): Promise<void> {
    await api.delete(`${CONFIG_BASE_URL}/asset-categories/${id}/`);
  },

  // Priorities
  async getPriorities(): Promise<Priority[]> {
    const response = await api.get(`${CONFIG_BASE_URL}/priorities/`);
    return response.data.results || response.data;
  },

  async getPriority(id: number): Promise<Priority> {
    const response = await api.get(`${CONFIG_BASE_URL}/priorities/${id}/`);
    return response.data;
  },

  async createPriority(data: Partial<Priority>): Promise<Priority> {
    const response = await api.post(`${CONFIG_BASE_URL}/priorities/`, data);
    return response.data;
  },

  async updatePriority(id: number, data: Partial<Priority>): Promise<Priority> {
    const response = await api.put(`${CONFIG_BASE_URL}/priorities/${id}/`, data);
    return response.data;
  },

  async deletePriority(id: number): Promise<void> {
    await api.delete(`${CONFIG_BASE_URL}/priorities/${id}/`);
  },

  // Work Order Types
  async getWorkOrderTypes(): Promise<WorkOrderType[]> {
    const response = await api.get(`${CONFIG_BASE_URL}/work-order-types/`);
    return response.data.results || response.data;
  },

  async getWorkOrderType(id: number): Promise<WorkOrderType> {
    const response = await api.get(`${CONFIG_BASE_URL}/work-order-types/${id}/`);
    return response.data;
  },

  async createWorkOrderType(data: Partial<WorkOrderType>): Promise<WorkOrderType> {
    const response = await api.post(`${CONFIG_BASE_URL}/work-order-types/`, data);
    return response.data;
  },

  async updateWorkOrderType(id: number, data: Partial<WorkOrderType>): Promise<WorkOrderType> {
    const response = await api.put(`${CONFIG_BASE_URL}/work-order-types/${id}/`, data);
    return response.data;
  },

  async deleteWorkOrderType(id: number): Promise<void> {
    await api.delete(`${CONFIG_BASE_URL}/work-order-types/${id}/`);
  },

  // System Parameters
  async getSystemParameters(): Promise<SystemParameter[]> {
    const response = await api.get(`${CONFIG_BASE_URL}/system-parameters/`);
    return response.data.results || response.data;
  },

  async getSystemParameter(id: number): Promise<SystemParameter> {
    const response = await api.get(`${CONFIG_BASE_URL}/system-parameters/${id}/`);
    return response.data;
  },

  async createSystemParameter(data: Partial<SystemParameter>): Promise<SystemParameter> {
    const response = await api.post(`${CONFIG_BASE_URL}/system-parameters/`, data);
    return response.data;
  },

  async updateSystemParameter(id: number, data: Partial<SystemParameter>): Promise<SystemParameter> {
    const response = await api.put(`${CONFIG_BASE_URL}/system-parameters/${id}/`, data);
    return response.data;
  },

  async deleteSystemParameter(id: number): Promise<void> {
    await api.delete(`${CONFIG_BASE_URL}/system-parameters/${id}/`);
  },

  // Audit Logs
  async getAuditLogs(filters?: { action?: string; model_name?: string }): Promise<AuditLog[]> {
    const response = await api.get(`${CONFIG_BASE_URL}/audit-logs/`, { params: filters });
    return response.data.results || response.data;
  },

  async getAuditLog(id: number): Promise<AuditLog> {
    const response = await api.get(`${CONFIG_BASE_URL}/audit-logs/${id}/`);
    return response.data;
  },
};
