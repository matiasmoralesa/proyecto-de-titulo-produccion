/**
 * Work Order types
 */

export type WorkOrderPriority = 'Baja' | 'Media' | 'Alta' | 'Urgente';
export type WorkOrderStatus = 'Pendiente' | 'En Progreso' | 'Completada' | 'Cancelada';

export interface WorkOrder {
  id: string;
  work_order_number: string;
  title: string;
  priority: WorkOrderPriority;
  status: WorkOrderStatus;
  asset: string;
  asset_name: string;
  assigned_to: string;
  assigned_to_name: string;
  scheduled_date: string;
  completed_date: string | null;
  created_by_name: string;
  created_at: string;
}

export interface WorkOrderDetail extends WorkOrder {
  description: string;
  completion_notes: string;
  actual_hours: number | null;
  asset_data: any;
  assigned_to_data: any;
  created_by_data: any;
  updated_at: string;
}
