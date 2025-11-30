/**
 * Service for Report API operations
 */
import api from './api';
import {
  KPIData,
  WorkOrderSummary,
  AssetDowntime,
  SparePartConsumption,
  MaintenanceCompliance,
  DashboardData,
  DateRange,
} from '../types/report';

const REPORT_BASE_URL = '/reports';

export const reportService = {
  // KPI endpoints
  async getKPIs(filters?: DateRange): Promise<KPIData> {
    const response = await api.get(`${REPORT_BASE_URL}/kpis/`, { params: filters });
    return response.data;
  },

  async getWorkOrderSummary(filters?: DateRange): Promise<WorkOrderSummary> {
    const response = await api.get(`${REPORT_BASE_URL}/work_order_summary/`, { params: filters });
    return response.data;
  },

  async getAssetDowntime(filters?: DateRange): Promise<AssetDowntime[]> {
    const response = await api.get(`${REPORT_BASE_URL}/asset_downtime/`, { params: filters });
    return response.data;
  },

  async getSparePartConsumption(filters?: DateRange): Promise<SparePartConsumption[]> {
    const response = await api.get(`${REPORT_BASE_URL}/spare_part_consumption/`, { params: filters });
    return response.data;
  },

  async getMaintenanceCompliance(filters?: DateRange): Promise<MaintenanceCompliance> {
    const response = await api.get(`${REPORT_BASE_URL}/maintenance_compliance/`, { params: filters });
    return response.data;
  },

  async getDashboardData(filters?: DateRange): Promise<DashboardData> {
    const response = await api.get(`${REPORT_BASE_URL}/dashboard/`, { params: filters });
    return response.data;
  },

  // Export endpoints
  async exportWorkOrders(filters?: DateRange): Promise<Blob> {
    const response = await api.get(`${REPORT_BASE_URL}/export_work_orders/`, {
      params: filters,
      responseType: 'blob',
    });
    return response.data;
  },

  async exportAssetDowntime(filters?: DateRange): Promise<Blob> {
    const response = await api.get(`${REPORT_BASE_URL}/export_asset_downtime/`, {
      params: filters,
      responseType: 'blob',
    });
    return response.data;
  },
};
