/**
 * Service for Checklist API operations
 */
import api from './api';
import {
  ChecklistTemplate,
  ChecklistResponse,
  ChecklistCompletionRequest,
  ChecklistItemResponse,
  ChecklistFilters,
} from '../types/checklist';

const CHECKLIST_BASE_URL = '/checklists';

export const checklistService = {
  // Template endpoints
  async getTemplates(vehicleType?: string): Promise<ChecklistTemplate[]> {
    const params = vehicleType ? { vehicle_type: vehicleType } : {};
    const response = await api.get(`${CHECKLIST_BASE_URL}/templates/`, { params });
    return response.data.results || response.data;
  },

  async getTemplate(id: number): Promise<ChecklistTemplate> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/templates/${id}/`);
    return response.data;
  },

  async getTemplateItems(id: number): Promise<any[]> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/templates/${id}/items/`);
    return response.data;
  },

  async getTemplatesByVehicleType(vehicleType: string): Promise<ChecklistTemplate[]> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/templates/by_vehicle_type/`, {
      params: { vehicle_type: vehicleType },
    });
    return response.data;
  },

  // Response endpoints
  async getResponses(filters?: ChecklistFilters): Promise<ChecklistResponse[]> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/responses/`, { params: filters });
    return response.data.results || response.data;
  },

  async getResponse(id: number): Promise<ChecklistResponse> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/responses/${id}/`);
    return response.data;
  },

  async createResponse(data: Partial<ChecklistResponse>): Promise<ChecklistResponse> {
    const response = await api.post(`${CHECKLIST_BASE_URL}/responses/`, data);
    return response.data;
  },

  async completeChecklist(data: ChecklistCompletionRequest): Promise<ChecklistResponse> {
    // Prepare the request data as JSON
    const requestData = {
      template_id: data.template_id,
      asset_id: data.asset_id,
      work_order_id: data.work_order_id || null,
      signature_data: data.signature_data || '',
      item_responses: data.item_responses.map(item => ({
        template_item_id: item.template_item_id,
        response_value: item.response_value,
        observations: item.observations || '',
        // Note: photos are not supported in this version
      })),
    };
    
    const response = await api.post(`${CHECKLIST_BASE_URL}/responses/complete/`, requestData);
    return response.data;
  },

  async addItemResponse(
    checklistId: number,
    data: Partial<ChecklistItemResponse>
  ): Promise<ChecklistItemResponse> {
    const formData = new FormData();
    
    if (data.template_item_id) {
      formData.append('template_item_id', data.template_item_id.toString());
    }
    
    if (data.response_value) {
      formData.append('response_value', data.response_value);
    }
    
    if (data.observations) {
      formData.append('observations', data.observations);
    }
    
    if (data.photo) {
      formData.append('photo', data.photo);
    }
    
    const response = await api.post(
      `${CHECKLIST_BASE_URL}/responses/${checklistId}/add_item_response/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  async finalizeChecklist(id: number, signatureData?: string): Promise<ChecklistResponse> {
    const response = await api.post(`${CHECKLIST_BASE_URL}/responses/${id}/finalize/`, {
      signature_data: signatureData,
    });
    return response.data;
  },

  async downloadPDF(id: number): Promise<Blob> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/responses/${id}/download_pdf/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  async getMyChecklists(): Promise<ChecklistResponse[]> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/responses/my_checklists/`);
    return response.data.results || response.data;
  },

  async getChecklistsByAsset(assetId: number): Promise<ChecklistResponse[]> {
    const response = await api.get(`${CHECKLIST_BASE_URL}/responses/by_asset/`, {
      params: { asset_id: assetId },
    });
    return response.data.results || response.data;
  },
};
