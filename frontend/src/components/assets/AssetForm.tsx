/**
 * Asset Form Component
 * Validates: Requirements 10.5
 */
import { useState, useEffect } from 'react';
import { FiX, FiSave, FiInfo } from 'react-icons/fi';
import { Asset } from '../../types/asset.types';
import assetService from '../../services/assetService';
import { useAuthStore } from '../../store/authStore';
import api from '../../services/api';

interface AssetFormProps {
  asset?: Asset;
  onClose: () => void;
  onSuccess: () => void;
}

interface Location {
  id: string;
  name: string;
}

export default function AssetForm({ asset, onClose, onSuccess }: AssetFormProps) {
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [locations, setLocations] = useState<Location[]>([]);
  const [formData, setFormData] = useState({
    name: asset?.name || '',
    model: asset?.model || '',
    serial_number: asset?.serial_number || '',
    vehicle_type: asset?.vehicle_type || 'Camión Supersucker',
    license_plate: asset?.license_plate || '',
    location: asset?.location || '',
    installation_date: asset?.installation_date
      ? new Date(asset.installation_date).toISOString().slice(0, 10)
      : '',
    status: asset?.status || 'Operando',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Role-based permissions
  // Validates: Requirements 10.5
  const isOperador = user?.role?.name === 'OPERADOR';
  const isSupervisor = user?.role?.name === 'SUPERVISOR';
  const isAdmin = user?.role?.name === 'ADMIN';

  // Field permissions - Only supervisors and admins can edit critical fields
  const canEditStatus = isSupervisor || isAdmin;
  const canEditLocation = isSupervisor || isAdmin;
  const canEditVehicleType = isAdmin; // Only admins can change vehicle type
  const canEditSerialNumber = isAdmin; // Only admins can change serial number

  const vehicleTypes = [
    'Camión Supersucker',
    'Camioneta MDO',
    'Retroexcavadora MDO',
    'Cargador Frontal MDO',
    'Minicargador MDO',
  ];

  const statusOptions = [
    'Operando',
    'Detenida',
    'En Mantenimiento',
    'Fuera de Servicio',
  ];

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const response = await api.get('/assets/locations/');
      setLocations(response.data.results || []);
    } catch (error) {
      console.error('Error loading locations:', error);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es requerido';
    }
    if (!formData.serial_number.trim()) {
      newErrors.serial_number = 'El número de serie es requerido';
    }
    if (!formData.model.trim()) {
      newErrors.model = 'El modelo es requerido';
    }
    if (!formData.location) {
      newErrors.location = 'Debe seleccionar una ubicación';
    }
    if (!formData.installation_date) {
      newErrors.installation_date = 'La fecha de instalación es requerida';
    } else {
      // Validate that installation date is not in the future
      const installationDate = new Date(formData.installation_date);
      const today = new Date();
      today.setHours(0, 0, 0, 0); // Reset time to compare only dates
      
      if (installationDate > today) {
        newErrors.installation_date = 'La fecha de instalación no puede ser posterior a la fecha actual';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setLoading(true);
    try {
      // Prepare data matching the backend model
      const dataToSend: any = {
        name: formData.name,
        model: formData.model,
        serial_number: formData.serial_number.toUpperCase(),
        vehicle_type: formData.vehicle_type,
        license_plate: formData.license_plate ? formData.license_plate.toUpperCase() : null,
        location: formData.location,
        installation_date: formData.installation_date,
        status: formData.status,
      };

      if (asset) {
        await assetService.updateAsset(asset.id, dataToSend);
      } else {
        await assetService.createAsset(dataToSend);
      }

      onSuccess();
      onClose();
    } catch (error: any) {
      console.error('Error saving asset:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">
            {asset ? 'Editar Activo' : 'Nuevo Activo'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Name and Model */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nombre <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.name ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: Camioneta MDO 001"
              />
              {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Modelo <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="model"
                value={formData.model}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.model ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: Hilux 4x4"
              />
              {errors.model && <p className="text-red-500 text-sm mt-1">{errors.model}</p>}
            </div>
          </div>

          {/* Vehicle Type and Status */}
          {/* Validates: Requirements 10.5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Vehículo <span className="text-red-500">*</span>
                {!canEditVehicleType && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="vehicle_type"
                value={formData.vehicle_type}
                onChange={handleChange}
                disabled={!canEditVehicleType}
                className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  !canEditVehicleType ? 'bg-gray-100 cursor-not-allowed' : ''
                }`}
              >
                {vehicleTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              {!canEditVehicleType && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo administradores pueden cambiar el tipo de vehículo
                  </p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Estado <span className="text-red-500">*</span>
                {!canEditStatus && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                disabled={!canEditStatus}
                className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  !canEditStatus ? 'bg-gray-100 cursor-not-allowed' : ''
                }`}
              >
                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
              {!canEditStatus && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden cambiar el estado
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Serial Number and Installation Date */}
          {/* Validates: Requirements 10.5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Número de Serie <span className="text-red-500">*</span>
                {!canEditSerialNumber && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <input
                type="text"
                name="serial_number"
                value={formData.serial_number}
                onChange={handleChange}
                disabled={!canEditSerialNumber}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.serial_number ? 'border-red-500' : 'border-gray-300'
                } ${!canEditSerialNumber ? 'bg-gray-100 cursor-not-allowed' : ''}`}
                placeholder="Ej: SN123456789"
              />
              {errors.serial_number && (
                <p className="text-red-500 text-sm mt-1">{errors.serial_number}</p>
              )}
              {!canEditSerialNumber && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo administradores pueden cambiar el número de serie
                  </p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha de Instalación <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                name="installation_date"
                value={formData.installation_date}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.installation_date ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.installation_date && (
                <p className="text-red-500 text-sm mt-1">{errors.installation_date}</p>
              )}
            </div>
          </div>

          {/* License Plate and Location */}
          {/* Validates: Requirements 10.5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Placa</label>
              <input
                type="text"
                name="license_plate"
                value={formData.license_plate}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Ej: ABC-123"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ubicación <span className="text-red-500">*</span>
                {!canEditLocation && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="location"
                value={formData.location}
                onChange={handleChange}
                disabled={!canEditLocation}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.location ? 'border-red-500' : 'border-gray-300'
                } ${!canEditLocation ? 'bg-gray-100 cursor-not-allowed' : ''}`}
              >
                <option value="">Seleccionar ubicación...</option>
                {locations.map((location) => (
                  <option key={location.id} value={location.id}>
                    {location.name}
                  </option>
                ))}
              </select>
              {errors.location && <p className="text-red-500 text-sm mt-1">{errors.location}</p>}
              {!canEditLocation && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden cambiar la ubicación
                  </p>
                </div>
              )}
            </div>
          </div>



          {/* Actions */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 font-medium transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Guardando...</span>
                </>
              ) : (
                <>
                  <FiSave className="w-4 h-4" />
                  <span>{asset ? 'Actualizar' : 'Crear'}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
