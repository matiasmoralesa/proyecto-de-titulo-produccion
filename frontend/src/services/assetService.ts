/**
 * Asset service
 */
import api from './api';
import { Asset, AssetDetail, AssetFormData, Location, AssetStatistics } from '../types/asset.types';

class AssetService {
  /**
   * Get all assets
   */
  async getAssets(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    vehicle_type?: string;
    status?: string;
    location?: string;
    include_archived?: boolean;
  }): Promise<{ results: Asset[]; count: number }> {
    const response = await api.get('/assets/assets/', { params });
    return response.data;
  }

  /**
   * Get asset by ID
   */
  async getAsset(id: string): Promise<AssetDetail> {
    const response = await api.get(`/assets/assets/${id}/`);
    return response.data;
  }

  /**
   * Create asset
   */
  async createAsset(data: AssetFormData): Promise<AssetDetail> {
    const response = await api.post('/assets/assets/', data);
    return response.data;
  }

  /**
   * Update asset
   */
  async updateAsset(id: string, data: Partial<AssetFormData>): Promise<AssetDetail> {
    const response = await api.patch(`/assets/assets/${id}/`, data);
    return response.data;
  }

  /**
   * Delete (archive) asset
   */
  async deleteAsset(id: string): Promise<void> {
    await api.delete(`/assets/assets/${id}/`);
  }

  /**
   * Restore archived asset
   */
  async restoreAsset(id: string): Promise<AssetDetail> {
    const response = await api.post(`/assets/assets/${id}/restore/`);
    return response.data;
  }

  /**
   * Get asset statistics
   */
  async getStatistics(): Promise<AssetStatistics> {
    const response = await api.get('/assets/assets/statistics/');
    return response.data;
  }

  /**
   * Get all locations
   */
  async getLocations(): Promise<Location[]> {
    const response = await api.get('/assets/locations/');
    return response.data.results || response.data;
  }

  /**
   * Upload document for asset
   */
  async uploadDocument(assetId: string, formData: FormData): Promise<void> {
    await api.post('/assets/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}

export default new AssetService();
