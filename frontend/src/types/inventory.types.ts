/**
 * TypeScript types for inventory module
 */

export interface SparePart {
  id: number;
  part_number: string;
  name: string;
  description: string;
  category: string;
  manufacturer: string;
  quantity: number;
  min_quantity: number;
  unit_of_measure: string;
  unit_cost: string;
  storage_location: string;
  is_active: boolean;
  stock_status: string;
  is_low_stock: boolean;
  total_value: string;
  created_by?: {
    id: number;
    username: string;
    email: string;
  };
  created_at: string;
  updated_at: string;
}

export interface SparePartFormData {
  part_number: string;
  name: string;
  description?: string;
  category?: string;
  manufacturer?: string;
  quantity: number;
  min_quantity: number;
  unit_of_measure: string;
  unit_cost: number;
  storage_location?: string;
  is_active: boolean;
}

export interface StockMovement {
  id: number;
  spare_part: {
    id: number;
    part_number: string;
    name: string;
    category: string;
    quantity: number;
    min_quantity: number;
    unit_of_measure: string;
    unit_cost: string;
    stock_status: string;
    is_low_stock: boolean;
    total_value: string;
    is_active: boolean;
  };
  movement_type: string;
  movement_type_display: string;
  quantity: number;
  quantity_before: number;
  quantity_after: number;
  unit_cost: string;
  total_cost: string;
  reference_type: string;
  reference_id: string;
  notes: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
  created_at: string;
}

export interface StockAdjustment {
  quantity_change: number;
  movement_type: string;
  notes?: string;
  reference_type?: string;
  reference_id?: string;
}

export interface LowStockAlert {
  id: number;
  part_number: string;
  name: string;
  category: string;
  quantity: number;
  min_quantity: number;
  stock_deficit: number;
  unit_of_measure: string;
  storage_location: string;
}

export interface InventoryStatistics {
  total_parts: number;
  low_stock_count: number;
  out_of_stock_count: number;
  total_inventory_value: number;
  categories: Array<{
    category: string;
    count: number;
    value: number;
  }>;
}

export const MOVEMENT_TYPES = {
  IN: 'Entrada',
  OUT: 'Salida',
  ADJUSTMENT: 'Ajuste',
  RETURN: 'Devolución',
  TRANSFER: 'Transferencia',
  INITIAL: 'Inventario Inicial',
} as const;

export type MovementType = keyof typeof MOVEMENT_TYPES;
