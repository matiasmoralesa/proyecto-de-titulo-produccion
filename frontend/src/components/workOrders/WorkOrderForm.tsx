/**
 * Work Order Form Component
 * Validates: Requirements 10.5
 */
import { useState, useEffect } from 'react';
import { FiX, FiSave, FiInfo } from 'react-icons/fi';
import { WorkOrderDetail } from '../../types/workOrder.types';
import { workOrderService, WorkOrderCreateData } from '../../services/workOrderService';
import { useAuthStore } from '../../store/authStore';
import api from '../../services/api';

interface WorkOrderFormProps {
  workOrder?: WorkOrderDetail;
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

export default function WorkOrderForm({ workOrder, onClose, onSuccess }: WorkOrderFormProps) {
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [formData, setFormData] = useState({
    title: workOrder?.title || '',
    description: workOrder?.description || '',
    priority: workOrder?.priority || 'Media',
    asset: workOrder?.asset || '',
    assigned_to: workOrder?.assigned_to || '',
    scheduled_date: workOrder?.scheduled_date
      ? new Date(workOrder.scheduled_date).toISOString().slice(0, 16)
      : '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Role-based permissions
  // Validates: Requirements 10.5
  const isOperador = user?.role_name === 'OPERADOR';
  const isSupervisor = user?.role_name === 'SUPERVISOR';
  const isAdmin = user?.role_name === 'ADMIN';

  // Field permissions
  const canEditPriority = isSupervisor || isAdmin;
  const canEditAsset = isSupervisor || isAdmin;
  const canEditAssignedTo = isSupervisor || isAdmin;
  const canEditScheduledDate = isSupervisor || isAdmin;

  useEffect(() => {
    loadAssets();
    loadUsers();
  }, []);

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
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'El título es requerido';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'La descripción es requerida';
    }
    if (!formData.asset) {
      newErrors.asset = 'Debe seleccionar un activo';
    }
    if (!formData.assigned_to) {
      newErrors.assigned_to = 'Debe asignar a un usuario';
    }
    if (!formData.scheduled_date) {
      newErrors.scheduled_date = 'La fecha programada es requerida';
    } else {
      // Validate that scheduled date is not in the past
      const scheduledDate = new Date(formData.scheduled_date);
      const now = new Date();
      
      // Only validate for new work orders or if status is not completed
      if (!workOrder || workOrder.status !== 'Completada') {
        if (scheduledDate < now) {
          newErrors.scheduled_date = 'La fecha programada no puede ser anterior a la fecha actual';
        }
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
      const data: WorkOrderCreateData = {
        ...formData,
        scheduled_date: new Date(formData.scheduled_date).toISOString(),
      };

      if (workOrder) {
        await workOrderService.update(workOrder.id, data);
      } else {
        await workOrderService.create(data);
      }

      onSuccess();
      onClose();
    } catch (error: any) {
      console.error('Error saving work order:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            {workOrder ? 'Editar Orden de Trabajo' : 'Nueva Orden de Trabajo'}
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
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Título <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                errors.title ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Ej: Cambio de aceite"
            />
            {errors.title && <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.title}</p>}
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
              rows={4}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
                errors.description ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="Describe el trabajo a realizar..."
            />
            {errors.description && (
              <p className="text-red-500 dark:text-red-400 text-sm mt-1">{errors.description}</p>
            )}
          </div>

          {/* Priority and Scheduled Date */}
          {/* Validates: Requirements 10.5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Prioridad <span className="text-red-500">*</span>
                {!canEditPriority && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                disabled={!canEditPriority}
                className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  !canEditPriority ? 'bg-gray-100 cursor-not-allowed' : ''
                }`}
              >
                <option value="Baja">Baja</option>
                <option value="Media">Media</option>
                <option value="Alta">Alta</option>
                <option value="Urgente">Urgente</option>
              </select>
              {!canEditPriority && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden cambiar la prioridad
                  </p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha Programada <span className="text-red-500">*</span>
                {!canEditScheduledDate && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <input
                type="datetime-local"
                name="scheduled_date"
                value={formData.scheduled_date}
                onChange={handleChange}
                disabled={!canEditScheduledDate}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.scheduled_date ? 'border-red-500' : 'border-gray-300'
                } ${!canEditScheduledDate ? 'bg-gray-100 cursor-not-allowed' : ''}`}
              />
              {errors.scheduled_date && (
                <p className="text-red-500 text-sm mt-1">{errors.scheduled_date}</p>
              )}
              {!canEditScheduledDate && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden cambiar la fecha
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Asset and Assigned To */}
          {/* Validates: Requirements 10.5 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Activo <span className="text-red-500">*</span>
                {!canEditAsset && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="asset"
                value={formData.asset}
                onChange={handleChange}
                disabled={!canEditAsset}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.asset ? 'border-red-500' : 'border-gray-300'
                } ${!canEditAsset ? 'bg-gray-100 cursor-not-allowed' : ''}`}
              >
                <option value="">Seleccionar activo...</option>
                {assets.map((asset) => (
                  <option key={asset.id} value={asset.id}>
                    {asset.asset_number} - {asset.name}
                  </option>
                ))}
              </select>
              {errors.asset && <p className="text-red-500 text-sm mt-1">{errors.asset}</p>}
              {!canEditAsset && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden cambiar el activo
                  </p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Asignado a <span className="text-red-500">*</span>
                {!canEditAssignedTo && (
                  <span className="ml-2 text-xs text-gray-500">(Solo lectura)</span>
                )}
              </label>
              <select
                name="assigned_to"
                value={formData.assigned_to}
                onChange={handleChange}
                disabled={!canEditAssignedTo}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
                  errors.assigned_to ? 'border-red-500' : 'border-gray-300'
                } ${!canEditAssignedTo ? 'bg-gray-100 cursor-not-allowed' : ''}`}
              >
                <option value="">Seleccionar usuario...</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.first_name} {user.last_name} ({user.username})
                  </option>
                ))}
              </select>
              {errors.assigned_to && (
                <p className="text-red-500 text-sm mt-1">{errors.assigned_to}</p>
              )}
              {!canEditAssignedTo && (
                <div className="flex items-start space-x-1 mt-1">
                  <FiInfo className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-blue-600">
                    Solo supervisores y administradores pueden reasignar órdenes
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
                  <span>{workOrder ? 'Actualizar' : 'Crear'}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
