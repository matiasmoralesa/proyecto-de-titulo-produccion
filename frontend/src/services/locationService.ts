/**
 * Service for Location API operations
 */
import api from './api';
import { Location } from '../types/location';

const LOCATION_BASE_URL = '/assets/locations';

export const locationService = {
  async getLocations(): Promise<Location[]> {
    const response = await api.get(`${LOCATION_BASE_URL}/`);
    return response.data.results || response.data;
  },

  async getLocation(id: string): Promise<Location> {
    const response = await api.get(`${LOCATION_BASE_URL}/${id}/`);
    return response.data;
  },

  async createLocation(data: Partial<Location>): Promise<Location> {
    const response = await api.post(`${LOCATION_BASE_URL}/`, data);
    return response.data;
  },

  async updateLocation(id: string, data: Partial<Location>): Promise<Location> {
    const response = await api.put(`${LOCATION_BASE_URL}/${id}/`, data);
    return response.data;
  },

  async deleteLocation(id: string): Promise<void> {
    await api.delete(`${LOCATION_BASE_URL}/${id}/`);
  },
};
