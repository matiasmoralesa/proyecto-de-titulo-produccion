import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import StatusUpdateForm from '../components/machine-status/StatusUpdateForm';
import ComprehensiveAssetDashboard from '../components/machine-status/ComprehensiveAssetDashboard';
import machineStatusService, { AssetStatus } from '../services/machineStatusService';
import { useAuthStore } from '../store/authStore';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

const MachineStatusPage: React.FC = () => {
  const { user } = useAuthStore();
  const [statuses, setStatuses] = useState<AssetStatus[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<AssetStatus | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    loadStatuses();
  }, [refreshTrigger]);

  const loadStatuses = async () => {
    try {
      setLoading(true);
      const response = await machineStatusService.getStatuses();
      const statusList = response.results || response;
      setStatuses(statusList);
    } catch (error) {
      console.error('Error loading statuses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = (status: AssetStatus) => {
    setSelectedStatus(status);
    setShowForm(true);
  };

  const handleSuccess = () => {
    setShowForm(false);
    setSelectedStatus(null);
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleCancel = () => {
    setShowForm(false);
    setSelectedStatus(null);
  };

  const getStatusColor = (statusType: string) => {
    switch (statusType) {
      case 'OPERANDO':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'DETENIDA':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'EN_MANTENIMIENTO':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'FUERA_DE_SERVICIO':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (statusType: string) => {
    switch (statusType) {
      case 'OPERANDO':
        return '✓';
      case 'DETENIDA':
        return '⏸';
      case 'EN_MANTENIMIENTO':
        return '🔧';
      case 'FUERA_DE_SERVICIO':
        return '⚠';
      default:
        return '•';
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Estado de Máquinas</h1>
          <p className="text-gray-600 mt-1">
            {user?.role === 'OPERADOR'
              ? 'Actualiza el estado de tus activos asignados'
              : 'Monitorea y actualiza el estado de todos los activos'}
          </p>
        </div>

        {/* Form or Dashboard */}
        {showForm ? (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">
              Actualizar Estado - {selectedStatus?.asset_name}
            </h2>
            <StatusUpdateForm
              statusId={selectedStatus?.id}
              assetId={selectedStatus?.asset}
              onSuccess={handleSuccess}
              onCancel={handleCancel}
            />
          </div>
        ) : (
          <ComprehensiveAssetDashboard />
        )}

        {/* Old Status Cards - Keeping for reference but hidden */}
        {false && (
          <>
            {/* Status Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {statuses.length === 0 ? (
                <div className="col-span-full text-center py-12 bg-white rounded-lg shadow">
                  <p className="text-gray-500">No hay activos disponibles</p>
                </div>
              ) : (
                statuses.map((status) => (
                  <div
                    key={status.id}
                    className="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
                  >
                    {/* Card Header */}
                    <div className="p-4 border-b border-gray-200">
                      <h3 className="font-semibold text-gray-900 text-lg">
                        {status.asset_name}
                      </h3>
                      <div className="mt-2">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(
                            status.status_type
                          )}`}
                        >
                          <span className="mr-1">{getStatusIcon(status.status_type)}</span>
                          {status.status_type_display}
                        </span>
                      </div>
                    </div>

                    {/* Card Body */}
                    <div className="p-4 space-y-3">
                      {/* Odometer */}
                      {status.odometer_reading && (
                        <div className="flex items-center text-sm">
                          <span className="text-gray-500 w-24">Odómetro:</span>
                          <span className="font-medium text-gray-900">
                            {status.odometer_reading}
                          </span>
                        </div>
                      )}

                      {/* Fuel Level */}
                      {status.fuel_level !== null && (
                        <div>
                          <div className="flex items-center justify-between text-sm mb-1">
                            <span className="text-gray-500">Combustible:</span>
                            <span className="font-medium text-gray-900">
                              {status.fuel_level}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${
                                status.fuel_level > 50
                                  ? 'bg-green-500'
                                  : status.fuel_level > 25
                                  ? 'bg-yellow-500'
                                  : 'bg-red-500'
                              }`}
                              style={{ width: `${status.fuel_level}%` }}
                            ></div>
                          </div>
                        </div>
                      )}

                      {/* Condition Notes */}
                      {status.condition_notes && (
                        <div className="text-sm">
                          <span className="text-gray-500 block mb-1">Notas:</span>
                          <p className="text-gray-700 line-clamp-2">
                            {status.condition_notes}
                          </p>
                        </div>
                      )}

                      {/* Last Updated */}
                      <div className="text-xs text-gray-500 pt-2 border-t border-gray-100">
                        Actualizado por {status.last_updated_by_name}
                        <br />
                        {new Date(status.updated_at).toLocaleString('es-ES')}
                      </div>
                    </div>

                    {/* Card Footer */}
                    <div className="p-4 bg-gray-50 border-t border-gray-200">
                      <button
                        onClick={() => handleUpdateStatus(status)}
                        className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
                      >
                        Actualizar Estado
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </>
        )}
      </div>
    </MainLayout>
  );
};

export default MachineStatusPage;
