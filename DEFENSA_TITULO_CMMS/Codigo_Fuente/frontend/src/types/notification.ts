/**
 * Notification types and interfaces
 */

export interface Notification {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  read_at: string | null;
  related_object_type: string;
  related_object_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface NotificationPreference {
  id: number;
  work_order_created: boolean;
  work_order_assigned: boolean;
  work_order_updated: boolean;
  work_order_completed: boolean;
  asset_status_changed: boolean;
  maintenance_due: boolean;
  low_stock: boolean;
  system: boolean;
  created_at: string;
  updated_at: string;
}

export const NOTIFICATION_TYPES = {
  WORK_ORDER_CREATED: 'work_order_created',
  WORK_ORDER_ASSIGNED: 'work_order_assigned',
  WORK_ORDER_UPDATED: 'work_order_updated',
  WORK_ORDER_COMPLETED: 'work_order_completed',
  ASSET_STATUS_CHANGED: 'asset_status_changed',
  MAINTENANCE_DUE: 'maintenance_due',
  LOW_STOCK: 'low_stock',
  SYSTEM: 'system',
} as const;
