/**
 * Service for inventory API calls
 */
import api from './api';
import type {
  SparePart,
  SparePartFormData,
  StockMovement,
  StockAdjustment,
  LowStockAlert,
  InventoryStatistics,
} from '../types/inventory.types';

export const inventoryService = {
  // Spare Parts
  getSpareParts: async (params?: {
    page?: number;
    search?: string;
    category?: string;
    is_active?: boolean;
    low_stock?: boolean;
    out_of_stock?: boolean;
  }) => {
    const response = await api.get('/inventory/spare-parts/', { params });
    return response.data;
  },

  getSparePart: async (id: number) => {
    const response = await api.get<SparePart>(`/inventory/spare-parts/${id}/`);
    return response.data;
  },

  createSparePart: async (data: SparePartFormData) => {
    const response = await api.post<SparePart>('/inventory/spare-parts/', data);
    return response.data;
  },

  updateSparePart: async (id: number, data: Partial<SparePartFormData>) => {
    const response = await api.patch<SparePart>(`/inventory/spare-parts/${id}/`, data);
    return response.data;
  },

  deleteSparePart: async (id: number) => {
    await api.delete(`/inventory/spare-parts/${id}/`);
  },

  // Stock Adjustments
  adjustStock: async (id: number, adjustment: StockAdjustment) => {
    const response = await api.post(`/inventory/spare-parts/${id}/adjust-stock/`, adjustment);
    return response.data;
  },

  getStockHistory: async (id: number, params?: {
    start_date?: string;
    end_date?: string;
    movement_type?: string;
  }) => {
    const response = await api.get<StockMovement[]>(
      `/inventory/spare-parts/${id}/stock-history/`,
      { params }
    );
    return response.data;
  },

  // Low Stock Alerts
  getLowStockAlerts: async () => {
    const response = await api.get<LowStockAlert[]>('/inventory/spare-parts/low-stock-alerts/');
    return response.data;
  },

  // Statistics
  getStatistics: async () => {
    const response = await api.get<InventoryStatistics>('/inventory/spare-parts/statistics/');
    return response.data;
  },

  // Stock Movements
  getStockMovements: async (params?: {
    page?: number;
    spare_part?: number;
    movement_type?: string;
    user?: number;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/inventory/stock-movements/', { params });
    return response.data;
  },

  getStockMovementsSummary: async (params?: {
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/inventory/stock-movements/summary/', { params });
    return response.data;
  },
};
