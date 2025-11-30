/**
 * Maintenance Plan Detail Component
 */
import { useState, useEffect } from 'react';
import {
  FiX,
  FiCalendar,
  FiClock,
  FiTruck,
  FiUser,
  FiEdit,
  FiTrash2,
  FiPause,
  FiPlay,
  FiCheckCircle,
  FiAlertCircle,
} from 'react-icons/fi';
import { MaintenancePlan, MaintenancePlanDetail as MaintenancePlanDetailType } from '../../types/maintenance.types';
import { maintenanceService } from '../../services/maintenanceService';

interface MaintenancePlanDetailProps {
  planId: string;
  onClose: () => void;
  onEdit: (plan: MaintenancePlan) => void;
  onDelete: () => void;
  onUpdate: () => void;
}

export default function MaintenancePlanDetail({
  planId,
  onClose,
  onEdit,
  onDelete,
  onUpdate,
}: MaintenancePlanDetailProps) {
  const [plan, setPlan] = useState<MaintenancePlanDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCompleteForm, setShowCompleteForm] = useState(false);
  const [completeData, setCompleteData] = useState({
    completion_date: new Date().toISOString().slice(0, 10),
    usage_value: '',
    notes: '',
  });

  useEffect(() => {
    loadPlan();
  }, [planId]);

  const loadPlan = async () => {
    try {
      const data = await maintenanceService.getById(planId);
      setPlan(data);
    } catch (error) {
      console.error('Error loading maintenance plan:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePauseResume = async () => {
    if (!plan) return;

    const action = plan.is_paused ? 'reanudar' : 'pausar';
    if (!window.confirm(`¿Estás seguro de que deseas ${action} este plan?`)) {
      return;
    }

    try {
      if (plan.is_paused) {
        await maintenanceService.resume(plan.id);
      } else {
        await maintenanceService.pause(plan.id);
      }
      await loadPlan();
      onUpdate();
    } catch (error: any) {
      console.error('Error pausing/resuming plan:', error);
      alert(error.response?.data?.detail || 'Error al cambiar el estado del plan');
    }
  };

  const handleComplete = async () => {
    if (!plan) return;

    if (!completeData.completion_date) {
      alert('La fecha de completación es requerida');
      return;
    }

    if (isUsageBased && !completeData.usage_value) {
      alert('El valor de uso actual es requerido para planes basados en uso');
      return;
    }

    try {
      await maintenanceService.complete(plan.id, {
        completion_date: completeData.completion_date,
        usage_value: completeData.usage_value ? parseInt(completeData.usage_value) : undefined,
        notes: completeData.notes,
      });
      setShowCompleteForm(false);
      setCompleteData({
        completion_date: new Date().toISOString().slice(0, 10),
        usage_value: '',
        notes: '',
      });
      await loadPlan();
      onUpdate();
      alert('Mantenimiento completado exitosamente');
    } catch (error: any) {
      console.error('Error completing maintenance:', error);
      alert(error.response?.data?.detail || 'Error al completar el mantenimiento');
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Activo: 'bg-green-100 text-green-800 border-green-200',
      Pausado: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      Completado: 'bg-blue-100 text-blue-800 border-blue-200',
      Cancelado: 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getDueStatusColor = () => {
    if (!plan) return 'text-gray-600';
    if (plan.is_overdue) return 'text-red-600';
    if (plan.is_due) return 'text-orange-600';
    return 'text-gray-600';
  };

  const getDueStatusText = () => {
    if (!plan) return 'N/A';
    if (plan.is_overdue) return 'Vencido';
    if (plan.is_due) return 'Por vencer';
    if (plan.days_until_due !== null) {
      return `${plan.days_until_due} días restantes`;
    }
    if (plan.usage_until_due !== null) {
      return `${plan.usage_until_due} ${
        plan.recurrence_type === 'Por Horas' ? 'hrs' : 'km'
      } restantes`;
    }
    return 'N/A';
  };

  const isUsageBased = plan && ['Por Horas', 'Por Kilómetros'].includes(plan.recurrence_type);

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!plan) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-xl font-bold text-gray-900">{plan.name}</h2>
              <span
                className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                  plan.status
                )}`}
              >
                {plan.status}
              </span>
              {plan.is_paused && (
                <span className="px-2 py-1 text-xs font-semibold bg-yellow-100 text-yellow-800 rounded">
                  <FiPause className="w-3 h-3 inline mr-1" />
                  Pausado
                </span>
              )}
            </div>
            <p className="text-gray-600">{plan.asset_data?.name}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Description */}
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Descripción</h3>
            <p className="text-gray-600 whitespace-pre-wrap">{plan.description}</p>
          </div>

          {/* Recurrence Info */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Información de Recurrencia</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start space-x-3">
                <FiCalendar className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Tipo de Recurrencia</p>
                  <p className="font-semibold text-gray-900">
                    {plan.recurrence_type} (cada {plan.recurrence_interval}{' '}
                    {plan.recurrence_interval === 1 ? 'vez' : 'veces'})
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiClock className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500">Fecha de Inicio</p>
                  <p className="font-semibold text-gray-900">
                    {new Date(plan.start_date).toLocaleDateString('es-ES')}
                  </p>
                </div>
              </div>

              {plan.next_due_date && (
                <div className="flex items-start space-x-3">
                  <FiAlertCircle className={`w-5 h-5 ${getDueStatusColor()} mt-0.5`} />
                  <div>
                    <p className="text-sm text-gray-500">Próximo Mantenimiento</p>
                    <p className={`font-semibold ${getDueStatusColor()}`}>
                      {new Date(plan.next_due_date).toLocaleDateString('es-ES')}
                    </p>
                    <p className={`text-sm ${getDueStatusColor()}`}>{getDueStatusText()}</p>
                  </div>
                </div>
              )}

              {plan.last_completed_date && (
                <div className="flex items-start space-x-3">
                  <FiCheckCircle className="w-5 h-5 text-green-500 mt-0.5" />
                  <div>
                    <p className="text-sm text-gray-500">Último Mantenimiento</p>
                    <p className="font-semibold text-gray-900">
                      {new Date(plan.last_completed_date).toLocaleDateString('es-ES')}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Usage-based Info */}
          {isUsageBased && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-900 mb-3">
                Mantenimiento Basado en Uso
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-blue-700">Umbral de Uso</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {plan.usage_threshold}{' '}
                    {plan.recurrence_type === 'Por Horas' ? 'hrs' : 'km'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-blue-700">Uso Actual</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {plan.last_usage_value || 0}{' '}
                    {plan.recurrence_type === 'Por Horas' ? 'hrs' : 'km'}
                  </p>
                </div>
                <div className="col-span-2">
                  <p className="text-sm text-blue-700">Uso Restante</p>
                  <p className="text-xl font-bold text-blue-900">
                    {plan.usage_until_due || 0}{' '}
                    {plan.recurrence_type === 'Por Horas' ? 'hrs' : 'km'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Additional Info */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Información Adicional</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {plan.estimated_duration_hours && (
                <div>
                  <p className="text-sm text-gray-500">Duración Estimada</p>
                  <p className="font-semibold text-gray-900">
                    {plan.estimated_duration_hours} horas
                  </p>
                </div>
              )}

              {plan.assigned_to_data && (
                <div className="flex items-start space-x-3">
                  <FiUser className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <p className="text-sm text-gray-500">Asignado a</p>
                    <p className="font-semibold text-gray-900">
                      {plan.assigned_to_data.first_name} {plan.assigned_to_data.last_name}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Complete Form */}
          {showCompleteForm && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-900 mb-3">Completar Mantenimiento</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-green-900 mb-1">
                    Fecha de Completación
                  </label>
                  <input
                    type="date"
                    value={completeData.completion_date}
                    onChange={(e) =>
                      setCompleteData({ ...completeData, completion_date: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>

                {isUsageBased && (
                  <div>
                    <label className="block text-sm font-medium text-green-900 mb-1">
                      Valor de Uso Actual
                    </label>
                    <input
                      type="number"
                      value={completeData.usage_value}
                      onChange={(e) =>
                        setCompleteData({ ...completeData, usage_value: e.target.value })
                      }
                      className="w-full px-3 py-2 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500"
                      placeholder={`Ej: ${plan.last_usage_value || 0}`}
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-green-900 mb-1">Notas</label>
                  <textarea
                    value={completeData.notes}
                    onChange={(e) =>
                      setCompleteData({ ...completeData, notes: e.target.value })
                    }
                    rows={3}
                    className="w-full px-3 py-2 border border-green-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    placeholder="Notas sobre el mantenimiento realizado..."
                  />
                </div>

                <div className="flex space-x-2">
                  <button
                    onClick={handleComplete}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
                  >
                    Confirmar Completación
                  </button>
                  <button
                    onClick={() => setShowCompleteForm(false)}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-medium"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Actions */}
          {!showCompleteForm && (plan.status === 'Activo' || plan.status === 'Pausado') && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Acciones</h4>
              <div className="flex flex-wrap gap-2">
                {!plan.is_paused && (
                  <button
                    onClick={() => setShowCompleteForm(true)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium text-sm flex items-center space-x-2"
                  >
                    <FiCheckCircle className="w-4 h-4" />
                    <span>Completar Mantenimiento</span>
                  </button>
                )}

                <button
                  onClick={handlePauseResume}
                  className={`px-4 py-2 text-white rounded-lg font-medium text-sm flex items-center space-x-2 ${
                    plan.is_paused
                      ? 'bg-blue-600 hover:bg-blue-700'
                      : 'bg-yellow-600 hover:bg-yellow-700'
                  }`}
                >
                  {plan.is_paused ? (
                    <>
                      <FiPlay className="w-4 h-4" />
                      <span>Reanudar Plan</span>
                    </>
                  ) : (
                    <>
                      <FiPause className="w-4 h-4" />
                      <span>Pausar Plan</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Status Info */}
          {(plan.status === 'Completado' || plan.status === 'Cancelado') && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <p className="text-gray-600">
                Este plan está en estado <strong>{plan.status}</strong> y no puede ser modificado.
              </p>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={() => onEdit(plan as any)}
            className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg font-medium transition-colors"
          >
            <FiEdit className="w-4 h-4" />
            <span>Editar</span>
          </button>
          <button
            onClick={onDelete}
            className="flex items-center space-x-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
          >
            <FiTrash2 className="w-4 h-4" />
            <span>Eliminar</span>
          </button>
        </div>
      </div>
    </div>
  );
}
