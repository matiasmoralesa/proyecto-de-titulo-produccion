/**
 * Types for Checklist system
 */

export type ResponseType = 'yes_no_na' | 'text' | 'numeric' | 'photo';

export type ResponseValue = 'yes' | 'no' | 'na' | string;

export type ChecklistStatus = 'IN_PROGRESS' | 'COMPLETED' | 'APPROVED' | 'REJECTED';

export interface ChecklistTemplateItem {
  id: number;
  section: string;
  order: number;
  question: string;
  response_type: ResponseType;
  required: boolean;
  observations_allowed: boolean;
}

export interface ChecklistTemplate {
  id: number;
  code: string;
  name: string;
  description: string;
  vehicle_type: string;
  is_system_template: boolean;
  passing_score: number;
  is_active: boolean;
  items: ChecklistTemplateItem[];
  total_items: number;
  required_items_count: number;
  created_at: string;
  updated_at: string;
  created_by: number | null;
  created_by_name: string | null;
}

export interface ChecklistItemResponse {
  id?: number;
  template_item?: ChecklistTemplateItem;
  template_item_id: number;
  response_value: string;
  observations: string;
  photo?: File | string | null;
  photo_url?: string | null;
  answered_at?: string;
}

export interface ChecklistResponse {
  id: number;
  template: ChecklistTemplate;
  template_id?: number;
  asset: {
    id: number;
    name: string;
    license_plate: string;
    vehicle_type: string;
  };
  asset_id?: number;
  work_order: number | null;
  work_order_id?: number | null;
  completed_by: number | null;
  completed_by_name: string | null;
  completed_at: string | null;
  score: number | null;
  status: ChecklistStatus;
  signature_data: string;
  pdf_file: string | null;
  pdf_url: string | null;
  item_responses: ChecklistItemResponse[];
  completion_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface ChecklistCompletionRequest {
  template_id: number;
  asset_id: number;
  work_order_id?: number | null;
  signature_data?: string;
  item_responses: {
    template_item_id: number;
    response_value: string;
    observations?: string;
    photo?: File | null;
  }[];
}

export interface ChecklistFilters {
  status?: ChecklistStatus;
  asset?: number;
  work_order?: number;
  completed_by?: number;
  template?: number;
  search?: string;
}
