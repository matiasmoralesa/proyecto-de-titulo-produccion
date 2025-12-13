/**
 * Maintenance Plan Form Component
 */
import { useState, useEffect } from 'react';
import { FiX, FiSave } from 'react-icons/fi';
import { MaintenancePlan, RecurrenceType, MaintenanceStatus } from '../../types/maintenance.types';
import { maintenanceService } from '../../services/maintenanceService';
import api from '../../services/api';

interface MaintenancePlanFormProps {
  plan?: MaintenancePlan;
  onClose: () => void;
  onSuccess: () => void;
}

interface Asset {
  id: string;
  name: string;
  asset_number: string;
}

interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
}

export default function MaintenancePlanForm({ plan, onClose, onSuccess }: MaintenancePlanFormProps) {
  const [loading, setLoading] = useState(false);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    asset: '',
    recurrence_type: 'Mensual' as RecurrenceType,
    recurrence_interval: 1,
    start_date: new Date().toISOString().slice(0, 10),
    usage_threshold: null as number | null,
    estimated_duration_hours: null as number | null,
    assigned_to: '',
    status: 'Activo' as MaintenanceStatus,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const recurrenceTypes: RecurrenceType[] = [
    'Diario',
    'Semanal',
    'Mensual',
    'Trimestral',
    'Anual',
    'Por Horas',
    'Por Kilómetros',
  ];

  const statusOptions: MaintenanceStatus[] = ['Activo', 'Pausado', 'Completado', 'Cancelado'];

  const isUsageBased = ['Por Horas', 'Por Kilómetros'].includes(formData.recurrence_type);

  useEffect(() => {
    loadAssets();
    loadUsers();
    
    // Load plan data if editing
    if (plan) {
      setFormData({
        name: plan.name || '',
        description: plan.description || '',
        asset: plan.asset || '',
        recurrence_type: (plan.recurrence_type as RecurrenceType) || 'Mensual',
        recurrence_interval: plan.recurrence_interval || 1,
        start_date: plan.start_date
          ? new Date(plan.start_date).toISOString().slice(0, 10)
          : new Date().toISOString().slice(0, 10),
        usage_threshold: plan.usage_threshold || null,
        estimated_duration_hours: plan.estimated_duration_hours || null,
        assigned_to: plan.assigned_to || '',
        status: (plan.status as MaintenanceStatus) || 'Activo',
      });
    }
  }, [plan]);

  const loadAssets = async () => {
    try {
      const response = await api.get('/assets/assets/');
      setAssets(response.data.results || []);
    } catch (error) {
      console.error('Error loading assets:', error);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await api.get('/auth/users/');
      setUsers(response.data.results || []);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es requerido';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'La descripción es requerida';
    }
    if (!formData.asset) {
      newErrors.asset = 'Debe seleccionar un activo';
    }
    if (!formData.start_date) {
      newErrors.start_date = 'La fecha de inicio es requerida';
    }
    if (formData.recurrence_interval < 1) {
      newErrors.recurrence_interval = 'El intervalo debe ser al menos 1';
    }
    if (isUsageBased && !formData.usage_threshold) {
      newErrors.usage_threshold = 'El umbral de uso es requerido para este tipo de recurrencia';
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
      const dataToSend: any = {
        name: formData.name,
        description: formData.description,
        asset: formData.asset,
        recurrence_type: formData.recurrence_type,
        recurrence_interval: parseInt(formData.recurrence_interval.toString()),
        start_date: formData.start_date,
        usage_threshold: isUsageBased && formData.usage_threshold
          ? parseInt(formData.usage_threshold.toString())
          : null,
        estimated_duration_hours: formData.estimated_duration_hours
          ? parseFloat(formData.estimated_duration_hours.toString())
          : null,
        assigned_to: formData.assigned_to || null,
        status: formData.status,
      };

      if (plan) {
        await maintenanceService.update(plan.id, dataToSend);
      } else {
        await maintenanceService.create(dataToSend);
      }

      onSuccess();
      onClose();
    } catch (error: any) {
      console.error('Error saving maintenance plan:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            {plan ? 'Editar Plan de Mantenimiento' : 'Nuevo Plan de Mantenimiento'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Name and Asset */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Nombre <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                  errors.name ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                }`}
                placeholder="Ej: Cambio de aceite"
              />
              {errors.name && <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.name}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Activo <span className="text-red-500">*</span>
              </label>
              <select
                name="asset"
                value={formData.asset}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                  errors.asset ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                }`}
              >
                <option value="">Seleccionar activo...</option>
                {assets.map((asset) => (
                  <option key={asset.id} value={asset.id}>
                    {asset.name}
                  </option>
                ))}
              </select>
              {errors.asset && <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.asset}</p>}
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Descripción <span className="text-red-500">*</span>
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                errors.description ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Describe el mantenimiento a realizar..."
            />
            {errors.description && (
              <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.description}</p>
            )}
          </div>

          {/* Recurrence Type and Interval */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Tipo de Recurrencia <span className="text-red-500">*</span>
              </label>
              <select
                name="recurrence_type"
                value={formData.recurrence_type}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                {recurrenceTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Intervalo <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="recurrence_interval"
                value={formData.recurrence_interval}
                onChange={handleChange}
                min="1"
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                  errors.recurrence_interval ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                }`}
                placeholder="Ej: 1"
              />
              {errors.recurrence_interval && (
                <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.recurrence_interval}</p>
              )}
            </div>
          </div>

          {/* Start Date and Usage Threshold */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Fecha de Inicio <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                  errors.start_date ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                }`}
              />
              {errors.start_date && (
                <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.start_date}</p>
              )}
            </div>

            {isUsageBased && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Umbral de Uso <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="usage_threshold"
                  value={formData.usage_threshold || ''}
                  onChange={handleChange}
                  min="1"
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                    errors.usage_threshold ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                  }`}
                  placeholder={
                    formData.recurrence_type === 'Por Horas' ? 'Ej: 100 horas' : 'Ej: 5000 km'
                  }
                />
                {errors.usage_threshold && (
                  <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.usage_threshold}</p>
                )}
              </div>
            )}
          </div>

          {/* Duration and Assigned To */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Duración Estimada (horas)
              </label>
              <input
                type="number"
                name="estimated_duration_hours"
                value={formData.estimated_duration_hours || ''}
                onChange={handleChange}
                step="0.5"
                min="0"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Ej: 2.5"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Asignado a</label>
              <select
                name="assigned_to"
                value={formData.assigned_to}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="">Sin asignar</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.first_name} {user.last_name} ({user.username})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Estado</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 font-medium transition-colors"
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
                  <span>{plan ? 'Actualizar' : 'Crear'}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
