import React, { useState, useEffect } from 'react';
import machineStatusService, { UpdateStatusData } from '../../services/machineStatusService';
import assetService from '../../services/assetService';

interface StatusUpdateFormProps {
  assetId?: string;
  statusId?: string;
  onSuccess: () => void;
  onCancel: () => void;
}

const StatusUpdateForm: React.FC<StatusUpdateFormProps> = ({
  assetId,
  statusId,
  onSuccess,
  onCancel,
}) => {
  const [assets, setAssets] = useState<any[]>([]);
  const [selectedAsset, setSelectedAsset] = useState(assetId || '');
  const [formData, setFormData] = useState<UpdateStatusData>({
    status_type: 'OPERANDO',
    odometer_reading: undefined,
    fuel_level: undefined,
    condition_notes: '',
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    loadAssets();
    if (statusId) {
      loadCurrentStatus();
    }
  }, [statusId]);

  const loadAssets = async () => {
    try {
      const response = await assetService.getAssets();
      const assetsList = response.results || response;
      setAssets(assetsList);
    } catch (error) {
      console.error('Error loading assets:', error);
    }
  };

  const loadCurrentStatus = async () => {
    if (!statusId) return;
    
    try {
      const status = await machineStatusService.getStatus(statusId);
      setFormData({
        status_type: status.status_type,
        odometer_reading: status.odometer_reading || undefined,
        fuel_level: status.fuel_level || undefined,
        condition_notes: status.condition_notes || '',
      });
      setSelectedAsset(status.asset);
    } catch (error) {
      console.error('Error loading status:', error);
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!selectedAsset && !statusId) {
      newErrors.asset = 'Debe seleccionar un activo';
    }

    if (!formData.status_type) {
      newErrors.status_type = 'Debe seleccionar un estado';
    }

    if (formData.fuel_level !== undefined) {
      if (formData.fuel_level < 0 || formData.fuel_level > 100) {
        newErrors.fuel_level = 'El nivel de combustible debe estar entre 0 y 100';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      if (statusId) {
        // Update existing status
        await machineStatusService.updateStatus(statusId, formData);
      } else {
        // Create new status
        await machineStatusService.createStatus({
          asset: selectedAsset,
          ...formData,
        });
      }
      alert('Estado actualizado exitosamente');
      onSuccess();
    } catch (error: any) {
      console.error('Error updating status:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      } else {
        alert('Error al actualizar el estado');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'odometer_reading' || name === 'fuel_level' 
        ? value ? parseFloat(value) : undefined 
        : value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Asset Selection (only for new status) */}
      {!statusId && (
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Activo *
          </label>
          <select
            value={selectedAsset}
            onChange={(e) => setSelectedAsset(e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
              errors.asset ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
          >
            <option value="">Seleccione un activo</option>
            {assets.map((asset) => (
              <option key={asset.id} value={asset.id}>
                {asset.name} - {asset.vehicle_type}
              </option>
            ))}
          </select>
          {errors.asset && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.asset}</p>
          )}
        </div>
      )}

      {/* Status Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Estado *
        </label>
        <select
          name="status_type"
          value={formData.status_type}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
            errors.status_type ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
          }`}
        >
          <option value="OPERANDO">Operando</option>
          <option value="DETENIDA">Detenida</option>
          <option value="EN_MANTENIMIENTO">En Mantenimiento</option>
          <option value="FUERA_DE_SERVICIO">Fuera de Servicio</option>
        </select>
        {errors.status_type && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.status_type}</p>
        )}
      </div>

      {/* Odometer Reading */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Lectura de Odómetro / Horómetro
        </label>
        <input
          type="number"
          name="odometer_reading"
          value={formData.odometer_reading || ''}
          onChange={handleChange}
          step="0.01"
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="Ej: 1000.50"
        />
      </div>

      {/* Fuel Level Slider */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Nivel de Combustible: {formData.fuel_level || 0}%
        </label>
        <input
          type="range"
          name="fuel_level"
          value={formData.fuel_level || 0}
          onChange={handleChange}
          min="0"
          max="100"
          className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
        />
        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>0%</span>
          <span>25%</span>
          <span>50%</span>
          <span>75%</span>
          <span>100%</span>
        </div>
        {errors.fuel_level && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.fuel_level}</p>
        )}
      </div>

      {/* Condition Notes */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Notas de Condición
        </label>
        <textarea
          name="condition_notes"
          value={formData.condition_notes}
          onChange={handleChange}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="Describa la condición del activo..."
        />
      </div>

      {/* Form Actions */}
      <div className="flex flex-col sm:flex-row gap-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 font-medium"
          disabled={loading}
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300 font-medium"
          disabled={loading}
        >
          {loading ? 'Actualizando...' : 'Actualizar Estado'}
        </button>
      </div>
    </form>
  );
};

export default StatusUpdateForm;
