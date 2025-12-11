/**
 * Asset Detail Component
 */
import { useState, useEffect } from 'react';
import {
  FiX,
  FiTruck,
  FiMapPin,
  FiHash,
  FiCreditCard,
  FiCalendar,
  FiEdit,
  FiTrash2,
  FiFileText,
  FiActivity,
  FiTool,
  FiClock,
  FiCheckCircle,
  FiAlertTriangle,
  FiBarChart3,
} from 'react-icons/fi';
import { Asset } from '../../types/asset.types';
import assetService from '../../services/assetService';
import api from '../../services/api';

interface AssetDetailProps {
  assetId: string;
  onClose: () => void;
  onEdit: (asset: Asset) => void;
  onDelete: () => void;
}

interface AssetStats {
  total_work_orders: number;
  completed_work_orders: number;
  pending_work_orders: number;
  in_progress_work_orders: number;
  total_maintenance_hours: number;
  last_maintenance_date: string | null;
  next_maintenance_date: string | null;
  total_documents: number;
  availability_percentage: number;
  total_cost: number;
  avg_completion_time: number;
}

export default function AssetDetail({ assetId, onClose, onEdit, onDelete }: AssetDetailProps) {
  const [asset, setAsset] = useState<Asset | null>(null);
  const [stats, setStats] = useState<AssetStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [statsLoading, setStatsLoading] = useState(true);

  useEffect(() => {
    loadAsset();
    loadAssetStats();
  }, [assetId]);

  const loadAsset = async () => {
    try {
      const data = await assetService.getAsset(assetId);
      setAsset(data);
    } catch (error) {
      console.error('Error loading asset:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAssetStats = async () => {
    try {
      const response = await api.get(`/assets/assets/${assetId}/stats/`);
      setStats(response.data);
    } catch (error) {
      console.error('Error loading asset stats:', error);
      // Set default stats if API fails
      setStats({
        total_work_orders: 0,
        completed_work_orders: 0,
        pending_work_orders: 0,
        in_progress_work_orders: 0,
        total_maintenance_hours: 0,
        last_maintenance_date: null,
        next_maintenance_date: null,
        total_documents: 0,
        availability_percentage: 100,
        total_cost: 0,
        avg_completion_time: 0,
      });
    } finally {
      setStatsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      Operando: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300 border-green-200 dark:border-green-700',
      Detenida: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-700',
      'En Mantenimiento': 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-700',
      'Fuera de Servicio': 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300 border-red-200 dark:border-red-700',
    };
    return colors[status] || 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-600';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!asset) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">{asset.name}</h2>
              <span
                className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                  asset.status
                )}`}
              >
                {asset.status}
              </span>
            </div>
            <p className="text-gray-600 dark:text-gray-400">{asset.asset_number}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <FiX className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Información Básica</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start space-x-3">
                <FiTruck className="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Tipo de Vehículo</p>
                  <p className="font-semibold text-gray-900 dark:text-white">{asset.vehicle_type}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiMapPin className="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Ubicación</p>
                  <p className="font-semibold text-gray-900 dark:text-white">{asset.location_name}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiHash className="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Número de Serie</p>
                  <p className="font-mono text-gray-900 dark:text-white">{asset.serial_number}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <FiCreditCard className="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Placa</p>
                  <p className="font-mono text-gray-900 dark:text-white">{asset.license_plate || 'N/A'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Vehicle Details */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Detalles del Vehículo</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Fabricante</p>
                <p className="font-semibold text-gray-900 dark:text-white">{asset.manufacturer || 'N/A'}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Modelo</p>
                <p className="font-semibold text-gray-900 dark:text-white">{asset.model || 'N/A'}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Año</p>
                <p className="font-semibold text-gray-900 dark:text-white">{asset.year || 'N/A'}</p>
              </div>

              <div className="flex items-start space-x-3">
                <FiCalendar className="w-5 h-5 text-gray-400 dark:text-gray-500 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Fecha de Registro</p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {new Date(asset.created_at).toLocaleDateString('es-ES')}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          {asset.description && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Descripción</h3>
              <p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{asset.description}</p>
            </div>
          )}

          {/* Documents Section */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Documentos</h3>
              <button className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium">
                + Subir Documento
              </button>
            </div>
            <div className="bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-4 text-center">
              <FiFileText className="w-8 h-8 text-gray-400 dark:text-gray-500 mx-auto mb-2" />
              <p className="text-sm text-gray-500 dark:text-gray-400">No hay documentos adjuntos</p>
            </div>
          </div>

          {/* Enhanced Statistics */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-blue-900 dark:text-blue-100 flex items-center">
                <FiBarChart3 className="w-6 h-6 mr-2" />
                Estadísticas del Equipo
              </h3>
              {statsLoading && (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
              )}
            </div>
            
            {stats && (
              <>
                {/* Primary Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-blue-100 dark:border-blue-800 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-2">
                      <FiActivity className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded-full">
                        Total
                      </span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_work_orders}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Órdenes de Trabajo</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-green-100 dark:border-green-800 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-2">
                      <FiCheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
                      <span className="text-xs font-medium text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900 px-2 py-1 rounded-full">
                        Completadas
                      </span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.completed_work_orders}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Mantenimientos</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-purple-100 dark:border-purple-800 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-2">
                      <FiClock className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                      <span className="text-xs font-medium text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900 px-2 py-1 rounded-full">
                        Horas
                      </span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_maintenance_hours.toLocaleString()}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Horas de Mantenimiento</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-orange-100 dark:border-orange-800 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-2">
                      <FiFileText className="w-5 h-5 text-orange-600 dark:text-orange-400" />
                      <span className="text-xs font-medium text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900 px-2 py-1 rounded-full">
                        Docs
                      </span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_documents}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Documentos</p>
                  </div>
                </div>

                {/* Secondary Stats */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900 dark:text-white">Estado Actual</h4>
                      <div className="flex items-center space-x-2">
                        {stats.pending_work_orders > 0 ? (
                          <FiAlertTriangle className="w-4 h-4 text-yellow-500" />
                        ) : (
                          <FiCheckCircle className="w-4 h-4 text-green-500" />
                        )}
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Pendientes:</span>
                        <span className="font-medium text-yellow-600 dark:text-yellow-400">{stats.pending_work_orders}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">En Progreso:</span>
                        <span className="font-medium text-blue-600 dark:text-blue-400">{stats.in_progress_work_orders}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Disponibilidad:</span>
                        <span className="font-medium text-green-600 dark:text-green-400">{stats.availability_percentage}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900 dark:text-white">Fechas Importantes</h4>
                      <FiCalendar className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    </div>
                    <div className="space-y-2">
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Último Mantenimiento:</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {formatDate(stats.last_maintenance_date)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Próximo Mantenimiento:</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {formatDate(stats.next_maintenance_date)}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900 dark:text-white">Rendimiento</h4>
                      <FiTool className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                    </div>
                    <div className="space-y-2">
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Tiempo Promedio:</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {stats.avg_completion_time} días
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Costo Total:</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {formatCurrency(stats.total_cost)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Progress Bar for Availability */}
                <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Disponibilidad del Equipo</span>
                    <span className="text-sm font-bold text-gray-900 dark:text-white">{stats.availability_percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full transition-all duration-500 ${
                        stats.availability_percentage >= 90 
                          ? 'bg-green-500' 
                          : stats.availability_percentage >= 70 
                          ? 'bg-yellow-500' 
                          : 'bg-red-500'
                      }`}
                      style={{ width: `${stats.availability_percentage}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700">
          <button
            onClick={() => onEdit(asset)}
            className="flex items-center space-x-2 px-4 py-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg font-medium transition-colors"
          >
            <FiEdit className="w-4 h-4" />
            <span>Editar</span>
          </button>
          <button
            onClick={onDelete}
            className="flex items-center space-x-2 px-4 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg font-medium transition-colors"
          >
            <FiTrash2 className="w-4 h-4" />
            <span>Eliminar</span>
          </button>
        </div>
      </div>
    </div>
  );
}
