import api from './api';

export interface AssetStatus {
  id: string;
  asset: string;
  asset_name: string;
  status_type: string;
  status_type_display: string;
  odometer_reading: number | null;
  fuel_level: number | null;
  condition_notes: string;
  last_updated_by: string;
  last_updated_by_name: string;
  updated_at: string;
  created_at: string;
}

export interface AssetStatusHistory {
  id: string;
  asset: string;
  asset_name: string;
  status_type: string;
  odometer_reading: number | null;
  fuel_level: number | null;
  condition_notes: string;
  updated_by: string;
  updated_by_name: string;
  timestamp: string;
  created_at: string;
}

export interface UpdateStatusData {
  status_type: string;
  odometer_reading?: number;
  fuel_level?: number;
  condition_notes?: string;
}

export interface StatusFilters {
  asset?: string;
  status_type?: string;
}

export interface HistoryFilters {
  asset?: string;
  status_type?: string;
  start_date?: string;
  end_date?: string;
}

const machineStatusService = {
  // Get all asset statuses
  getStatuses: async (filters?: StatusFilters) => {
    const params = new URLSearchParams();
    if (filters?.asset) params.append('asset', filters.asset);
    if (filters?.status_type) params.append('status_type', filters.status_type);
    
    const response = await api.get(`/machine-status/status/?${params.toString()}`);
    return response.data;
  },

  // Get single asset status
  getStatus: async (id: string) => {
    const response = await api.get(`/machine-status/status/${id}/`);
    return response.data;
  },

  // Create asset status
  createStatus: async (data: { asset: string } & UpdateStatusData) => {
    const response = await api.post('/machine-status/status/', data);
    return response.data;
  },

  // Update asset status
  updateStatus: async (id: string, data: UpdateStatusData) => {
    const response = await api.patch(`/machine-status/status/${id}/`, data);
    return response.data;
  },

  // Get status history
  getHistory: async (filters?: HistoryFilters) => {
    const params = new URLSearchParams();
    if (filters?.asset) params.append('asset', filters.asset);
    if (filters?.status_type) params.append('status_type', filters.status_type);
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    
    const response = await api.get(`/machine-status/history/?${params.toString()}`);
    return response.data;
  },
};

export default machineStatusService;


export interface AssetHistoryActivity {
  type: string;
  timestamp: string;
  user: {
    id: string;
    name: string;
  };
  data: any;
}

export interface AssetHistoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: AssetHistoryActivity[];
}

export interface AssetKPIs {
  asset: {
    id: string;
    name: string;
    vehicle_type: string;
    serial_number: string;
  };
  current_status: {
    status_type: string;
    status_type_display: string;
    fuel_level: number | null;
    odometer_reading: number | null;
    last_updated: string;
  } | null;
  kpis: {
    total_maintenance_hours: number;
    total_work_orders: number;
    completed_work_orders: number;
    pending_work_orders: number;
    in_progress_work_orders: number;
    downtime_events: number;
    total_maintenance_cost: number;
    average_hours_per_work_order: number;
  };
  date_range: {
    start_date: string;
    end_date: string;
  };
}

export interface HistoryFiltersExtended extends HistoryFilters {
  activity_type?: string;
  page?: number;
  page_size?: number;
}

const assetHistoryService = {
  // Get complete asset history
  getCompleteHistory: async (assetId: string, filters?: HistoryFiltersExtended): Promise<AssetHistoryResponse> => {
    const params = new URLSearchParams();
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    if (filters?.activity_type) params.append('activity_type', filters.activity_type);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.page_size) params.append('page_size', filters.page_size.toString());
    
    const response = await api.get(`/machine-status/asset-history/${assetId}/complete-history/?${params.toString()}`);
    return response.data;
  },

  // Get asset KPIs
  getAssetKPIs: async (assetId: string, filters?: { start_date?: string; end_date?: string }): Promise<AssetKPIs> => {
    const params = new URLSearchParams();
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    
    const response = await api.get(`/machine-status/asset-history/${assetId}/kpis/?${params.toString()}`);
    return response.data;
  },
};

export { assetHistoryService };
