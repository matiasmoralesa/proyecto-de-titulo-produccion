import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import AssetTimeline from '../components/machine-status/AssetTimeline';
import assetService from '../services/assetService';
import { AssetDetail } from '../types/asset.types';
import machineStatusService, { AssetStatus } from '../services/machineStatusService';
import { assetHistoryService, AssetKPIs } from '../services/machineStatusService';

const AssetDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [asset, setAsset] = useState<AssetDetail | null>(null);
  const [status, setStatus] = useState<AssetStatus | null>(null);
  const [kpis, setKpis] = useState<AssetKPIs | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'info' | 'timeline' | 'kpis'>('info');

  useEffect(() => {
    if (id) {
      loadAssetData();
    }
  }, [id]);

  const loadAssetData = async () => {
    if (!id) {
      console.error('No asset ID provided');
      return;
    }
    
    console.log('Loading asset data for ID:', id);
    
    try {
      setLoading(true);
      
      // Load asset data first
      console.log('Fetching asset...');
      const assetData = await assetService.getAsset(id);
      console.log('Asset loaded:', assetData);
      setAsset(assetData);
      
      // Load status data
      console.log('Fetching status...');
      const statusesData = await machineStatusService.getStatuses({ asset: id });
      console.log('Status loaded:', statusesData);
      const statusList = statusesData.results || statusesData;
      if (statusList.length > 0) {
        setStatus(statusList[0]);
      }
      
      // Load KPIs
      console.log('Fetching KPIs...');
      const kpisData = await assetHistoryService.getAssetKPIs(id);
      console.log('KPIs loaded:', kpisData);
      setKpis(kpisData);
      
    } catch (error) {
      console.error('Error loading asset data:', error);
      // Don't set asset to null on error, keep trying to show what we have
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (statusType: string) => {
    switch (statusType) {
      case 'OPERANDO':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'DETENIDA':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'EN_MANTENIMIENTO':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'FUERA_DE_SERVICIO':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
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

  if (!asset) {
    return (
      <MainLayout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900">Activo no encontrado</h2>
          <button
            onClick={() => navigate('/machine-status')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Volver al Dashboard
          </button>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <button
              onClick={() => navigate('/machine-status')}
              className="text-blue-600 hover:text-blue-800 mb-2 flex items-center"
            >
              ← Volver al Dashboard
            </button>
            <h1 className="text-3xl font-bold text-gray-900">{asset.name}</h1>
            <p className="text-gray-600 mt-1">{asset.model}</p>
          </div>
          <div>
            {status && (
              <span className={`px-4 py-2 rounded-full text-sm font-semibold border-2 ${getStatusColor(status.status_type)}`}>
                {status.status_type_display}
              </span>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('info')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'info'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Información General
            </button>
            <button
              onClick={() => setActiveTab('kpis')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'kpis'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              KPIs y Estadísticas
            </button>
            <button
              onClick={() => setActiveTab('timeline')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'timeline'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Historial de Actividades
            </button>
          </nav>
        </div>

        {/* Content */}
        {activeTab === 'info' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Asset Information */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Información del Activo</h3>
              <dl className="space-y-3">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Tipo de Vehículo</dt>
                  <dd className="mt-1 text-sm text-gray-900">{asset.vehicle_type}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Modelo</dt>
                  <dd className="mt-1 text-sm text-gray-900">{asset.model}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Número de Serie</dt>
                  <dd className="mt-1 text-sm text-gray-900">{asset.serial_number}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Placa</dt>
                  <dd className="mt-1 text-sm text-gray-900">{asset.license_plate || 'N/A'}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Ubicación</dt>
                  <dd className="mt-1 text-sm text-gray-900">{asset.location_name}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Fecha de Instalación</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {new Date(asset.installation_date).toLocaleDateString('es-ES')}
                  </dd>
                </div>
              </dl>
            </div>

            {/* Current Status */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Estado Actual</h3>
              {status ? (
                <dl className="space-y-3">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Estado</dt>
                    <dd className="mt-1">
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor(status.status_type)}`}>
                        {status.status_type_display}
                      </span>
                    </dd>
                  </div>
                  {status.odometer_reading && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Odómetro</dt>
                      <dd className="mt-1 text-sm text-gray-900">{status.odometer_reading}</dd>
                    </div>
                  )}
                  {status.fuel_level !== null && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Nivel de Combustible</dt>
                      <dd className="mt-1">
                        <div className="flex items-center">
                          <div className="flex-1 mr-2">
                            <div className="w-full bg-gray-200 rounded-full h-3">
                              <div
                                className={`h-3 rounded-full ${
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
                          <span className="text-sm text-gray-900 font-medium">
                            {status.fuel_level}%
                          </span>
                        </div>
                      </dd>
                    </div>
                  )}
                  {status.condition_notes && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Notas de Condición</dt>
                      <dd className="mt-1 text-sm text-gray-900 italic">"{status.condition_notes}"</dd>
                    </div>
                  )}
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Última Actualización</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {new Date(status.updated_at).toLocaleString('es-ES')}
                      <br />
                      <span className="text-gray-500">por {status.last_updated_by_name}</span>
                    </dd>
                  </div>
                </dl>
              ) : (
                <p className="text-gray-500">No hay información de estado disponible</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'kpis' && kpis && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Horas de Mantenimiento</div>
                <div className="mt-2 text-3xl font-bold text-gray-900">
                  {kpis.kpis.total_maintenance_hours.toFixed(1)}
                </div>
                <div className="mt-1 text-sm text-gray-500">horas totales</div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Órdenes de Trabajo</div>
                <div className="mt-2 text-3xl font-bold text-gray-900">
                  {kpis.kpis.completed_work_orders}
                </div>
                <div className="mt-1 text-sm text-gray-500">
                  de {kpis.kpis.total_work_orders} completadas
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Eventos de Downtime</div>
                <div className="mt-2 text-3xl font-bold text-gray-900">
                  {kpis.kpis.downtime_events}
                </div>
                <div className="mt-1 text-sm text-gray-500">eventos registrados</div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Costo de Mantenimiento</div>
                <div className="mt-2 text-3xl font-bold text-gray-900">
                  ${kpis.kpis.total_maintenance_cost.toFixed(2)}
                </div>
                <div className="mt-1 text-sm text-gray-500">costo total</div>
              </div>
            </div>

            {/* Additional Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Órdenes Pendientes</div>
                <div className="mt-2 text-2xl font-bold text-yellow-600">
                  {kpis.kpis.pending_work_orders}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Órdenes en Progreso</div>
                <div className="mt-2 text-2xl font-bold text-blue-600">
                  {kpis.kpis.in_progress_work_orders}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow">
                <div className="text-sm font-medium text-gray-500">Promedio Horas/Orden</div>
                <div className="mt-2 text-2xl font-bold text-gray-900">
                  {kpis.kpis.average_hours_per_work_order.toFixed(1)}
                </div>
              </div>
            </div>

            {/* Date Range Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>Período de análisis:</strong>{' '}
                {new Date(kpis.date_range.start_date).toLocaleDateString('es-ES')} -{' '}
                {new Date(kpis.date_range.end_date).toLocaleDateString('es-ES')}
              </p>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && id && (
          <AssetTimeline assetId={id} assetName={asset.name} />
        )}

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => navigate('/work-orders')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Ir a Órdenes de Trabajo
            </button>
            <button
              onClick={() => navigate('/machine-status')}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Actualizar Estado
            </button>
            <button
              onClick={() => navigate('/assets')}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Ver Todos los Activos
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default AssetDetailPage;
