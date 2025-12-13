/**
 * Maintenance types
 */

export type RecurrenceType =
  | 'Diario'
  | 'Semanal'
  | 'Mensual'
  | 'Trimestral'
  | 'Anual'
  | 'Por Horas'
  | 'Por Kilómetros';

export type MaintenanceStatus = 'Activo' | 'Pausado' | 'Completado' | 'Cancelado';

export interface MaintenancePlan {
  id: string;
  name: string;
  asset: string;
  asset_name: string;
  recurrence_type: RecurrenceType;
  recurrence_interval: number;
  next_due_date: string | null;
  status: MaintenanceStatus;
  is_paused: boolean;
  assigned_to: string | null;
  assigned_to_name: string | null;
  created_by_name: string;
  is_due: boolean;
  is_overdue: boolean;
  days_until_due: number | null;
  usage_until_due: number | null;
  created_at: string;
  updated_at: string;
}

export interface MaintenancePlanDetail extends MaintenancePlan {
  description: string;
  start_date: string;
  last_completed_date: string | null;
  usage_threshold: number | null;
  last_usage_value: number | null;
  estimated_duration_hours: number | null;
  paused_at: string | null;
  paused_by: string | null;
  asset_data: any;
  assigned_to_data: any;
  created_by_data: any;
  paused_by_data: any;
}

export interface MaintenancePlanFormData {
  name: string;
  description: string;
  asset: string;
  recurrence_type: RecurrenceType;
  recurrence_interval: number;
  start_date: string;
  usage_threshold: number | null;
  estimated_duration_hours: number | null;
  assigned_to: string | null;
  status: MaintenanceStatus;
}
