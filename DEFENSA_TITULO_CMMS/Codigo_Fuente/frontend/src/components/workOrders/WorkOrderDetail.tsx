/**
 * Work Order Detail Component
 */
import { useState, useEffect } from 'react';
import {
  FiX,
  FiClock,
  FiUser,
  FiTruck,
  FiAlertCircle,
  FiCheckCircle,
  FiEdit,
  FiTrash2,
} from 'react-icons/fi';
import { WorkOrderDetail as WorkOrderDetailType } from '../../types/workOrder.types';
import { workOrderService } from '../../services/workOrderService';

interface WorkOrderDetailProps {
  workOrderId: string;
  onClose: () => void;
  onEdit: (workOrder: WorkOrderDetailType) => void;
  onDelete: () => void;
  onUpdate: () => void;
}

export default function WorkOrderDetail({
  workOrderId,
  onClose,
  onEdit,
  onDelete,
  onUpdate,
}: WorkOrderDetailProps) {
  const [workOrder, setWorkOrder] = useState<WorkOrderDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCompleteForm, setShowCompleteForm] = useState(false);
  const [completeData, setCompleteData] = useState({
    completion_notes: '',
    actual_hours: '',
  });

  useEffect(() => {
    loadWorkOrder();
  }, [workOrderId]);

  const loadWorkOrder = async () => {
    try {
      const data = await workOrderService.getById(workOrderId);
      setWorkOrder(data);
    } catch (error) {
      console.error('Error loading work order:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusTransition = async (newStatus: string) => {
    if (!workOrder) return;

    try {
      await workOrderService.transitionStatus(workOrder.id, newStatus);
      await loadWorkOrder();
      onUpdate();
    } catch (error: any) {
      console.error('Error transitioning status:', error);
      alert(error.response?.data?.error || 'Error al cambiar el estado');
    }
  };

  const handleComplete = async () => {
    if (!workOrder) return;

    try {
      await workOrderService.complete(workOrder.id, {
        completion_notes: completeData.completion_notes,
        actual_hours: parseFloat(completeData.actual_hours),
      });
      setShowCompleteForm(false);
      await loadWorkOrder();
      onUpdate();
    } catch (error: any) {
      console.error('Error completing work order:', error);
      alert(error.response?.data?.error || 'Error al completar la orden');
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Pendiente: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'En Progreso': 'bg-blue-100 text-blue-800 border-blue-200',
      Completada: 'bg-green-100 text-green-800 border-green-200',
      Cancelada: 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      Baja: 'text-gray-600',
      Media: 'text-blue-600',
      Alta: 'text-orange-600',
      Urgente: 'text-red-600',
    };
    return colors[priority] || 'text-gray-600';
  };

  const getAvailableTransitions = () => {
    if (!workOrder) return [];

    const transitions: Record<string, string[]> = {
      Pendiente: ['En Progreso', 'Cancelada'],
      'En Progreso': ['Completada', 'Cancelada'],
      Completada: [],
      Cancelada: [],
    };

    return transitions[workOrder.status] || [];
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!workOrder) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-xl font-bold text-gray-900">{workOrder.work_order_number}</h2>
              <span
                className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                  workOrder.status
                )}`}
              >
                {workOrder.status}
              </span>
            </div>
            <h3 className="text-lg text-gray-700">{workOrder.title}</h3>
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
          {/* Priority and Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <FiAlertCircle className={`w-5 h-5 ${getPriorityColor(workOrder.priority)}`} />
              <div>
                <p className="text-sm text-gray-500">Prioridad</p>
                <p className={`font-semibold ${getPriorityColor(workOrder.priority)}`}>
                  {workOrder.priority}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <FiClock className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Fecha Programada</p>
                <p className="font-semibold text-gray-900">
                  {new Date(workOrder.scheduled_date).toLocaleString('es-ES')}
                </p>
              </div>
            </div>
          </div>

          {/* Asset and Assignment */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <FiTruck className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Activo</p>
                <p className="font-semibold text-gray-900">{workOrder.asset_name}</p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <FiUser className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Asignado a</p>
                <p className="font-semibold text-gray-900">{workOrder.assigned_to_name}</p>
              </div>
            </div>
          </div>

          {/* Description */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Descripción</h4>
            <p className="text-gray-600 whitespace-pre-wrap">{workOrder.description}</p>
          </div>

          {/* Completion Info */}
          {workOrder.status === 'Completada' && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-3">
                <FiCheckCircle className="w-5 h-5 text-green-600" />
                <h4 className="font-semibold text-green-900">Trabajo Completado</h4>
              </div>
              <div className="space-y-2">
                <div>
                  <p className="text-sm text-green-700">Fecha de Completación</p>
                  <p className="font-medium text-green-900">
                    {workOrder.completed_date
                      ? new Date(workOrder.completed_date).toLocaleString('es-ES')
                      : 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-green-700">Horas Trabajadas</p>
                  <p className="font-medium text-green-900">{workOrder.actual_hours || 'N/A'} hrs</p>
                </div>
                {workOrder.completion_notes && (
                  <div>
                    <p className="text-sm text-green-700">Notas de Completación</p>
                    <p className="text-green-900 whitespace-pre-wrap">
                      {workOrder.completion_notes}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Complete Form */}
          {showCompleteForm && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-3">Completar Orden de Trabajo</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-1">
                    Horas Trabajadas *
                  </label>
                  <input
                    type="number"
                    step="0.5"
                    value={completeData.actual_hours}
                    onChange={(e) =>
                      setCompleteData({ ...completeData, actual_hours: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Ej: 2.5"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-900 mb-1">
                    Notas de Completación *
                  </label>
                  <textarea
                    value={completeData.completion_notes}
                    onChange={(e) =>
                      setCompleteData({ ...completeData, completion_notes: e.target.value })
                    }
                    rows={3}
                    className="w-full px-3 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Describe el trabajo realizado..."
                  />
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={handleComplete}
                    disabled={!completeData.actual_hours || !completeData.completion_notes}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
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

          {/* Status Transitions */}
          {getAvailableTransitions().length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Cambiar Estado</h4>
              <div className="flex flex-wrap gap-2">
                {getAvailableTransitions().map((status) => (
                  <button
                    key={status}
                    onClick={() => {
                      if (status === 'Completada') {
                        setShowCompleteForm(true);
                      } else {
                        handleStatusTransition(status);
                      }
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm"
                  >
                    Marcar como {status}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={() => onEdit(workOrder)}
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
