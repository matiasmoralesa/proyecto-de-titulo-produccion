import React, { useState, useEffect } from 'react';
import { assetHistoryService, AssetHistoryActivity } from '../../services/machineStatusService';

interface AssetTimelineProps {
  assetId: string;
  assetName?: string;
}

const AssetTimeline: React.FC<AssetTimelineProps> = ({ assetId, assetName }) => {
  const [activities, setActivities] = useState<AssetHistoryActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    loadHistory();
  }, [assetId, filterType, startDate, endDate, page]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const response = await assetHistoryService.getCompleteHistory(assetId, {
        activity_type: filterType || undefined,
        start_date: startDate || undefined,
        end_date: endDate || undefined,
        page,
        page_size: 20
      });
      
      setActivities(response.results);
      setTotalCount(response.count);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'status_update':
        return '📊';
      case 'work_order_created':
        return '📝';
      case 'work_order_completed':
        return '✅';
      case 'maintenance_plan_created':
        return '🔧';
      case 'checklist_completed':
        return '📋';
      case 'spare_part_used':
        return '🔩';
      default:
        return '•';
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'status_update':
        return 'bg-blue-100 border-blue-300 text-blue-800';
      case 'work_order_created':
        return 'bg-purple-100 border-purple-300 text-purple-800';
      case 'work_order_completed':
        return 'bg-green-100 border-green-300 text-green-800';
      case 'maintenance_plan_created':
        return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      case 'checklist_completed':
        return 'bg-indigo-100 border-indigo-300 text-indigo-800';
      case 'spare_part_used':
        return 'bg-orange-100 border-orange-300 text-orange-800';
      default:
        return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getActivityTitle = (activity: AssetHistoryActivity) => {
    switch (activity.type) {
      case 'status_update':
        return `Estado actualizado a: ${activity.data.status_type_display}`;
      case 'work_order_created':
        return `Orden de trabajo creada: ${activity.data.work_order_number}`;
      case 'work_order_completed':
        return `Orden de trabajo completada: ${activity.data.work_order_number}`;
      case 'maintenance_plan_created':
        return `Plan de mantenimiento creado: ${activity.data.name}`;
      case 'checklist_completed':
        return `Checklist completado: ${activity.data.template_name}`;
      case 'spare_part_used':
        return `Repuesto utilizado: ${activity.data.spare_part_name}`;
      default:
        return 'Actividad';
    }
  };

  const renderActivityDetails = (activity: AssetHistoryActivity) => {
    switch (activity.type) {
      case 'status_update':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            {activity.data.odometer_reading && (
              <p>Odómetro: {activity.data.odometer_reading}</p>
            )}
            {activity.data.fuel_level !== null && (
              <p>Combustible: {activity.data.fuel_level}%</p>
            )}
            {activity.data.condition_notes && (
              <p className="italic">"{activity.data.condition_notes}"</p>
            )}
          </div>
        );
      
      case 'work_order_created':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            <p><strong>Título:</strong> {activity.data.title}</p>
            <p><strong>Prioridad:</strong> {activity.data.priority}</p>
            <p><strong>Asignado a:</strong> {activity.data.assigned_to}</p>
            <p><strong>Estado:</strong> {activity.data.status}</p>
          </div>
        );
      
      case 'work_order_completed':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            <p><strong>Título:</strong> {activity.data.title}</p>
            {activity.data.actual_hours && (
              <p><strong>Horas trabajadas:</strong> {activity.data.actual_hours}</p>
            )}
            {activity.data.completion_notes && (
              <p className="italic">"{activity.data.completion_notes}"</p>
            )}
          </div>
        );
      
      case 'maintenance_plan_created':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            <p><strong>Descripción:</strong> {activity.data.description}</p>
            <p><strong>Recurrencia:</strong> {activity.data.recurrence_type}</p>
            {activity.data.next_due_date && (
              <p><strong>Próxima fecha:</strong> {new Date(activity.data.next_due_date).toLocaleDateString('es-ES')}</p>
            )}
          </div>
        );
      
      case 'checklist_completed':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            <p><strong>Código:</strong> {activity.data.template_code}</p>
            <p><strong>Completado:</strong> {activity.data.completion_percentage}%</p>
            {activity.data.pdf_report && (
              <a 
                href={activity.data.pdf_report} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                Ver PDF
              </a>
            )}
          </div>
        );
      
      case 'spare_part_used':
        return (
          <div className="mt-2 space-y-1 text-sm text-gray-600">
            <p><strong>Número de parte:</strong> {activity.data.spare_part_number}</p>
            <p><strong>Cantidad:</strong> {activity.data.quantity}</p>
            {activity.data.work_order_number && (
              <p><strong>Orden de trabajo:</strong> {activity.data.work_order_number}</p>
            )}
            {activity.data.notes && (
              <p className="italic">"{activity.data.notes}"</p>
            )}
          </div>
        );
      
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const activityTypes = [
    { value: '', label: 'Todas las actividades' },
    { value: 'status', label: 'Actualizaciones de estado' },
    { value: 'work_order', label: 'Órdenes de trabajo' },
    { value: 'maintenance', label: 'Mantenimiento' },
    { value: 'checklist', label: 'Checklists' },
    { value: 'spare_part', label: 'Repuestos' }
  ];

  if (loading && activities.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      {assetName && (
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Historial de Actividades</h2>
          <p className="text-gray-600 mt-1">{assetName}</p>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <select
            value={filterType}
            onChange={(e) => {
              setFilterType(e.target.value);
              setPage(1);
            }}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            {activityTypes.map(type => (
              <option key={type.value} value={type.value}>{type.label}</option>
            ))}
          </select>

          <input
            type="date"
            value={startDate}
            onChange={(e) => {
              setStartDate(e.target.value);
              setPage(1);
            }}
            placeholder="Fecha inicio"
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />

          <input
            type="date"
            value={endDate}
            onChange={(e) => {
              setEndDate(e.target.value);
              setPage(1);
            }}
            placeholder="Fecha fin"
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />

          <button
            onClick={() => {
              setFilterType('');
              setStartDate('');
              setEndDate('');
              setPage(1);
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Limpiar Filtros
          </button>
        </div>
      </div>

      {/* Timeline */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flow-root">
          <ul className="-mb-8">
            {activities.length === 0 ? (
              <li className="text-center py-12 text-gray-500">
                No hay actividades registradas
              </li>
            ) : (
              activities.map((activity, idx) => (
                <li key={`${activity.type}-${activity.timestamp}-${idx}`}>
                  <div className="relative pb-8">
                    {idx !== activities.length - 1 && (
                      <span
                        className="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    )}
                    <div className="relative flex items-start space-x-3">
                      {/* Icon */}
                      <div>
                        <div className={`h-10 w-10 rounded-full border-2 flex items-center justify-center ${getActivityColor(activity.type)}`}>
                          <span className="text-xl">{getActivityIcon(activity.type)}</span>
                        </div>
                      </div>

                      {/* Content */}
                      <div className="min-w-0 flex-1">
                        <div>
                          <div className="text-sm">
                            <span className="font-medium text-gray-900">
                              {activity.user.name}
                            </span>
                          </div>
                          <p className="mt-0.5 text-sm text-gray-500">
                            {formatDate(activity.timestamp)}
                          </p>
                        </div>
                        <div className="mt-2">
                          <p className="text-base font-semibold text-gray-900">
                            {getActivityTitle(activity)}
                          </p>
                          {renderActivityDetails(activity)}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))
            )}
          </ul>
        </div>

        {/* Pagination */}
        {totalCount > 20 && (
          <div className="mt-6 flex items-center justify-between border-t border-gray-200 pt-4">
            <div className="text-sm text-gray-700">
              Mostrando {(page - 1) * 20 + 1} - {Math.min(page * 20, totalCount)} de {totalCount} actividades
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page * 20 >= totalCount}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AssetTimeline;
