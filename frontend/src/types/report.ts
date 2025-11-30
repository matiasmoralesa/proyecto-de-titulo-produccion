/**
 * Report types and interfaces
 */

export interface KPIData {
  mtbf: number | null;
  mttr: number;
  oee: number;
}

export interface WorkOrderSummary {
  total: number;
  by_status: Record<string, { count: number; label: string }>;
  by_priority: Record<string, { count: number; label: string }>;
  by_type: Record<string, { count: number; label: string }>;
  avg_completion_time: number;
  total_hours_worked: number;
}

export interface AssetDowntime {
  asset__id: number;
  asset__name: string;
  asset__vehicle_type: string;
  total_downtime: number;
  work_order_count: number;
}

export interface SparePartConsumption {
  spare_part__id: number;
  spare_part__name: string;
  spare_part__part_number: string;
  total_quantity: number;
  movement_count: number;
}

export interface MaintenanceCompliance {
  total_plans: number;
  overdue_plans: number;
  upcoming_plans: number;
  compliance_rate: number;
  on_schedule: number;
}

export interface DashboardData {
  mtbf: number | null;
  mttr: number;
  oee: number;
  work_order_summary: WorkOrderSummary;
  maintenance_compliance: MaintenanceCompliance;
}

export interface DateRange {
  start_date?: string;
  end_date?: string;
  asset_id?: number;
}
