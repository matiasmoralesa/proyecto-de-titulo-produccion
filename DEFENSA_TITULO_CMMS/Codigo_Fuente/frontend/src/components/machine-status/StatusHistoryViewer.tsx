import React, { useState, useEffect } from 'react';
import machineStatusService, {
  AssetStatusHistory,
  HistoryFilters,
} from '../../services/machineStatusService';

interface StatusHistoryViewerProps {
  assetId?: string;
}

const StatusHistoryViewer: React.FC<StatusHistoryViewerProps> = ({ assetId }) => {
  const [history, setHistory] = useState<AssetStatusHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<HistoryFilters>({
    asset: assetId,
  });

  useEffect(() => {
    loadHistory();
  }, [filters]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const response = await machineStatusService.getHistory(filters);
      const historyList = response.results || response;
      setHistory(historyList);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: keyof HistoryFilters, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || undefined,
    }));
  };

  const getStatusColor = (statusType: string) => {
    switch (statusType) {
      case 'OPERANDO':
        return 'bg-green-500';
      case 'DETENIDA':
        return 'bg-yellow-500';
      case 'EN_MANTENIMIENTO':
        return 'bg-blue-500';
      case 'FUERA_DE_SERVICIO':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusLabel = (statusType: string) => {
    const labels: Record<string, string> = {
      OPERANDO: 'Operando',
      DETENIDA: 'Detenida',
      EN_MANTENIMIENTO: 'En Mantenimiento',
      FUERA_DE_SERVICIO: 'Fuera de Servicio',
    };
    return labels[statusType] || statusType;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      {!assetId && (
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Status Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Estado
              </label>
              <select
                value={filters.status_type || ''}
                onChange={(e) => handleFilterChange('status_type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Todos</option>
                <option value="OPERANDO">Operando</option>
                <option value="DETENIDA">Detenida</option>
                <option value="EN_MANTENIMIENTO">En Mantenimiento</option>
                <option value="FUERA_DE_SERVICIO">Fuera de Servicio</option>
              </select>
            </div>

            {/* Start Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha Inicio
              </label>
              <input
                type="date"
                value={filters.start_date || ''}
                onChange={(e) => handleFilterChange('start_date', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* End Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fecha Fin
              </label>
              <input
                type="date"
                value={filters.end_date || ''}
                onChange={(e) => handleFilterChange('end_date', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Clear Filters */}
            <div className="flex items-end">
              <button
                onClick={() => setFilters({ asset: assetId })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Limpiar Filtros
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Timeline */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Historial de Estados
        </h3>

        {history.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No hay historial disponible
          </div>
        ) : (
          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>

            {/* Timeline Items */}
            <div className="space-y-6">
              {history.map((record, index) => (
                <div key={record.id} className="relative pl-10">
                  {/* Timeline Dot */}
                  <div
                    className={`absolute left-0 w-8 h-8 rounded-full ${getStatusColor(
                      record.status_type
                    )} flex items-center justify-center`}
                  >
                    <div className="w-3 h-3 bg-white rounded-full"></div>
                  </div>

                  {/* Content */}
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2">
                      <div>
                        <span className="font-semibold text-gray-900">
                          {getStatusLabel(record.status_type)}
                        </span>
                        {!assetId && (
                          <span className="text-gray-600 ml-2">
                            - {record.asset_name}
                          </span>
                        )}
                      </div>
                      <span className="text-sm text-gray-500">
                        {new Date(record.timestamp).toLocaleString('es-ES')}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                      {record.odometer_reading && (
                        <div>
                          <span className="text-gray-500">Odómetro:</span>
                          <span className="ml-2 font-medium text-gray-900">
                            {record.odometer_reading}
                          </span>
                        </div>
                      )}

                      {record.fuel_level !== null && (
                        <div>
                          <span className="text-gray-500">Combustible:</span>
                          <span className="ml-2 font-medium text-gray-900">
                            {record.fuel_level}%
                          </span>
                        </div>
                      )}

                      <div>
                        <span className="text-gray-500">Por:</span>
                        <span className="ml-2 font-medium text-gray-900">
                          {record.updated_by_name}
                        </span>
                      </div>
                    </div>

                    {record.condition_notes && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-sm text-gray-700">
                          <span className="font-medium">Notas:</span>{' '}
                          {record.condition_notes}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatusHistoryViewer;
