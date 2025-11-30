/**
 * Asset types
 */

export type VehicleType =
  | 'Camión Supersucker'
  | 'Camioneta MDO'
  | 'Retroexcavadora MDO'
  | 'Cargador Frontal MDO'
  | 'Minicargador MDO';

export type AssetStatus = 'Operando' | 'Detenida' | 'En Mantenimiento' | 'Fuera de Servicio';

export type DocumentType = 'manual' | 'certificate' | 'invoice' | 'photo' | 'other';

export interface Location {
  id: string;
  name: string;
  address: string;
  coordinates: string;
  description: string;
  asset_count: number;
  created_at: string;
  updated_at: string;
}

export interface AssetDocument {
  id: string;
  asset: string;
  title: string;
  document_type: DocumentType;
  file: string;
  file_url: string;
  file_size: number;
  description: string;
  uploaded_by: string;
  uploaded_by_name: string;
  created_at: string;
  updated_at: string;
}

export interface Asset {
  id: string;
  name: string;
  vehicle_type: VehicleType;
  model: string;
  serial_number: string;
  license_plate: string | null;
  location: string;
  location_name: string;
  installation_date: string;
  status: AssetStatus;
  is_archived: boolean;
  document_count: number;
  created_by_name: string;
  created_at: string;
  updated_at: string;
}

export interface AssetDetail extends Asset {
  location_data: Location;
  created_by: string;
  created_by_email: string;
  documents: AssetDocument[];
}

export interface AssetFormData {
  name: string;
  vehicle_type: VehicleType;
  model: string;
  serial_number: string;
  license_plate?: string;
  location: string;
  installation_date: string;
  status: AssetStatus;
}

export interface AssetStatistics {
  total: number;
  by_vehicle_type: Record<VehicleType, number>;
  by_status: Record<AssetStatus, number>;
  archived: number;
}
