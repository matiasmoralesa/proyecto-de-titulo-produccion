/**
 * Configuration and master data types
 */

export interface AssetCategory {
  id: number;
  name: string;
  description: string;
  code: string;
  is_active: boolean;
  created_by: number | null;
  created_by_name: string | null;
  created_at: string;
  updated_at: string;
  can_delete: boolean;
}

export interface Priority {
  id: number;
  name: string;
  description: string;
  level: number;
  color_code: string;
  is_active: boolean;
  created_by: number | null;
  created_by_name: string | null;
  created_at: string;
  updated_at: string;
  can_delete: boolean;
}

export interface WorkOrderType {
  id: number;
  name: string;
  description: string;
  code: string;
  requires_approval: boolean;
  is_active: boolean;
  created_by: number | null;
  created_by_name: string | null;
  created_at: string;
  updated_at: string;
  can_delete: boolean;
}

export interface SystemParameter {
  id: number;
  key: string;
  value: string;
  description: string;
  data_type: 'string' | 'integer' | 'float' | 'boolean' | 'json';
  is_editable: boolean;
  modified_by: number | null;
  modified_by_name: string | null;
  created_at: string;
  updated_at: string;
  typed_value: any;
}

export interface AuditLog {
  id: number;
  timestamp: string;
  user: number | null;
  user_name: string;
  action: 'CREATE' | 'UPDATE' | 'DELETE';
  action_display: string;
  model_name: string;
  object_id: string;
  object_repr: string;
  changes: Record<string, { old: any; new: any }>;
  ip_address: string | null;
}
